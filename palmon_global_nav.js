(function () {
  const NAV_ID = "palmonGlobalNav";
  if (document.getElementById(NAV_ID)) return;

  const pages = [
    { href: "index.html", label: { pt: "Inicio", en: "Home" }, icon: "home", match: ["", "index.html"] },
    { href: "palmon_survival_pedia_completa.html", label: { pt: "Pedia", en: "Pedia" }, icon: "library-big", match: ["palmon_survival_pedia_completa.html"] },
    { href: "palmon_battle_simulator.html?mode=builder", label: { pt: "Montar time", en: "Team builder" }, icon: "layout-template", match: ["palmon_battle_simulator.html?mode=builder"] },
    { href: "palmon_battle_simulator.html", label: { pt: "Simular", en: "Simulate" }, icon: "swords", match: ["palmon_battle_simulator.html"] },
    { href: "palmon_mount_auditor.html", label: { pt: "Montarias", en: "Mounts" }, icon: "scan-search", match: ["palmon_mount_auditor.html"] },
    { href: "palmon_apk_0_5_325_report.html", label: { pt: "Base tecnica", en: "Technical base" }, icon: "file-search", match: ["palmon_apk_0_5_325_report.html"] }
  ];

  function currentFile() {
    return (window.location.pathname.split("/").pop() || "index.html").toLowerCase();
  }

  function currentLang() {
    const queryLang = new URLSearchParams(window.location.search).get("lang");
    const stored = localStorage.getItem("palmon_lang");
    if (queryLang === "en" || queryLang === "pt") return queryLang;
    if (stored === "en" || stored === "pt") return stored;
    return "pt";
  }

  function withLang(href) {
    const lang = currentLang();
    const url = new URL(href, window.location.href);
    url.searchParams.set("lang", lang);
    return url.pathname.split("/").pop() + url.search + url.hash;
  }

  function isActive(page) {
    const file = currentFile();
    const query = window.location.search.toLowerCase();
    if (page.href.includes("?mode=builder")) return file === "palmon_battle_simulator.html" && query.includes("mode=builder");
    if (page.href === "palmon_battle_simulator.html") return file === "palmon_battle_simulator.html" && !query.includes("mode=builder");
    return page.match.includes(file) || (file === "index.html" && page.href === "index.html");
  }

  function injectStyles() {
    const style = document.createElement("style");
    style.textContent = `
      .palmon-global-nav{position:sticky;top:0;z-index:9999;background:#ffffffee;backdrop-filter:blur(14px);border-bottom:1px solid #d8e2ee;box-shadow:0 8px 26px rgba(23,32,51,.08)}
      .palmon-global-inner{width:min(1380px,calc(100% - 24px));margin:0 auto;min-height:62px;display:flex;align-items:center;gap:14px;justify-content:space-between}
      .palmon-global-brand{display:flex;align-items:center;gap:10px;font-weight:950;color:#13233a;text-decoration:none;white-space:nowrap}
      .palmon-global-mark{width:34px;height:34px;border-radius:8px;display:grid;place-items:center;background:linear-gradient(135deg,#1d58ca,#38bdf8);color:#fff;box-shadow:0 10px 18px rgba(29,88,202,.22)}
      .palmon-global-brand small{display:block;font-size:11px;color:#667085;font-weight:800;line-height:1.1}
      .palmon-global-links{display:flex;align-items:center;gap:6px;flex-wrap:wrap;justify-content:flex-end}
      .palmon-global-link,.palmon-lang-btn{display:inline-flex;align-items:center;gap:7px;min-height:36px;padding:0 10px;border-radius:8px;border:1px solid transparent;color:#344054;background:transparent;text-decoration:none;font-size:13px;font-weight:850;cursor:pointer}
      .palmon-global-link:hover,.palmon-lang-btn:hover{background:#f2f6fb;text-decoration:none}
      .palmon-global-link.active{background:#eaf2ff;border-color:#bfd7ff;color:#174ea6}
      .palmon-global-link svg,.palmon-global-mark svg{width:16px;height:16px;stroke-width:2.4}
      .palmon-global-lang{display:inline-flex;margin-left:4px;border:1px solid #d8e2ee;border-radius:8px;overflow:hidden;background:#fff}
      .palmon-lang-btn{border-radius:0;min-height:34px;padding:0 9px}
      .palmon-lang-btn.active{background:#13233a;color:#fff}
      @media(max-width:820px){.palmon-global-inner{align-items:flex-start;flex-direction:column;padding:10px 0}.palmon-global-links{justify-content:flex-start}.palmon-global-link{min-height:34px}.palmon-global-brand small{display:none}}
    `;
    document.head.appendChild(style);
  }

  function render() {
    injectStyles();
    const lang = currentLang();
    const nav = document.createElement("div");
    nav.id = NAV_ID;
    nav.className = "palmon-global-nav";
    nav.innerHTML = `
      <div class="palmon-global-inner">
        <a class="palmon-global-brand" href="${withLang("index.html")}" aria-label="Voltar ao inicio">
          <span class="palmon-global-mark"><i data-lucide="compass"></i></span>
          <span>Palmon Hub<small>Base e ferramentas 2026</small></span>
        </a>
        <div class="palmon-global-links">
          ${pages.map((page) => `<a class="palmon-global-link ${isActive(page) ? "active" : ""}" href="${withLang(page.href)}"><i data-lucide="${page.icon}"></i>${page.label[lang] || page.label.pt}</a>`).join("")}
          <span class="palmon-global-lang" aria-label="Idioma">
            <button class="palmon-lang-btn ${lang === "pt" ? "active" : ""}" type="button" data-lang="pt">PT</button>
            <button class="palmon-lang-btn ${lang === "en" ? "active" : ""}" type="button" data-lang="en">EN</button>
          </span>
        </div>
      </div>
    `;
    document.body.prepend(nav);
    nav.querySelectorAll("[data-lang]").forEach((button) => {
      button.addEventListener("click", () => {
        const next = button.dataset.lang;
        localStorage.setItem("palmon_lang", next);
        const url = new URL(window.location.href);
        url.searchParams.set("lang", next);
        window.location.href = url.toString();
      });
    });

    if (window.lucide && typeof window.lucide.createIcons === "function") {
      window.lucide.createIcons();
    } else {
      const script = document.createElement("script");
      script.src = "https://unpkg.com/lucide@0.468.0/dist/umd/lucide.min.js";
      script.onload = () => window.lucide && window.lucide.createIcons();
      document.head.appendChild(script);
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", render);
  else render();
})();
