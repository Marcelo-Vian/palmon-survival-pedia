import json
import os
import pathlib


ROOT = pathlib.Path(r"D:\Linkedin")
PEDIA_DIR = ROOT / "palmon_survival_pedia"
DATA_FILE = PEDIA_DIR / os.environ.get("PALMON_SHOP_DATA", "shop_active_offers_20260616.json")
OUT_HTML = PEDIA_DIR / "palmon_shop_captures.html"
THUMB_DIR = PEDIA_DIR / "assets" / "shop_offer_thumbs"


def load_data() -> dict:
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    for offer in data.get("offers", []):
        offer_id = offer.get("id")
        if not offer_id:
            continue
        thumb_path = THUMB_DIR / f"{offer_id}.jpg"
        if thumb_path.exists():
            offer["thumbnail"] = f"assets/shop_offer_thumbs/{offer_id}.jpg"
    return data


def html_page(data: dict) -> str:
    data_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Palmon Survival - Shop Table Analyzer</title>
<style>
:root{{--bg:#f4f8ff;--paper:#fff;--ink:#14243b;--muted:#607086;--line:#d7e4f5;--blue:#2563eb;--green:#0f7a4f;--amber:#a95b04;--red:#b42318;--shadow:0 14px 30px rgba(21,36,58,.10)}}
*{{box-sizing:border-box}}body{{margin:0;font-family:Inter,Segoe UI,Arial,sans-serif;background:linear-gradient(180deg,#eef7ff,#f8fbff 30%,#eef4fa);color:var(--ink)}}a{{color:inherit;text-decoration:none}}button,input,select{{font:inherit}}
.wrap{{width:min(1440px,calc(100% - 28px));margin:0 auto;padding:22px 0 46px}}
.hero{{background:linear-gradient(135deg,#fff,#edf7ff);border:1px solid var(--line);border-radius:18px;padding:22px;box-shadow:var(--shadow);display:grid;gap:16px}}
.topline{{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}}.eyebrow{{display:inline-flex;border:1px solid #bdd6fb;background:#e9f3ff;color:#1556c4;border-radius:999px;padding:7px 11px;font-weight:900;font-size:12px}}
h1{{font-size:clamp(30px,4.4vw,54px);line-height:1.02;margin:0}}p{{color:var(--muted);line-height:1.55;margin:0}}.hero-actions{{display:flex;gap:10px;flex-wrap:wrap}}.btn{{display:inline-flex;align-items:center;justify-content:center;min-height:42px;padding:0 14px;border-radius:11px;border:1px solid var(--line);background:#fff;font-weight:900;cursor:pointer}}.btn.primary{{background:#172033;color:#fff;border-color:#172033}}.btn.active{{background:#dbeafe;border-color:#93c5fd;color:#174ea6}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}}.stat{{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:13px;box-shadow:0 1px 2px #0000000a}}.stat span{{display:block;color:var(--muted);font-size:12px;font-weight:900;text-transform:uppercase}}.stat strong{{display:block;font-size:25px;margin-top:6px}}.stat small{{color:var(--muted);font-weight:700}}
.panel{{background:#fff;border:1px solid var(--line);border-radius:16px;padding:16px;margin-top:16px;box-shadow:var(--shadow)}}.panel h2{{margin:0 0 12px;font-size:22px}}.filters{{display:grid;grid-template-columns:2fr repeat(4,minmax(145px,1fr));gap:10px;margin-top:12px}}.filters input,.filters select{{width:100%;border:1px solid #c8d5e6;border-radius:10px;background:#fff;padding:11px;color:var(--ink)}}.hint{{font-size:13px;color:var(--muted)}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}}.score-card{{border:1px solid var(--line);border-radius:13px;padding:12px;background:#f8fbff}}.score-card b{{display:block;margin-bottom:6px}}.score-card strong{{font-size:22px}}.score-card small{{display:block;color:var(--muted);margin-top:3px}}
.table-wrap{{overflow:auto;border:1px solid #e5edf7;border-radius:12px}}table{{width:100%;border-collapse:collapse;font-size:13px;background:#fff}}th,td{{border-bottom:1px solid #e5edf7;padding:9px 10px;text-align:left;vertical-align:top}}th{{position:sticky;top:0;background:#f8fbff;color:#34445d;z-index:1}}tr:hover td{{background:#fbfdff}}.visual-col{{width:190px}}.offer-thumb{{display:block;width:178px;height:70px;border-radius:10px;border:1px solid #c9d8ea;object-fit:cover;background:#eef6ff;box-shadow:0 2px 8px #00000012}}.no-thumb{{width:178px;height:70px;border-radius:10px;border:1px dashed #c9d8ea;display:flex;align-items:center;justify-content:center;background:#f8fbff;color:var(--muted);font-weight:900;font-size:12px}}.offer-name{{font-weight:900;font-size:14px}}.muted{{color:var(--muted)}}.mono{{font-family:ui-monospace,Consolas,monospace}}.pill{{display:inline-flex;align-items:center;border-radius:999px;padding:4px 7px;font-size:12px;font-weight:900;border:1px solid #d4e0ef;background:#f7fbff;color:#34445d;margin:1px 3px 1px 0;white-space:nowrap}}.pill.ok{{background:#edfdf5;color:#086444;border-color:#b9ebd2}}.pill.warn{{background:#fff7ed;color:#8b3f04;border-color:#fed7aa}}.pill.bad{{background:#fff1f1;color:#991b1b;border-color:#fecaca}}.pill.blue{{background:#eff6ff;color:#1d4ed8;border-color:#bfdbfe}}.items{{display:flex;gap:5px;flex-wrap:wrap;max-width:560px}}.decision{{min-width:230px}}.foot{{margin-top:14px;color:var(--muted);font-size:13px;line-height:1.55}}
@media(max-width:900px){{.filters{{grid-template-columns:1fr 1fr}}h1{{font-size:34px}}}}
@media(max-width:560px){{.wrap{{width:min(100% - 18px,1440px)}}.filters{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<main class="wrap">
  <section class="hero">
    <div class="topline">
      <span class="eyebrow">Palmon Survival Shop Analyzer 2026</span>
      <div class="hero-actions">
        <a class="btn primary" href="index.html">Voltar ao hub</a>
        <a class="btn" href="palmon_survival_pedia_completa.html">Abrir Pedia</a>
      </div>
    </div>
    <h1>Tabela de pacotes, itens e preços extraída dos prints</h1>
    <p>Sem publicar telas completas: esta página usa os prints como fonte, mostra só recortes pequenos dos pacotes e transforma as ofertas ativas em tabela filtrável. Itens com ícone sem texto oficial ficam com nome funcional e confiança marcada.</p>
    <div class="stats" id="stats"></div>
  </section>

  <section class="panel">
    <h2>Melhores decisões rápidas</h2>
    <div class="cards" id="bestCards"></div>
    <p class="foot">Regra prática: compare por recurso-alvo. Pacote de Palmon só vale se você usa aquele Palmon; passe de evento só vale se você completa a trilha; Pallite pura deve ser comparada por Pallite/R$.</p>
  </section>

  <section class="panel">
    <h2>Filtros</h2>
    <div class="filters">
      <input id="search" placeholder="Buscar pacote, item, seção ou cap">
      <select id="categoryFilter"><option value="">Todas categorias</option></select>
      <select id="statusFilter">
        <option value="">Todos status</option>
        <option value="ativo">Ativo</option>
        <option value="pendente">Pendente/amanhã</option>
        <option value="comprado">Comprado/indisponível</option>
      </select>
      <select id="resourceFilter"><option value="">Ordenar por recurso</option></select>
      <select id="confidenceFilter">
        <option value="">Toda confiança</option>
        <option value="alta">Alta</option>
        <option value="media">Média</option>
        <option value="baixa">Baixa/parcial</option>
      </select>
    </div>
    <p class="hint" id="filterHint"></p>
  </section>

  <section class="panel">
    <h2>Ofertas extraídas <span class="hint" id="countLabel"></span></h2>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th class="visual-col">Visual</th>
            <th>Pacote</th>
            <th>Preço</th>
            <th>Itens</th>
            <th>Score do filtro</th>
            <th>Decisão</th>
            <th>Fonte</th>
          </tr>
        </thead>
        <tbody id="offerRows"></tbody>
      </table>
    </div>
    <p class="foot">Fonte: {data.get("captured_at", "")}. {data.get("source_note", "")}</p>
  </section>
</main>

<script id="shop-data" type="application/json">{data_json}</script>
<script>
const DATA = JSON.parse(document.getElementById('shop-data').textContent);
const OFFERS = DATA.offers || [];
const els = {{
  stats: document.getElementById('stats'),
  bestCards: document.getElementById('bestCards'),
  search: document.getElementById('search'),
  category: document.getElementById('categoryFilter'),
  status: document.getElementById('statusFilter'),
  resource: document.getElementById('resourceFilter'),
  confidence: document.getElementById('confidenceFilter'),
  hint: document.getElementById('filterHint'),
  count: document.getElementById('countLabel'),
  rows: document.getElementById('offerRows'),
}};
function esc(value) {{ return String(value ?? '').replace(/[&<>"']/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c])); }}
function norm(value) {{ return String(value || '').normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase(); }}
function brl(value) {{ return Number.isFinite(Number(value)) ? Number(value).toLocaleString('pt-BR', {{ style:'currency', currency:'BRL' }}) : '-'; }}
function fmt(value) {{ return Number.isFinite(Number(value)) ? Number(value).toLocaleString('pt-BR', {{ maximumFractionDigits: 2 }}) : '-'; }}
function itemMetric(item) {{ return Number(item.metric_qty ?? item.qty); }}
function resourceTotal(offer, category) {{
  if (!category) return null;
  let total = 0;
  for (const item of offer.items || []) {{
    if (item.category !== category) continue;
    const qty = itemMetric(item);
    if (Number.isFinite(qty)) total += qty;
  }}
  return total || null;
}}
function unitLabel(offer, category) {{
  const item = (offer.items || []).find(row => row.category === category && Number.isFinite(itemMetric(row)));
  if (!item) return category;
  return item.metric_unit || item.unit || category;
}}
function score(offer, category) {{
  const total = resourceTotal(offer, category);
  const price = Number(offer.price_brl);
  if (!total || !Number.isFinite(price) || price <= 0) return null;
  return total / price;
}}
function allCategories() {{
  return Array.from(new Set(OFFERS.flatMap(offer => (offer.items || []).map(item => item.category)).filter(Boolean))).sort();
}}
function optionList() {{
  for (const category of allCategories()) {{
    els.category.insertAdjacentHTML('beforeend', `<option value="${{esc(category)}}">${{esc(category)}}</option>`);
    els.resource.insertAdjacentHTML('beforeend', `<option value="${{esc(category)}}">${{esc(category)}} / R$</option>`);
  }}
}}
function statusClass(value) {{
  const v = norm(value);
  if (v.includes('ativo')) return 'ok';
  if (v.includes('pendente')) return 'warn';
  return 'bad';
}}
function confidenceClass(value) {{
  if (value === 'alta') return 'ok';
  if (value === 'media') return 'warn';
  return 'bad';
}}
function itemsText(offer) {{
  return (offer.items || []).map(item => `${{item.name}} ${{item.qty ?? ''}} ${{item.unit || ''}} ${{item.category}}`).join(' ');
}}
function matches(offer) {{
  const q = norm(els.search.value).split(/\\s+/).filter(Boolean);
  const blob = norm(`${{offer.name}} ${{offer.section}} ${{offer.type}} ${{offer.status}} ${{offer.source_caps}} ${{itemsText(offer)}}`);
  if (q.length && !q.every(token => blob.includes(token))) return false;
  if (els.category.value && !(offer.items || []).some(item => item.category === els.category.value)) return false;
  if (els.status.value && !norm(offer.status).includes(norm(els.status.value))) return false;
  if (els.confidence.value && offer.confidence !== els.confidence.value) return false;
  return true;
}}
function sortedRows(rows) {{
  const resource = els.resource.value;
  if (!resource) return rows.sort((a,b) => (Number(a.price_brl) || 999999) - (Number(b.price_brl) || 999999));
  return rows.sort((a,b) => (score(b, resource) || -1) - (score(a, resource) || -1));
}}
function statCards() {{
  const active = OFFERS.filter(o => norm(o.status).includes('ativo')).length;
  const priced = OFFERS.filter(o => Number.isFinite(Number(o.price_brl))).length;
  const categories = allCategories().length;
  const prices = OFFERS.map(o => Number(o.price_brl)).filter(Number.isFinite);
  const min = Math.min(...prices);
  els.stats.innerHTML = `
    <div class="stat"><span>Ofertas</span><strong>${{OFFERS.length}}</strong><small>linhas deduplicadas</small></div>
    <div class="stat"><span>Ativas</span><strong>${{active}}</strong><small>com preço/compra visível</small></div>
    <div class="stat"><span>Com preço</span><strong>${{priced}}</strong><small>R$ extraído do print</small></div>
    <div class="stat"><span>Categorias</span><strong>${{categories}}</strong><small>itens filtráveis</small></div>
    <div class="stat"><span>Menor ticket</span><strong>${{brl(min)}}</strong><small>pacote mais barato</small></div>
  `;
}}
function bestFor(category) {{
  return OFFERS
    .filter(o => norm(o.status).includes('ativo') && Number.isFinite(Number(o.price_brl)) && score(o, category))
    .sort((a,b) => score(b, category) - score(a, category))[0];
}}
function bestCards() {{
  const pallite = bestFor('Pallite');
  const speed = bestFor('Acelerador');
  const skill = bestFor('Skillfruit');
  const lowSpend = OFFERS.filter(o => norm(o.status).includes('ativo') && Number(o.price_brl) <= 20).sort((a,b)=>Number(a.price_brl)-Number(b.price_brl))[0];
  const cards = [
    ['Melhor Pallite/R$', pallite, 'Pallite'],
    ['Melhor acelerador/R$', speed, 'Acelerador'],
    ['Melhor Skillfruit/R$', skill, 'Skillfruit'],
    ['Menor gasto útil', lowSpend, 'Pallite'],
  ];
  els.bestCards.innerHTML = cards.map(([title, offer, category]) => {{
    if (!offer) return `<div class="score-card"><b>${{esc(title)}}</b><span class="muted">Sem dado confirmado.</span></div>`;
    const s = score(offer, category);
    const label = s ? `${{fmt(s)}} ${{esc(unitLabel(offer, category))}}/R$` : brl(offer.price_brl);
    return `<div class="score-card"><b>${{esc(title)}}</b><strong>${{esc(offer.name)}}</strong><small>${{brl(offer.price_brl)}} · ${{label}}</small></div>`;
  }}).join('');
}}
function itemsHtml(offer) {{
  return `<div class="items">${{(offer.items || []).map(item => {{
    const qty = item.qty === null || item.qty === undefined ? '' : ` <b>${{esc(item.qty)}}</b>`;
    const unit = item.unit ? ` ${{esc(item.unit)}}` : '';
    return `<span class="pill blue" title="${{esc(item.category)}}">${{esc(item.name)}}${{qty}}${{unit}}</span>`;
  }}).join('')}}</div>`;
}}
function thumbHtml(offer) {{
  if (!offer.thumbnail) return '<div class="no-thumb">sem recorte</div>';
  return `<a href="${{esc(offer.thumbnail)}}" target="_blank" rel="noopener"><img class="offer-thumb" src="${{esc(offer.thumbnail)}}" alt="Recorte do pacote ${{esc(offer.name)}}"></a>`;
}}
function scoreHtml(offer) {{
  const category = els.resource.value;
  if (!category) return '<span class="muted">Escolha recurso para calcular.</span>';
  const total = resourceTotal(offer, category);
  const s = score(offer, category);
  if (!total || !s) return '<span class="muted">Sem qtd. comparável.</span>';
  return `<b>${{fmt(s)}} ${{esc(unitLabel(offer, category))}}/R$</b><br><span class="muted">total: ${{fmt(total)}} ${{esc(unitLabel(offer, category))}}</span>`;
}}
function rowHtml(offer) {{
  return `<tr>
    <td>${{thumbHtml(offer)}}</td>
    <td>
      <div class="offer-name">${{esc(offer.name)}}</div>
      <span class="pill">${{esc(offer.section)}}</span>
      <span class="pill">${{esc(offer.type)}}</span>
      <span class="pill ${{statusClass(offer.status)}}">${{esc(offer.status)}}</span>
      <span class="pill ${{confidenceClass(offer.confidence)}}">conf. ${{esc(offer.confidence)}}</span>
    </td>
    <td><b>${{brl(offer.price_brl)}}</b><br><span class="muted">${{offer.currency_bonus ? '+' + esc(offer.currency_bonus) + ' moeda/evento' : '-'}}</span><br><span class="muted">${{esc(offer.limit || '')}}</span></td>
    <td>${{itemsHtml(offer)}}</td>
    <td>${{scoreHtml(offer)}}</td>
    <td class="decision">${{esc(offer.recommendation || '')}}</td>
    <td><span class="mono">${{esc(offer.source_caps)}}</span></td>
  </tr>`;
}}
function render() {{
  const rows = sortedRows(OFFERS.filter(matches));
  els.count.textContent = `(${{rows.length}} de ${{OFFERS.length}})`;
  const res = els.resource.value;
  els.hint.textContent = res ? `Ordenando por melhor custo de ${{res}} por real. Linhas sem quantidade comparável ficam embaixo.` : 'Escolha um recurso em "Ordenar por recurso" para comparar custo/benefício.';
  els.rows.innerHTML = rows.length ? rows.map(rowHtml).join('') : '<tr><td colspan="7"><span class="muted">Nenhuma oferta para este filtro.</span></td></tr>';
}}
optionList();
statCards();
bestCards();
for (const el of [els.search, els.category, els.status, els.resource, els.confidence]) {{
  el.addEventListener('input', render);
  el.addEventListener('change', render);
}}
render();
</script>
<script src="palmon_i18n.js"></script>
</body>
</html>
"""


def main() -> None:
    data = load_data()
    OUT_HTML.write_text(html_page(data), encoding="utf-8")
    print(f"Generated {OUT_HTML} with {len(data.get('offers', []))} offers.")


if __name__ == "__main__":
    main()
