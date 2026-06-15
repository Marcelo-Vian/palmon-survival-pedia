import csv
import json
import pathlib
import re


ROOT = pathlib.Path(r"D:\Linkedin")
PEDIA_DIR = ROOT / "palmon_survival_pedia"
RANK_CSV = ROOT / "palmon_survival_rank_visual" / "palmon_ranking_geral_melhor_pior.csv"
FICHAS_JSON = ROOT / "palmon_survival_apk" / "analysis" / "parsed" / "palmon_fichas_apk_enriquecidas.json"
TRAITS_CSV = ROOT / "palmon_survival_apk" / "analysis" / "parsed" / "traits_s_apk.csv"
OUT_HTML = PEDIA_DIR / "palmon_team_builder.html"


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


def parse_float(value, default=0.0):
    match = re.search(r"-?\d+(?:\.\d+)?", str(value or ""))
    return float(match.group(0)) if match else default


def load_data():
    rank_rows = list(csv.DictReader(RANK_CSV.read_text(encoding="utf-8-sig").splitlines(), delimiter=";"))
    fichas = json.loads(FICHAS_JSON.read_text(encoding="utf-8"))
    traits = list(csv.DictReader(TRAITS_CSV.read_text(encoding="utf-8-sig").splitlines(), delimiter=";"))
    by_name = {row["nome"]: row for row in fichas}

    palmons = []
    for row in rank_rows:
        if not row.get("nome"):
            continue
        detail = by_name.get(row["nome"], {})
        skills = []
        for skill in detail.get("skills", []) or []:
            skills.append(
                {
                    "name": fix_text(skill.get("nome")),
                    "description": fix_text(skill.get("descricao")),
                    "damage": parse_float(skill.get("dano_5estrelas_lv30")),
                    "target": skill.get("alvo") or [],
                }
            )
        palmons.append(
            {
                "id": fix_text(row["nome"]),
                "rank": int(row.get("rank_geral") or 999),
                "tier": fix_text(row.get("tier")),
                "name": fix_text(row.get("nome")),
                "evolved": fix_text(row.get("evoluido")),
                "rarity": fix_text(row.get("raridade")),
                "element": fix_text(row.get("elemento")),
                "strong": fix_text(row.get("forte")),
                "weak": fix_text(row.get("fraco")),
                "line": fix_text(row.get("posicao")),
                "role": fix_text(row.get("perk_perfil")),
                "function": fix_text(row.get("funcao")),
                "slotRecommended": fix_text(row.get("slot_recomendado")),
                "slotAlt": fix_text(row.get("slot_alternativo")),
                "skillFocus": fix_text(row.get("focar_primeiro")),
                "skillPriority": fix_text(row.get("skill_prioridade")),
                "skillReason": fix_text(row.get("motivo_skill")),
                "perksRecommended": fix_text(row.get("perks_recomendadas")),
                "perksAlt": fix_text(row.get("perks_alternativas")),
                "attack": parse_float(row.get("attack")),
                "defense": parse_float(row.get("defense")),
                "hp": parse_float(row.get("hp")),
                "power": parse_float(row.get("power")),
                "damagePct": parse_float(row.get("dano_principal")),
                "image": fix_text(row.get("imagem")),
                "imageEvolved": fix_text(row.get("imagem_evoluida")),
                "skills": skills,
            }
        )

    trait_options = []
    for trait in traits:
        effect = fix_text(trait.get("effect"))
        name = fix_text(trait.get("name"))
        label = f"{name} / {fix_text(trait.get('name_pt'))}: {effect}"
        trait_options.append(
            {
                "id": name,
                "label": label,
                "effect": effect,
                "value": parse_float(trait.get("fight_value")),
                "raw": parse_float(trait.get("value_raw")) / 100,
            }
        )
    return palmons, trait_options


CSS = r"""
:root{--ink:#172033;--muted:#657386;--line:#d8e1ed;--soft:#f4f7fb;--blue:#2563eb;--green:#16a34a;--gold:#b7791f;--red:#dc2626;--purple:#7c3aed;--teal:#0f766e}
*{box-sizing:border-box}body{margin:0;font-family:Inter,Segoe UI,Arial,sans-serif;background:#f3f6fa;color:var(--ink)}button,input,select{font:inherit}button{border:1px solid #cbd5e1;background:#fff;border-radius:7px;padding:8px 10px;cursor:pointer;font-weight:800}button.primary{background:#172033;color:#fff;border-color:#172033}button.good{background:#ecfdf3;border-color:#86efac;color:#14532d}button.warn{background:#fff7ed;border-color:#fdba74;color:#7c2d12}.app{display:grid;grid-template-columns:360px minmax(0,1fr);min-height:100vh}.side{background:#fff;border-right:1px solid var(--line);padding:14px;position:sticky;top:0;height:100vh;overflow:auto}.main{min-width:0}.top{padding:18px 22px;background:linear-gradient(180deg,#e8f1ff,#fff);border-bottom:1px solid var(--line)}h1{margin:0 0 6px;font-size:28px}h2{font-size:20px;margin:0 0 10px}h3{margin:0 0 8px;font-size:16px}.note{color:var(--muted);line-height:1.45;margin:0}.controls{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0}.controls input,.controls select,.config select,.config input,.battle-select{border:1px solid #cbd5e1;border-radius:7px;padding:8px;background:#fff;width:100%}.roster{display:grid;gap:8px}.roster-card{display:grid;grid-template-columns:54px 1fr;gap:8px;border:1px solid var(--line);border-radius:8px;background:#fff;padding:7px;cursor:grab}.roster-card:hover{border-color:#93c5fd;background:#f8fbff}.roster-card img{width:54px;height:54px;object-fit:contain}.roster-card b{display:block}.roster-card small{color:var(--muted)}.tier{display:inline-flex;min-width:32px;height:22px;align-items:center;justify-content:center;border-radius:6px;color:white;font-weight:900;font-size:12px}.tier-SS{background:var(--purple)}.tier-S{background:var(--teal)}.tier-A{background:var(--blue)}.tier-B{background:var(--gold)}.tier-C{background:#64748b}.builder{padding:18px 22px}.panel{background:#fff;border:1px solid var(--line);border-radius:9px;padding:14px;margin-bottom:14px;box-shadow:0 1px 2px #0000000c}.toolbar{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.toolbar>*{min-width:160px}.field{background:#dbeafe;border:1px solid #bfdbfe;border-radius:10px;padding:18px;position:relative;overflow:hidden}.field:before{content:"";position:absolute;left:0;right:0;top:50%;border-top:2px dashed #93c5fd}.row-label{font-weight:900;color:#475569;margin:0 0 8px}.formation-row{display:grid;gap:12px;position:relative;z-index:1}.front{grid-template-columns:repeat(3,minmax(170px,1fr));margin-bottom:22px}.back{grid-template-columns:repeat(4,minmax(150px,1fr))}.slot{min-height:174px;background:#ffffffdd;border:2px dashed #9ab1cf;border-radius:9px;padding:9px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;transition:.15s}.slot.selected{border-color:#172033;box-shadow:0 0 0 3px #17203322}.slot.filled{border-style:solid;background:#fff}.slot .slot-name{font-weight:900;font-size:13px;color:#475569}.slot img{width:82px;height:82px;object-fit:contain}.slot b{display:block}.slot small{color:var(--muted)}.slot .metrics{margin-top:5px;font-size:12px;display:grid;grid-template-columns:1fr 1fr;gap:4px;width:100%}.metric-pill{background:#f1f5f9;border-radius:5px;padding:3px}.summary-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.summary-card{border:1px solid var(--line);border-radius:8px;padding:12px;background:#fff}.summary-card span{display:block;font-size:24px;font-weight:900}.config-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:12px}.config{border:1px solid var(--line);border-radius:9px;padding:10px;background:#fff}.config-head{display:grid;grid-template-columns:56px 1fr;gap:8px;align-items:center}.config-head img{width:56px;height:56px;object-fit:contain}.config-controls{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px}.perk-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px}.advice{display:grid;grid-template-columns:1fr 1fr;gap:12px}.advice ul{margin:0;padding-left:20px}.advice li{margin:7px 0}.ok{color:#166534}.bad{color:#991b1b}.warntext{color:#92400e}.formula{font-family:ui-monospace,Consolas,monospace;background:#f8fafc;border:1px solid var(--line);border-radius:7px;padding:10px;overflow:auto}.hidden{display:none!important}@media(max-width:1180px){.app{grid-template-columns:1fr}.side{position:static;height:auto}.front,.back{grid-template-columns:repeat(2,1fr)}.summary-grid,.advice{grid-template-columns:1fr 1fr}}@media(max-width:720px){.builder,.top{padding:14px}.front,.back,.summary-grid,.advice,.config-grid{grid-template-columns:1fr}.controls{grid-template-columns:1fr}.toolbar>*{min-width:100%}}
"""


def build_html(palmons, traits):
    data_json = json.dumps({"palmons": palmons, "traits": traits}, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Palmon Survival - Montador de Time</title>
<style>{CSS}</style>
</head>
<body>
<div class="app">
  <aside class="side">
    <h2>PalmonDex</h2>
    <p class="note">Arraste um Palmon para uma posição ou clique em um slot e depois no Palmon. Use filtros para achar rápido.</p>
    <div class="controls">
      <input id="rosterSearch" placeholder="Buscar Palmon">
      <select id="rosterRole"><option value="all">Todas funções</option><option>Tank</option><option>DPS fundo</option><option>DPS frente/bruiser</option><option>Suporte/controle</option></select>
      <select id="rosterElement"><option value="all">Todos elementos</option><option>Agua</option><option>Fogo</option><option>Terra</option><option>Eletrico</option></select>
      <select id="rosterTier"><option value="all">Todos tiers</option><option>SS</option><option>S</option><option>A</option><option>B</option><option>C</option></select>
    </div>
    <div class="roster" id="roster"></div>
  </aside>
  <main class="main">
    <header class="top">
      <h1>Montador de Time - Palmon Survival</h1>
      <p class="note">Monte os 7 slots, ajuste skill/perks e veja dano estimado, sobrevivência, bônus elemental e sugestões de melhoria. O cálculo é comparativo, não fórmula oficial.</p>
    </header>
    <section class="builder">
      <div class="panel">
        <div class="toolbar">
          <label>Elemento inimigo<select class="battle-select" id="enemyElement"><option value="none">Não considerar</option><option value="Agua">Água</option><option value="Fogo">Fogo</option><option value="Terra">Terra</option><option value="Eletrico">Elétrico</option></select></label>
          <button class="primary" id="autoBest">Preencher melhor geral</button>
          <button class="good" id="autoEnemy">Otimizar contra inimigo</button>
          <button class="warn" id="clearTeam">Limpar time</button>
          <a href="palmon_survival_pedia_completa.html">Voltar para Palmon Pedia</a>
          <a href="palmon_shop_analyzer.html">Shop Analyzer</a>
        </div>
      </div>
      <div class="panel field">
        <p class="row-label">Frente</p>
        <div class="formation-row front" id="frontRow"></div>
        <p class="row-label">Atrás</p>
        <div class="formation-row back" id="backRow"></div>
      </div>
      <div class="panel">
        <h2>Resumo do time</h2>
        <div class="summary-grid" id="summary"></div>
      </div>
      <div class="panel">
        <h2>Configuração dos Palmons em campo</h2>
        <div class="config-grid" id="configs"></div>
      </div>
      <div class="panel">
        <h2>Sugestões</h2>
        <div class="advice"><div><h3>Melhorias recomendadas</h3><ul id="adviceList"></ul></div><div><h3>Alertas do time</h3><ul id="warningList"></ul></div></div>
      </div>
      <div class="panel">
        <h2>Como o cálculo funciona</h2>
        <p class="note">Não encontramos fórmula oficial completa de dano. Esta ferramenta usa o ATK do APK, o percentual da skill principal em Lv30/5 estrelas, counters, bônus de mesmo elemento, perks e nível de skill para criar um score comparativo.</p>
        <div class="formula">Dano estimado = ATK x skill% x nível da skill x estrelas x bônus de ATK/perks x counter elemental x bônus de mesmo elemento x ajuste efetivo de crítico/acerto.</div>
      </div>
    </section>
  </main>
</div>
<script id="data" type="application/json">{data_json}</script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const PALMONS = DATA.palmons;
const TRAITS = DATA.traits;
const SLOT_META = {{
  "1": {{label:"Slot 1 - Frente esquerda", row:"front", ideal:"DPS frente/bruiser"}},
  "2": {{label:"Slot 2 - Frente meio", row:"front", ideal:"Tank"}},
  "6": {{label:"Slot 6 - Frente direita", row:"front", ideal:"DPS frente/bruiser"}},
  "3": {{label:"Slot 3 - Fundo esquerda", row:"back", ideal:"DPS fundo"}},
  "4": {{label:"Slot 4 - Fundo meio-esquerda", row:"back", ideal:"DPS fundo"}},
  "5": {{label:"Slot 5 - Fundo meio-direita", row:"back", ideal:"DPS fundo"}},
  "7": {{label:"Slot 7 - Fundo direita", row:"back", ideal:"Suporte/controle"}}
}};
const SLOT_ORDER = ["1","2","6","3","4","5","7"];
const PROFILE_PERKS = {{
  "Tank": ["Vigorous","Unshakeable","Robust","Steel Skull"],
  "DPS fundo": ["Warlike","Belligerent","Blessed","Heartless"],
  "DPS frente/bruiser": ["Warlike","Belligerent","Robust","Vigorous"],
  "Suporte/controle": ["Vigorous","Robust","Unshakeable","Iron Will"]
}};
const state = {{ slots: Object.fromEntries(SLOT_ORDER.map(s=>[s,null])), cfg: {{}}, selectedSlot: "2" }};

function palById(id) {{ return PALMONS.find(p => p.id === id); }}
function traitById(id) {{ return TRAITS.find(t => t.id === id); }}
function defaultConfig(pal) {{ return {{ skillLevel: 30, stars: 5, profile: pal.role, perks: [...(PROFILE_PERKS[pal.role] || PROFILE_PERKS["DPS fundo"])] }}; }}
function fmt(n) {{ return Math.round(n).toLocaleString('pt-BR'); }}
function counterMult(pal, enemy) {{
  if (!enemy || enemy === 'none') return {{damage:1, survival:1, label:'neutro'}};
  if (pal.strong === enemy) return {{damage:1.10, survival:1.10, label:'counter +10%'}};
  if (pal.weak === enemy) return {{damage:0.90, survival:0.90, label:'fraco -10%'}};
  return {{damage:1, survival:1, label:'neutro'}};
}}
function sameElementBonus() {{
  const counts = {{}};
  Object.values(state.slots).forEach(id => {{ if (id) {{ const e = palById(id).element; counts[e] = (counts[e]||0)+1; }} }});
  let best = 0, bestElement = 'nenhum';
  Object.entries(counts).forEach(([el,c]) => {{ let b = c>=7?30:c>=6?25:c>=5?20:c>=4?10:c>=3?5:0; if (b > best) {{ best = b; bestElement = el; }} }});
  return {{ bonus: best/100, label: best ? `${{bestElement}} +${{best}}%` : 'sem bônus 3+' }};
}}
function perkStats(perks) {{
  const out = {{atk:0,hp:0,def:0,critRate:0,critDamage:0,accuracy:0,tenacity:0,evasion:0,critRed:0,stun:0}};
  perks.forEach(id => {{
    const t = traitById(id); if (!t) return;
    const e = t.effect;
    if (e.includes('Attack')) out.atk += t.value;
    if (e.includes('HP')) out.hp += t.value;
    if (e.includes('Defense')) out.def += t.value;
    if (e.includes('Crit Rate')) out.critRate += t.value;
    if (e.includes('Crit Damage Reduction')) out.critRed += t.value;
    else if (e.includes('Crit Damage')) out.critDamage += t.value;
    if (e.includes('Accuracy')) out.accuracy += t.value;
    if (e.includes('Tenacity')) out.tenacity += t.value;
    if (e.includes('Evasion')) out.evasion += t.value;
    if (e.includes('Stun Resist')) out.stun += t.value;
  }});
  return out;
}}
function estimate(slot) {{
  const id = state.slots[slot]; if (!id) return null;
  const pal = palById(id), cfg = state.cfg[slot] || defaultConfig(pal), pstats = perkStats(cfg.perks);
  const enemy = document.getElementById('enemyElement').value;
  const counter = counterMult(pal, enemy);
  const teamBonus = sameElementBonus().bonus;
  const skillFactor = 0.65 + 0.35 * (Number(cfg.skillLevel) / 30);
  const starFactor = [0, .70, .80, .90, .97, 1][Number(cfg.stars)] || 1;
  const effectiveCrit = 1 + ((pstats.critRate * .5) + (pstats.critDamage * .4) + (pstats.accuracy * .25)) / 100;
  const atkMult = 1 + pstats.atk/100 + teamBonus;
  const damage = pal.attack * (pal.damagePct/100) * skillFactor * starFactor * atkMult * counter.damage * effectiveCrit;
  const survivalPerks = 1 + pstats.hp/100 + (pstats.def*.75)/100 + (pstats.tenacity*.45)/100 + (pstats.evasion*.35)/100 + (pstats.critRed*.35)/100 + (pstats.stun*.25)/100;
  const survival = pal.hp * survivalPerks * (1 + teamBonus) * counter.survival;
  const slotOk = pal.slotRecommended.includes(`Slot ${{slot}}`);
  const rowOk = (SLOT_META[slot].row === 'front' && pal.line === 'Frente') || (SLOT_META[slot].row === 'back' && pal.line === 'Fundo');
  const synergy = (slotOk ? 10 : rowOk ? 4 : -12) + (pal.role === SLOT_META[slot].ideal ? 6 : 0);
  return {{pal,cfg,pstats,damage,survival,slotOk,rowOk,synergy,counter}};
}}
function teamMetrics() {{
  const estimates = SLOT_ORDER.map(estimate).filter(Boolean);
  return {{
    damage: estimates.reduce((s,e)=>s+e.damage,0),
    survival: estimates.reduce((s,e)=>s+e.survival,0),
    synergy: estimates.reduce((s,e)=>s+e.synergy,0),
    count: estimates.length,
    same: sameElementBonus()
  }};
}}
function renderRoster() {{
  const q = document.getElementById('rosterSearch').value.toLowerCase();
  const role = document.getElementById('rosterRole').value, el = document.getElementById('rosterElement').value, tier = document.getElementById('rosterTier').value;
  const used = new Set(Object.values(state.slots).filter(Boolean));
  const list = PALMONS.filter(p => !used.has(p.id) && (!q || (p.name+p.evolved+p.skillFocus).toLowerCase().includes(q)) && (role==='all'||p.role===role) && (el==='all'||p.element===el) && (tier==='all'||p.tier===tier)).slice(0,80);
  document.getElementById('roster').innerHTML = list.map(p => `<div class="roster-card" draggable="true" data-id="${{p.id}}"><img src="${{p.image}}" alt=""><div><b>#${{p.rank}} ${{p.name}}</b><small><span class="tier tier-${{p.tier}}">${{p.tier}}</span> ${{p.element}} · ${{p.role}}<br>Foco: ${{p.skillFocus}}</small></div></div>`).join('');
  document.querySelectorAll('.roster-card').forEach(card => {{
    card.addEventListener('dragstart', e => e.dataTransfer.setData('text/plain', card.dataset.id));
    card.addEventListener('click', () => assignPalmon(state.selectedSlot, card.dataset.id));
  }});
}}
function renderSlots() {{
  const front = [], back = [];
  SLOT_ORDER.forEach(slot => {{
    const meta = SLOT_META[slot], est = estimate(slot);
    let inner = `<div class="slot-name">${{meta.label}}</div>`;
    if (est) inner += `<img src="${{est.pal.image}}" alt=""><b>${{est.pal.name}}</b><small>${{est.pal.element}} · ${{est.pal.role}}</small><div class="metrics"><span class="metric-pill">Dano ${{fmt(est.damage)}}</span><span class="metric-pill">Vida ${{fmt(est.survival)}}</span></div><button data-clear="${{slot}}">limpar</button>`;
    else inner += `<small>Solte aqui<br>${{meta.ideal}}</small>`;
    const html = `<div class="slot ${{est?'filled':''}} ${{state.selectedSlot===slot?'selected':''}}" data-slot="${{slot}}">${{inner}}</div>`;
    (meta.row === 'front' ? front : back).push(html);
  }});
  document.getElementById('frontRow').innerHTML = front.join('');
  document.getElementById('backRow').innerHTML = back.join('');
  document.querySelectorAll('.slot').forEach(s => {{
    s.addEventListener('click', () => {{ state.selectedSlot = s.dataset.slot; renderAll(); }});
    s.addEventListener('dragover', e => e.preventDefault());
    s.addEventListener('drop', e => {{ e.preventDefault(); assignPalmon(s.dataset.slot, e.dataTransfer.getData('text/plain')); }});
  }});
  document.querySelectorAll('[data-clear]').forEach(btn => btn.addEventListener('click', e => {{ e.stopPropagation(); clearSlot(btn.dataset.clear); }}));
}}
function renderSummary() {{
  const m = teamMetrics();
  document.getElementById('summary').innerHTML = `<div class="summary-card"><span>${{m.count}}/7</span><small>Palmons no time</small></div><div class="summary-card"><span>${{fmt(m.damage)}}</span><small>Dano estimado</small></div><div class="summary-card"><span>${{fmt(m.survival)}}</span><small>Sobrevivência estimada</small></div><div class="summary-card"><span>${{m.same.label}}</span><small>Bônus de elemento</small></div>`;
}}
function traitSelect(value, slot, index) {{
  return `<select data-perk-slot="${{slot}}" data-perk-index="${{index}}">${{TRAITS.map(t=>`<option value="${{t.id}}" ${{t.id===value?'selected':''}}>${{t.label}}</option>`).join('')}}</select>`;
}}
function renderConfigs() {{
  const html = SLOT_ORDER.map(slot => {{
    const est = estimate(slot); if (!est) return '';
    const p = est.pal, cfg = est.cfg;
    return `<div class="config"><div class="config-head"><img src="${{p.image}}" alt=""><div><b>${{SLOT_META[slot].label}}</b><br><small>#${{p.rank}} ${{p.name}} · ${{p.element}} · ${{p.role}}</small></div></div><div class="config-controls"><label>Skill Lv<input type="number" min="1" max="30" value="${{cfg.skillLevel}}" data-skill="${{slot}}"></label><label>Estrelas<select data-stars="${{slot}}">${{[1,2,3,4,5].map(n=>`<option value="${{n}}" ${{n==cfg.stars?'selected':''}}>${{n}} estrela${{n>1?'s':''}}</option>`).join('')}}</select></label><label>Perfil<select data-profile="${{slot}}">${{Object.keys(PROFILE_PERKS).map(name=>`<option value="${{name}}" ${{name===cfg.profile?'selected':''}}>${{name}}</option>`).join('')}}</select></label><button data-apply-profile="${{slot}}">Aplicar perfil</button></div><div class="perk-grid">${{cfg.perks.map((perk,i)=>traitSelect(perk,slot,i)).join('')}}</div><p class="note">Dano: <b>${{fmt(est.damage)}}</b> · Sobrevivência: <b>${{fmt(est.survival)}}</b> · ${{est.counter.label}}</p></div>`;
  }}).join('');
  document.getElementById('configs').innerHTML = html || '<p class="note">Coloque Palmons nos slots para configurar skill e perks.</p>';
  document.querySelectorAll('[data-skill]').forEach(el => el.addEventListener('input', () => {{ state.cfg[el.dataset.skill].skillLevel = Math.max(1, Math.min(30, Number(el.value)||1)); renderAll(false); }}));
  document.querySelectorAll('[data-stars]').forEach(el => el.addEventListener('change', () => {{ state.cfg[el.dataset.stars].stars = Number(el.value); renderAll(false); }}));
  document.querySelectorAll('[data-profile]').forEach(el => el.addEventListener('change', () => {{ state.cfg[el.dataset.profile].profile = el.value; }}));
  document.querySelectorAll('[data-apply-profile]').forEach(btn => btn.addEventListener('click', () => {{ const slot=btn.dataset.applyProfile; state.cfg[slot].perks=[...PROFILE_PERKS[state.cfg[slot].profile]]; renderAll(false); }}));
  document.querySelectorAll('[data-perk-slot]').forEach(el => el.addEventListener('change', () => {{ const c=state.cfg[el.dataset.perkSlot]; c.perks[Number(el.dataset.perkIndex)] = el.value; renderAll(false); }}));
}}
function renderAdvice() {{
  const advice = [], warnings = [];
  if (!state.slots["2"]) advice.push('Coloque um tank no Slot 2. Melhor padrão: Mammolith; alternativas: Embergeist, Ghillant, Statchew.');
  if (SLOT_ORDER.filter(s => state.slots[s]).length < 7) advice.push('Preencha todos os 7 slots antes de comparar dano total.');
  const hasSupport = SLOT_ORDER.some(s => state.slots[s] && palById(state.slots[s]).role === 'Suporte/controle');
  if (!hasSupport) advice.push('Considere 1 suporte/controle se estiver morrendo ou perdendo por controle inimigo.');
  const m = teamMetrics();
  if (m.same.bonus === 0) advice.push('Você ainda não ativou bônus de 3+ Palmons do mesmo elemento.');
  SLOT_ORDER.forEach(slot => {{
    const est = estimate(slot); if (!est) return;
    if (!est.rowOk) warnings.push(`${{est.pal.name}} está em linha errada para o APK (${{est.pal.line}}). Melhor: ${{est.pal.slotRecommended}}.`);
    else if (!est.slotOk) warnings.push(`${{est.pal.name}} funciona nessa linha, mas o slot recomendado é ${{est.pal.slotRecommended}}.`);
    if (est.counter.damage < 1) warnings.push(`${{est.pal.name}} está em desvantagem contra o elemento inimigo selecionado.`);
    if (est.cfg.skillLevel < 15) warnings.push(`${{est.pal.name}} está com skill Lv baixo; subir a skill principal deve aumentar muito o score.`);
    const recommended = PROFILE_PERKS[est.pal.role] || [];
    const overlap = est.cfg.perks.filter(p => recommended.includes(p)).length;
    if (overlap < 2) warnings.push(`${{est.pal.name}} está com perks longe do perfil recomendado de ${{est.pal.role}}.`);
  }});
  document.getElementById('adviceList').innerHTML = advice.length ? advice.map(x=>`<li class="ok">${{x}}</li>`).join('') : '<li class="ok">Time bem preenchido para o modelo atual.</li>';
  document.getElementById('warningList').innerHTML = warnings.length ? warnings.map(x=>`<li class="warntext">${{x}}</li>`).join('') : '<li class="ok">Sem alertas fortes no modelo atual.</li>';
}}
function assignPalmon(slot, id) {{
  if (!slot || !id) return;
  for (const s of SLOT_ORDER) if (state.slots[s] === id) {{ state.slots[s] = null; delete state.cfg[s]; }}
  state.slots[slot] = id;
  state.cfg[slot] = defaultConfig(palById(id));
  state.selectedSlot = slot;
  renderAll();
}}
function clearSlot(slot) {{ state.slots[slot]=null; delete state.cfg[slot]; renderAll(); }}
function compatible(slot, pal) {{
  const row = SLOT_META[slot].row;
  if (row === 'front' && pal.line !== 'Frente') return false;
  if (row === 'back' && pal.line !== 'Fundo') return false;
  if (slot === '2') return pal.role === 'Tank';
  if (slot === '7') return pal.role === 'Suporte/controle' || pal.role === 'DPS fundo';
  return true;
}}
function baseScoreFor(slot, pal) {{
  const enemy = document.getElementById('enemyElement').value;
  const c = counterMult(pal, enemy).damage;
  const roleBoost = pal.role === SLOT_META[slot].ideal ? 1.10 : 1;
  return (1000 - pal.rank*8) + pal.attack * (pal.damagePct/100) * c * roleBoost;
}}
function autoFill(vsEnemy=false) {{
  state.slots = Object.fromEntries(SLOT_ORDER.map(s=>[s,null])); state.cfg = {{}};
  const used = new Set();
  SLOT_ORDER.forEach(slot => {{
    const candidates = PALMONS.filter(p => !used.has(p.id) && compatible(slot,p)).sort((a,b) => vsEnemy ? baseScoreFor(slot,b)-baseScoreFor(slot,a) : a.rank-b.rank);
    if (candidates[0]) {{ state.slots[slot]=candidates[0].id; state.cfg[slot]=defaultConfig(candidates[0]); used.add(candidates[0].id); }}
  }});
  renderAll();
}}
function renderAll(refreshRoster=true) {{ renderSlots(); renderSummary(); renderConfigs(); renderAdvice(); if (refreshRoster) renderRoster(); }}
['rosterSearch','rosterRole','rosterElement','rosterTier','enemyElement'].forEach(id => document.getElementById(id).addEventListener('input', renderAll));
document.getElementById('autoBest').addEventListener('click', () => autoFill(false));
document.getElementById('autoEnemy').addEventListener('click', () => autoFill(true));
document.getElementById('clearTeam').addEventListener('click', () => {{ state.slots=Object.fromEntries(SLOT_ORDER.map(s=>[s,null])); state.cfg={{}}; renderAll(); }});
renderAll();
</script>
</body>
</html>"""


def main():
    PEDIA_DIR.mkdir(parents=True, exist_ok=True)
    palmons, traits = load_data()
    OUT_HTML.write_text(build_html(palmons, traits), encoding="utf-8")
    print(f"HTML: {OUT_HTML}")
    print(f"Palmons: {len(palmons)} | Traits: {len(traits)} | bytes: {OUT_HTML.stat().st_size}")


if __name__ == "__main__":
    main()
