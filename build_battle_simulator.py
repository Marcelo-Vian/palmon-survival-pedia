import csv
import json
import pathlib
import re


ROOT = pathlib.Path(r"D:\Linkedin")
PEDIA_DIR = ROOT / "palmon_survival_pedia"
RANK_CSV = ROOT / "palmon_survival_rank_visual" / "palmon_ranking_geral_melhor_pior.csv"
FICHAS_JSON = ROOT / "palmon_survival_apk" / "analysis" / "parsed" / "palmon_fichas_apk_enriquecidas.json"
TRAITS_CSV = ROOT / "palmon_survival_apk" / "analysis" / "parsed" / "traits_s_apk.csv"
OUT_HTML = PEDIA_DIR / "palmon_battle_simulator.html"


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
                    "idBase": skill.get("id_base"),
                    "idLv30": skill.get("id_lv30"),
                    "name": fix_text(skill.get("nome")),
                    "nameEn": fix_text(skill.get("nome_en")),
                    "description": fix_text(skill.get("descricao")),
                    "damage": parse_float(skill.get("dano_5estrelas_lv30")),
                    "damageRaw": fix_text(skill.get("dano_5estrelas_lv30")),
                    "typeShow": skill.get("tipo_show"),
                    "typeSkill": skill.get("tipo_skill"),
                    "target": skill.get("alvo") or [],
                    "paraValue": skill.get("para_value") or [],
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
        name = fix_text(trait.get("name"))
        trait_options.append(
            {
                "id": name,
                "label": f"{name} / {fix_text(trait.get('name_pt'))}: {fix_text(trait.get('effect'))}",
                "effect": fix_text(trait.get("effect")),
                "value": parse_float(trait.get("fight_value")),
            }
        )
    return {"palmons": palmons, "traits": trait_options}


TEMPLATE = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Palmon Survival - Simulador de Batalha</title>
<style>
:root{--ink:#172033;--muted:#64748b;--line:#d9e2ee;--soft:#f4f7fb;--blue:#2563eb;--red:#dc2626;--green:#16a34a;--gold:#a16207;--purple:#7c3aed;--teal:#0f766e}
*{box-sizing:border-box}body{margin:0;font-family:Inter,Segoe UI,Arial,sans-serif;background:#f3f6fa;color:var(--ink)}button,input,select{font:inherit}button{border:1px solid #cbd5e1;background:#fff;border-radius:7px;padding:8px 10px;cursor:pointer;font-weight:800}button.primary{background:#172033;color:#fff;border-color:#172033}button.good{background:#ecfdf3;border-color:#86efac;color:#14532d}button.warn{background:#fff7ed;border-color:#fdba74;color:#7c2d12}.app{display:grid;grid-template-columns:340px minmax(0,1fr);min-height:100vh}.side{background:#fff;border-right:1px solid var(--line);padding:14px;position:sticky;top:0;height:100vh;overflow:auto}.main{min-width:0}.top{padding:18px 22px;background:linear-gradient(180deg,#e8f1ff,#fff);border-bottom:1px solid var(--line)}h1{margin:0 0 6px;font-size:28px}h2{font-size:20px;margin:0 0 10px}h3{font-size:16px;margin:0 0 8px}.note{color:var(--muted);line-height:1.45;margin:0}.controls{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0}.controls input,.controls select,.config select,.config input{border:1px solid #cbd5e1;border-radius:7px;padding:8px;background:#fff;width:100%}.roster{display:grid;gap:8px}.roster-card{display:grid;grid-template-columns:54px 1fr;gap:8px;border:1px solid var(--line);border-radius:8px;background:#fff;padding:7px;cursor:grab}.roster-card:hover{border-color:#93c5fd;background:#f8fbff}.roster-card img{width:54px;height:54px;object-fit:contain}.roster-card b{display:block}.roster-card small{color:var(--muted)}.tier{display:inline-flex;min-width:32px;height:22px;align-items:center;justify-content:center;border-radius:6px;color:#fff;font-weight:900;font-size:12px}.tier-SS{background:var(--purple)}.tier-S{background:var(--teal)}.tier-A{background:var(--blue)}.tier-B{background:var(--gold)}.tier-C{background:#64748b}.sim{padding:18px 22px}.panel{background:#fff;border:1px solid var(--line);border-radius:9px;padding:14px;margin-bottom:14px;box-shadow:0 1px 2px #0000000c}.toolbar{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.toolbar>*{min-width:160px}.teams{display:grid;grid-template-columns:1fr 1fr;gap:14px}.team-panel{border:1px solid var(--line);border-radius:10px;padding:12px;background:#f8fbff}.team-panel.enemy{background:#fff8f8}.team-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:8px}.team-head button{padding:6px 8px}.field{background:#dbeafe;border:1px solid #bfdbfe;border-radius:10px;padding:12px;position:relative}.enemy .field{background:#fee2e2;border-color:#fecaca}.row-label{font-weight:900;color:#475569;margin:0 0 6px}.formation-row{display:grid;gap:8px}.front{grid-template-columns:repeat(3,minmax(110px,1fr));margin-bottom:12px}.back{grid-template-columns:repeat(4,minmax(95px,1fr))}.slot{min-height:150px;background:#ffffffdd;border:2px dashed #9ab1cf;border-radius:9px;padding:7px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;transition:.15s}.slot.selected{border-color:#172033;box-shadow:0 0 0 3px #17203322}.slot.filled{border-style:solid;background:#fff;cursor:grab}.slot .slot-name{font-weight:900;font-size:12px;color:#475569}.slot img{width:72px;height:72px;object-fit:contain}.slot b{display:block;font-size:14px}.slot small{color:var(--muted);font-size:12px}.slot .metrics{margin-top:4px;font-size:11px;display:grid;grid-template-columns:1fr 1fr;gap:4px;width:100%}.metric-pill{background:#f1f5f9;border-radius:5px;padding:3px}.summary-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}.summary-card{border:1px solid var(--line);border-radius:8px;padding:12px;background:#fff}.summary-card span{display:block;font-size:22px;font-weight:900}.config-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:12px}.config{border:1px solid var(--line);border-radius:9px;padding:10px;background:#fff}.config-head{display:grid;grid-template-columns:56px 1fr;gap:8px;align-items:center}.config-head img{width:56px;height:56px;object-fit:contain}.config-controls{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:8px}.perk-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px}.skill-grid{display:grid;gap:8px;margin-top:10px}.skill-card{border:1px solid var(--line);border-radius:8px;background:#f8fbff;padding:9px}.skill-card.main{border-color:#93c5fd;background:#eff6ff}.skill-top{display:grid;grid-template-columns:minmax(0,1fr) 86px;gap:8px;align-items:center}.skill-top b{font-size:13px}.skill-card small{display:block;color:var(--muted);line-height:1.35;margin-top:5px}.skill-tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}.skill-tag{display:inline-flex;border-radius:6px;background:#e2e8f0;color:#334155;padding:3px 6px;font-size:11px;font-weight:800}.skill-tag.focus{background:#dbeafe;color:#1d4ed8}.skill-tools{display:grid;grid-template-columns:150px repeat(4,minmax(72px,auto));gap:8px;align-items:end;margin-top:10px}.skill-tools button{padding:7px 8px}.advice{display:grid;grid-template-columns:1fr 1fr;gap:12px}.advice ul,.battle-log ol{margin:0;padding-left:20px}.advice li,.battle-log li{margin:7px 0}.ok{color:#166534}.bad{color:#991b1b}.warntext{color:#92400e}.winner{font-size:26px;font-weight:900}.formula{font-family:ui-monospace,Consolas,monospace;background:#f8fafc;border:1px solid var(--line);border-radius:7px;padding:10px;overflow:auto}.hidden{display:none!important}@media(max-width:1280px){.app{grid-template-columns:1fr}.side{position:static;height:auto}.teams{grid-template-columns:1fr}.summary-grid{grid-template-columns:repeat(2,1fr)}}@media(max-width:760px){.sim,.top{padding:14px}.front,.back,.config-grid,.advice{grid-template-columns:1fr}.controls,.config-controls,.perk-grid,.skill-tools{grid-template-columns:1fr}.toolbar>*{min-width:100%}}
</style>
</head>
<body>
<div class="app">
  <aside class="side">
    <h2>PalmonDex</h2>
    <p class="note">Arraste para qualquer slot do seu time ou do inimigo. Também dá para arrastar Palmon já colocado para outro slot.</p>
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
      <h1>Simulador de Batalha - Palmon Survival</h1>
      <p class="note">Monte o time que voce tem no jogo e o time inimigo, escolha forma base/evoluida, preencha o nivel de cada skill e perks, e rode uma simulacao estimada por turnos. O botao Otimizar meu time so realoca os Palmons ja colocados em Meu Time.</p>
    </header>
    <section class="sim">
      <div class="panel">
        <div class="toolbar">
          <button class="primary" id="autoMy">Meu melhor time</button>
          <button class="good" id="autoEnemy">Gerar inimigo forte</button>
          <button class="good" id="optimizeVsEnemy">Otimizar meu time contra inimigo</button>
          <button class="primary" id="simulateNow">Simular agora</button>
          <button class="warn" id="clearAll">Limpar tudo</button>
          <a href="palmon_survival_pedia_completa.html">Voltar para Palmon Pedia</a>
          <a href="palmon_shop_analyzer.html">Shop Analyzer</a>
        </div>
        <p class="note">Dica: arraste um Palmon da lista para um slot. Depois de colocado, clique nele e depois clique no slot de destino, ou arraste o proprio slot preenchido, para mover/trocar de posicao inclusive entre Meu Time e Time Inimigo. Otimizar nao adiciona Palmon novo: ele so reorganiza o time atual.</p>
      </div>
      <div class="teams">
        <div class="team-panel" id="myPanel"><div class="team-head"><h2>Meu Time</h2><small>Clique num slot para selecionar</small></div><div class="field" id="myField"></div></div>
        <div class="team-panel enemy" id="enemyPanel"><div class="team-head"><h2>Time Inimigo</h2><small>Monte o adversário do print</small></div><div class="field" id="enemyField"></div></div>
      </div>
      <div class="panel">
        <h2>Resultado estimado</h2>
        <div class="summary-grid" id="summary"></div>
      </div>
      <div class="panel">
        <h2>Configuração dos Palmons em campo</h2>
        <div class="config-grid" id="configs"></div>
      </div>
      <div class="panel">
        <h2>Sugestões</h2>
        <div class="advice"><div><h3>Melhorias recomendadas</h3><ul id="adviceList"></ul></div><div><h3>Alertas</h3><ul id="warningList"></ul></div></div>
      </div>
      <div class="panel battle-log">
        <h2>Log da simulação</h2>
        <ol id="battleLog"></ol>
      </div>
      <div class="panel">
        <h2>Como o cálculo funciona</h2>
        <p class="note">A formula oficial completa nao foi confirmada. A forma evoluida usa nome/imagem reais e multiplicador estimado de evolucao: +18% ATK/DEF/HP e +10% no peso da skill. A simulacao usa prioridade de alvo por linha, counter elemental, bonus de mesmo elemento, niveis individuais de skill, estrelas e perks.</p>
        <div class="formula">Score de ataque = ATK x skill foco x passivas ofensivas x estrelas x perks x counter x bonus elemental x evolucao. Vida efetiva = HP x perks defensivas x skills defensivas x counter defensivo x bonus elemental x evolucao.</div>
      </div>
    </section>
  </main>
</div>
<script id="palmon-data" type="application/json">%%DATA%%</script>
<script>
const DATA = JSON.parse(document.getElementById('palmon-data').textContent);
const PALMONS = DATA.palmons;
const TRAITS = DATA.traits;
const SLOT_META = {
  "1": {label:"Slot 1 - Frente esquerda", row:"front", ideal:"DPS frente/bruiser"},
  "2": {label:"Slot 2 - Frente meio", row:"front", ideal:"Tank"},
  "6": {label:"Slot 6 - Frente direita", row:"front", ideal:"DPS frente/bruiser"},
  "3": {label:"Slot 3 - Fundo esquerda", row:"back", ideal:"DPS fundo"},
  "4": {label:"Slot 4 - Fundo meio-esquerda", row:"back", ideal:"DPS fundo"},
  "5": {label:"Slot 5 - Fundo meio-direita", row:"back", ideal:"DPS fundo"},
  "7": {label:"Slot 7 - Fundo direita", row:"back", ideal:"Suporte/controle"}
};
const SLOT_ORDER = ["1","2","6","3","4","5","7"];
const PROFILE_PERKS = {
  "Tank": ["Vigorous","Unshakeable","Robust","Steel Skull"],
  "DPS fundo": ["Warlike","Belligerent","Blessed","Heartless"],
  "DPS frente/bruiser": ["Warlike","Belligerent","Robust","Vigorous"],
  "Suporte/controle": ["Vigorous","Robust","Unshakeable","Iron Will"]
};
const state = {
  selected: {team:"my", slot:"2"},
  moveArmed: false,
  lastOptimization: "",
  teams: {
    my: {slots: Object.fromEntries(SLOT_ORDER.map(s=>[s,null])), cfg: {}},
    enemy: {slots: Object.fromEntries(SLOT_ORDER.map(s=>[s,null])), cfg: {}}
  }
};
function palById(id){ return PALMONS.find(p=>p.id===id); }
function traitById(id){ return TRAITS.find(t=>t.id===id); }
function canEvolve(p){ return !!(p.evolved && p.imageEvolved); }
function displayName(p,cfg){ return cfg.form === 'evolved' && canEvolve(p) ? p.evolved : p.name; }
function displayImage(p,cfg){ return cfg.form === 'evolved' && canEvolve(p) ? p.imageEvolved : p.image; }
function defaultConfig(p,maxed=false){ return {skillLevels:(p.skills||[]).map(()=>maxed?30:1), skillBudget:0, stars:5, form:"base", profile:p.role, perks:[...(PROFILE_PERKS[p.role] || PROFILE_PERKS["DPS fundo"])]}; }
function cloneCfg(cfg){ return JSON.parse(JSON.stringify(cfg)); }
function fmt(n){ return Math.round(n).toLocaleString('pt-BR'); }
function safe(s){ return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function clamp(n,min,max){ return Math.max(min,Math.min(max,Number(n)||min)); }
function skillLevel(cfg,index){ return clamp((cfg.skillLevels||[])[index] ?? cfg.skillLevel ?? 1,1,30); }
function skillNamesPriority(p){
  return String(p.skillPriority||p.skillFocus||'').split('>').map(x=>x.trim().toLowerCase()).filter(Boolean);
}
function skillPriorityRank(p,skill,index){
  const names=skillNamesPriority(p), name=String(skill.name||'').toLowerCase();
  const hit=names.findIndex(n=>name.includes(n)||n.includes(name));
  if(hit>=0) return hit+1;
  if(String(skill.name||'').toLowerCase()===String(p.skillFocus||'').toLowerCase()) return 1;
  if(skill.damage>0) return index+2;
  return 9;
}
function skillKeywordScore(skill,p,index=0){
  const txt=String((skill.name||'')+' '+(skill.description||'')).toLowerCase();
  let score=skill.damage>0?Math.max(80,skill.damage):45;
  if(txt.includes('todos os inimigos')||txt.includes('linha de trás')||txt.includes('linha de tras')||txt.includes('aleat')) score*=1.18;
  if(txt.includes('paralis')||txt.includes('atordo')||txt.includes('congel')||txt.includes('emaranh')) score+=650;
  if(txt.includes('reduz')||txt.includes('escudo')||txt.includes('absorve')||txt.includes('defesa')||txt.includes('pv')||txt.includes('dano recebido')) score+=p.role==='Tank'?900:260;
  if(txt.includes('ataque')||txt.includes('dano final')||txt.includes('crítico')||txt.includes('critico')||txt.includes('fúria')||txt.includes('furia')||txt.includes('velocidade')) score+=p.role==='Tank'?180:420;
  const rank=skillPriorityRank(p,skill,index);
  score*=[1.35,1.18,1.00,.82,.70,.62,.56,.50,.45][Math.min(rank-1,8)]||.45;
  return score;
}
function focusSkillIndex(p){
  const focus=String(p.skillFocus||'').toLowerCase();
  let idx=(p.skills||[]).findIndex(s=>String(s.name||'').toLowerCase().includes(focus)||focus.includes(String(s.name||'').toLowerCase()));
  if(idx>=0) return idx;
  let best=-1,bestScore=-1;
  (p.skills||[]).forEach((s,i)=>{ const score=skillKeywordScore(s,p,i); if(score>bestScore){best=i;bestScore=score;} });
  return Math.max(0,best);
}
function skillProfile(p,cfg){
  const skills=p.skills||[], focusIdx=focusSkillIndex(p), main=skills[focusIdx]||skills[0]||{};
  const mainLevel=skillLevel(cfg,focusIdx), mainFactor=.65+.35*(mainLevel/30);
  let passiveAtk=0, passiveDef=0, control=controlScore(p), secondary=0;
  skills.forEach((s,i)=>{
    const level=skillLevel(cfg,i), scale=level/30, txt=String((s.name||'')+' '+(s.description||'')).toLowerCase();
    if(i!==focusIdx && s.damage>0 && p.damagePct>0) secondary+=Math.min(.28,(s.damage/p.damagePct)*.055*scale);
    if(txt.includes('ataque')||txt.includes('dano final')||txt.includes('crítico')||txt.includes('critico')||txt.includes('fúria')||txt.includes('furia')||txt.includes('velocidade')) passiveAtk+=.055*scale;
    if(txt.includes('reduz')||txt.includes('escudo')||txt.includes('absorve')||txt.includes('defesa')||txt.includes('pv')||txt.includes('dano recebido')) passiveDef+=(p.role==='Tank'?.115:.065)*scale;
    if(txt.includes('paralis')||txt.includes('atordo')||txt.includes('congel')||txt.includes('emaranh')) control+=.45*scale;
  });
  return {main,focusIdx,mainLevel,offenseMult:mainFactor*(1+passiveAtk+Math.min(.35,secondary)),survivalMult:1+passiveDef,controlScore:control};
}
function recommendedSkillOrder(p){
  return (p.skills||[]).map((skill,index)=>({skill,index,score:skillKeywordScore(skill,p,index),rank:skillPriorityRank(p,skill,index)})).sort((a,b)=>a.rank-b.rank||b.score-a.score);
}
function suggestSkillPlan(p,cfg,budget){
  const levels=[...(cfg.skillLevels||[])]; while(levels.length<(p.skills||[]).length) levels.push(1);
  const plan=levels.map(x=>clamp(x,1,30));
  let points=clamp(budget,0,999);
  while(points>0 && plan.some(x=>x<30)){
    const candidates=recommendedSkillOrder(p).filter(x=>plan[x.index]<30);
    if(!candidates.length) break;
    candidates.sort((a,b)=>(b.score*(1+(30-plan[b.index])/120))-(a.score*(1+(30-plan[a.index])/120)));
    plan[candidates[0].index]++; points--;
  }
  return plan;
}
function perkStats(perks){
  const out={atk:0,hp:0,def:0,critRate:0,critDamage:0,accuracy:0,tenacity:0,evasion:0,critRed:0,stun:0};
  perks.forEach(id=>{ const t=traitById(id); if(!t)return; const e=t.effect;
    if(e.includes('Attack')) out.atk+=t.value; if(e.includes('HP')) out.hp+=t.value; if(e.includes('Defense')) out.def+=t.value;
    if(e.includes('Crit Rate')) out.critRate+=t.value; if(e.includes('Crit Damage Reduction')) out.critRed+=t.value; else if(e.includes('Crit Damage')) out.critDamage+=t.value;
    if(e.includes('Accuracy')) out.accuracy+=t.value; if(e.includes('Tenacity')) out.tenacity+=t.value; if(e.includes('Evasion')) out.evasion+=t.value; if(e.includes('Stun Resist')) out.stun+=t.value;
  });
  return out;
}
function sameElementBonus(team){
  const counts={}; Object.values(state.teams[team].slots).forEach(id=>{ if(id){ const e=palById(id).element; counts[e]=(counts[e]||0)+1; }});
  let best=0, el='nenhum';
  Object.entries(counts).forEach(([k,c])=>{ const b=c>=7?30:c>=6?25:c>=5?20:c>=4?10:c>=3?5:0; if(b>best){best=b; el=k;} });
  return {bonus:best/100,label:best?`${el} +${best}%`:'sem bônus 3+'};
}
function counterMult(attacker, target){
  if(!target) return {damage:1,survival:1,label:'neutro'};
  if(attacker.strong===target.element) return {damage:1.10,survival:1.10,label:'counter'};
  if(attacker.weak===target.element) return {damage:.90,survival:.90,label:'fraco'};
  return {damage:1,survival:1,label:'neutro'};
}
function targetCount(p){
  const txt=(p.skillReason||'').toLowerCase();
  const m=txt.match(/(\\d+) (inimigos|alvos|golpes|dardos)/); if(m) return Math.min(7,Math.max(1,Number(m[1])));
  if(txt.includes('todos os inimigos')) return 5;
  if(txt.includes('linha de trás') || txt.includes('linha de tras')) return 3;
  if(txt.includes('aleatórios') || txt.includes('aleatorios')) return 3;
  return 1;
}
function controlScore(p){
  const txt=(p.skillReason||'').toLowerCase();
  if(txt.includes('paralis')||txt.includes('atordo')||txt.includes('congel')||txt.includes('emaranh')) return 1;
  return 0;
}
function estimateUnit(team, slot, targetPal=null){
  const id=state.teams[team].slots[slot]; if(!id) return null;
  const p=palById(id), cfg=state.teams[team].cfg[slot]||defaultConfig(p), ps=perkStats(cfg.perks), same=sameElementBonus(team).bonus;
  const evoStat = cfg.form==='evolved' && canEvolve(p) ? 1.18 : 1;
  const evoSkill = cfg.form==='evolved' && canEvolve(p) ? 1.10 : 1;
  const sp=skillProfile(p,cfg), starFactor=[0,.70,.80,.90,.97,1][Number(cfg.stars)]||1;
  const counter=counterMult(p,targetPal);
  const crit=1+((ps.critRate*.5)+(ps.critDamage*.4)+(ps.accuracy*.25))/100;
  const atkMult=1+ps.atk/100+same;
  const baseAtk=p.attack*evoStat, hp=p.hp*evoStat, def=p.defense*evoStat;
  const damage=baseAtk*(p.damagePct/100)*sp.offenseMult*starFactor*atkMult*counter.damage*crit*evoSkill;
  const surv=hp*(1+ps.hp/100+(ps.def*.75)/100+(ps.tenacity*.45)/100+(ps.evasion*.35)/100+(ps.critRed*.35)/100+(ps.stun*.25)/100+same)*sp.survivalMult*counter.survival;
  const rowOk=(SLOT_META[slot].row==='front'&&p.line==='Frente')||(SLOT_META[slot].row==='back'&&p.line==='Fundo');
  const slotOk=p.slotRecommended.includes(`Slot ${slot}`);
  return {team,slot,p,cfg,ps,sp,damage,surv,def,rowOk,slotOk,tCount:targetCount(p),control:sp.controlScore,name:displayName(p,cfg),img:displayImage(p,cfg)};
}
function teamUnits(team){
  return SLOT_ORDER.map(s=>estimateUnit(team,s)).filter(Boolean);
}
function teamSummary(team){
  const units=teamUnits(team);
  return {count:units.length, damage:units.reduce((a,u)=>a+u.damage,0), surv:units.reduce((a,u)=>a+u.surv,0), control:units.reduce((a,u)=>a+u.control,0), same:sameElementBonus(team)};
}
function simulateBattle(){
  const my=teamUnits('my').map(u=>({...u,hp:u.surv,maxHp:u.surv,side:'my'}));
  const enemy=teamUnits('enemy').map(u=>({...u,hp:u.surv,maxHp:u.surv,side:'enemy'}));
  const log=[];
  if(!my.length||!enemy.length) return {winner:'Monte os dois times', rounds:0, myHp:0, enemyHp:0, log:['Preencha Meu Time e Time Inimigo para simular.']};
  function alive(side){ return side.filter(u=>u.hp>0); }
  function pickTarget(side){
    const front=alive(side).filter(u=>['1','2','6'].includes(u.slot));
    const pool=front.length?front:alive(side);
    return pool.sort((a,b)=>(a.slot==='2'?-1:0)-(b.slot==='2'?-1:0)||a.hp-b.hp)[0];
  }
  function attack(attacker, defenders, round){
    if(attacker.hp<=0) return;
    const aliveDefs=alive(defenders); if(!aliveDefs.length) return;
    const targets=[];
    const count=Math.min(attacker.tCount, aliveDefs.length);
    for(let i=0;i<count;i++){
      const t=i===0?pickTarget(aliveDefs):aliveDefs.filter(x=>!targets.includes(x)).sort((a,b)=>a.hp-b.hp)[0];
      if(t) targets.push(t);
    }
    const roleMult=attacker.p.role==='Tank'?.70:attacker.p.role==='Suporte/controle'?.75:1;
    targets.forEach(t=>{
      const c=counterMult(attacker.p,t.p).damage;
      const raw=(attacker.damage*roleMult*c)/(Math.max(1,targets.length)*3.8);
      const mitig=1/(1+(t.def/900));
      const dmg=Math.max(1,raw*mitig);
      t.hp-=dmg;
    });
  }
  let winner='Empate estimado', rounds=0;
  for(let r=1;r<=20;r++){
    rounds=r;
    [...alive(my),...alive(enemy)].sort((a,b)=>b.p.rank-a.p.rank).forEach(u=>attack(u,u.side==='my'?enemy:my,r));
    const mhp=alive(my).reduce((a,u)=>a+u.hp,0), ehp=alive(enemy).reduce((a,u)=>a+u.hp,0);
    log.push(`Rodada ${r}: Meu HP ${fmt(mhp)} | Inimigo HP ${fmt(ehp)}`);
    if(mhp<=0||ehp<=0){ winner=mhp>ehp?'Meu Time vence':ehp>mhp?'Inimigo vence':'Empate estimado'; break; }
  }
  const myHp=alive(my).reduce((a,u)=>a+u.hp,0), enemyHp=alive(enemy).reduce((a,u)=>a+u.hp,0);
  if(rounds===20) winner=myHp>enemyHp?'Meu Time vence por HP restante':enemyHp>myHp?'Inimigo vence por HP restante':'Empate estimado';
  return {winner,rounds,myHp,enemyHp,log};
}
function renderRoster(){
  const q=document.getElementById('rosterSearch').value.toLowerCase(), role=document.getElementById('rosterRole').value, el=document.getElementById('rosterElement').value, tier=document.getElementById('rosterTier').value;
  const list=PALMONS.filter(p=>(!q||(p.name+p.evolved+p.skillFocus).toLowerCase().includes(q))&&(role==='all'||p.role===role)&&(el==='all'||p.element===el)&&(tier==='all'||p.tier===tier)).slice(0,90);
  document.getElementById('roster').innerHTML=list.map(p=>`<div class="roster-card" draggable="true" data-id="${p.id}"><img src="${p.image}" alt=""><div><b>#${p.rank} ${p.name}</b><small><span class="tier tier-${p.tier}">${p.tier}</span> ${p.element} · ${p.role}<br>Foco: ${p.skillFocus}</small></div></div>`).join('');
  document.querySelectorAll('.roster-card').forEach(card=>{
    card.addEventListener('dragstart',e=>e.dataTransfer.setData('application/json',JSON.stringify({type:'roster',id:card.dataset.id})));
    card.addEventListener('click',()=>assignPalmon(state.selected.team,state.selected.slot,card.dataset.id));
  });
}
function renderTeam(team){
  const target=document.getElementById(team==='my'?'myField':'enemyField');
  const front=[],back=[];
  SLOT_ORDER.forEach(slot=>{
    const est=estimateUnit(team,slot); let inner=`<div class="slot-name">${SLOT_META[slot].label}</div>`;
    if(est) inner+=`<img src="${est.img}" alt=""><b>${est.name}</b><small>${est.p.element} · ${est.p.role}</small><div class="metrics"><span class="metric-pill">Dano ${fmt(est.damage)}</span><span class="metric-pill">HP ${fmt(est.surv)}</span></div><button data-clear-team="${team}" data-clear-slot="${slot}">limpar</button>`;
    else inner+=`<small>Solte aqui<br>${SLOT_META[slot].ideal}</small>`;
    const html=`<div class="slot ${est?'filled':''} ${state.selected.team===team&&state.selected.slot===slot?'selected':''}" draggable="${est?'true':'false'}" data-team="${team}" data-slot="${slot}">${inner}</div>`;
    (SLOT_META[slot].row==='front'?front:back).push(html);
  });
  target.innerHTML=`<p class="row-label">Frente</p><div class="formation-row front">${front.join('')}</div><p class="row-label">Atrás</p><div class="formation-row back">${back.join('')}</div>`;
}
function renderSlots(){
  renderTeam('my'); renderTeam('enemy');
  document.querySelectorAll('.slot').forEach(s=>{
    s.addEventListener('click',()=>{
      const from=state.selected, to={team:s.dataset.team,slot:s.dataset.slot};
      if(state.moveArmed && from.team && from.slot && (from.team!==to.team || from.slot!==to.slot) && state.teams[from.team].slots[from.slot]){
        moveSlot(from.team,from.slot,to.team,to.slot);
        return;
      }
      state.selected=to;
      state.moveArmed=!!state.teams[to.team].slots[to.slot];
      renderAll(false);
    });
    s.addEventListener('dragstart',e=>{ if(s.classList.contains('filled')) e.dataTransfer.setData('application/json',JSON.stringify({type:'slot',team:s.dataset.team,slot:s.dataset.slot})); });
    s.addEventListener('dragover',e=>e.preventDefault());
    s.addEventListener('drop',e=>{ e.preventDefault(); const payload=JSON.parse(e.dataTransfer.getData('application/json')||'{}'); handleDrop(payload,s.dataset.team,s.dataset.slot); });
  });
  document.querySelectorAll('[data-clear-team]').forEach(btn=>btn.addEventListener('click',e=>{e.stopPropagation(); clearSlot(btn.dataset.clearTeam,btn.dataset.clearSlot);}));
}
function handleDrop(payload,toTeam,toSlot){
  if(payload.type==='roster') assignPalmon(toTeam,toSlot,payload.id);
  if(payload.type==='slot') moveSlot(payload.team,payload.slot,toTeam,toSlot);
}
function assignPalmon(team,slot,id){
  if(!team||!slot||!id)return;
  state.teams[team].slots[slot]=id; state.teams[team].cfg[slot]=defaultConfig(palById(id)); state.selected={team,slot}; state.moveArmed=false; renderAll();
}
function moveSlot(fromTeam,fromSlot,toTeam,toSlot){
  const a=state.teams[fromTeam], b=state.teams[toTeam];
  const moving=a.slots[fromSlot], movingCfg=a.cfg[fromSlot]; if(!moving)return;
  const target=b.slots[toSlot], targetCfg=b.cfg[toSlot];
  b.slots[toSlot]=moving; b.cfg[toSlot]=movingCfg;
  a.slots[fromSlot]=target||null; if(target) a.cfg[fromSlot]=targetCfg; else delete a.cfg[fromSlot];
  state.selected={team:toTeam,slot:toSlot}; state.moveArmed=false; renderAll();
}
function clearSlot(team,slot){ state.teams[team].slots[slot]=null; delete state.teams[team].cfg[slot]; state.moveArmed=false; renderAll(); }
function renderSummary(){
  const my=teamSummary('my'), en=teamSummary('enemy'), sim=simulateBattle();
  document.getElementById('summary').innerHTML=`<div class="summary-card"><span class="winner">${sim.winner}</span><small>Resultado estimado</small></div><div class="summary-card"><span>${fmt(my.damage)}</span><small>Dano meu time</small></div><div class="summary-card"><span>${fmt(en.damage)}</span><small>Dano inimigo</small></div><div class="summary-card"><span>${my.same.label}</span><small>Bônus meu time</small></div><div class="summary-card"><span>${en.same.label}</span><small>Bônus inimigo</small></div>`;
  document.getElementById('battleLog').innerHTML=sim.log.map(x=>`<li>${x}</li>`).join('');
}
function traitSelect(value,team,slot,index){
  return `<select data-perk-team="${team}" data-perk-slot="${slot}" data-perk-index="${index}">${TRAITS.map(t=>`<option value="${t.id}" ${t.id===value?'selected':''}>${t.label}</option>`).join('')}</select>`;
}
function skillPlanSummary(p,cfg){
  const order=recommendedSkillOrder(p), current=(cfg.skillLevels||[]).map(x=>clamp(x,1,30));
  const next=order.find(x=>current[x.index]<30);
  if(!next) return 'Todas as skills cadastradas ja estao no nivel 30.';
  const focus=order[0];
  const focusLevel=current[focus.index]||1;
  const maxLower=Math.max(...order.slice(1).map(x=>current[x.index]||1),1);
  const bad=maxLower>focusLevel+5 ? ' Possivel gasto torto: uma skill secundaria esta mais alta que a skill foco.' : '';
  return `Proximo foco: ${next.skill.name} ate nivel 30. Prioridade base: ${p.skillPriority || p.skillFocus}.${bad}`;
}
function skillCards(est){
  const p=est.p,cfg=est.cfg,order=recommendedSkillOrder(p), focusIdx=order[0]?.index ?? focusSkillIndex(p);
  return (p.skills||[]).map((skill,index)=>{
    const level=skillLevel(cfg,index), rank=skillPriorityRank(p,skill,index), main=index===focusIdx;
    const raw=skill.damageRaw|| (skill.damage?`${skill.damage}%`:'sem dano direto');
    const tag=rank===1?'Foco':rank===2?'2o foco':rank===3?'3o foco':'situacional';
    return `<div class="skill-card ${main?'main':''}">
      <div class="skill-top">
        <b>${safe(index+1)}. ${safe(skill.name || 'Skill')}</b>
        <label>Lv<input type="number" min="1" max="30" value="${level}" data-skill-level-team="${est.team}" data-skill-level-slot="${est.slot}" data-skill-level-index="${index}"></label>
      </div>
      <div class="skill-tags"><span class="skill-tag ${main?'focus':''}">${tag}</span><span class="skill-tag">${safe(raw)}</span></div>
      <small>${safe(skill.description || 'Sem descricao extraida.')}</small>
    </div>`;
  }).join('');
}
function renderConfigs(){
  const items=[];
  ['my','enemy'].forEach(team=>SLOT_ORDER.forEach(slot=>{
    const est=estimateUnit(team,slot); if(!est)return; const p=est.p,cfg=est.cfg;
    items.push(`<div class="config"><div class="config-head"><img src="${est.img}" alt=""><div><b>${team==='my'?'Meu':'Inimigo'} · ${SLOT_META[slot].label}</b><br><small>#${p.rank} ${displayName(p,cfg)} · ${p.element} · ${p.role}</small></div></div>
      <div class="config-controls">
        <label>Forma<select data-form-team="${team}" data-form-slot="${slot}"><option value="base" ${cfg.form==='base'?'selected':''}>Base</option><option value="evolved" ${cfg.form==='evolved'?'selected':''} ${canEvolve(p)?'':'disabled'}>Evoluido</option></select></label>
        <label>Estrelas<select data-stars-team="${team}" data-stars-slot="${slot}">${[1,2,3,4,5].map(n=>`<option value="${n}" ${n==cfg.stars?'selected':''}>${n}</option>`).join('')}</select></label>
        <label>Perfil<select data-profile-team="${team}" data-profile-slot="${slot}">${Object.keys(PROFILE_PERKS).map(name=>`<option value="${name}" ${name===cfg.profile?'selected':''}>${name}</option>`).join('')}</select></label>
      </div>
      <div class="skill-tools">
        <label>Pontos livres<input type="number" min="0" max="120" value="${cfg.skillBudget||0}" data-skill-budget-team="${team}" data-skill-budget-slot="${slot}"></label>
        <button data-opt-skill-team="${team}" data-opt-skill-slot="${slot}">Otimizar skills</button>
        <button data-skill-preset-team="${team}" data-skill-preset-slot="${slot}" data-skill-preset="1">Lv 1</button>
        <button data-skill-preset-team="${team}" data-skill-preset-slot="${slot}" data-skill-preset="10">Lv 10</button>
        <button data-skill-preset-team="${team}" data-skill-preset-slot="${slot}" data-skill-preset="30">Lv 30</button>
      </div>
      <div class="skill-grid">${skillCards(est)}</div>
      <button data-apply-profile-team="${team}" data-apply-profile-slot="${slot}">Aplicar perks do perfil</button>
      <div class="perk-grid">${cfg.perks.map((perk,i)=>traitSelect(perk,team,slot,i)).join('')}</div>
      <p class="note">Dano ${fmt(est.damage)} · HP efetivo ${fmt(est.surv)} · ${est.slotOk?'slot ideal':'slot alternativo/ruim'}<br>${safe(skillPlanSummary(p,cfg))}</p></div>`);
  }));
  document.getElementById('configs').innerHTML=items.join('')||'<p class="note">Coloque Palmons nos slots para configurar.</p>';
  document.querySelectorAll('[data-form-team]').forEach(el=>el.addEventListener('change',()=>{state.teams[el.dataset.formTeam].cfg[el.dataset.formSlot].form=el.value;renderAll(false);}));
  document.querySelectorAll('[data-skill-level-team]').forEach(el=>el.addEventListener('input',()=>{const c=state.teams[el.dataset.skillLevelTeam].cfg[el.dataset.skillLevelSlot]; c.skillLevels[Number(el.dataset.skillLevelIndex)]=clamp(el.value,1,30);renderAll(false);}));
  document.querySelectorAll('[data-skill-budget-team]').forEach(el=>el.addEventListener('input',()=>{const c=state.teams[el.dataset.skillBudgetTeam].cfg[el.dataset.skillBudgetSlot]; c.skillBudget=clamp(el.value,0,120);}));
  document.querySelectorAll('[data-opt-skill-team]').forEach(btn=>btn.addEventListener('click',()=>{const c=state.teams[btn.dataset.optSkillTeam].cfg[btn.dataset.optSkillSlot], p=palById(state.teams[btn.dataset.optSkillTeam].slots[btn.dataset.optSkillSlot]); c.skillLevels=suggestSkillPlan(p,c,c.skillBudget||0); renderAll(false);}));
  document.querySelectorAll('[data-skill-preset-team]').forEach(btn=>btn.addEventListener('click',()=>{const c=state.teams[btn.dataset.skillPresetTeam].cfg[btn.dataset.skillPresetSlot], p=palById(state.teams[btn.dataset.skillPresetTeam].slots[btn.dataset.skillPresetSlot]); c.skillLevels=(p.skills||[]).map(()=>Number(btn.dataset.skillPreset)); renderAll(false);}));
  document.querySelectorAll('[data-stars-team]').forEach(el=>el.addEventListener('change',()=>{state.teams[el.dataset.starsTeam].cfg[el.dataset.starsSlot].stars=Number(el.value);renderAll(false);}));
  document.querySelectorAll('[data-profile-team]').forEach(el=>el.addEventListener('change',()=>{state.teams[el.dataset.profileTeam].cfg[el.dataset.profileSlot].profile=el.value;}));
  document.querySelectorAll('[data-apply-profile-team]').forEach(btn=>btn.addEventListener('click',()=>{const c=state.teams[btn.dataset.applyProfileTeam].cfg[btn.dataset.applyProfileSlot]; c.perks=[...PROFILE_PERKS[c.profile]]; renderAll(false);}));
  document.querySelectorAll('[data-perk-team]').forEach(el=>el.addEventListener('change',()=>{state.teams[el.dataset.perkTeam].cfg[el.dataset.perkSlot].perks[Number(el.dataset.perkIndex)]=el.value;renderAll(false);}));
}
function renderAdvice(){
  const advice=[],warnings=[];
  if(state.lastOptimization) advice.push(state.lastOptimization);
  if(!state.teams.my.slots['2']) advice.push('Coloque seu melhor tank no Slot 2.');
  if(!state.teams.enemy.slots['2']) advice.push('Monte o tank inimigo no Slot 2 para a simulação ficar mais real.');
  ['my','enemy'].forEach(team=>SLOT_ORDER.forEach(slot=>{
    const est=estimateUnit(team,slot); if(!est)return; const prefix=team==='my'?'Seu':'Inimigo';
    if(!est.rowOk) warnings.push(`${prefix} ${est.name} está em linha errada para o APK. Recomendado: ${est.p.slotRecommended}.`);
    else if(!est.slotOk && team==='my') advice.push(`${est.name}: tente ${est.p.slotRecommended} para ganhar eficiência de posição.`);
    const rec=PROFILE_PERKS[est.p.role]||[]; const overlap=est.cfg.perks.filter(p=>rec.includes(p)).length;
    if(team==='my' && overlap<2) warnings.push(`${est.name} está com perks longe do perfil ${est.p.role}.`);
    if(team==='my'){
      const order=recommendedSkillOrder(est.p), focus=order[0], levels=(est.cfg.skillLevels||[]).map(x=>clamp(x,1,30));
      const next=order.find(x=>(levels[x.index]||1)<30);
      if(next) advice.push(`${est.name}: proxima skill para focar é ${next.skill.name} (atual Lv ${levels[next.index]||1}).`);
      if(focus){
        const focusLv=levels[focus.index]||1;
        order.slice(1).forEach(x=>{
          const lv=levels[x.index]||1;
          if(lv>focusLv+5) warnings.push(`${est.name}: ${x.skill.name} Lv ${lv} está muito acima da skill foco ${focus.skill.name} Lv ${focusLv}. Pode ter ponto mal gasto para o objetivo atual.`);
        });
      }
    }
  }));
  const my=teamSummary('my'), en=teamSummary('enemy');
  if(my.same.bonus===0) advice.push('Seu time não ativou bônus de 3+ mesmo elemento.');
  if(en.damage>my.damage*1.2) warnings.push('O dano estimado inimigo está muito acima do seu; use counter elemental, evolua carry ou ajuste perks.');
  document.getElementById('adviceList').innerHTML=advice.length?advice.map(x=>`<li class="ok">${x}</li>`).join(''):'<li class="ok">Sem melhoria óbvia pelo modelo atual.</li>';
  document.getElementById('warningList').innerHTML=warnings.length?warnings.map(x=>`<li class="warntext">${x}</li>`).join(''):'<li class="ok">Sem alertas fortes.</li>';
}
function compatible(slot,p){
  const row=SLOT_META[slot].row; if(row==='front'&&p.line!=='Frente')return false; if(row==='back'&&p.line!=='Fundo')return false;
  if(slot==='2') return p.role==='Tank'; return true;
}
function scoreForSlot(slot,p,enemyTeam=false){
  let score=(1000-p.rank*7)+p.attack*(p.damagePct/100);
  if(p.role===SLOT_META[slot].ideal) score*=1.15;
  if(slot==='2'&&p.role==='Tank') score+=5000;
  return score;
}
function autoFill(team,strong=false){
  state.teams[team].slots=Object.fromEntries(SLOT_ORDER.map(s=>[s,null])); state.teams[team].cfg={};
  const used=new Set();
  SLOT_ORDER.forEach(slot=>{
    const c=PALMONS.filter(p=>!used.has(p.id)&&compatible(slot,p)).sort((a,b)=>strong?scoreForSlot(slot,b,true)-scoreForSlot(slot,a,true):a.rank-b.rank);
    if(c[0]){state.teams[team].slots[slot]=c[0].id;state.teams[team].cfg[slot]=defaultConfig(c[0],true);used.add(c[0].id);}
  });
}
function sameElementBonusFromIds(ids){
  const counts={}; ids.forEach(id=>{ const p=palById(id); if(p){counts[p.element]=(counts[p.element]||0)+1;} });
  let best=0, el='nenhum';
  Object.entries(counts).forEach(([k,c])=>{ const b=c>=7?30:c>=6?25:c>=5?20:c>=4?10:c>=3?5:0; if(b>best){best=b; el=k;} });
  return {bonus:best/100,label:best?`${el} +${best}%`:'sem bônus 3+'};
}
function likelyTargetForOptimizer(p){
  const enemies=teamUnits('enemy');
  if(!enemies.length) return null;
  const front=enemies.filter(u=>['1','2','6'].includes(u.slot));
  const pool=front.length?front:enemies;
  return pool.sort((a,b)=>counterMult(p,b.p).damage-counterMult(p,a.p).damage || a.surv-b.surv)[0]?.p || null;
}
function estimatePlacement(p,cfg,slot,sameBonus,targetPal=null){
  const ps=perkStats(cfg.perks), evoStat=cfg.form==='evolved'&&canEvolve(p)?1.18:1, evoSkill=cfg.form==='evolved'&&canEvolve(p)?1.10:1;
  const sp=skillProfile(p,cfg), starFactor=[0,.70,.80,.90,.97,1][Number(cfg.stars)]||1, counter=counterMult(p,targetPal);
  const crit=1+((ps.critRate*.5)+(ps.critDamage*.4)+(ps.accuracy*.25))/100;
  const atkMult=1+ps.atk/100+sameBonus;
  const baseAtk=p.attack*evoStat, hp=p.hp*evoStat, def=p.defense*evoStat;
  const damage=baseAtk*(p.damagePct/100)*sp.offenseMult*starFactor*atkMult*counter.damage*crit*evoSkill;
  const surv=hp*(1+ps.hp/100+(ps.def*.75)/100+(ps.tenacity*.45)/100+(ps.evasion*.35)/100+(ps.critRed*.35)/100+(ps.stun*.25)/100+sameBonus)*sp.survivalMult*counter.survival;
  const rowOk=(SLOT_META[slot].row==='front'&&p.line==='Frente')||(SLOT_META[slot].row==='back'&&p.line==='Fundo');
  const slotOk=p.slotRecommended.includes(`Slot ${slot}`);
  return {damage,surv,control:sp.controlScore,rowOk,slotOk};
}
function placementScore(unit,slot,sameBonus){
  const p=unit.p, cfg=unit.cfg, target=likelyTargetForOptimizer(p), est=estimatePlacement(p,cfg,slot,sameBonus,target);
  const row=SLOT_META[slot].row, front=row==='front';
  let damageW = front ? (p.role === 'Tank' ? .45 : 1.02) : 1.22;
  let survW = slot === '2' ? 1.70 : (front ? .85 : .25);
  let controlW=(p.role==='Suporte/controle'||slot==='7')?1900:950;
  let score=est.damage*damageW + est.surv*survW + est.control*controlW;
  if(!est.rowOk) score*=.55;
  if(est.slotOk) score*=1.18;
  if(p.role===SLOT_META[slot].ideal) score*=1.10;
  if(slot==='2'&&p.role==='Tank') score*=1.25;
  if(slot==='2'&&p.role!=='Tank') score*=.70;
  if((slot==='4'||slot==='5')&&p.role==='DPS fundo') score*=1.08;
  if(slot==='7'&&p.role==='Suporte/controle') score*=1.12;
  return score;
}
function optimizeVsEnemy(){
  const units=SLOT_ORDER.filter(slot=>state.teams.my.slots[slot]).map(slot=>{
    const id=state.teams.my.slots[slot], p=palById(id);
    return {originalSlot:slot,id,p,cfg:cloneCfg(state.teams.my.cfg[slot]||defaultConfig(p))};
  });
  if(!units.length){state.lastOptimization='Coloque seus Palmons em Meu Time primeiro. O otimizador nao adiciona Palmon de fora.'; renderAll(); return;}
  const same=sameElementBonusFromIds(units.map(u=>u.id)).bonus;
  let best={score:-Infinity,assign:null};
  function recurse(i,used,assign){
    if(i===units.length){
      const score=assign.reduce((sum,item)=>sum+placementScore(item.unit,item.slot,same),0);
      if(score>best.score) best={score,assign:assign.map(x=>({...x}))};
      return;
    }
    SLOT_ORDER.forEach(slot=>{
      if(used.has(slot)) return;
      used.add(slot); assign.push({slot,unit:units[i]});
      recurse(i+1,used,assign);
      assign.pop(); used.delete(slot);
    });
  }
  recurse(0,new Set(),[]);
  state.teams.my.slots=Object.fromEntries(SLOT_ORDER.map(s=>[s,null]));
  state.teams.my.cfg={};
  const moves=[];
  (best.assign||[]).forEach(({slot,unit})=>{
    state.teams.my.slots[slot]=unit.id;
    state.teams.my.cfg[slot]=unit.cfg;
    if(unit.originalSlot!==slot) moves.push(`${unit.p.name}: Slot ${unit.originalSlot} -> Slot ${slot}`);
  });
  state.lastOptimization=`Otimizei somente os ${units.length} Palmons que ja estavam no seu time; nenhum Palmon de fora foi adicionado.${moves.length?' Mudancas: '+moves.join('; '):' A melhor avaliacao manteve as posicoes atuais.'}`;
  renderAll();
}
function renderAll(refreshRoster=true){renderSlots();renderSummary();renderConfigs();renderAdvice();if(refreshRoster)renderRoster();}
['rosterSearch','rosterRole','rosterElement','rosterTier'].forEach(id=>document.getElementById(id).addEventListener('input',renderRoster));
document.getElementById('autoMy').addEventListener('click',()=>{autoFill('my',false);renderAll();});
document.getElementById('autoEnemy').addEventListener('click',()=>{autoFill('enemy',true);renderAll();});
document.getElementById('optimizeVsEnemy').addEventListener('click',optimizeVsEnemy);
document.getElementById('simulateNow').addEventListener('click',()=>renderAll(false));
document.getElementById('clearAll').addEventListener('click',()=>{['my','enemy'].forEach(t=>{state.teams[t].slots=Object.fromEntries(SLOT_ORDER.map(s=>[s,null]));state.teams[t].cfg={};});renderAll();});
renderAll();
</script>
</body>
</html>"""


def main():
    PEDIA_DIR.mkdir(parents=True, exist_ok=True)
    data = load_data()
    OUT_HTML.write_text(TEMPLATE.replace("%%DATA%%", json.dumps(data, ensure_ascii=False)), encoding="utf-8")
    print(f"HTML: {OUT_HTML}")
    print(f"Palmons: {len(data['palmons'])} | Traits: {len(data['traits'])} | bytes: {OUT_HTML.stat().st_size}")


if __name__ == "__main__":
    main()
