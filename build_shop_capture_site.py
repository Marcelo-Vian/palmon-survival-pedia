import json
import pathlib
import re
from collections import Counter, defaultdict
from datetime import datetime

from PIL import Image


ROOT = pathlib.Path(r"D:\Linkedin")
SOURCE_DIR = ROOT / "palmon_survival_prints" / "loja" / "prints"
PEDIA_DIR = ROOT / "palmon_survival_pedia"
ASSET_DIR = PEDIA_DIR / "assets" / "shop_captures"
OUT_HTML = PEDIA_DIR / "palmon_shop_captures.html"


CAPTURE_RE = re.compile(
    r"^angroid_shop_(?P<session>\d+)_loja(?P<shop>\d+)_cap(?P<cap>\d+)_"
    r"(?P<kind>.+?)_precos_(?P<prices>\d+)__tabs_(?P<tabs>\d+)__"
    r"claim_(?P<claim>\d+)__rows_(?P<rows>\d+)__(?P<stamp>\d{8}_\d{6})\.png$",
    re.I,
)

KIND_LABEL = {
    "bundle_list": "Lista de bundles",
    "offer_popup": "Oferta popup",
    "pass_or_privilege": "Passe/privilegio",
    "single_offer": "Oferta unica",
}


def ensure_dir(path: pathlib.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def fit_image(image: Image.Image, max_width: int) -> Image.Image:
    if image.width <= max_width:
        return image.copy()
    height = round(image.height * (max_width / image.width))
    return image.resize((max_width, height), Image.Resampling.LANCZOS)


def overlay_score(image: Image.Image) -> tuple[bool, str]:
    # Android Helper overlay usually sits in the upper-left quadrant. This does
    # not try to OCR it; it only warns when that region is visibly covered.
    def dark_ratio(box: tuple[int, int, int, int]) -> float:
        crop = image.crop(box).convert("RGB")
        pixels = list(crop.getdata())
        dark = sum(1 for r, g, b in pixels if r < 55 and g < 70 and b < 85)
        return dark / max(1, len(pixels))

    top_ratio = dark_ratio((0, 70, min(620, image.width), min(390, image.height)))
    middle_ratio = dark_ratio(
        (
            0,
            round(image.height * 0.45),
            min(660, image.width),
            round(image.height * 0.73),
        )
    )
    if top_ratio > 0.33:
        return True, "Overlay cobre topo/esquerda; pode esconder titulo, abas ou nome do pacote."
    if middle_ratio > 0.28:
        return True, "Overlay cobre meio/esquerda; pode esconder nome do pacote, itens ou parte da primeira oferta."
    if top_ratio > 0.18 or middle_ratio > 0.18:
        return True, "Overlay possivel no topo; conferir se nome/aba ficou legivel."
    return False, "Sem overlay relevante detectado na area principal."


def sold_out_score(image: Image.Image) -> bool:
    # The "Sold Out" stamp appears as one large red/pink connected shape.
    # Small red UI accents and item icons should not trigger this warning.
    crop = image.crop(
        (
            round(image.width * 0.38),
            round(image.height * 0.34),
            round(image.width * 0.96),
            round(image.height * 0.92),
        )
    ).convert("RGB")
    crop = crop.resize((220, 300), Image.Resampling.LANCZOS)
    mask = []
    for r, g, b in crop.getdata():
        mask.append(r > 185 and g < 125 and b < 145 and (r - g) > 60 and (r - b) > 55)

    width, height = crop.size
    seen = [False] * (width * height)
    biggest = 0
    for idx, is_red in enumerate(mask):
        if not is_red or seen[idx]:
            continue
        stack = [idx]
        seen[idx] = True
        size = 0
        while stack:
            current = stack.pop()
            size += 1
            x = current % width
            y = current // width
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if nx < 0 or ny < 0 or nx >= width or ny >= height:
                    continue
                next_idx = ny * width + nx
                if mask[next_idx] and not seen[next_idx]:
                    seen[next_idx] = True
                    stack.append(next_idx)
        biggest = max(biggest, size)
    return biggest > 420


def make_assets(path: pathlib.Path, key: str) -> tuple[str, str]:
    image = Image.open(path).convert("RGB")
    full = fit_image(image, 900)
    thumb = fit_image(image, 310)
    full_name = f"{key}.jpg"
    thumb_name = f"{key}_thumb.jpg"
    full.save(ASSET_DIR / full_name, "JPEG", quality=82, optimize=True)
    thumb.save(ASSET_DIR / thumb_name, "JPEG", quality=74, optimize=True)
    return f"assets/shop_captures/{full_name}", f"assets/shop_captures/{thumb_name}"


def parse_capture(path: pathlib.Path) -> dict | None:
    match = CAPTURE_RE.match(path.name)
    if not match:
        return None
    data = match.groupdict()
    cap = int(data["cap"])
    shop = int(data["shop"])
    key = f"loja{shop}_cap{cap:03d}"
    image = Image.open(path).convert("RGB")
    full, thumb = make_assets(path, key)
    overlay, overlay_note = overlay_score(image)
    sold_out = sold_out_score(image)
    stamp = datetime.strptime(data["stamp"], "%Y%m%d_%H%M%S")
    kind = data["kind"]
    return {
        "key": key,
        "file": path.name,
        "shop": shop,
        "cap": cap,
        "kind": kind,
        "kindLabel": KIND_LABEL.get(kind, kind.replace("_", " ").title()),
        "prices": int(data["prices"]),
        "tabs": int(data["tabs"]),
        "claim": int(data["claim"]),
        "rows": int(data["rows"]),
        "stamp": stamp.isoformat(timespec="seconds"),
        "stampLabel": stamp.strftime("%d/%m/%Y %H:%M:%S"),
        "session": data["session"],
        "width": image.width,
        "height": image.height,
        "full": full,
        "thumb": thumb,
        "overlay": overlay,
        "overlayNote": overlay_note,
        "soldOutLikely": sold_out,
        "reviewStatus": "Precisa leitura visual/OCR" if int(data["prices"]) else "Sem preco detectado pelo helper",
    }


def build_data() -> list[dict]:
    ensure_dir(ASSET_DIR)
    captures = []
    for path in sorted(SOURCE_DIR.glob("angroid_shop_*.png")):
        item = parse_capture(path)
        if item:
            captures.append(item)
    captures.sort(key=lambda row: (row["shop"], row["cap"]))
    return captures


def html_page(captures: list[dict]) -> str:
    by_shop = Counter(row["shop"] for row in captures)
    by_kind = Counter(row["kindLabel"] for row in captures)
    overlay_count = sum(1 for row in captures if row["overlay"])
    sold_count = sum(1 for row in captures if row["soldOutLikely"])
    price_total = sum(row["prices"] for row in captures)
    row_total = sum(row["rows"] for row in captures)
    shop_cards = "".join(
        f"<div class='stat'><span>Loja {shop}</span><strong>{count}</strong><small>capturas</small></div>"
        for shop, count in sorted(by_shop.items())
    )
    kind_options = "".join(f"<option>{label}</option>" for label in sorted(by_kind))
    data_json = json.dumps(captures, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Palmon Survival - Shop Capture Analyzer</title>
<style>
:root{{--bg:#f3f7fc;--paper:#fff;--ink:#15243a;--muted:#627086;--line:#d8e3f2;--blue:#2463eb;--green:#11845b;--amber:#b25b05;--red:#b42318;--shadow:0 14px 32px rgba(21,36,58,.10)}}
*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,Segoe UI,Arial,sans-serif;background:linear-gradient(180deg,#eef6ff,#f7fbff 28%,#eef3f8);color:var(--ink)}}a{{color:inherit;text-decoration:none}}button,input,select{{font:inherit}}
.wrap{{width:min(1420px,calc(100% - 32px));margin:0 auto;padding:24px 0 44px}}
.hero{{display:grid;grid-template-columns:minmax(0,1.1fr) auto;gap:18px;align-items:start;background:linear-gradient(135deg,#fff,#eff7ff);border:1px solid var(--line);border-radius:18px;padding:22px;box-shadow:var(--shadow)}}
.eyebrow{{display:inline-flex;border:1px solid #bdd6fb;background:#e9f3ff;color:#1556c4;border-radius:999px;padding:7px 11px;font-weight:900;font-size:12px}}h1{{font-size:clamp(30px,4vw,48px);line-height:1.02;margin:14px 0 10px}}p{{color:var(--muted);line-height:1.55;margin:0}}.hero-actions{{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}}.btn{{display:inline-flex;align-items:center;justify-content:center;min-height:42px;padding:0 14px;border-radius:11px;border:1px solid var(--line);background:#fff;font-weight:900}}.btn.primary{{background:#172033;color:#fff;border-color:#172033}}
.stats{{display:grid;grid-template-columns:repeat(6,minmax(120px,1fr));gap:10px;margin-top:16px}}.stat{{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:13px;box-shadow:0 1px 2px #0000000a}}.stat span{{display:block;color:var(--muted);font-size:12px;font-weight:900;text-transform:uppercase}}.stat strong{{display:block;font-size:26px;margin-top:6px}}.stat small{{color:var(--muted);font-weight:700}}
.filters{{display:grid;grid-template-columns:2fr repeat(5,minmax(130px,1fr));gap:10px;margin:18px 0}}.filters input,.filters select{{width:100%;border:1px solid #c8d5e6;border-radius:10px;background:#fff;padding:11px;color:var(--ink)}}.panel{{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px;margin-top:16px;box-shadow:var(--shadow)}}.panel h2{{margin:0 0 12px;font-size:22px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,310px));gap:14px;align-items:start}}.card{{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 8px 20px rgba(21,36,58,.07);display:grid;cursor:pointer}}.card img{{width:100%;aspect-ratio:9/16;object-fit:cover;object-position:top;background:#dbeafe;cursor:pointer}}.card-body{{padding:12px;display:grid;gap:9px}}.card h3{{margin:0;font-size:17px}}.chips{{display:flex;flex-wrap:wrap;gap:6px}}.chip{{border:1px solid #d4e0ef;background:#f7fbff;border-radius:999px;padding:4px 7px;font-size:12px;font-weight:900;color:#34445d}}.chip.ok{{background:#edfdf5;color:#086444;border-color:#b9ebd2}}.chip.warn{{background:#fff7ed;color:#8b3f04;border-color:#fed7aa}}.chip.bad{{background:#fff1f1;color:#991b1b;border-color:#fecaca}}.note{{font-size:13px;color:var(--muted)}}.table-wrap{{overflow:auto}}table{{width:100%;border-collapse:collapse;font-size:13px}}th,td{{border-bottom:1px solid #e5edf7;padding:9px 10px;text-align:left;vertical-align:top}}th{{background:#f8fbff;color:#34445d;position:sticky;top:0}}tr:hover td{{background:#fbfdff}}.mono{{font-family:ui-monospace,Consolas,monospace}}.hidden{{display:none!important}}
.modal{{position:fixed;inset:0;background:rgba(10,20,35,.72);display:none;align-items:center;justify-content:center;padding:22px;z-index:10000}}.modal.open{{display:flex}}.modal-card{{width:min(1120px,100%);height:min(92vh,980px);background:#fff;border-radius:16px;overflow:hidden;display:grid;grid-template-columns:minmax(0,1fr) 320px}}.modal-img{{width:100%;height:100%;object-fit:contain;background:#0f172a}}.modal-side{{padding:16px;overflow:auto}}.modal-side h2{{margin:0 0 8px}}.modal-side dl{{display:grid;grid-template-columns:110px 1fr;gap:8px;font-size:13px}}.modal-side dt{{font-weight:900;color:#64748b}}.modal-side dd{{margin:0;word-break:break-word}}.close{{position:absolute;right:22px;top:18px;border:0;background:#fff;color:#172033;border-radius:999px;width:42px;height:42px;font-weight:900;cursor:pointer;z-index:10001}}
.workflow{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:10px}}.workflow div{{border:1px solid var(--line);border-radius:12px;padding:12px;background:#fbfdff}}.workflow b{{display:block;margin-bottom:5px}}
@media(max-width:900px){{.hero{{grid-template-columns:1fr}}.stats,.filters{{grid-template-columns:1fr 1fr}}.modal-card{{grid-template-columns:1fr;height:92vh}}.modal-side{{max-height:36vh}}}}
@media(max-width:560px){{.wrap{{width:min(100% - 18px,1420px)}}.stats,.filters{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<div class="wrap">
  <section class="hero">
    <div>
      <span class="eyebrow">Palmon Survival Shop Flow</span>
      <h1>Análise da loja por prints do Android Helper</h1>
      <p>Esta página lê o padrão <b>angroid_shop_*.png</b>, organiza o fluxo capturado e mostra onde há preço, rows, abas, sold out provável e overlay visível. Os valores em R$ e itens ainda são conferidos visualmente no print.</p>
      <div class="hero-actions">
        <a class="btn primary" href="index.html">Voltar ao hub</a>
        <a class="btn" href="palmon_survival_pedia_completa.html">Abrir Pedia</a>
        <a class="btn" href="palmon_battle_simulator.html?mode=builder">Montar time</a>
      </div>
    </div>
    <div>
      <div class="stats">
        <div class="stat"><span>Capturas</span><strong>{len(captures)}</strong><small>prints lidos</small></div>
        <div class="stat"><span>Preços</span><strong>{price_total}</strong><small>botões detectados</small></div>
        <div class="stat"><span>Rows</span><strong>{row_total}</strong><small>linhas detectadas</small></div>
        <div class="stat"><span>Overlay</span><strong>{overlay_count}</strong><small>visível</small></div>
        <div class="stat"><span>Sold out</span><strong>{sold_count}</strong><small>provável</small></div>
        <div class="stat"><span>Lojas</span><strong>{len(by_shop)}</strong><small>fluxos</small></div>
      </div>
    </div>
  </section>

  <section class="panel">
    <h2>Resumo por loja</h2>
    <div class="stats">{shop_cards}</div>
  </section>

  <section class="panel">
    <h2>Fluxo recomendado</h2>
    <div class="workflow">
      <div><b>1. Filtre por item/preço</b><span class="note">Use loja, tipo e quantidade de preços para achar telas úteis.</span></div>
      <div><b>2. Abra o print</b><span class="note">Clique no card para ver o print grande e confirmar preço/itens.</span></div>
      <div><b>3. Marque valor real</b><span class="note">Quando quisermos, adiciono campos manuais de preço e item para cálculo automático.</span></div>
      <div><b>4. Próximas capturas</b><span class="note">Se o alerta de overlay aparecer, mova o overlay para não cobrir título/abas.</span></div>
    </div>
  </section>

  <div class="filters">
    <input id="search" placeholder="Buscar por arquivo, tipo, loja ou cap">
    <select id="shopFilter"><option value="all">Todas lojas</option>{''.join(f"<option>Loja {shop}</option>" for shop in sorted(by_shop))}</select>
    <select id="kindFilter"><option value="all">Todos tipos</option>{kind_options}</select>
    <select id="priceFilter"><option value="all">Qualquer preço</option><option value="with">Com preço</option><option value="none">Sem preço</option></select>
    <select id="overlayFilter"><option value="all">Overlay: todos</option><option value="warn">Com overlay</option><option value="ok">Sem overlay</option></select>
    <select id="soldFilter"><option value="all">Sold out: todos</option><option value="yes">Provável sold out</option><option value="no">Sem sold out provável</option></select>
  </div>

  <section class="panel">
    <h2>Capturas <span class="note" id="countLabel"></span></h2>
    <div class="grid" id="cards"></div>
  </section>

  <section class="panel">
    <h2>Tabela de auditoria</h2>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Cap</th><th>Tipo</th><th>Preços</th><th>Rows</th><th>Abas</th><th>Overlay</th><th>Sold out</th><th>Arquivo</th></tr></thead>
        <tbody id="rows"></tbody>
      </table>
    </div>
  </section>
</div>

<div class="modal" id="modal">
  <button class="close" id="closeModal">X</button>
  <div class="modal-card">
    <img class="modal-img" id="modalImg" alt="">
    <aside class="modal-side">
      <h2 id="modalTitle"></h2>
      <p class="note" id="modalNote"></p>
      <dl id="modalMeta"></dl>
    </aside>
  </div>
</div>

<script id="capture-data" type="application/json">{data_json}</script>
<script>
const DATA = JSON.parse(document.getElementById('capture-data').textContent);
const els = {{
  cards: document.getElementById('cards'),
  rows: document.getElementById('rows'),
  count: document.getElementById('countLabel'),
  search: document.getElementById('search'),
  shop: document.getElementById('shopFilter'),
  kind: document.getElementById('kindFilter'),
  price: document.getElementById('priceFilter'),
  overlay: document.getElementById('overlayFilter'),
  sold: document.getElementById('soldFilter'),
  modal: document.getElementById('modal'),
  modalImg: document.getElementById('modalImg'),
  modalTitle: document.getElementById('modalTitle'),
  modalNote: document.getElementById('modalNote'),
  modalMeta: document.getElementById('modalMeta'),
}};
function esc(value){{return String(value ?? '').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));}}
function chip(text, cls=''){{return `<span class="chip ${{cls}}">${{esc(text)}}</span>`;}}
function matches(row){{
  const q = els.search.value.trim().toLowerCase();
  const hay = `${{row.file}} ${{row.kindLabel}} loja ${{row.shop}} cap ${{row.cap}}`.toLowerCase();
  if(q && !hay.includes(q)) return false;
  if(els.shop.value !== 'all' && els.shop.value !== `Loja ${{row.shop}}`) return false;
  if(els.kind.value !== 'all' && els.kind.value !== row.kindLabel) return false;
  if(els.price.value === 'with' && row.prices <= 0) return false;
  if(els.price.value === 'none' && row.prices > 0) return false;
  if(els.overlay.value === 'warn' && !row.overlay) return false;
  if(els.overlay.value === 'ok' && row.overlay) return false;
  if(els.sold.value === 'yes' && !row.soldOutLikely) return false;
  if(els.sold.value === 'no' && row.soldOutLikely) return false;
  return true;
}}
function openModal(row){{
  els.modalImg.src = row.full;
  els.modalTitle.textContent = `Loja ${{row.shop}} · Cap ${{row.cap}}`;
  els.modalNote.textContent = row.overlayNote;
  els.modalMeta.innerHTML = `
    <dt>Tipo</dt><dd>${{esc(row.kindLabel)}}</dd>
    <dt>Preços</dt><dd>${{row.prices}}</dd>
    <dt>Rows</dt><dd>${{row.rows}}</dd>
    <dt>Abas</dt><dd>${{row.tabs}}</dd>
    <dt>Claim</dt><dd>${{row.claim}}</dd>
    <dt>Sold out</dt><dd>${{row.soldOutLikely ? 'provável' : 'não detectado'}}</dd>
    <dt>Horário</dt><dd>${{esc(row.stampLabel)}}</dd>
    <dt>Arquivo</dt><dd class="mono">${{esc(row.file)}}</dd>
  `;
  els.modal.classList.add('open');
}}
function card(row){{
  const overlay = row.overlay ? chip('overlay visível','warn') : chip('sem overlay','ok');
  const sold = row.soldOutLikely ? chip('sold out provável','bad') : chip('sem sold out','ok');
  const prices = row.prices ? chip(`${{row.prices}} preços`,'ok') : chip('sem preço','warn');
  return `<article class="card" data-key="${{esc(row.key)}}">
    <img src="${{esc(row.thumb)}}" alt="${{esc(row.file)}}" loading="lazy" data-open="${{esc(row.key)}}">
    <div class="card-body">
      <h3>Loja ${{row.shop}} · Cap ${{row.cap}}</h3>
      <div class="chips">${{chip(row.kindLabel)}}${{prices}}${{chip(row.rows + ' rows')}}${{overlay}}${{sold}}</div>
      <p class="note">${{esc(row.overlayNote)}}</p>
      <p class="note mono">${{esc(row.file)}}</p>
    </div>
  </article>`;
}}
function rowHtml(row){{
  return `<tr>
    <td><b>Loja ${{row.shop}}</b><br>Cap ${{row.cap}}</td>
    <td>${{esc(row.kindLabel)}}<br><span class="note">${{esc(row.stampLabel)}}</span></td>
    <td>${{row.prices}}</td>
    <td>${{row.rows}}</td>
    <td>${{row.tabs}}</td>
    <td>${{row.overlay ? '<span class="chip warn">visível</span>' : '<span class="chip ok">não</span>'}}</td>
    <td>${{row.soldOutLikely ? '<span class="chip bad">provável</span>' : '<span class="chip ok">não</span>'}}</td>
    <td class="mono">${{esc(row.file)}}</td>
  </tr>`;
}}
function render(){{
  const rows = DATA.filter(matches);
  els.count.textContent = `(${{rows.length}} de ${{DATA.length}})`;
  els.cards.innerHTML = rows.map(card).join('');
  els.rows.innerHTML = rows.map(rowHtml).join('');
  document.querySelectorAll('.card[data-key]').forEach(cardEl => cardEl.addEventListener('click', () => openModal(DATA.find(row => row.key === cardEl.dataset.key))));
}}
['input','change'].forEach(evt => {{
  [els.search, els.shop, els.kind, els.price, els.overlay, els.sold].forEach(el => el.addEventListener(evt, render));
}});
document.getElementById('closeModal').addEventListener('click', () => els.modal.classList.remove('open'));
els.modal.addEventListener('click', event => {{ if(event.target === els.modal) els.modal.classList.remove('open'); }});
render();
</script>
<script src="palmon_i18n.js"></script>
</body>
</html>
"""


def main() -> None:
    captures = build_data()
    OUT_HTML.write_text(html_page(captures), encoding="utf-8")
    print(f"Generated {OUT_HTML} with {len(captures)} captures.")


if __name__ == "__main__":
    main()
