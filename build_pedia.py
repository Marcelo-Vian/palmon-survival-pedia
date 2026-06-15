import csv
import html
import json
import pathlib
import re
from collections import Counter


ROOT = pathlib.Path(r"D:\Linkedin")
PEDIA_DIR = ROOT / "palmon_survival_pedia"
RANK_CSV = ROOT / "palmon_survival_rank_visual" / "palmon_ranking_geral_melhor_pior.csv"
FICHAS_JSON = ROOT / "palmon_survival_apk" / "analysis" / "parsed" / "palmon_fichas_apk_enriquecidas.json"
TRAITS_CSV = ROOT / "palmon_survival_apk" / "analysis" / "parsed" / "traits_s_apk.csv"
OUT_HTML = PEDIA_DIR / "palmon_survival_pedia_completa.html"
OUT_MD = PEDIA_DIR / "palmon_survival_pedia_resumo.md"


def fix_text(value):
    if value is None:
        return ""
    text = str(value)
    replacements = {
        "El?trico": "Eletrico",
        "?gua": "Agua",
        "?pico": "Epico",
        "m?ximo": "maximo",
        "posi??o": "posicao",
        "redu??o": "reducao",
        "evolu??o": "evolucao",
        "est?": "esta",
        "b?nus": "bonus",
        "estrat?gico": "estrategico",
        "extra?dos": "extraidos",
        "PerdiÃ§Ã£o": "Perdição",
        "ProteÃ§Ã£o": "Proteção",
        "ExplosÃ£o": "Explosão",
        "RelÃ¢mpago": "Relâmpago",
        "GÃ©lida": "Gélida",
        "Ãguas": "Águas",
        "Ãmpeto": "Ímpeto",
        "VÃ³rtice": "Vórtice",
        "BÃªnÃ§Ã£o": "Bênção",
        "DinÃ¢mica": "Dinâmica",
        "ElÃ©trica": "Elétrica",
        "IÃ´nicos": "Iônicos",
        "AbÃ³bora": "Abóbora",
        "CrÃ¢nio": "Crânio",
        "Inabalavel": "Inabalável",
        "Determinacao": "Determinação",
        "Aco": "Aço",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def esc(value):
    return html.escape(fix_text(value))


def short_num(value):
    try:
        number = float(value)
        if abs(number - int(number)) < 0.001:
            return f"{int(number):,}".replace(",", ".")
        return f"{number:.1f}"
    except Exception:
        return fix_text(value)


def pct_from_skill(skill):
    for key in ("dano_5estrelas_lv30", "damage_server_5star", "damage_client"):
        if skill.get(key) not in (None, ""):
            return fix_text(skill.get(key))
    return ""


def tier_class(tier):
    return "tier-" + re.sub("[^A-Za-z0-9]", "", tier or "")


def load_data():
    rank_rows = list(csv.DictReader(RANK_CSV.read_text(encoding="utf-8-sig").splitlines(), delimiter=";"))
    fichas = json.loads(FICHAS_JSON.read_text(encoding="utf-8"))
    traits = list(csv.DictReader(TRAITS_CSV.read_text(encoding="utf-8-sig").splitlines(), delimiter=";"))
    by_name = {row["nome"]: row for row in fichas}
    rows = []
    for row in rank_rows:
        if not row.get("nome"):
            continue
        fixed = {key: fix_text(value) for key, value in row.items()}
        fixed["_detail"] = by_name.get(row["nome"], {})
        rows.append(fixed)
    return rows, traits


def bar_list(counter):
    total = sum(counter.values()) or 1
    parts = []
    for key, value in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        width = (value / total) * 100
        parts.append(
            f'<div class="bar-row"><span>{esc(key)}</span>'
            f'<div class="bar"><i style="width:{width:.1f}%"></i></div><b>{value}</b></div>'
        )
    return "".join(parts)


def source_table():
    rows = [
        (
            "XAPK/APK Palmon Survival 0.5.277",
            "Arquivo local analisado em 2026-06-05",
            "APK/config",
            "Alta para dados internos da versão",
            "hero, card_skill_pal, card_buff_pal, hero_evolve_potency, traits, scene_map",
        ),
        (
            "AllClash - Important Rules for Breeding",
            "https://www.allclash.com/important-rules-for-breeding-in-palmon-survival/",
            "Guia comunidade",
            "Média",
            "Publicado em 2026-04-30; usado para regras de breeding/perks",
        ),
        (
            "Site oficial Palmon Survival",
            "https://palmonsurvival-official.lilith.com/",
            "Oficial",
            "Alta",
            "Usado para identidade/canais oficiais; pouco detalhe mecânico",
        ),
        (
            "Google Play",
            "https://play.google.com/store/apps/details?id=com.funfizz.palmon.gp",
            "Loja oficial",
            "Alta",
            "Descrição do jogo, compras no app e dados de loja da pesquisa 2026",
        ),
        (
            "App Store",
            "https://apps.apple.com/us/app/palmon-survival/id6739345737",
            "Loja oficial",
            "Alta",
            "Versão, categoria, loot boxes/compras e dados de loja",
        ),
        (
            "X oficial - patch 2026-01-27",
            "https://x.com/PalmonSurvival/status/2016058598250405897",
            "Patch oficial",
            "Alta",
            "Guild Nursery, Electric Frenzy, Skin Hub, Monday Market, VIP Shop, Surging Snows e fixes",
        ),
        (
            "PalmonGuide 2026",
            "https://www.palmonguide.com/",
            "Guia comunidade",
            "Média",
            "Evolution, traits, Palmanac e builds gerais; tratar como comunidade",
        ),
        (
            "Reddit guias 2026",
            "https://www.reddit.com/r/PalmonSurvival/",
            "Comunidade/forum",
            "Baixa-média",
            "Usado como evidência de jogador; nunca como regra oficial isolada",
        ),
    ]
    cells = []
    for name, link, kind, confidence, notes in rows:
        link_html = f'<a href="{link}" target="_blank">abrir</a>' if link.startswith("http") else esc(link)
        cells.append(
            f"<tr><td>{esc(name)}</td><td>{link_html}</td><td>{esc(kind)}</td>"
            f"<td>{esc(confidence)}</td><td>{esc(notes)}</td></tr>"
        )
    return "".join(cells)


PERK_PROFILES = [
    (
        "Tank",
        "Vigorous/Vigoroso HP +10% | Unshakeable/Inabalável DEF +10% | Robust/Robusto HP +7% | Steel Skull/Crânio de Aço Crit Dmg Reduction +8%",
        "Unyielding/Indomável, Steadfast/Firme, Clear-Headed/Lúcido, Elusive/Evasivo",
        "Tank do Slot 2; precisa durar e absorver pressão.",
    ),
    (
        "DPS fundo",
        "Warlike/Guerreiro ATK +10% | Belligerent/Beligerante ATK +7% | Blessed/Abençoado Crit Rate +8% | Heartless/Impiedoso Crit Dmg +15%",
        "Deadeye/Certeiro, Sharpshooter/Franco-atirador, Ruthless/Cruel, Fortunate/Afortunado, Robust se morrer cedo",
        "Carry protegido na backline; maximiza dano.",
    ),
    (
        "DPS frente/bruiser",
        "Warlike/Guerreiro ATK +10% | Belligerent/Beligerante ATK +7% | Robust/Robusto HP +7% | Vigorous/Vigoroso HP +10%",
        "Steel Skull, Unyielding ou Blessed se o combate pedir mais defesa ou dano",
        "Frontliner agressivo dos flancos; dano sem explodir cedo.",
    ),
    (
        "Suporte/controle",
        "Vigorous/Vigoroso HP +10% | Robust/Robusto HP +7% | Unshakeable/Inabalável DEF +10% | Iron Will/Determinação de Ferro Tenacity +8%",
        "Clear-Headed contra stun, Steel Skull contra burst, Belligerent se também for carry",
        "Precisa sobreviver para buffar, reduzir dano ou controlar mais vezes.",
    ),
]

SLOT_MAP = [
    ("1", "Frente esquerda", "off-tank, controle, bruiser lateral"),
    ("2", "Frente meio", "tank principal ou iniciador mais importante"),
    ("6", "Frente direita", "flanco agressivo, salto/backline, controle"),
    ("3", "Fundo esquerda", "DPS secundário ou suporte menos prioritário"),
    ("4", "Fundo meio-esquerda", "DPS/buffer mais valioso protegido"),
    ("5", "Fundo meio-direita", "DPS/controle AOE protegido"),
    ("7", "Fundo direita", "DPS secundário, atacante de linha de trás ou isca lateral"),
]


def build_rank_table(rows):
    table_rows = []
    for row in rows:
        img = esc(row.get("imagem", ""))
        data = (
            f'data-name="{esc(row.get("nome", "")).lower()}" data-tier="{esc(row.get("tier"))}" '
            f'data-element="{esc(row.get("elemento"))}" data-pos="{esc(row.get("posicao"))}" '
            f'data-role="{esc(row.get("perk_perfil"))}"'
        )
        table_rows.append(
            f"<tr {data}><td class=\"ranknum\">{esc(row.get('rank_geral'))}</td>"
            f"<td><span class=\"tier {tier_class(row.get('tier'))}\">{esc(row.get('tier'))}</span></td>"
            f"<td><img src=\"{img}\" class=\"mini\" alt=\"{esc(row.get('nome'))}\"></td>"
            f"<td><b>{esc(row.get('nome'))}</b><br><small>{esc(row.get('evoluido'))}</small></td>"
            f"<td>{esc(row.get('elemento'))}<br><small>forte {esc(row.get('forte'))} · fraco {esc(row.get('fraco'))}</small></td>"
            f"<td>{esc(row.get('posicao'))}</td><td>{esc(row.get('slot_recomendado'))}</td>"
            f"<td><b>{esc(row.get('focar_primeiro'))}</b><br><small>{esc(row.get('skill_prioridade'))}</small></td>"
            f"<td>{esc(row.get('perk_perfil'))}</td><td>{esc(row.get('rank_bruto'))}</td></tr>"
        )
    return "".join(table_rows)


def build_pal_cards(rows):
    cards = []
    for row in rows:
        detail = row.get("_detail", {})
        skill_items = []
        for skill in detail.get("skills", []) or []:
            meta = []
            damage = pct_from_skill(skill)
            target = skill.get("alvo")
            if damage:
                meta.append(f"Valor: {damage}")
            if target not in (None, [], ""):
                meta.append(f"Alvo APK: {target}")
            meta_html = f"<small>{esc(' · '.join(meta))}</small>" if meta else ""
            skill_items.append(
                f"<li><b>{esc(skill.get('nome'))}</b> {meta_html}<br>{esc(skill.get('descricao'))}</li>"
            )
        skill_html = "".join(skill_items)
        img = esc(row.get("imagem", ""))
        evo_img = esc(row.get("imagem_evoluida", ""))
        evo_tag = f'<img class="evo" src="{evo_img}" alt="{esc(row.get("evoluido"))}">' if evo_img else ""
        data = (
            f'data-name="{esc(row.get("nome", "")).lower()}" data-tier="{esc(row.get("tier"))}" '
            f'data-element="{esc(row.get("elemento"))}" data-pos="{esc(row.get("posicao"))}" '
            f'data-role="{esc(row.get("perk_perfil"))}"'
        )
        cards.append(
            f"""<article class="pal-card" {data}>
<div class="card-media"><span class="rank-badge">#{esc(row.get('rank_geral'))}</span><img src="{img}" alt="{esc(row.get('nome'))}">{evo_tag}</div>
<div class="card-body">
  <div class="card-title"><h3>{esc(row.get('nome'))}</h3><span class="tier {tier_class(row.get('tier'))}">{esc(row.get('tier'))}</span></div>
  <p class="evo-line">Evolução: <b>{esc(row.get('evoluido') or 'não confirmada')}</b></p>
  <div class="chips"><span>{esc(row.get('raridade'))}</span><span>{esc(row.get('elemento'))}</span><span>{esc(row.get('posicao'))}</span><span>{esc(row.get('perk_perfil'))}</span></div>
  <p><b>Função:</b> {esc(row.get('funcao'))}</p>
  <p><b>Elemento:</b> forte contra {esc(row.get('forte'))}; fraco contra {esc(row.get('fraco'))}.</p>
  <p><b>Melhor slot:</b> {esc(row.get('slot_recomendado'))}<br><small>{esc(row.get('slot_motivo'))} Alt.: {esc(row.get('slot_alternativo'))}</small></p>
  <p class="perk"><b>Perks:</b> {esc(row.get('perks_recomendadas'))}<br><small>Alternativas: {esc(row.get('perks_alternativas'))}</small></p>
  <p class="focus"><b>Skill para focar:</b> {esc(row.get('focar_primeiro'))}<br>{esc(row.get('motivo_skill'))}</p>
  <p><b>Stats APK:</b> Power {esc(short_num(row.get('power')))} · ATK {esc(short_num(row.get('attack')))} · DEF {esc(short_num(row.get('defense')))} · HP {esc(short_num(row.get('hp')))}</p>
  <details><summary>Habilidades completas</summary><ul>{skill_html}</ul></details>
</div>
</article>"""
        )
    return "".join(cards)


def build_html(rows, traits):
    image_count = len(list((PEDIA_DIR / "images").glob("*.png")))
    element_counts = Counter(row.get("elemento") for row in rows)
    tier_counts = Counter(row.get("tier") for row in rows)
    pos_counts = Counter(row.get("posicao") for row in rows)
    role_counts = Counter(row.get("perk_perfil") for row in rows)

    stat_cards = "".join(
        f'<div class="stat-card"><span>{value}</span><small>{label}</small></div>'
        for label, value in [
            ("Palmons catalogados", len(rows)),
            ("Imagens locais", image_count),
            ("Tier SS", sum(1 for row in rows if row.get("tier") == "SS")),
            ("UR no ranking", sum(1 for row in rows if row.get("raridade") == "UR")),
            ("Frente", sum(1 for row in rows if row.get("posicao") == "Frente")),
            ("Fundo", sum(1 for row in rows if row.get("posicao") == "Fundo")),
        ]
    )

    perk_cards = "".join(
        f'<article class="rule-card"><h3>{esc(name)}</h3><p><b>4 perks padrão:</b><br>{esc(perks)}</p>'
        f"<p><b>Alternativas:</b><br>{esc(alts)}</p><p><b>Uso:</b> {esc(use)}</p></article>"
        for name, perks, alts, use in PERK_PROFILES
    )
    slot_cards = "".join(
        f'<div class="slot-card {"front" if "Frente" in label else "back"}"><b>Slot {slot}</b>'
        f"<span>{esc(label)}</span><small>{esc(use)}</small></div>"
        for slot, label, use in SLOT_MAP
    )
    traits_table = "".join(
        f"<tr><td>{esc(row.get('name'))}</td><td>{esc(row.get('name_pt'))}</td><td>{esc(row.get('effect'))}</td>"
        f"<td>{esc(row.get('fight_value'))}</td><td>{esc(row.get('value_raw'))}</td></tr>"
        for row in traits
    )
    rank_table = build_rank_table(rows)
    pal_cards = build_pal_cards(rows)

    best_tanks = "".join(
        f"<li><b>#{esc(row['rank_geral'])} {esc(row['nome'])}</b> <span>{esc(row['slot_recomendado'])} · {esc(row['focar_primeiro'])}</span></li>"
        for row in rows
        if row.get("perk_perfil") == "Tank"
    )
    best_dps = "".join(
        f"<li><b>#{esc(row['rank_geral'])} {esc(row['nome'])}</b> <span>{esc(row['elemento'])} · {esc(row['slot_recomendado'])} · foco {esc(row['focar_primeiro'])}</span></li>"
        for row in rows
        if row.get("perk_perfil") in ("DPS fundo", "DPS frente/bruiser") and int(row.get("rank_geral", "999")) <= 16
    )
    best_support = "".join(
        f"<li><b>#{esc(row['rank_geral'])} {esc(row['nome'])}</b> <span>{esc(row['slot_recomendado'])} · {esc(row['focar_primeiro'])}</span></li>"
        for row in rows
        if row.get("perk_perfil") == "Suporte/controle"
    )

    css = r"""
:root{--ink:#162033;--muted:#667085;--line:#dbe3ee;--paper:#fff;--soft:#f5f7fb;--blue:#2563eb;--green:#16a34a;--gold:#b7791f;--purple:#7c3aed;--teal:#0f766e;--radius:8px}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:Inter,Segoe UI,Arial,sans-serif;background:#f3f6fa;color:var(--ink)}a{color:#1d4ed8;text-decoration:none}a:hover{text-decoration:underline}
.layout{display:grid;grid-template-columns:270px minmax(0,1fr);min-height:100vh}aside{position:sticky;top:0;height:100vh;overflow:auto;background:#fff;border-right:1px solid var(--line);padding:18px 14px}main{min-width:0}.brand{font-weight:900;font-size:20px;line-height:1.1;margin-bottom:4px}.brand small{display:block;color:var(--muted);font-weight:700;font-size:12px;margin-top:6px}nav a{display:block;padding:8px 10px;border-radius:6px;color:#293548;font-weight:700;font-size:13px}nav a:hover{background:#eef4ff;text-decoration:none}
.hero{background:linear-gradient(180deg,#e8f1ff,#fff);border-bottom:1px solid var(--line);padding:28px 28px 22px}.hero h1{font-size:34px;margin:0 0 8px;letter-spacing:0}.hero p{max-width:920px;color:#475467;font-size:15px;line-height:1.5;margin:0}.stat-grid{display:grid;grid-template-columns:repeat(6,minmax(120px,1fr));gap:10px;margin-top:18px}.stat-card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:12px;box-shadow:0 1px 2px #0000000c}.stat-card span{font-size:24px;font-weight:900;display:block}.stat-card small{color:var(--muted);font-weight:700}
.section{padding:22px 28px;border-bottom:1px solid var(--line)}.section h2{font-size:24px;margin:0 0 10px}.section h3{font-size:17px;margin:0 0 8px}.lead{color:#475467;max-width:980px;line-height:1.5}.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:14px}.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.rule-card,.info-card,.element-card,.slot-card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:13px;box-shadow:0 1px 2px #0000000b}.rule-card{background:#fbfffc;border-color:#c9efd5}.info-card ul{margin:8px 0 0 18px;padding:0}.info-card li{margin:7px 0}.info-card span{color:var(--muted)}.callout{background:#fffaf0;border-left:4px solid #d69e2e;border-radius:6px;padding:10px 12px;margin:10px 0;color:#45320b}.danger{background:#fff5f5;border-left-color:#e53e3e;color:#591b1b}.ok{background:#f0fff4;border-left-color:#16a34a;color:#12351f}
.table-wrap{overflow:auto;background:#fff;border:1px solid var(--line);border-radius:var(--radius)}table{width:100%;border-collapse:collapse;font-size:13px}th,td{padding:9px 10px;border-bottom:1px solid #e8edf5;text-align:left;vertical-align:top}th{background:#f8fafc;color:#344054;position:sticky;top:0;z-index:1}tr:last-child td{border-bottom:0}.ranknum{font-size:18px;font-weight:900;text-align:center}.mini{width:46px;height:46px;object-fit:contain}.tier{display:inline-flex;min-width:34px;height:24px;align-items:center;justify-content:center;border-radius:6px;color:#fff;font-weight:900;font-size:12px}.tier-SS{background:var(--purple)}.tier-S{background:var(--teal)}.tier-A{background:var(--blue)}.tier-B{background:var(--gold)}.tier-C{background:#64748b}
.filters{display:grid;grid-template-columns:2fr repeat(4,1fr);gap:8px;margin:12px 0}input,select{border:1px solid #cfd8e3;background:#fff;border-radius:6px;padding:9px 10px;font:inherit;font-size:14px}.toolbar-note{font-size:12px;color:var(--muted);margin-top:6px}.pal-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:14px}.pal-card{background:#fff;border:1px solid var(--line);border-radius:var(--radius);display:grid;grid-template-columns:138px 1fr;min-height:320px;overflow:hidden;box-shadow:0 1px 2px #0000000c}.card-media{position:relative;background:linear-gradient(180deg,#eef4ff,#fff);display:flex;align-items:center;justify-content:center;padding:12px}.card-media img{max-width:130px;max-height:230px;object-fit:contain}.card-media .evo{position:absolute;right:6px;bottom:6px;width:58px;height:72px;background:#ffffffdf;border:1px solid var(--line);border-radius:6px}.rank-badge{position:absolute;top:8px;left:8px;background:#162033;color:#fff;font-weight:900;border-radius:6px;padding:4px 8px}.card-body{padding:13px}.card-title{display:flex;align-items:center;gap:8px;justify-content:space-between}.card-title h3{font-size:19px;margin:0}.evo-line{margin:5px 0;color:#475467}.chips{display:flex;flex-wrap:wrap;gap:5px;margin:8px 0}.chips span{border:1px solid #ccd6e4;border-radius:999px;padding:2px 7px;font-size:12px;font-weight:800;background:#fafcff}.focus{background:#fff8df;border-left:4px solid #e3b525;border-radius:4px;padding:7px 8px}.perk{background:#eefcf3;border-left:4px solid var(--green);border-radius:4px;padding:7px 8px}details{margin-top:8px}summary{font-weight:900;cursor:pointer}details ul{padding-left:18px}details li{margin:8px 0;line-height:1.35}small{color:var(--muted)}
.slots{display:grid;grid-template-columns:repeat(7,minmax(120px,1fr));gap:8px}.slot-card b{display:block}.slot-card span{display:block;font-weight:900;margin:4px 0}.slot-card.front{background:#fff7ed;border-color:#fdba74}.slot-card.back{background:#eff6ff;border-color:#93c5fd}.elements{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.element-card.water{border-color:#7dd3fc;background:#f0f9ff}.element-card.fire{border-color:#fca5a5;background:#fff5f5}.element-card.earth{border-color:#d6c17b;background:#fffbea}.element-card.electric{border-color:#fde047;background:#fffde8}.bars{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.barbox{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:12px}.bar-row{display:grid;grid-template-columns:88px 1fr 28px;align-items:center;gap:8px;margin:8px 0;font-size:13px}.bar{height:8px;background:#e6edf5;border-radius:999px;overflow:hidden}.bar i{display:block;height:100%;background:#2563eb;border-radius:999px}.kbd{font-family:ui-monospace,Consolas,monospace;background:#eef2f7;border:1px solid #d4dce8;padding:1px 5px;border-radius:4px}.hidden{display:none!important}footer{padding:22px 28px;color:#667085;font-size:13px}
@media(max-width:1100px){.layout{grid-template-columns:1fr}aside{position:static;height:auto}nav{display:grid;grid-template-columns:repeat(3,1fr)}.stat-grid{grid-template-columns:repeat(3,1fr)}.grid-2,.grid-3,.bars{grid-template-columns:1fr}.elements{grid-template-columns:repeat(2,1fr)}.slots{grid-template-columns:repeat(2,1fr)}.filters{grid-template-columns:1fr 1fr}}
@media(max-width:680px){.hero,.section{padding:18px 14px}.hero h1{font-size:26px}.stat-grid{grid-template-columns:repeat(2,1fr)}nav{grid-template-columns:1fr 1fr}.pal-grid{grid-template-columns:1fr}.pal-card{grid-template-columns:110px 1fr}.card-media img{max-width:105px}.filters{grid-template-columns:1fr}.elements{grid-template-columns:1fr}}
"""

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Palmon Survival Pedia 2026 - Enciclopédia Completa</title>
<style>{css}</style>
</head>
<body>
<div class="layout">
<aside>
  <div class="brand">Palmon Pedia<small>Base consolidada 2026</small></div>
  <nav>
    <a href="#resumo">Resumo</a><a href="palmon_team_builder.html">Montador de time</a><a href="palmon_battle_simulator.html">Simulador de batalha</a><a href="palmon_shop_analyzer.html">Shop Analyzer</a><a href="#fontes">Fontes</a><a href="#loop">Loop e progressão</a><a href="#combate">Combate</a><a href="#elementos">Elementos</a><a href="#slots">7 posições</a><a href="#perks">Perks e breeding</a><a href="#tier">Tier list</a><a href="#palmondex">PalmonDex</a><a href="#estrategias">Estratégias</a><a href="#screenshots">Prints</a><a href="#lacunas">Lacunas</a>
  </nav>
</aside>
<main>
<header class="hero" id="resumo">
  <h1>Palmon Survival Pedia 2026</h1>
  <p>Enciclopédia consolidada com tudo que temos até agora: dados extraídos do APK/XAPK, ranking estratégico, habilidades, elementos, posições de batalha, perks, breeding, progressão, eventos e guia para responder prints. Onde não há confirmação de 2026, está marcado como lacuna.</p>
  <div class="stat-grid">{stat_cards}</div>
</header>

<section class="section">
  <h2>Leitura rápida</h2>
  <div class="grid-3">
    <article class="info-card"><h3>Faça primeiro</h3><ul><li>Monte 1 tank central, 2-3 DPS protegidos e 1 controle/suporte.</li><li>Use o bônus de elemento se conseguir 3+ Palmons do mesmo tipo sem destruir a função do time.</li><li>Antes de evoluir, defina as 4 perks do Palmon.</li></ul></article>
    <article class="info-card"><h3>Evite</h3><ul><li>Gastar Skillfruit/Omni Token em Palmon que vai sair do time.</li><li>Colocar DPS frágil no Slot 2.</li><li>Breedar com pais cheios de traits ruins, porque aumenta o RNG.</li></ul></article>
    <article class="info-card"><h3>Melhor base atual</h3><ul><li><b>Tank:</b> Mammolith ou Embergeist; Ghillant/Statchew como alternativas.</li><li><b>DPS:</b> Zapantis, Hexkit, Rootwarden, Glacewing, Thundertooth, Plunderjaw.</li><li><b>Slots:</b> tank no 2; carries no 4/5; agressivos nos 1/6.</li></ul></article>
  </div>
  <p class="callout ok"><b>Nota de confiança:</b> Palmons, stats, skills, elementos, linhas, slots e traits vêm do APK/XAPK. Estratégia de rank/perks é inferência prática baseada nesses dados + fontes 2026.</p>
  <p class="callout"><b>Ferramentas novas:</b> use o <a href="palmon_team_builder.html">Montador de Time</a> para montar sua formação, o <a href="palmon_battle_simulator.html">Simulador de Batalha</a> para testar posições/skills/perks e o <a href="palmon_shop_analyzer.html">Shop Analyzer</a> para comparar lojas, pacotes e custo-benefício de recursos.</p>
</section>

<section class="section" id="fontes">
  <h2>Fontes e confiabilidade</h2>
  <p class="lead">A Pedia prioriza APK/config local e fontes oficiais. Guias de comunidade entram como recomendação, não como regra oficial.</p>
  <div class="table-wrap"><table><thead><tr><th>Fonte</th><th>Link/data</th><th>Tipo</th><th>Confiabilidade</th><th>Uso na Pedia</th></tr></thead><tbody>{source_table()}</tbody></table></div>
</section>

<section class="section" id="loop">
  <h2>Loop de gameplay e progressão</h2>
  <div class="grid-2">
    <article class="info-card"><h3>Loop principal</h3><ul><li>Obter Palmons por Hatchery, summons/eventos, breeding e recompensas.</li><li>Usar Palmons em combate e trabalho/base.</li><li>Melhorar base/camp para liberar sistemas, produção e evolução.</li><li>Guardar recursos para janelas de evento quando quiser otimizar.</li><li>Participar de guilda para Nursery, presentes, rallies, Dojo/GvG e progresso social.</li></ul></article>
    <article class="info-card"><h3>Prioridade de investimento</h3><ul><li><b>Início:</b> use os melhores que tiver, mas não espalhe recurso raro.</li><li><b>Meio:</b> feche 1 carry + 1 tank + 2 DPS/controle + bônus elemental possível.</li><li><b>Avançado:</b> refine perks, estrelas, evolução e slots finos por matchup.</li><li><b>F2P:</b> maximize eventos, guilda e breeding inteligente antes de gastar premium.</li></ul></article>
  </div>
</section>

<section class="section" id="combate">
  <h2>Mecânicas de combate</h2>
  <div class="grid-3">
    <article class="info-card"><h3>Funções</h3><ul><li><b>Tank:</b> segura o centro e absorve pressão.</li><li><b>DPS fundo:</b> dano principal protegido.</li><li><b>DPS frente/bruiser:</b> dano com sobrevivência nos flancos.</li><li><b>Suporte/controle:</b> buff, debuff, stun, freeze, paralyze, shield ou redução de dano.</li></ul></article>
    <article class="info-card"><h3>Skills</h3><ul><li>Todo Palmon tem ataque básico, skill principal/fúria e passivas.</li><li>A prioridade da página foca a skill que muda combate: dano alto, controle, escudo ou buff.</li><li>Skills com alvo backline/aleatório podem mudar valor conforme o inimigo.</li></ul></article>
    <article class="info-card"><h3>Rank bruto APK</h3><ul><li>É a ordem/config técnica extraída, útil para auditoria.</li><li>Não é a melhor ordem para jogar sozinha.</li><li>O Rank Geral combina APK + função + skill + controle + perks + posição.</li></ul></article>
  </div>
  <div class="bars">
    <div class="barbox"><h3>Elementos</h3>{bar_list(element_counts)}</div>
    <div class="barbox"><h3>Tier</h3>{bar_list(tier_counts)}</div>
    <div class="barbox"><h3>Linha</h3>{bar_list(pos_counts)}</div>
    <div class="barbox"><h3>Perfil de perks</h3>{bar_list(role_counts)}</div>
  </div>
</section>

<section class="section" id="elementos">
  <h2>Elementos e counters</h2>
  <p class="lead">Counter confirmado: dano causado +10% e dano recebido -10% quando seu elemento vence o alvo. A cadeia atual é Elétrico &gt; Água &gt; Fogo &gt; Terra &gt; Elétrico.</p>
  <div class="elements">
    <article class="element-card water"><h3>Água</h3><p><b>Forte contra:</b> Fogo<br><b>Fraco contra:</b> Elétrico</p><small>Confirmado por APK/screenshot: bônus de counter dá +10% dano causado e -10% dano recebido.</small></article>
    <article class="element-card fire"><h3>Fogo</h3><p><b>Forte contra:</b> Terra<br><b>Fraco contra:</b> Água</p><small>Use Fire contra times Terra; evite contra Água.</small></article>
    <article class="element-card earth"><h3>Terra</h3><p><b>Forte contra:</b> Elétrico<br><b>Fraco contra:</b> Fogo</p><small>Boa base defensiva e muitos tanks/controle.</small></article>
    <article class="element-card electric"><h3>Elétrico</h3><p><b>Forte contra:</b> Água<br><b>Fraco contra:</b> Terra</p><small>Forte para pressão, backline e paralisação.</small></article>
  </div>
  <p class="callout"><b>Bônus de mesma composição:</b> 3 Palmons do mesmo tipo = +5% ATK/DEF/HP; 4 = +10%; 5 = +20%; 6 = +25%; 7 = +30%. Não force 7 do mesmo elemento se isso destruir tank/DPS/controle.</p>
</section>

<section class="section" id="slots">
  <h2>Formação e 7 posições</h2>
  <p class="lead">O APK confirma coordenadas de 7 slots em <span class="kbd">constant_func.lua &gt; scene_map[-1].attacker_init_pos</span>. Pela coordenada de avanço, 1/2/6 ficam na frente e 3/4/5/7 ficam atrás.</p>
  <div class="slots">{slot_cards}</div>
  <div class="grid-2">
    <article class="info-card"><h3>Regra prática</h3><ul><li><b>Slot 2:</b> tank principal.</li><li><b>Slots 1/6:</b> bruiser, controle, salto/backline.</li><li><b>Slots 4/5:</b> melhores DPS e buffers.</li><li><b>Slots 3/7:</b> DPS secundário, isca lateral ou suporte menos crítico.</li></ul></article>
    <article class="info-card"><h3>O que ainda não é 100% fechado</h3><ul><li>O APK confirma posições, mas não uma regra pública dizendo que “lado X recebe mais dano”.</li><li>O lado exato é recomendação estratégica por proteção, alvo e valor do Palmon.</li><li>Se o inimigo pune um lado, troque carry entre Slot 4 e 5.</li></ul></article>
  </div>
</section>

<section class="section" id="perks">
  <h2>Perks, traits e breeding</h2>
  <p class="lead">As traits S abaixo vêm do APK. A regra de breeding usada vem da AllClash 2026: guardar Palmons com trait S, montar blueprint com 4 traits e usar o slot esquerdo do Nursery para definir qual Palmon nasce.</p>
  <div class="grid-2"><div>{perk_cards}</div><div class="table-wrap"><table><thead><tr><th>Trait EN</th><th>PT</th><th>Efeito</th><th>Valor</th><th>Raw</th></tr></thead><tbody>{traits_table}</tbody></table></div></div>
  <p class="callout danger"><b>Cuidado:</b> páginas individuais públicas não confirmam as 4 perks perfeitas de todos os Palmons. Por isso a Pedia usa perfil por função e marca como recomendação prática.</p>
</section>

<section class="section" id="tier">
  <h2>Tier list e decisões rápidas</h2>
  <div class="grid-3">
    <article class="info-card"><h3>Melhores tanks</h3><ol>{best_tanks}</ol></article>
    <article class="info-card"><h3>Melhores DPS/top core</h3><ol>{best_dps}</ol></article>
    <article class="info-card"><h3>Suportes/controle puros</h3><ol>{best_support}</ol></article>
  </div>
  <div class="filters"><input id="tableSearch" placeholder="Buscar na tier list"><select id="tableTier"><option value="all">Todos tiers</option><option>SS</option><option>S</option><option>A</option><option>B</option><option>C</option></select><select id="tableElement"><option value="all">Todos elementos</option><option>Agua</option><option>Fogo</option><option>Terra</option><option>Eletrico</option></select><select id="tablePos"><option value="all">Frente/Fundo</option><option>Frente</option><option>Fundo</option></select><select id="tableRole"><option value="all">Todas funções</option><option>Tank</option><option>DPS fundo</option><option>DPS frente/bruiser</option><option>Suporte/controle</option></select></div>
  <div class="table-wrap"><table id="rankTable"><thead><tr><th>Rank</th><th>Tier</th><th></th><th>Palmon</th><th>Elemento</th><th>Linha</th><th>Slot</th><th>Skill foco</th><th>Perks</th><th>Bruto APK</th></tr></thead><tbody>{rank_table}</tbody></table></div>
</section>

<section class="section" id="palmondex">
  <h2>PalmonDex completa</h2>
  <p class="lead">Cada ficha mostra forma base, evolução, elemento, fraqueza/vantagem, posição, perks recomendadas, skill para focar, stats do APK e todas as habilidades que extraímos.</p>
  <div class="filters"><input id="cardSearch" placeholder="Buscar Palmon ou skill"><select id="cardTier"><option value="all">Todos tiers</option><option>SS</option><option>S</option><option>A</option><option>B</option><option>C</option></select><select id="cardElement"><option value="all">Todos elementos</option><option>Agua</option><option>Fogo</option><option>Terra</option><option>Eletrico</option></select><select id="cardPos"><option value="all">Frente/Fundo</option><option>Frente</option><option>Fundo</option></select><select id="cardRole"><option value="all">Todas funções</option><option>Tank</option><option>DPS fundo</option><option>DPS frente/bruiser</option><option>Suporte/controle</option></select></div>
  <p class="toolbar-note"><span id="cardCount">{len(rows)}</span> Palmons visíveis.</p>
  <div class="pal-grid" id="palGrid">{pal_cards}</div>
</section>

<section class="section" id="estrategias">
  <h2>Estratégias práticas</h2>
  <div class="grid-3">
    <article class="info-card"><h3>Iniciante</h3><ul><li>Não gaste recurso raro em filler C/B.</li><li>Use qualquer tank decente no Slot 2 e proteja DPS no 4/5.</li><li>Guarde Palmons com trait S mesmo se forem fracos.</li></ul></article>
    <article class="info-card"><h3>Meio de jogo</h3><ul><li>Feche 4 perks do carry e do tank antes de espalhar evolução.</li><li>Monte 3+ do mesmo elemento se o bônus não sacrificar função.</li><li>Atualize skill principal antes de passivas fracas.</li></ul></article>
    <article class="info-card"><h3>Avançado/competitivo</h3><ul><li>Troque slots 4/5 conforme inimigo mira lateral/centro.</li><li>Use counter elemental quando a diferença de power não for absurda.</li><li>Tenha variações: burst, controle, mono-elemento e anti-backline.</li></ul></article>
  </div>
  <div class="grid-2">
    <article class="info-card"><h3>Free-to-play</h3><ul><li>Escolha poucos Palmons para investir.</li><li>Use guilda, eventos e breeding para multiplicar valor.</li><li>Moeda premium deve priorizar gargalos reais, não reroll impulsivo.</li></ul></article>
    <article class="info-card"><h3>Pagante leve</h3><ul><li>Compre aceleração apenas quando fechar evento/objetivo.</li><li>Não compre poder em Palmon sem perks boas.</li><li>Priorize recursos que destravam evolução/skill do core.</li></ul></article>
  </div>
</section>

<section class="section" id="screenshots">
  <h2>Guia para analisar prints</h2>
  <div class="grid-2">
    <article class="info-card"><h3>O que olhar primeiro</h3><ul><li>Tela: formação, trait filter, skill, evolução, evento, base ou recompensa.</li><li>Moedas raras visíveis: Pallite, tokens, skillfruit, essence, eggs.</li><li>Alertas: botão vermelho, recompensa pendente, upgrade disponível, tempo acabando.</li><li>Se há risco de gastar premium em ação reversível ou irreversível.</li></ul></article>
    <article class="info-card"><h3>Como responder decisão</h3><ul><li>Identificar o Palmon e função.</li><li>Comparar com rank, slot, elemento e perks recomendadas.</li><li>Dizer: faça primeiro, evite, vale/não vale gastar.</li><li>Se faltar dado: marcar como não confirmado em fonte 2026/APK.</li></ul></article>
  </div>
</section>

<section class="section" id="lacunas">
  <h2>Incertezas e lacunas</h2>
  <ul class="lead">
    <li>Fórmula completa de dano, defesa, crítico e tenacity não foi confirmada em fonte pública de 2026.</li>
    <li>Drop rates oficiais de Hatchery/Aurora e custos completos de todos os prédios não estão consolidados nesta Pedia.</li>
    <li>O APK confirma 7 posições, mas o lado exato como alvo preferencial depende de AI/targeting e matchup; tratamos como recomendação prática.</li>
    <li>Guias individuais de perks por Palmon estão parcialmente travados ou não são todos de 2026; usamos perfis por função.</li>
    <li>Eventos mudam por servidor/temporada; sempre valide prazo e recompensa no print/evento atual.</li>
  </ul>
</section>
<footer>Gerado em 2026-06-06 a partir de dados locais analisados em 2026. Esta Pedia separa dado confirmado, inferência prática e lacuna para evitar invenção de mecânica.</footer>
</main>
</div>
<script>
function matchFilters(el, prefix) {{
  const q = document.getElementById(prefix+'Search')?.value.trim().toLowerCase() || '';
  const tier = document.getElementById(prefix+'Tier')?.value || 'all';
  const element = document.getElementById(prefix+'Element')?.value || 'all';
  const pos = document.getElementById(prefix+'Pos')?.value || 'all';
  const role = document.getElementById(prefix+'Role')?.value || 'all';
  const text = el.textContent.toLowerCase();
  return (!q || text.includes(q)) && (tier==='all'||el.dataset.tier===tier) && (element==='all'||el.dataset.element===element) && (pos==='all'||el.dataset.pos===pos) && (role==='all'||el.dataset.role===role);
}}
function filterTable() {{
  document.querySelectorAll('#rankTable tbody tr').forEach(tr => tr.classList.toggle('hidden', !matchFilters(tr,'table')));
}}
function filterCards() {{
  let count = 0;
  document.querySelectorAll('#palGrid .pal-card').forEach(card => {{ const show = matchFilters(card,'card'); card.classList.toggle('hidden', !show); if (show) count++; }});
  document.getElementById('cardCount').textContent = count;
}}
['tableSearch','tableTier','tableElement','tablePos','tableRole'].forEach(id => document.getElementById(id)?.addEventListener('input', filterTable));
['cardSearch','cardTier','cardElement','cardPos','cardRole'].forEach(id => document.getElementById(id)?.addEventListener('input', filterCards));
</script>
</body>
</html>"""


def build_summary(rows, image_count):
    lines = [
        "# Palmon Survival Pedia 2026",
        "",
        f"- Palmons catalogados: {len(rows)}",
        f"- Imagens locais: {image_count}",
        "- Arquivo HTML: palmon_survival_pedia_completa.html",
        "",
        "## Top 10",
    ]
    for row in rows[:10]:
        lines.append(
            f"{row['rank_geral']}. {row['nome']} -> {row.get('evoluido','')} | {row['tier']} | "
            f"{row['elemento']} | {row['posicao']} | {row['perk_perfil']} | foco: {row['focar_primeiro']}"
        )
    lines.append("")
    lines.append("## Perks padrão")
    for name, perks, alternatives, _ in PERK_PROFILES:
        lines.append(f"- {name}: {perks}. Alternativas: {alternatives}.")
    return "\n".join(lines)


def main():
    PEDIA_DIR.mkdir(parents=True, exist_ok=True)
    rows, traits = load_data()
    html_doc = build_html(rows, traits)
    OUT_HTML.write_text(html_doc, encoding="utf-8")
    image_count = len(list((PEDIA_DIR / "images").glob("*.png")))
    OUT_MD.write_text(build_summary(rows, image_count), encoding="utf-8")
    print(f"HTML: {OUT_HTML}")
    print(f"MD: {OUT_MD}")
    print(f"Palmons: {len(rows)} | Images: {image_count} | HTML bytes: {OUT_HTML.stat().st_size}")


if __name__ == "__main__":
    main()
