(() => {
  const STORAGE_KEY = 'palmon-profile-workspace-v5';
  const clone = value => JSON.parse(JSON.stringify(value));
  const BASE = clone(window.PALMON_S3.player);
  const slotOrder = ['1', '2', '6', '3', '4', '5', '7'];
  const slotMeta = {
    1: ['Frente esquerda', 'front'], 2: ['Frente centro', 'front'], 6: ['Frente direita', 'front'],
    3: ['Fundo esquerda', 'back'], 4: ['Fundo centro E', 'back'], 5: ['Fundo centro D', 'back'], 7: ['Fundo direita', 'back'],
  };
  const tierValue = window.PALMON_KNOWLEDGE?.tierScore || { 'S+': 100, S: 80, A: 60, B: 40, C: 20, SP: 90, '?': 24 };
  const gearNames = ['Arma', 'Armadura', 'Acessório', 'Capacete'];
  const gearQuality = [['?', 'Não informado'], ['0', 'Sem peça'], ['1', 'Branco'], ['2', 'Verde'], ['3', 'Azul'], ['4', 'Roxo'], ['5', 'Laranja']];
  const $ = id => document.getElementById(id);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
  const fmt = value => new Intl.NumberFormat('pt-BR').format(Math.max(0, Math.round(Number(value) || 0)));
  const parsePower = value => Number(String(value || '').replace(/[^0-9]/g, '')) || 0;
  let elementFilter = 'all';
  let teamIndex = 0;
  let state = load();

  function known(card) { return window.PALMON_KNOWLEDGE?.withKnowledge ? window.PALMON_KNOWLEDGE.withKnowledge(card) : card; }
  function detail(card) { return window.PALMON_KNOWLEDGE?.descriptor ? window.PALMON_KNOWLEDGE.descriptor(card) : { name: card.name, image: card.image, stage: 'base', stageLabel: card.form || 'Base', tier: card.tier, evolutionPath: [card.name] }; }
  function formStages(card) { return window.PALMON_KNOWLEDGE?.availableStages ? window.PALMON_KNOWLEDGE.availableStages(window.PALMON_KNOWLEDGE.lineFor(card)) : ['base', 'evolved']; }

  function hydrate(profile) {
    profile.account = profile.account || {};
    profile.roster = (profile.roster || []).map(card => {
      const referencePower = card.referencePower ?? card.power ?? '';
      const migrated = { ...card, owned: card.owned !== false, referencePower };
      // v4 stored a generic display form. Infer the actual form from the APK art/name once.
      if (!migrated.stage) delete migrated.form;
      return known(window.PalmonPower.defaults(migrated));
    });
    // The snapshot seeds what the player owns; the full APK catalog stays editable below it.
    (window.PALMON_KNOWLEDGE?.catalog || []).forEach(line => {
      const exists = profile.roster.some(card => window.PALMON_KNOWLEDGE.lineFor(card)?.id === line.id);
      if (!exists) profile.roster.push(known(window.PalmonPower.defaults({ id: `catalog-${line.id.toLowerCase()}`, name: line.base, baseName: line.base, lineId: line.id, element: line.element, role: line.role, rarity: line.rarity, image: line.image, level: 1, stars: 0, owned: false, referencePower: '' })));
    });
    profile.teams = (profile.teams || []).map(team => {
      const members = (team.members || []).map(value => {
        if (profile.roster.some(card => card.id === value)) return value;
        return profile.roster.find(card => card.name === value)?.id || null;
      }).slice(0, 7);
      while (members.length < 7) members.push(null);
      return { ...team, members };
    });
    while (profile.teams.length < 4) profile.teams.push({ name: `Time ${profile.teams.length + 1}`, members: [null, null, null, null, null, null, null] });
    profile.auroraSnapshot = profile.auroraSnapshot || { orbs: 0, affinity: '', selected: '' };
    profile.mounts = profile.mounts || [];
    return profile;
  }

  function load() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || localStorage.getItem('palmon-profile-workspace-v4') || localStorage.getItem('palmon-profile-workspace-v3') || 'null');
      if (saved && Array.isArray(saved.roster) && Array.isArray(saved.teams)) return hydrate(saved);
    } catch (_) { /* Use the imported snapshot when local data is invalid. */ }
    return hydrate(clone(BASE));
  }

  function save(silent = false) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    if (!silent) toast('Alteração salva neste navegador.');
  }

  function toast(message) {
    const node = $('toast');
    node.textContent = message;
    node.classList.add('show');
    clearTimeout(toast.timer);
    toast.timer = setTimeout(() => node.classList.remove('show'), 2200);
  }

  function owned() { return state.roster.filter(card => card.owned); }
  function pal(id) { return state.roster.find(card => card.id === id); }
  function currentTeam() { return state.teams[teamIndex]; }
  function teamSlots() { return currentTeam().members.map(id => pal(id)?.owned ? id : null).slice(0, 7); }
  function filledIds() { return teamSlots().filter(Boolean); }
  function calc(card) { return window.PalmonPower.calculate(card); }
  function effectivePower(card) { const result = calc(card); return result.exact ? result.total : parsePower(card.referencePower); }
  function score(card) {
    const gamePower = effectivePower(card);
    const level = Math.min(310, Number(card.level) || 0);
    const stars = Math.min(25, Number(card.stars) || 0);
    const knowledgeScore = window.PALMON_KNOWLEDGE?.strategicScore ? window.PALMON_KNOWLEDGE.strategicScore(card) : (tierValue[card.tier] || 20);
    return Math.round(knowledgeScore * 0.52 + level / 310 * 18 + stars / 25 * 7 + Math.min(25, gamePower / 600000));
  }
  function objectiveLabel() {
    const value = $('objective').value;
    return value === 'general' ? 'meta geral' : value === 'pvp' ? 'PvP / maior poder' : `time só ${value}`;
  }
  function candidatePool() {
    const objective = $('objective').value;
    return (objective === 'general' || objective === 'pvp' ? owned() : owned().filter(card => card.element === objective));
  }
  function roleWeight(card, slot) {
    const role = (card.role || '').toLowerCase();
    const front = ['1', '2', '6'].includes(slot);
    if (front && /(frente|tanque|controle)/.test(role)) return 12;
    if (!front && !/(frente|tanque)/.test(role)) return 8;
    return 0;
  }
  function recommend() {
    const pool = candidatePool().sort((a, b) => score(b) - score(a));
    const picks = [];
    slotOrder.forEach(slot => {
      const next = pool.filter(card => !picks.includes(card.id)).sort((a, b) => (score(b) + roleWeight(b, slot)) - (score(a) + roleWeight(a, slot)))[0];
      if (next) picks.push(next.id);
    });
    return picks;
  }
  function teamScore(ids) { return ids.reduce((total, id) => total + (pal(id) ? score(pal(id)) : 0), 0); }
  function teamPower(ids) { return ids.reduce((total, id) => total + (pal(id) ? effectivePower(pal(id)) : 0), 0); }
  function teamIsExact(ids) { return ids.length > 0 && ids.every(id => calc(pal(id)).exact); }
  function elementBonus(ids) {
    const counts = {};
    ids.forEach(id => { const element = pal(id)?.element; if (element) counts[element] = (counts[element] || 0) + 1; });
    let element = ''; let count = 0;
    Object.entries(counts).forEach(([name, value]) => { if (value > count) { element = name; count = value; } });
    const bonus = count >= 7 ? 30 : count >= 6 ? 25 : count >= 5 ? 20 : count >= 4 ? 10 : count >= 3 ? 5 : 0;
    return { element, count, bonus };
  }

  function setSlot(slot, id) {
    const members = [...currentTeam().members];
    const index = slotOrder.indexOf(slot);
    while (members.length < 7) members.push(null);
    const already = members.indexOf(id);
    if (id && already >= 0 && already !== index) members[already] = null;
    members[index] = id || null;
    currentTeam().members = members;
    save(true);
    render();
  }

  function applyPlan() {
    currentTeam().members = [...recommend(), null, null, null, null, null, null].slice(0, 7);
    save(true);
    render();
    toast(`Melhor time aplicado ao ${currentTeam().name}.`);
  }

  function renderTeamPicker() {
    $('teamPick').innerHTML = state.teams.map((team, index) => `<option value="${index}">${esc(team.name)}</option>`).join('');
    $('teamPick').value = teamIndex;
  }

  function slotHtml(slot) {
    const id = teamSlots()[slotOrder.indexOf(slot)] || '';
    const card = pal(id);
    const options = ['<option value="">Vazio</option>'].concat(owned().map(item => `<option value="${esc(item.id)}" ${item.id === id ? 'selected' : ''}>${esc(detail(item).name)} · Lv ${item.level}</option>`)).join('');
    const info = card && detail(card);
    const art = info?.image;
    return `<article class="slot"><div class="slot-art">${card ? (art ? `<img src="${esc(art)}" alt="${esc(info.name)}">` : '<span class="pill">SP</span>') : '<span class="pill">Vazio</span>'}<span><b>${esc(slotMeta[slot][0])}</b><small>${card ? `${esc(card.element)} · ${esc(info.tier)} · ${fmt(effectivePower(card))}` : 'Escolha um Palmon'}</small></span></div><select data-slot="${slot}">${options}</select></article>`;
  }

  function renderFormation() {
    $('frontSlots').innerHTML = ['1', '2', '6'].map(slotHtml).join('');
    $('backSlots').innerHTML = ['3', '4', '5', '7'].map(slotHtml).join('');
    document.querySelectorAll('[data-slot]').forEach(select => select.addEventListener('change', () => setSlot(select.dataset.slot, select.value)));
  }

  function renderAdvice() {
    const current = filledIds();
    const plan = recommend();
    const pool = candidatePool();
    const currentScore = teamScore(current);
    const recommendedScore = teamScore(plan);
    const bonus = elementBonus(current);
    const missing = plan.filter(id => !current.includes(id));
    const weak = current.filter(id => !plan.includes(id));
    $('decisionTitle').textContent = current.length ? `Seu ${currentTeam().name} pode ganhar ${Math.max(0, recommendedScore - currentScore)} pontos comparativos para ${objectiveLabel()}.` : `Monte ${currentTeam().name} para o advisor calcular a próxima troca.`;
    $('decisionCopy').textContent = $('objective').value !== 'general' && $('objective').value !== 'pvp' && pool.length < 7 ? `Você tem ${pool.length} Palmons marcados desse elemento. O plano usa somente o seu elenco.` : 'O plano considera somente cards marcados como seus. O poder mostrado vem do cálculo APK quando todos os atributos foram preenchidos; antes disso mantém a leitura do seu print como referência.';
    const exact = teamIsExact(current);
    $('stats').innerHTML = `<div class="stat"><b>${current.length}/7</b><small>Slots ocupados</small></div><div class="stat"><b>${fmt(teamPower(current))}</b><small>Poder dos 7${exact ? '' : ' · referência parcial'}</small></div><div class="stat"><b>${currentScore}</b><small>Score atual</small></div><div class="stat"><b>${bonus.bonus ? `+${bonus.bonus}%` : '0%'}</b><small>${bonus.element ? `${bonus.element} · ${bonus.count} no time` : 'Bônus elemental'}</small></div>`;
    const notes = [];
    if (!current.length) notes.push('<span class="warn-text">Escolha cards nos slots ou use “Aplicar melhor time”.</span>');
    if (missing.length) {
      const pairs = missing.slice(0, 3).map((inId, index) => weak[index] ? `troque <b>${esc(detail(pal(weak[index])).name)}</b> por <b>${esc(detail(pal(inId)).name)}</b>` : `adicione <b>${esc(detail(pal(inId)).name)}</b>`);
      notes.push(`Prioridade: ${pairs.join('; ')}.`);
    } else if (current.length === 7) notes.push('<span class="ok">Nenhuma troca clara no objetivo atual. Complete skills, evolução e equipamento para fechar o poder calculado.</span>');
    if (bonus.count < 3 && current.length >= 3) notes.push(`Seu maior grupo elemental é ${bonus.element} com ${bonus.count}. Três iguais liberam o primeiro bônus de sinergia.`);
    if (!exact && current.length) notes.push('Há cards com build incompleta. O total do squad usa o poder registrado no print somente nesses cards, até o cálculo APK ficar completo.');
    $('advice').innerHTML = notes.map(note => `<li>${note}</li>`).join('');
  }

  function renderAccount() {
    $('title').textContent = state.account.name || 'Seu advisor';
    $('accountName').value = state.account.name || '';
    $('server').value = state.account.server || '';
    $('accountPower').value = state.account.power || '';
    $('orbs').value = state.auroraSnapshot.orbs ?? '';
    $('affinity').value = state.auroraSnapshot.affinity || '';
    $('auroraTarget').value = state.auroraSnapshot.selected || '';
    $('mounts').innerHTML = state.mounts.map((mount, index) => `<div class="mount"><span><b>${esc(mount.name)}</b><small>${esc(mount.decision || '')}</small></span><label class="field">Nível<input data-mount="${index}" data-mount-field="level" type="number" min="1" value="${Number(mount.level || 1)}"></label><label class="field">Skill<input data-mount="${index}" data-mount-field="skill" type="number" min="1" max="5" value="${Number(mount.skill || 1)}"></label></div>`).join('');
    document.querySelectorAll('[data-mount]').forEach(input => input.addEventListener('input', () => { state.mounts[Number(input.dataset.mount)][input.dataset.mountField] = Number(input.value) || 0; save(true); }));
  }

  function componentHtml(result) {
    if (!result.available) return '<span class="warn-text">Sem tabela correspondente no APK.</span>';
    const labels = [['base', 'Base'], ['level', 'Nível'], ['stars', 'Estrelas'], ['skills', 'Skills'], ['evolution', 'Evolução'], ['equipment', 'Equipamento']];
    return labels.map(([key, label]) => `<span>${label}: <b>${fmt(result.components[key])}</b></span>`).join('');
  }

  function skillFields(card, result) {
    if (!result.available) return '';
    return result.skills.map(skill => `<label class="field">Skill ${skill.index + 1}<input data-skill="${esc(card.id)}" data-skill-index="${skill.index}" type="number" min="1" max="${skill.max || 1}" value="${Number(card.skills[skill.index] || 1)}"><small>Lv ${skill.level || '?'} · +${fmt(skill.power)}</small></label>`).join('');
  }

  function evolutionFields(card) {
    const options = window.PalmonPower.evolutionOptions(card);
    if (!options.length) return '<p class="sub">Este Palmon não possui árvore de evolução na tabela do APK.</p>';
    return options.map((evolution, evolutionIndex) => {
      const saved = card.evolution?.[evolution.id] || {};
      const nodes = evolution.roots.map((root, nodeIndex) => {
        const selected = Number(saved.nodes?.[nodeIndex] || root.rootId);
        const choices = root.nodes.map(node => `<option value="${node.id}" ${node.id === selected ? 'selected' : ''}>Estágio ${node.stage} · +${fmt(node.power)}</option>`).join('');
        return `<label class="field">Nó ${nodeIndex + 1}<select data-evo-node="${esc(card.id)}" data-evo-id="${evolution.id}" data-evo-index="${nodeIndex}" ${saved.active ? '' : 'disabled'}>${choices}</select></label>`;
      }).join('');
      return `<div class="evolution-group"><label class="owned"><input data-evo-active="${esc(card.id)}" data-evo-id="${evolution.id}" type="checkbox" ${saved.active ? 'checked' : ''}> Evolução ${evolutionIndex + 1} ativa</label><div class="mini-fields">${nodes}</div></div>`;
    }).join('');
  }

  function equipmentFields(card) {
    return gearNames.map((name, index) => {
      const item = (card.equipment || [])[index];
      const quality = item?.quality;
      const options = gearQuality.map(([value, label]) => `<option value="${value}" ${String(quality ?? '?') === value ? 'selected' : ''}>${label}</option>`).join('');
      return `<div class="gear"><b>${name}</b><label class="field">Qualidade<select data-gear-quality="${esc(card.id)}" data-gear-index="${index}">${options}</select></label><label class="field">Reforço<input data-gear-level="${esc(card.id)}" data-gear-index="${index}" type="number" min="0" value="${item?.level ?? ''}" placeholder="Lv"></label><label class="field">Estrelas<input data-gear-stars="${esc(card.id)}" data-gear-index="${index}" type="number" min="0" value="${item?.stars ?? ''}" placeholder="0"></label></div>`;
    }).join('');
  }

  function cardHtml(card) {
    const result = calc(card);
    const info = detail(card);
    const reference = parsePower(card.referencePower);
    const exactLabel = result.exact ? '<span class="power-ok">Confirmado pelo APK</span>' : `<span class="power-warn">Falta: ${esc(result.missing.join(', '))}</span>`;
    const stages = formStages(card).map(stage => `<option value="${stage}" ${info.stage === stage ? 'selected' : ''}>${esc(window.PALMON_KNOWLEDGE.stageLabel(stage))}</option>`).join('');
    const path = info.evolutionPath.join(' → ');
    const portrait = info.image ? `<img src="${esc(info.image)}" alt="${esc(info.name)}">` : '<span class="pill">SP</span>';
    return `<article class="pal"><div class="pal-top">${portrait}<div><div class="pal-title"><b>${esc(info.name)}</b><span class="pill">${esc(info.tier)}</span></div><div class="pal-meta">${esc(card.element)} · ${esc(card.role)} · ${esc(info.stageLabel)}</div><div class="pal-meta">${esc(path)}</div><div class="pal-meta">${esc(info.tierSource)} · ${esc(info.tierConfidence)}</div><label class="owned"><input data-owned="${esc(card.id)}" type="checkbox" ${card.owned ? 'checked' : ''}> Eu tenho</label></div></div><div class="power-result"><div><span>Poder calculado no APK</span><b>${result.available ? fmt(result.total) : '—'}</b>${exactLabel}</div><div><span>Poder registrado no print</span><b>${reference ? fmt(reference) : 'Não capturado'}</b></div></div><div class="power-components">${componentHtml(result)}</div><div class="pal-fields"><label class="field">Nível<input data-roster="${esc(card.id)}" data-field="level" type="number" min="1" value="${Number(card.level || 1)}"></label><label class="field">Estrelas<select data-roster="${esc(card.id)}" data-field="stars">${Array.from({ length: 26 }, (_, star) => `<option value="${star}" ${Number(card.stars) === star ? 'selected' : ''}>${star}</option>`).join('')}</select></label><label class="field">Estágio<select data-roster="${esc(card.id)}" data-field="stage">${stages}</select></label><label class="field">ID no APK<input value="${result.heroId || 'Não identificado'}" readonly></label></div><details class="build-details"><summary>Skills, evolução e equipamento</summary><div class="build-block"><b>Skills</b><div class="mini-fields">${skillFields(card, result)}</div></div><div class="build-block"><b>Evolução</b><p class="sub">Marque apenas os grupos realmente ativos e escolha o estágio de cada nó. A árvore soma exatamente os valores configurados no APK.</p>${evolutionFields(card)}</div><div class="build-block"><b>Equipamento</b><p class="sub">Cada peça aplica a fórmula oficial: (base + reforço) × efeito de estrela + poder da estrela.</p><div class="gear-grid">${equipmentFields(card)}</div></div></details></article>`;
  }

  function bindCardEditors() {
    document.querySelectorAll('[data-owned]').forEach(input => input.addEventListener('change', () => {
      const card = pal(input.dataset.owned);
      card.owned = input.checked;
      if (!card.owned) state.teams.forEach(team => { team.members = (team.members || []).map(id => id === card.id ? null : id); });
      save(true); render();
    }));
    document.querySelectorAll('[data-roster]').forEach(input => input.addEventListener('change', () => {
      const card = pal(input.dataset.roster); const field = input.dataset.field;
      if (field === 'stage') Object.assign(card, known({ ...card, stage: input.value, form: window.PALMON_KNOWLEDGE.stageLabel(input.value) }));
      else card[field] = field === 'level' || field === 'stars' ? Number(input.value) || 0 : input.value;
      save(true); render();
    }));
    document.querySelectorAll('[data-skill]').forEach(input => input.addEventListener('change', () => {
      const card = pal(input.dataset.skill); card.skills[Number(input.dataset.skillIndex)] = Number(input.value) || 1; save(true); render();
    }));
    document.querySelectorAll('[data-evo-active]').forEach(input => input.addEventListener('change', () => {
      const card = pal(input.dataset.evoActive); const id = input.dataset.evoId;
      card.evolution[id] = card.evolution[id] || { active: false, nodes: [] };
      card.evolution[id].active = input.checked;
      save(true); render();
    }));
    document.querySelectorAll('[data-evo-node]').forEach(input => input.addEventListener('change', () => {
      const card = pal(input.dataset.evoNode); const id = input.dataset.evoId; const index = Number(input.dataset.evoIndex);
      card.evolution[id] = card.evolution[id] || { active: true, nodes: [] };
      card.evolution[id].nodes[index] = Number(input.value) || 0;
      save(true); render();
    }));
    document.querySelectorAll('[data-gear-quality],[data-gear-level],[data-gear-stars]').forEach(input => input.addEventListener('change', () => {
      const cardId = input.dataset.gearQuality || input.dataset.gearLevel || input.dataset.gearStars;
      const index = Number(input.dataset.gearIndex); const card = pal(cardId);
      card.equipment[index] = card.equipment[index] || {};
      if (input.dataset.gearQuality) card.equipment[index].quality = input.value === '?' ? null : Number(input.value);
      if (input.dataset.gearLevel) card.equipment[index].level = Number(input.value) || 0;
      if (input.dataset.gearStars) card.equipment[index].stars = Number(input.value) || 0;
      save(true); render();
    }));
  }

  function renderRoster() {
    const search = $('search').value.trim().toLowerCase();
    const matches = card => (elementFilter === 'all' || card.element === elementFilter) && `${detail(card).name} ${detail(card).evolutionPath.join(' ')}`.toLowerCase().includes(search);
    const mine = state.roster.filter(card => card.owned && matches(card)).sort((a, b) => effectivePower(b) - effectivePower(a));
    const missing = state.roster.filter(card => !card.owned && matches(card)).sort((a, b) => a.name.localeCompare(b.name));
    $('rosterCount').textContent = `${mine.length} no seu elenco · ${missing.length} ainda não obtidos`;
    const grid = list => list.length ? `<div class="roster">${list.map(cardHtml).join('')}</div>` : '<div class="empty">Nenhum Palmon neste filtro.</div>';
    $('roster').innerHTML = `<section class="roster-group"><div class="roster-group-head"><h3>Seu elenco</h3><span class="pill">${mine.length}</span></div>${grid(mine)}</section><section class="roster-group missing"><div class="roster-group-head"><h3>Palmon que faltam</h3><span class="pill">${missing.length}</span></div>${grid(missing)}</section>`;
    bindCardEditors();
  }

  function render() {
    renderTeamPicker(); renderAccount(); renderAdvice(); renderFormation(); renderRoster();
  }

  $('teamPick').addEventListener('change', () => { teamIndex = Number($('teamPick').value); render(); });
  $('objective').addEventListener('change', render);
  $('applyPlan').addEventListener('click', applyPlan);
  $('saveNow').addEventListener('click', () => save());
  [['accountName', 'name'], ['server', 'server'], ['accountPower', 'power']].forEach(([id, key]) => $(id).addEventListener('input', () => { state.account[key] = $(id).value; save(true); $('title').textContent = state.account.name || 'Seu advisor'; }));
  [['orbs', 'orbs'], ['affinity', 'affinity'], ['auroraTarget', 'selected']].forEach(([id, key]) => $(id).addEventListener('input', () => { state.auroraSnapshot[key] = key === 'orbs' ? Number($(id).value) || 0 : $(id).value; save(true); }));
  $('search').addEventListener('input', renderRoster);
  $('elementFilters').addEventListener('click', event => {
    const button = event.target.closest('[data-element]'); if (!button) return;
    elementFilter = button.dataset.element;
    document.querySelectorAll('[data-element]').forEach(node => node.classList.toggle('active', node === button));
    renderRoster();
  });
  $('exportProfile').addEventListener('click', () => {
    const blob = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' });
    const link = document.createElement('a'); link.href = URL.createObjectURL(blob); link.download = 'palmon-profile-workspace.json'; link.click(); URL.revokeObjectURL(link.href); toast('Perfil exportado em JSON.');
  });
  $('importProfile').addEventListener('change', event => {
    const file = event.target.files?.[0]; if (!file) return;
    const reader = new FileReader();
    reader.onload = () => { try { state = hydrate(JSON.parse(reader.result)); teamIndex = 0; save(true); render(); toast('Perfil importado.'); } catch (_) { toast('Esse arquivo não é um perfil válido.'); } };
    reader.readAsText(file); event.target.value = '';
  });
  $('resetProfile').addEventListener('click', () => { state = hydrate(clone(BASE)); teamIndex = 0; save(true); render(); toast('Snapshot original restaurado.'); });
  render();
})();
