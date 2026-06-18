import json
import os
import pathlib


ROOT = pathlib.Path(r"D:\Linkedin")
PEDIA_DIR = ROOT / "palmon_survival_pedia"
DATA_FILE = PEDIA_DIR / os.environ.get("PALMON_SHOP_DATA", "shop_active_offers_20260617.json")
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
    captured_at = data.get("captured_at", "")
    source_note = data.get("source_note", "")
    template = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Palmon Survival - Shop Desk</title>
<style>
:root {
  --bg: #eef5fb;
  --surface: #ffffff;
  --surface-2: #f7fbff;
  --ink: #10233b;
  --muted: #63758c;
  --line: #d7e4f2;
  --blue: #1769e0;
  --blue-soft: #e8f2ff;
  --green: #08794f;
  --green-soft: #eafaf2;
  --amber: #9a5a05;
  --amber-soft: #fff6e6;
  --red: #b42318;
  --red-soft: #fff1f1;
  --shadow: 0 18px 42px rgba(17, 37, 64, .10);
  --radius: 8px;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background:
    linear-gradient(120deg, rgba(23,105,224,.13), transparent 36%),
    linear-gradient(240deg, rgba(8,121,79,.10), transparent 38%),
    var(--bg);
  color: var(--ink);
  font-family: Inter, "Segoe UI", Arial, sans-serif;
}
a { color: inherit; text-decoration: none; }
button, input, select { font: inherit; }
button { cursor: pointer; }
.app {
  width: min(1500px, calc(100% - 28px));
  margin: 0 auto;
  padding: 18px 0 42px;
}
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 12px 0;
}
.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 220px;
}
.mark {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: linear-gradient(135deg, #1769e0, #23b7de);
  box-shadow: inset 0 -10px 18px rgba(255,255,255,.25);
  position: relative;
}
.mark:after {
  content: "";
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 3px solid #fff;
  position: absolute;
  inset: 8px;
}
.brand b { display: block; font-size: 15px; }
.brand span { display: block; color: var(--muted); font-size: 12px; }
.nav {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}
.btn {
  min-height: 40px;
  border: 1px solid #bfd0e5;
  background: rgba(255,255,255,.82);
  color: #123154;
  border-radius: var(--radius);
  padding: 0 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
}
.btn.primary {
  border-color: #135fc8;
  background: linear-gradient(135deg, #1769e0, #28bce7);
  color: #fff;
}
.lang {
  display: inline-grid;
  grid-template-columns: 1fr 1fr;
  border: 1px solid #bfd0e5;
  border-radius: 999px;
  overflow: hidden;
  background: #fff;
}
.lang button {
  border: 0;
  background: transparent;
  padding: 8px 10px;
  font-weight: 900;
  color: #56708f;
}
.lang button.active {
  background: #10233b;
  color: #fff;
}
.hero {
  background: rgba(255,255,255,.92);
  border: 1px solid #cfe0f3;
  border-radius: 16px;
  box-shadow: var(--shadow);
  padding: 22px;
  display: grid;
  grid-template-columns: 1.3fr .7fr;
  gap: 18px;
  align-items: stretch;
}
.hero h1 {
  margin: 10px 0 10px;
  font-size: clamp(32px, 4.4vw, 58px);
  line-height: 1;
  letter-spacing: 0;
}
.eyebrow {
  display: inline-flex;
  border: 1px solid #bcd4f5;
  background: #e9f3ff;
  color: #135fc8;
  border-radius: 999px;
  padding: 7px 11px;
  font-size: 12px;
  font-weight: 950;
}
.lead {
  max-width: 900px;
  color: #33506f;
  line-height: 1.55;
  font-size: 17px;
}
.hero-side {
  border: 1px solid var(--line);
  background: linear-gradient(180deg, #f7fbff, #fff);
  border-radius: 12px;
  padding: 14px;
  display: grid;
  gap: 10px;
}
.stat-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 9px;
}
.stat {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: #fff;
  padding: 11px;
}
.stat span {
  display: block;
  color: var(--muted);
  font-size: 11px;
  font-weight: 950;
  text-transform: uppercase;
}
.stat strong {
  display: block;
  margin-top: 5px;
  font-size: 25px;
}
.update-note {
  border-left: 4px solid var(--blue);
  background: var(--blue-soft);
  border-radius: var(--radius);
  padding: 10px 12px;
  color: #214766;
  line-height: 1.45;
  font-size: 13px;
}
.objective-strip {
  display: grid;
  grid-template-columns: repeat(6, minmax(130px, 1fr));
  gap: 10px;
  margin-top: 16px;
}
.objective {
  border: 1px solid var(--line);
  background: rgba(255,255,255,.9);
  border-radius: 12px;
  padding: 13px;
  text-align: left;
  box-shadow: 0 8px 22px rgba(18,49,84,.06);
}
.objective.active {
  border-color: #67a8f8;
  background: #ecf6ff;
  outline: 2px solid rgba(23,105,224,.14);
}
.objective b { display: block; }
.objective span {
  display: block;
  margin-top: 4px;
  color: var(--muted);
  font-size: 12px;
}
.workspace {
  display: grid;
  grid-template-columns: 300px minmax(0, 1fr);
  gap: 16px;
  margin-top: 16px;
}
.sidebar {
  display: grid;
  gap: 12px;
  align-content: start;
  position: sticky;
  top: 12px;
}
.panel {
  border: 1px solid var(--line);
  background: rgba(255,255,255,.94);
  border-radius: 14px;
  box-shadow: var(--shadow);
  padding: 14px;
  min-width: 0;
}
.panel h2, .panel h3 {
  margin: 0 0 11px;
  line-height: 1.1;
}
.panel h2 { font-size: 22px; }
.panel h3 { font-size: 16px; }
.field {
  display: grid;
  gap: 6px;
  margin-bottom: 10px;
}
.field label {
  font-size: 12px;
  color: #405672;
  font-weight: 900;
}
.field input, .field select {
  width: 100%;
  min-height: 40px;
  border-radius: var(--radius);
  border: 1px solid #c2d2e5;
  background: #fff;
  color: var(--ink);
  padding: 9px 10px;
}
.toggle-row {
  display: flex;
  gap: 7px;
  flex-wrap: wrap;
}
.chip-button {
  border: 1px solid #c9d8ea;
  background: #fff;
  color: #234461;
  border-radius: 999px;
  min-height: 32px;
  padding: 0 10px;
  font-size: 12px;
  font-weight: 900;
}
.chip-button.active {
  background: #10233b;
  color: #fff;
  border-color: #10233b;
}
.content {
  display: grid;
  gap: 16px;
  min-width: 0;
}
.section-head {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}
.section-head p {
  margin: 4px 0 0;
  color: var(--muted);
  line-height: 1.45;
}
.best-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 12px;
}
.best-card {
  border: 1px solid #cfe0f3;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  display: grid;
  min-height: 0;
  min-width: 0;
}
.best-card img {
  width: 100%;
  height: auto;
  aspect-ratio: 2.55 / 1;
  object-fit: cover;
  display: block;
  background: #eaf3ff;
}
.best-body {
  padding: 11px;
  display: grid;
  align-content: center;
  gap: 5px;
  min-width: 0;
}
.best-body small {
  color: var(--muted);
  font-weight: 900;
}
.best-body b {
  font-size: 15px;
  overflow-wrap: anywhere;
}
.best-body strong {
  color: var(--green);
}
.offer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(285px, 1fr));
  gap: 12px;
}
.offer-card {
  border: 1px solid #d1deef;
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  display: grid;
  box-shadow: 0 9px 22px rgba(18,49,84,.06);
}
.offer-card.selected {
  border-color: #1769e0;
  outline: 2px solid rgba(23,105,224,.16);
}
.thumb-wrap {
  position: relative;
  background: #e9f3ff;
}
.offer-card img {
  display: block;
  width: 100%;
  aspect-ratio: 2.55 / 1;
  object-fit: cover;
}
.thumb-placeholder {
  aspect-ratio: 2.55 / 1;
  display: grid;
  place-items: center;
  color: var(--muted);
  font-weight: 900;
  background: #f3f8ff;
}
.badge-row {
  position: absolute;
  left: 8px;
  right: 8px;
  bottom: 8px;
  display: flex;
  justify-content: space-between;
  gap: 7px;
}
.badge {
  display: inline-flex;
  align-items: center;
  min-height: 24px;
  border: 1px solid rgba(255,255,255,.6);
  background: rgba(16,35,59,.86);
  color: #fff;
  border-radius: 999px;
  padding: 0 8px;
  font-size: 12px;
  font-weight: 950;
  white-space: nowrap;
}
.badge.status-active { background: rgba(8,121,79,.92); }
.badge.status-wait { background: rgba(154,90,5,.92); }
.badge.status-off { background: rgba(180,35,24,.92); }
.card-body {
  padding: 12px;
  display: grid;
  gap: 10px;
}
.card-title {
  display: grid;
  gap: 3px;
}
.card-title b {
  font-size: 16px;
  line-height: 1.15;
  overflow-wrap: anywhere;
}
.card-title span {
  color: var(--muted);
  font-size: 12px;
  font-weight: 800;
}
.pill-line {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}
.pill {
  display: inline-flex;
  align-items: center;
  min-height: 24px;
  padding: 0 8px;
  border-radius: 999px;
  border: 1px solid #d4e0ef;
  background: #f8fbff;
  color: #34445d;
  font-size: 12px;
  font-weight: 900;
}
.pill.good { background: var(--green-soft); border-color: #b9e8d1; color: var(--green); }
.pill.warn { background: var(--amber-soft); border-color: #f5d49a; color: var(--amber); }
.pill.bad { background: var(--red-soft); border-color: #f6b9b4; color: var(--red); }
.card-metric {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.metric-box {
  border: 1px solid #e0e9f4;
  background: #f9fcff;
  border-radius: var(--radius);
  padding: 8px;
}
.metric-box span {
  display: block;
  color: var(--muted);
  font-size: 11px;
  font-weight: 950;
  text-transform: uppercase;
}
.metric-box b {
  display: block;
  margin-top: 3px;
  font-size: 15px;
}
.recommend {
  color: #2e4660;
  font-size: 13px;
  line-height: 1.42;
  min-height: 38px;
  overflow-wrap: anywhere;
}
.card-actions {
  display: flex;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
}
.small-btn {
  border: 1px solid #c9d8ea;
  background: #fff;
  min-height: 34px;
  padding: 0 10px;
  border-radius: var(--radius);
  font-weight: 900;
  color: #123154;
}
.compare-check {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 900;
}
.detail-layout {
  display: grid;
  grid-template-columns: minmax(260px, 430px) 1fr;
  gap: 14px;
  min-width: 0;
}
.detail-image {
  width: 100%;
  border: 1px solid #c9d8ea;
  border-radius: 12px;
  background: #eef6ff;
}
.detail-list {
  display: grid;
  gap: 8px;
  min-width: 0;
}
.item-line {
  display: grid;
  grid-template-columns: minmax(130px, 1fr) 86px 110px;
  gap: 8px;
  align-items: center;
  border-bottom: 1px solid #edf2f8;
  padding-bottom: 7px;
  font-size: 13px;
}
.item-line b { color: #10233b; }
.item-line span { color: var(--muted); }
.item-line b, .item-line span { overflow-wrap: anywhere; }
.compare-box {
  display: none;
}
.compare-box.active {
  display: block;
}
.compare-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 10px;
}
.compare-card {
  border: 1px solid #d5e2f2;
  border-radius: 12px;
  background: #fff;
  padding: 10px;
}
.compare-card img {
  width: 100%;
  aspect-ratio: 2.6 / 1;
  object-fit: cover;
  border-radius: var(--radius);
  background: #eef6ff;
  margin-bottom: 8px;
}
.table-wrap {
  overflow: auto;
  border: 1px solid #d8e4f2;
  border-radius: 12px;
}
table {
  width: 100%;
  border-collapse: collapse;
  min-width: 1050px;
  background: #fff;
  font-size: 13px;
}
th, td {
  border-bottom: 1px solid #e7eef7;
  padding: 9px 10px;
  text-align: left;
  vertical-align: top;
}
th {
  background: #f5f9fe;
  color: #41536c;
  font-size: 12px;
  text-transform: uppercase;
}
.table-thumb {
  width: 148px;
  height: 58px;
  border-radius: var(--radius);
  object-fit: cover;
  border: 1px solid #c9d8ea;
  background: #eef6ff;
}
.muted { color: var(--muted); }
.mono { font-family: ui-monospace, Consolas, "Liberation Mono", monospace; }
.empty {
  border: 1px dashed #bdcde1;
  background: #f8fbff;
  border-radius: 12px;
  padding: 28px;
  color: var(--muted);
  text-align: center;
  font-weight: 900;
}
@media (max-width: 1120px) {
  .hero { grid-template-columns: 1fr; }
  .objective-strip { grid-template-columns: repeat(3, 1fr); }
  .workspace { grid-template-columns: 1fr; }
  .sidebar { position: static; }
  .best-grid { grid-template-columns: 1fr; }
}
@media (max-width: 720px) {
  .app { width: min(100% - 18px, 1500px); }
  .topbar, .nav { align-items: stretch; }
  .topbar { display: grid; }
  .nav { justify-content: stretch; }
  .btn { flex: 1 1 auto; }
  .hero { padding: 16px; }
  .stat-grid, .objective-strip, .card-metric, .detail-layout { grid-template-columns: 1fr; }
  .best-card { grid-template-columns: 1fr; }
  .best-card img { width: 100%; height: auto; aspect-ratio: 2.55 / 1; }
}
</style>
</head>
<body>
<main class="app">
  <header class="topbar">
    <a class="brand" href="index.html" aria-label="Palmon Survival Hub">
      <span class="mark" aria-hidden="true"></span>
      <span><b>Palmon Survival</b><span data-copy="brandSub">Shop Desk 2026</span></span>
    </a>
    <nav class="nav">
      <a class="btn primary" href="index.html" data-copy="backHub">Voltar ao hub</a>
      <a class="btn" href="palmon_survival_pedia_completa.html" data-copy="openPedia">Abrir Pedia</a>
      <a class="btn" href="palmon_battle_simulator.html" data-copy="openSimulator">Simulador</a>
      <span class="lang" aria-label="Language">
        <button type="button" data-lang="pt">PT</button>
        <button type="button" data-lang="en">EN</button>
      </span>
    </nav>
  </header>

  <section class="hero">
    <div>
      <span class="eyebrow" data-copy="eyebrow">Loja reconstruída do zero</span>
      <h1 data-copy="title">Comprar melhor, esperar melhor, gastar menos</h1>
      <p class="lead" data-copy="lead">A loja virou uma mesa de decisão: veja a foto do pacote, filtre pelo recurso que você precisa e compare custo-benefício sem depender de lembrar onde cada bundle aparece no jogo.</p>
    </div>
    <aside class="hero-side">
      <div class="stat-grid" id="statGrid"></div>
      <div class="update-note">
        <b data-copy="dataSource">Fonte dos dados</b><br>
        <span id="sourceLine"></span>
      </div>
    </aside>
  </section>

  <section class="objective-strip" id="objectiveStrip" aria-label="Objetivos de compra"></section>

  <div class="workspace">
    <aside class="sidebar">
      <section class="panel">
        <h2 data-copy="filters">Filtros</h2>
        <div class="field">
          <label for="search" data-copy="searchLabel">Buscar</label>
          <input id="search" placeholder="pacote, item, cap, seção">
        </div>
        <div class="field">
          <label for="categoryFilter" data-copy="categoryLabel">Categoria</label>
          <select id="categoryFilter"></select>
        </div>
        <div class="field">
          <label for="statusFilter" data-copy="statusLabel">Status</label>
          <select id="statusFilter"></select>
        </div>
        <div class="field">
          <label for="sortFilter" data-copy="sortLabel">Ordenação</label>
          <select id="sortFilter"></select>
        </div>
        <div class="field">
          <label data-copy="confidenceLabel">Confiança</label>
          <div class="toggle-row" id="confidenceButtons"></div>
        </div>
        <button class="btn" type="button" id="resetFilters" data-copy="reset">Limpar filtros</button>
      </section>

      <section class="panel compare-box" id="compareBox">
        <h3 data-copy="compareTitle">Comparação</h3>
        <div id="compareList" class="compare-grid"></div>
      </section>
    </aside>

    <section class="content">
      <section class="panel">
        <div class="section-head">
          <div>
            <h2 data-copy="bestTitle">Melhores escolhas por objetivo</h2>
            <p id="bestHint"></p>
          </div>
        </div>
        <div class="best-grid" id="bestGrid"></div>
      </section>

      <section class="panel" id="detailPanel">
        <div class="section-head">
          <div>
            <h2 data-copy="detailTitle">Detalhe do pacote selecionado</h2>
            <p data-copy="detailHint">Clique em qualquer pacote para ver itens, fonte e recomendação.</p>
          </div>
        </div>
        <div id="detailContent"></div>
      </section>

      <section class="panel">
        <div class="section-head">
          <div>
            <h2><span data-copy="offersTitle">Biblioteca visual de ofertas</span> <span class="muted" id="countLabel"></span></h2>
            <p id="libraryHint"></p>
          </div>
        </div>
        <div class="offer-grid" id="offerGrid"></div>
      </section>

      <section class="panel">
        <div class="section-head">
          <div>
            <h2 data-copy="tableTitle">Tabela técnica</h2>
            <p data-copy="tableHint">A tabela serve para conferência rápida e busca fina por item, preço, fonte e recomendação.</p>
          </div>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th data-copy="visual">Visual</th>
                <th data-copy="package">Pacote</th>
                <th data-copy="price">Preço</th>
                <th data-copy="items">Itens</th>
                <th data-copy="score">Score</th>
                <th data-copy="decision">Decisão</th>
                <th data-copy="source">Fonte</th>
              </tr>
            </thead>
            <tbody id="tableRows"></tbody>
          </table>
        </div>
      </section>
    </section>
  </div>
</main>

<script id="shop-data" type="application/json">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById("shop-data").textContent);
const OFFERS = DATA.offers || [];
const STORAGE_KEY = "palmon_lang";
const TEXT = {
  pt: {
    brandSub: "Shop Desk 2026",
    backHub: "Voltar ao hub",
    openPedia: "Abrir Pedia",
    openSimulator: "Simulador",
    eyebrow: "Loja reconstruída do zero",
    title: "Comprar melhor, esperar melhor, gastar menos",
    lead: "A loja virou uma mesa de decisão: veja a foto do pacote, filtre pelo recurso que você precisa e compare custo-benefício sem depender de lembrar onde cada bundle aparece no jogo.",
    dataSource: "Fonte dos dados",
    filters: "Filtros",
    searchLabel: "Buscar",
    categoryLabel: "Categoria",
    statusLabel: "Status",
    sortLabel: "Ordenação",
    confidenceLabel: "Confiança",
    reset: "Limpar filtros",
    compareTitle: "Comparação",
    bestTitle: "Melhores escolhas por objetivo",
    detailTitle: "Detalhe do pacote selecionado",
    detailHint: "Clique em qualquer pacote para ver itens, fonte e recomendação.",
    offersTitle: "Biblioteca visual de ofertas",
    tableTitle: "Tabela técnica",
    tableHint: "A tabela serve para conferência rápida e busca fina por item, preço, fonte e recomendação.",
    visual: "Visual",
    package: "Pacote",
    price: "Preço",
    items: "Itens",
    score: "Score",
    decision: "Decisão",
    source: "Fonte",
    allCategories: "Todas categorias",
    allStatus: "Todos status",
    active: "Ativo",
    pending: "Pendente",
    unavailable: "Comprado/indisponível",
    sortBest: "Melhor custo-benefício",
    sortPriceLow: "Menor preço",
    sortPriceHigh: "Maior preço",
    sortName: "Nome",
    confAll: "Todas",
    confHigh: "Alta",
    confMedium: "Média",
    confLow: "Baixa",
    seeDetails: "Ver detalhes",
    compare: "Comparar",
    noResults: "Nenhuma oferta encontrada com estes filtros.",
    chooseGoal: "Objetivo atual",
    scoreEmpty: "Sem quantidade comparável",
    noThumb: "sem foto",
    bestHint: "Escolha um objetivo acima para reorganizar as recomendações.",
    libraryHint: "Cards grandes para reconhecer o pacote no jogo. A tabela fica logo abaixo para checagem fina.",
    selected: "Selecionado",
    limit: "Limite",
    confidence: "Confiança",
    section: "Seção",
    type: "Tipo",
    recommendation: "Recomendação",
    category: "Categoria",
    quantity: "Qtd.",
    unit: "Unidade",
    instantDecision: "Leitura rápida",
    extracted: "extraído",
    thumbnails: "fotos",
    priced: "com preço",
    categories: "categorias",
    lowest: "menor ticket",
    sourceNote: "Observação",
  },
  en: {
    brandSub: "Shop Desk 2026",
    backHub: "Back to hub",
    openPedia: "Open Pedia",
    openSimulator: "Simulator",
    eyebrow: "Shop rebuilt from scratch",
    title: "Buy better, wait better, spend less",
    lead: "The shop is now a decision desk: see the package image, filter by the resource you need, and compare value without remembering where each bundle appears in-game.",
    dataSource: "Data source",
    filters: "Filters",
    searchLabel: "Search",
    categoryLabel: "Category",
    statusLabel: "Status",
    sortLabel: "Sort",
    confidenceLabel: "Confidence",
    reset: "Clear filters",
    compareTitle: "Comparison",
    bestTitle: "Best picks by goal",
    detailTitle: "Selected package details",
    detailHint: "Click any package to see items, source, and recommendation.",
    offersTitle: "Visual offer library",
    tableTitle: "Technical table",
    tableHint: "Use the table for precise checks by item, price, source, and recommendation.",
    visual: "Visual",
    package: "Package",
    price: "Price",
    items: "Items",
    score: "Score",
    decision: "Decision",
    source: "Source",
    allCategories: "All categories",
    allStatus: "All status",
    active: "Active",
    pending: "Pending",
    unavailable: "Bought/unavailable",
    sortBest: "Best value",
    sortPriceLow: "Lowest price",
    sortPriceHigh: "Highest price",
    sortName: "Name",
    confAll: "All",
    confHigh: "High",
    confMedium: "Medium",
    confLow: "Low",
    seeDetails: "Details",
    compare: "Compare",
    noResults: "No offers found with these filters.",
    chooseGoal: "Current goal",
    scoreEmpty: "No comparable quantity",
    noThumb: "no image",
    bestHint: "Choose a goal above to reorganize recommendations.",
    libraryHint: "Large cards help you recognize the package in-game. The table below is for precise checking.",
    selected: "Selected",
    limit: "Limit",
    confidence: "Confidence",
    section: "Section",
    type: "Type",
    recommendation: "Recommendation",
    category: "Category",
    quantity: "Qty.",
    unit: "Unit",
    instantDecision: "Quick read",
    extracted: "extracted",
    thumbnails: "images",
    priced: "priced",
    categories: "categories",
    lowest: "lowest ticket",
    sourceNote: "Note",
  }
};
const GOALS = [
  { id: "Pallite", label: "Pallite", hint: "moeda premium" },
  { id: "Acelerador", label: "Acelerador", hint: "tempo por real" },
  { id: "Skillfruit", label: "Skillfruit", hint: "upar skills" },
  { id: "Palmon", label: "Palmon", hint: "tokens e ovos" },
  { id: "Captura", label: "Captura", hint: "palcatcher" },
  { id: "Passe", label: "Passe", hint: "coleta diária" },
];
const state = {
  lang: localStorage.getItem(STORAGE_KEY) || "pt",
  goal: "Pallite",
  confidence: "",
  selectedId: OFFERS[0]?.id || "",
  compare: new Set(),
};
const $ = (id) => document.getElementById(id);
const els = {
  statGrid: $("statGrid"),
  objectiveStrip: $("objectiveStrip"),
  sourceLine: $("sourceLine"),
  search: $("search"),
  category: $("categoryFilter"),
  status: $("statusFilter"),
  sort: $("sortFilter"),
  confidence: $("confidenceButtons"),
  reset: $("resetFilters"),
  bestGrid: $("bestGrid"),
  bestHint: $("bestHint"),
  detail: $("detailContent"),
  grid: $("offerGrid"),
  count: $("countLabel"),
  libraryHint: $("libraryHint"),
  rows: $("tableRows"),
  compareBox: $("compareBox"),
  compareList: $("compareList"),
};
function t(key) { return (TEXT[state.lang] && TEXT[state.lang][key]) || TEXT.pt[key] || key; }
function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (c) => {
    if (c === "&") return "&amp;";
    if (c === "<") return "&lt;";
    if (c === ">") return "&gt;";
    if (c === '"') return "&quot;";
    return "&#39;";
  });
}
function norm(value) {
  return String(value || "").normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").toLowerCase();
}
function brl(value) {
  const n = Number(value);
  return Number.isFinite(n) ? n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" }) : "-";
}
function fmt(value) {
  const n = Number(value);
  return Number.isFinite(n) ? n.toLocaleString("pt-BR", { maximumFractionDigits: 2 }) : "-";
}
function categories() {
  return Array.from(new Set(OFFERS.flatMap((offer) => (offer.items || []).map((item) => item.category)).filter(Boolean))).sort();
}
function price(offer) {
  if (offer.price_brl === null || offer.price_brl === undefined || offer.price_brl === "") return null;
  const value = Number(offer.price_brl);
  return Number.isFinite(value) ? value : null;
}
function metricQty(item) {
  const value = Number(item.metric_qty ?? item.qty);
  return Number.isFinite(value) ? value : null;
}
function totalFor(offer, category) {
  let total = 0;
  for (const item of offer.items || []) {
    if (item.category !== category) continue;
    const qty = metricQty(item);
    if (qty) total += qty;
  }
  return total || null;
}
function unitFor(offer, category) {
  const item = (offer.items || []).find((row) => row.category === category && metricQty(row));
  return item?.metric_unit || item?.unit || category;
}
function valueScore(offer, category = state.goal) {
  const total = totalFor(offer, category);
  const p = price(offer);
  if (!total || !p || p <= 0) return null;
  return total / p;
}
function statusType(offer) {
  const value = norm(offer.status);
  if (value.includes("ativo")) return "active";
  if (value.includes("pendente") || value.includes("amanha")) return "pending";
  return "unavailable";
}
function statusLabel(type) {
  if (type === "active") return t("active");
  if (type === "pending") return t("pending");
  return t("unavailable");
}
function confidenceClass(value) {
  if (value === "alta") return "good";
  if (value === "media") return "warn";
  return "bad";
}
function statusBadgeClass(offer) {
  const type = statusType(offer);
  if (type === "active") return "status-active";
  if (type === "pending") return "status-wait";
  return "status-off";
}
function itemBlob(offer) {
  return (offer.items || []).map((item) => `${item.name} ${item.qty ?? ""} ${item.unit || ""} ${item.category}`).join(" ");
}
function searchMatches(offer) {
  const tokens = norm(els.search.value).split(/\\s+/).filter(Boolean);
  const blob = norm(`${offer.name} ${offer.section} ${offer.type} ${offer.status} ${offer.source_caps} ${offer.confidence} ${itemBlob(offer)}`);
  if (tokens.length && !tokens.every((token) => blob.includes(token))) return false;
  if (els.category.value && !(offer.items || []).some((item) => item.category === els.category.value)) return false;
  if (els.status.value && statusType(offer) !== els.status.value) return false;
  if (state.confidence && offer.confidence !== state.confidence) return false;
  return true;
}
function sortedOffers(rows) {
  const mode = els.sort.value;
  const copy = [...rows];
  if (mode === "price-low") return copy.sort((a, b) => (price(a) ?? 999999) - (price(b) ?? 999999));
  if (mode === "price-high") return copy.sort((a, b) => (price(b) ?? -1) - (price(a) ?? -1));
  if (mode === "name") return copy.sort((a, b) => String(a.name).localeCompare(String(b.name)));
  return copy.sort((a, b) => (valueScore(b) ?? -1) - (valueScore(a) ?? -1));
}
function filteredOffers() {
  return sortedOffers(OFFERS.filter(searchMatches));
}
function thumb(offer, className = "") {
  if (!offer.thumbnail) return `<div class="thumb-placeholder ${className}">${esc(t("noThumb"))}</div>`;
  return `<img class="${className}" src="${esc(offer.thumbnail)}" alt="${esc(offer.name)}">`;
}
function shortItems(offer, limit = 3) {
  const items = offer.items || [];
  const visible = items.slice(0, limit).map((item) => {
    const qty = item.qty === null || item.qty === undefined ? "" : ` x${esc(item.qty)}`;
    return `<span class="pill">${esc(item.name)}${qty}</span>`;
  }).join("");
  const more = items.length > limit ? `<span class="pill">+${items.length - limit}</span>` : "";
  return `<div class="pill-line">${visible}${more}</div>`;
}
function scoreLabel(offer, category = state.goal) {
  const score = valueScore(offer, category);
  if (!score) return t("scoreEmpty");
  return `${fmt(score)} ${unitFor(offer, category)}/R$`;
}
function buyRead(offer) {
  const type = statusType(offer);
  if (type === "pending") return state.lang === "en" ? "Wait" : "Esperar";
  if (type === "unavailable") return state.lang === "en" ? "Unavailable" : "Indisponível";
  const score = valueScore(offer);
  if (!score) return state.lang === "en" ? "Situational" : "Situacional";
  return state.lang === "en" ? "Compare by goal" : "Compare pelo objetivo";
}
function applyCopy() {
  document.documentElement.lang = state.lang === "en" ? "en" : "pt-BR";
  document.querySelectorAll("[data-copy]").forEach((node) => {
    node.textContent = t(node.dataset.copy);
  });
  document.querySelectorAll("[data-lang]").forEach((button) => {
    button.classList.toggle("active", button.dataset.lang === state.lang);
  });
  els.search.placeholder = state.lang === "en" ? "package, item, cap, section" : "pacote, item, cap, seção";
  els.sourceLine.innerHTML = `${esc(DATA.captured_at || "__CAPTURED__")}<br><span class="muted">${esc(t("sourceNote"))}: ${esc(DATA.source_note || "__SOURCE_NOTE__")}</span>`;
}
function fillSelects() {
  els.category.innerHTML = `<option value="">${esc(t("allCategories"))}</option>` + categories().map((cat) => `<option value="${esc(cat)}">${esc(cat)}</option>`).join("");
  els.status.innerHTML = `
    <option value="">${esc(t("allStatus"))}</option>
    <option value="active">${esc(t("active"))}</option>
    <option value="pending">${esc(t("pending"))}</option>
    <option value="unavailable">${esc(t("unavailable"))}</option>
  `;
  els.sort.innerHTML = `
    <option value="best">${esc(t("sortBest"))}</option>
    <option value="price-low">${esc(t("sortPriceLow"))}</option>
    <option value="price-high">${esc(t("sortPriceHigh"))}</option>
    <option value="name">${esc(t("sortName"))}</option>
  `;
  const confs = [
    ["", t("confAll")],
    ["alta", t("confHigh")],
    ["media", t("confMedium")],
    ["baixa", t("confLow")],
  ];
  els.confidence.innerHTML = confs.map(([value, label]) => `<button type="button" class="chip-button ${state.confidence === value ? "active" : ""}" data-confidence="${esc(value)}">${esc(label)}</button>`).join("");
  els.confidence.querySelectorAll("[data-confidence]").forEach((button) => {
    button.addEventListener("click", () => {
      state.confidence = button.dataset.confidence;
      render();
    });
  });
}
function renderStats() {
  const active = OFFERS.filter((offer) => statusType(offer) === "active").length;
  const thumbs = OFFERS.filter((offer) => offer.thumbnail).length;
  const priced = OFFERS.filter((offer) => price(offer) !== null).length;
  const catCount = categories().length;
  const minPrice = Math.min(...OFFERS.map(price).filter((value) => value !== null));
  const cards = [
    [t("extracted"), OFFERS.length],
    [t("thumbnails"), thumbs],
    [t("priced"), priced],
    [t("categories"), catCount],
    [t("lowest"), brl(minPrice)],
  ];
  els.statGrid.innerHTML = cards.map(([label, value]) => `<div class="stat"><span>${esc(label)}</span><strong>${esc(value)}</strong></div>`).join("");
}
function renderObjectives() {
  els.objectiveStrip.innerHTML = GOALS.map((goal) => `
    <button type="button" class="objective ${state.goal === goal.id ? "active" : ""}" data-goal="${esc(goal.id)}">
      <b>${esc(goal.label)}</b>
      <span>${esc(goal.hint)}</span>
    </button>
  `).join("");
  els.objectiveStrip.querySelectorAll("[data-goal]").forEach((button) => {
    button.addEventListener("click", () => {
      state.goal = button.dataset.goal;
      render();
    });
  });
}
function bestOffersForGoal(goalId, limit = 3) {
  return OFFERS
    .filter((offer) => statusType(offer) === "active" && valueScore(offer, goalId))
    .sort((a, b) => valueScore(b, goalId) - valueScore(a, goalId))
    .slice(0, limit);
}
function renderBest() {
  els.bestHint.textContent = t("bestHint");
  const best = bestOffersForGoal(state.goal, 3);
  els.bestGrid.innerHTML = best.length ? best.map((offer) => `
    <article class="best-card" role="button" tabindex="0" data-select="${esc(offer.id)}">
      ${thumb(offer)}
      <div class="best-body">
        <small>${esc(t("chooseGoal"))}: ${esc(state.goal)}</small>
        <b>${esc(offer.name)}</b>
        <strong>${esc(scoreLabel(offer))}</strong>
        <span class="muted">${esc(brl(offer.price_brl))}</span>
      </div>
    </article>
  `).join("") : `<div class="empty">${esc(t("scoreEmpty"))}</div>`;
  els.bestGrid.querySelectorAll("[data-select]").forEach(bindSelect);
}
function renderDetail() {
  const offer = OFFERS.find((item) => item.id === state.selectedId) || OFFERS[0];
  if (!offer) {
    els.detail.innerHTML = `<div class="empty">${esc(t("noResults"))}</div>`;
    return;
  }
  const items = (offer.items || []).map((item) => `
    <div class="item-line">
      <b>${esc(item.name)}</b>
      <span>${item.qty === null || item.qty === undefined ? "-" : esc(item.qty)}</span>
      <span>${esc(item.metric_unit || item.unit || item.category || "")}</span>
    </div>
  `).join("");
  els.detail.innerHTML = `
    <div class="detail-layout">
      <div>${offer.thumbnail ? `<img class="detail-image" src="${esc(offer.thumbnail)}" alt="${esc(offer.name)}">` : `<div class="thumb-placeholder">${esc(t("noThumb"))}</div>`}</div>
      <div class="detail-list">
        <h3>${esc(offer.name)}</h3>
        <div class="pill-line">
          <span class="pill good">${esc(brl(offer.price_brl))}</span>
          <span class="pill">${esc(offer.section || "-")}</span>
          <span class="pill">${esc(offer.type || "-")}</span>
          <span class="pill ${confidenceClass(offer.confidence)}">${esc(t("confidence"))}: ${esc(offer.confidence || "-")}</span>
          <span class="pill">${esc(scoreLabel(offer))}</span>
        </div>
        <p class="recommend"><b>${esc(t("instantDecision"))}:</b> ${esc(buyRead(offer))}</p>
        <p class="recommend"><b>${esc(t("recommendation"))}:</b> ${esc(offer.recommendation || "-")}</p>
        <p class="muted"><b>${esc(t("source"))}:</b> <span class="mono">${esc(offer.source_caps || "-")}</span>${offer.limit ? ` · <b>${esc(t("limit"))}:</b> ${esc(offer.limit)}` : ""}</p>
        <div>${items}</div>
      </div>
    </div>
  `;
}
function bindSelect(node) {
  node.addEventListener("click", () => {
    state.selectedId = node.dataset.select;
    renderDetail();
    document.querySelectorAll(".offer-card").forEach((card) => card.classList.toggle("selected", card.dataset.select === state.selectedId));
  });
  node.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      node.click();
    }
  });
}
function offerCard(offer) {
  const selected = offer.id === state.selectedId ? "selected" : "";
  const checked = state.compare.has(offer.id) ? "checked" : "";
  return `
    <article class="offer-card ${selected}" data-select="${esc(offer.id)}">
      <div class="thumb-wrap">
        ${thumb(offer)}
        <div class="badge-row">
          <span class="badge ${statusBadgeClass(offer)}">${esc(statusLabel(statusType(offer)))}</span>
          <span class="badge">${esc(brl(offer.price_brl))}</span>
        </div>
      </div>
      <div class="card-body">
        <div class="card-title">
          <b>${esc(offer.name)}</b>
          <span>${esc(offer.section || "-")} · ${esc(offer.source_caps || "-")}</span>
        </div>
        ${shortItems(offer)}
        <div class="card-metric">
          <div class="metric-box"><span>${esc(t("score"))}</span><b>${esc(scoreLabel(offer))}</b></div>
          <div class="metric-box"><span>${esc(t("confidence"))}</span><b>${esc(offer.confidence || "-")}</b></div>
        </div>
        <p class="recommend">${esc(offer.recommendation || "")}</p>
        <div class="card-actions">
          <button class="small-btn" type="button" data-detail="${esc(offer.id)}">${esc(t("seeDetails"))}</button>
          <label class="compare-check"><input type="checkbox" data-compare="${esc(offer.id)}" ${checked}> ${esc(t("compare"))}</label>
        </div>
      </div>
    </article>
  `;
}
function renderGrid(rows) {
  els.count.textContent = `(${rows.length}/${OFFERS.length})`;
  els.libraryHint.textContent = t("libraryHint");
  els.grid.innerHTML = rows.length ? rows.map(offerCard).join("") : `<div class="empty">${esc(t("noResults"))}</div>`;
  els.grid.querySelectorAll("[data-select]").forEach(bindSelect);
  els.grid.querySelectorAll("[data-detail]").forEach((button) => {
    button.addEventListener("click", (event) => {
      event.stopPropagation();
      state.selectedId = button.dataset.detail;
      renderDetail();
      document.getElementById("detailPanel").scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
  els.grid.querySelectorAll("[data-compare]").forEach((checkbox) => {
    checkbox.addEventListener("click", (event) => event.stopPropagation());
    checkbox.addEventListener("change", () => {
      const id = checkbox.dataset.compare;
      if (checkbox.checked) state.compare.add(id);
      else state.compare.delete(id);
      renderCompare();
    });
  });
}
function renderCompare() {
  const selected = Array.from(state.compare).map((id) => OFFERS.find((offer) => offer.id === id)).filter(Boolean);
  els.compareBox.classList.toggle("active", selected.length > 0);
  els.compareList.innerHTML = selected.map((offer) => `
    <article class="compare-card">
      ${thumb(offer)}
      <b>${esc(offer.name)}</b>
      <p class="muted">${esc(brl(offer.price_brl))} · ${esc(scoreLabel(offer))}</p>
    </article>
  `).join("");
}
function itemsCell(offer) {
  return (offer.items || []).map((item) => {
    const qty = item.qty === null || item.qty === undefined ? "" : ` x${esc(item.qty)}`;
    return `<span class="pill">${esc(item.name)}${qty}</span>`;
  }).join(" ");
}
function renderTable(rows) {
  els.rows.innerHTML = rows.length ? rows.map((offer) => `
    <tr>
      <td>${offer.thumbnail ? `<img class="table-thumb" src="${esc(offer.thumbnail)}" alt="${esc(offer.name)}">` : esc(t("noThumb"))}</td>
      <td><b>${esc(offer.name)}</b><br><span class="muted">${esc(offer.section || "-")} · ${esc(offer.type || "-")}</span></td>
      <td><b>${esc(brl(offer.price_brl))}</b><br><span class="muted">${offer.currency_bonus ? "+" + esc(offer.currency_bonus) : "-"}</span></td>
      <td>${itemsCell(offer)}</td>
      <td><b>${esc(scoreLabel(offer))}</b><br><span class="muted">${esc(state.goal)}</span></td>
      <td>${esc(offer.recommendation || "")}</td>
      <td><span class="mono">${esc(offer.source_caps || "-")}</span></td>
    </tr>
  `).join("") : `<tr><td colspan="7">${esc(t("noResults"))}</td></tr>`;
}
function render() {
  applyCopy();
  fillSelects();
  renderStats();
  renderObjectives();
  renderBest();
  renderDetail();
  const rows = filteredOffers();
  renderGrid(rows);
  renderTable(rows);
  renderCompare();
}
function wire() {
  document.querySelectorAll("[data-lang]").forEach((button) => {
    button.addEventListener("click", () => {
      state.lang = button.dataset.lang;
      localStorage.setItem(STORAGE_KEY, state.lang);
      render();
    });
  });
  [els.search, els.category, els.status, els.sort].forEach((node) => {
    node.addEventListener("input", render);
    node.addEventListener("change", render);
  });
  els.reset.addEventListener("click", () => {
    els.search.value = "";
    els.category.value = "";
    els.status.value = "";
    els.sort.value = "best";
    state.confidence = "";
    render();
  });
}
wire();
render();
</script>
</body>
</html>
"""
    return (
        template
        .replace("__DATA__", data_json)
        .replace("__CAPTURED__", str(captured_at))
        .replace("__SOURCE_NOTE__", str(source_note))
    )


def main() -> None:
    data = load_data()
    OUT_HTML.write_text(html_page(data), encoding="utf-8")
    print(f"Generated {OUT_HTML} with {len(data.get('offers', []))} offers.")


if __name__ == "__main__":
    main()
