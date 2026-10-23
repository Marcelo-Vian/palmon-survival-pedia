(() => {
  const STORAGE_KEY = 'palmon-profile-workspace-v7';
  const clone = value => JSON.parse(JSON.stringify(value));
  const BASE = clone(window.PALMON_S3.player);
  const screenshotSkillSeeds = new Map((BASE.roster || []).filter(card => Array.isArray(card.skills)).map(card => [card.id, { skills: [...card.skills], skillsSource: card.skillsSource || 'prints-2026-10-19' }]));
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
  function isAdvisorRarity(card) {
    const rarity = detail(card).line?.rarity || card.rarity || '';
    return rarity === 'UR' || rarity === 'SP Mythic';
  }
  function normalizeBoss(boss) {
    return {
      id: boss.id || String(boss.name || 'boss').toLowerCase().replace(/[^a-z0-9]+/g, '-'),
      name: boss.name || 'Boss sem nome', element: boss.element || 'Nao confirmado', image: boss.image || '',
      level: boss.level ?? '', stars: boss.stars ?? '', power: boss.power ?? '',
      skills: Array.isArray(boss.skills) ? [...boss.skills, '', '', ''].slice(0, 3) : ['', '', ''],
      taming: boss.taming || '', detail: boss.detail || '', source: boss.source || 'Campo editavel',
    };
  }

  function lineupSignatureFor(profile, members) {
    return (members || []).map(id => {
      const card = (profile.roster || []).find(item => item.id === id);
      return window.PALMON_KNOWLEDGE?.lineFor(card)?.id || card?.lineId || card?.id || '';
    }).filter(Boolean).sort().join('|');
  }

  function hydrate(profile) {
    profile.account = profile.account || {};
    profile.roster = (profile.roster || []).map(card => {
      const referencePower = card.referencePower ?? card.power ?? '';
      const migrated = { ...card, owned: card.owned !== false, referencePower };
      const hasManualSkillEdit = migrated.skillsSource === 'manual' || (!migrated.skillsSource && Array.isArray(migrated.skills) && migrated.skills.some(level => level !== 1));
      const skillSeed = screenshotSkillSeeds.get(migrated.id);
      // Older workspace versions invented Lv 1 for every missing skill. Replace only that old
      // placeholder with the values actually read from the player's screenshots.
      if (!hasManualSkillEdit && skillSeed) Object.assign(migrated, clone(skillSeed));
      else if (!hasManualSkillEdit && !skillSeed) {
        migrated.skills = null;
        migrated.skillsSource = 'nao-capturada';
      } else if (hasManualSkillEdit && !migrated.skillsSource) migrated.skillsSource = 'manual';
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
      const seed = (BASE.teams || []).find(item => item.name === team.name) || {};
      const members = (team.members || []).map(value => {
        if (profile.roster.some(card => card.id === value)) return value;
        return profile.roster.find(card => card.name === value)?.id || null;
      }).slice(0, 7);
      while (members.length < 7) members.push(null);
      const merged = { ...seed, ...team, power: team.power ?? seed.power ?? '', members };
      const currentSignature = lineupSignatureFor(profile, members);
      const observedSignature = (seed.observedLineIds || []).slice().sort().join('|');
      if (merged.name === 'Time 1' && (!team.source || team.source === 'Captura de tela 2026-10-22 084155')) {
        merged.source = seed.source;
        merged.observedLabels = seed.observedLabels;
        merged.observedLineIds = seed.observedLineIds;
        merged.observedAura = seed.observedAura;
        merged.validation = seed.validation;
        merged.note = seed.note;
      }
      merged.squadPower = {
        selectedBossId: '', armigoPower: '', jewelPower: '', calibration: null,
        ...(seed.squadPower || {}), ...(team.squadPower || {}),
      };
      if (!merged.powerLineupSignature && merged.power && merged.name === 'Time 1' && currentSignature === observedSignature) {
        merged.powerLineupSignature = currentSignature;
        merged.powerReferenceState = 'current';
      } else if (!merged.powerLineupSignature && merged.power) {
        merged.powerReferenceState = 'legacy';
      }
      return merged;
    });
    while (profile.teams.length < 4) profile.teams.push({ name: `Time ${profile.teams.length + 1}`, members: [null, null, null, null, null, null, null] });
    profile.auroraSnapshot = profile.auroraSnapshot || { orbs: 0, affinity: '', selected: '' };
    profile.mounts = profile.mounts || [];
    const previousBosses = Array.isArray(profile.bosses) ? profile.bosses : [];
    const seedBosses = window.PALMON_S3?.bosses || [];
    profile.bosses = seedBosses.map(seed => normalizeBoss({ ...seed, ...(previousBosses.find(saved => saved.id === seed.id || saved.name === seed.name) || {}) }));
    previousBosses.filter(saved => !profile.bosses.some(boss => boss.id === saved.id || boss.name === saved.name)).forEach(saved => profile.bosses.push(normalizeBoss(saved)));
    return profile;
  }

  function load() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || localStorage.getItem('palmon-profile-workspace-v6') || localStorage.getItem('palmon-profile-workspace-v5') || localStorage.getItem('palmon-profile-workspace-v4') || localStorage.getItem('palmon-profile-workspace-v3') || 'null');
      if (saved && Array.isArray(saved.roster) && Array.isArray(saved.teams)) return hydrate(saved);
    } catch (_) { /* Use the imported snapshot when local data is invalid. */ }
    return hydrate(clone(BASE));
  }

  function save(silent = false) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    if (!silent) toast('Alteração salva neste navegador.');
  }

  function profileMarkdown(profile) {
    const ownedCount = profile.roster.filter(card => card.owned).length;
    const bossCount = (profile.bosses || []).length;
    return `# Perfil Palmon Survival\n\n- Exportado pelo Palmon Advisor\n- Snapshot local: ${new Date().toLocaleString('pt-BR')}\n- Elenco marcado como seu: ${ownedCount}\n- Bosses registrados: ${bossCount}\n\nEste arquivo preserva o perfil editável. Para carregar de volta, use **Importar perfil** na página Meu perfil.\n\n\`\`\`json\n${JSON.stringify(profile, null, 2)}\n\`\`\`\n`;
  }

  function parseProfileFile(raw) {
    try { return JSON.parse(raw); } catch (_) { /* Markdown exportado pelo advisor. */ }
    const match = String(raw).match(/```json\s*([\s\S]*?)\s*```/i);
    if (!match) throw new Error('Perfil não encontrado no Markdown.');
    return JSON.parse(match[1]);
  }

  function toast(message) {
    const node = $('toast');
    node.textContent = message;
    node.classList.add('show');
    clearTimeout(toast.timer);
    toast.timer = setTimeout(() => node.classList.remove('show'), 2200);
  }

  function owned() { return state.roster.filter(card => card.owned && isAdvisorRarity(card)); }
  function pal(id) { return state.roster.find(card => card.id === id); }
  function currentTeam() { return state.teams[teamIndex]; }
  function teamSlots() { return currentTeam().members.map(id => pal(id)?.owned && isAdvisorRarity(pal(id)) ? id : null).slice(0, 7); }
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
    const aura = window.PALMON_SQUAD_POWER.auraForElements(ids.map(id => pal(id)?.element));
    const counts = aura.counts;
    let element = ''; let count = 0;
    Object.entries(counts).forEach(([name, value]) => { if (value > count) { element = name; count = value; } });
    return { ...aura, element, count, bonus: aura.percent };
  }

  function lineupSignature(ids = teamSlots()) {
    return ids.map(id => window.PALMON_KNOWLEDGE?.lineFor(pal(id))?.id || pal(id)?.lineId || id || '').filter(Boolean).sort().join('|');
  }

  function isCurrentPowerReference(team = currentTeam()) {
    return Boolean(team?.power && team.powerLineupSignature && team.powerLineupSignature === lineupSignature());
  }

  function squadConfig(team = currentTeam()) {
    team.squadPower = { selectedBossId: '', armigoPower: '', jewelPower: '', calibration: null, ...(team.squadPower || {}) };
    return team.squadPower;
  }

  function squadModel() {
    const team = currentTeam();
    const ids = filledIds();
    const cards = ids.map(pal).filter(Boolean);
    const aura = elementBonus(ids);
    const config = squadConfig(team);
    const boss = state.bosses.find(item => item.id === config.selectedBossId);
    const officialPower = parsePower(team.power);
    const bossPower = boss ? parsePower(boss.power) : 0;
    const armigoPower = parsePower(config.armigoPower);
    const jewelPower = parsePower(config.jewelPower);
    const currentReference = isCurrentPowerReference(team);
    const solved = currentReference
      ? window.PALMON_SQUAD_POWER.solveCompensatedProperty({ officialPower, bossPower, armigoPower, jewelPower, auraBps: aura.bps })
      : { available: false, value: 0, total: 0 };
    const calculated = solved.available
      ? window.PALMON_SQUAD_POWER.calculate({ propertyPower: solved.value, bossPower, armigoPower, jewelPower, auraBps: aura.bps })
      : null;
    const referencePowerTotal = cards.reduce((sum, card) => sum + parsePower(card.referencePower), 0);
    const calibration = config.calibration;
    let forecast = null;
    if (!currentReference && calibration?.referencePowerTotal > 0 && calibration?.compensatedPower >= 0) {
      const projectedProperty = Math.round(calibration.compensatedPower * referencePowerTotal / calibration.referencePowerTotal);
      forecast = window.PALMON_SQUAD_POWER.calculate({ propertyPower: projectedProperty, bossPower, armigoPower, jewelPower, auraBps: aura.bps });
    }
    const displayCalculation = calculated || forecast;
    const distribution = displayCalculation
      ? window.PALMON_SQUAD_POWER.distributeCompensation(cards.map(card => ({ id: card.id, referencePower: parsePower(card.referencePower) })), currentReference ? solved.value : Math.round((calibration?.compensatedPower || 0) * (referencePowerTotal / Math.max(1, calibration?.referencePowerTotal || 1))))
      : [];
    const target = team.validation || {};
    const targetPower = parsePower(target.power);
    const difference = displayCalculation && officialPower ? displayCalculation.total - officialPower : null;
    const validationPass = Boolean(targetPower) && currentReference && Boolean(displayCalculation) && difference === 0
      && officialPower === targetPower
      && (!target.auraBps || aura.bps === target.auraBps);
    return { team, ids, cards, aura, config, boss, officialPower, bossPower, armigoPower, jewelPower, currentReference, solved, calculated, forecast, displayCalculation, distribution, referencePowerTotal, difference, validationPass };
  }

  function captureCalibration() {
    const model = squadModel();
    if (!model.currentReference || !model.solved.available || !model.officialPower) return;
    model.config.calibration = {
      signature: lineupSignature(), officialPower: model.officialPower, auraBps: model.aura.bps,
      compensatedPower: model.solved.value, referencePowerTotal: model.referencePowerTotal,
    };
  }

  function positionAdvice(ids) {
    const mismatch = ids.map((id, index) => ({ card: pal(id), slot: slotOrder[index] }))
      .find(({ card, slot }) => card && ((slotMeta[slot][1] === 'front') !== /(frente|tanque|controle)/i.test(card.role || '')));
    if (!mismatch) return '';
    const lane = /(frente|tanque|controle)/i.test(mismatch.card.role || '') ? 'frente' : 'retaguarda';
    return `Posição tática: ${esc(detail(mismatch.card).name)} rende melhor na ${lane}; mover de slot não altera o poder exibido.`;
  }

  function auraSwapAdvice(ids) {
    const now = elementBonus(ids);
    const current = new Set(ids);
    let best = null;
    ids.forEach(outId => owned().filter(card => !current.has(card.id)).forEach(inCard => {
      const proposal = ids.map(id => id === outId ? inCard.id : id);
      const candidate = elementBonus(proposal);
      if (candidate.bps > now.bps && (!best || candidate.bps > best.aura.bps)) best = { outId, inCard, aura: candidate };
    }));
    if (!best) return '';
    return `Aura: trocar <b>${esc(detail(pal(best.outId)).name)}</b> por <b>${esc(detail(best.inCard).name)}</b> leva a sinergia de +${now.percent}% para +${best.aura.percent}%.`;
  }

  function setSlot(slot, id) {
    captureCalibration();
    const previousSignature = lineupSignature();
    const members = [...currentTeam().members];
    const index = slotOrder.indexOf(slot);
    while (members.length < 7) members.push(null);
    const nextId = id || null;
    const changed = members[index] !== nextId;
    const already = members.indexOf(id);
    if (id && already >= 0 && already !== index) members[already] = null;
    members[index] = nextId;
    currentTeam().members = members;
    if (changed && currentTeam().power && previousSignature !== lineupSignature()) currentTeam().powerReferenceState = 'stale';
    save(true);
    render();
  }

  function applyPlan() {
    captureCalibration();
    currentTeam().members = [...recommend(), null, null, null, null, null, null].slice(0, 7);
    if (currentTeam().power) currentTeam().powerReferenceState = 'stale';
    save(true);
    render();
    toast(`Melhor time aplicado ao ${currentTeam().name}.`);
  }

  function renderTeamPicker() {
    $('teamPick').innerHTML = state.teams.map((team, index) => `<option value="${index}">${esc(team.name)}</option>`).join('');
    $('teamPick').value = teamIndex;
    $('teamPower').value = currentTeam().power || '';
  }

  function slotHtml(slot) {
    const id = teamSlots()[slotOrder.indexOf(slot)] || '';
    const card = pal(id);
    const options = ['<option value="">Vazio</option>'].concat(owned().map(item => `<option value="${esc(item.id)}" ${item.id === id ? 'selected' : ''}>${esc(detail(item).name)} · Lv ${item.level}</option>`)).join('');
    const info = card && detail(card);
    const art = info?.image;
    return `<article class="slot"><div class="slot-art">${card ? (art ? `<img src="${esc(art)}" alt="${esc(info.name)}">` : '<span class="pill">SP</span>') : '<span class="pill">Vazio</span>'}<span><b>${esc(slotMeta[slot][0])}</b><small>${card ? `${esc(card.element)} · Lv ${card.level}` : 'Escolha um Palmon'}</small></span></div><select data-slot="${slot}">${options}</select></article>`;
  }

  function renderFormation() {
    $('frontSlots').innerHTML = ['1', '2', '6'].map(slotHtml).join('');
    $('backSlots').innerHTML = ['3', '4', '5', '7'].map(slotHtml).join('');
    document.querySelectorAll('[data-slot]').forEach(select => select.addEventListener('change', () => setSlot(select.dataset.slot, select.value)));
  }

  function bossCardHtml(boss, index) {
    const skills = boss.skills || [];
    const art = boss.image ? `<img class="boss-art" src="${esc(boss.image)}" alt="${esc(boss.name)}">` : `<span class="boss-element">${esc(boss.element)}</span>`;
    return `<article class="boss-card"><div class="boss-card-head">${art}<span><h4>${esc(boss.name)}</h4><p>Boss de ${esc(boss.element)} · fora dos 7 slots</p></span></div><div class="boss-fields"><label class="field">Nível<input data-boss="${index}" data-boss-field="level" inputmode="numeric" value="${esc(boss.level)}"></label><label class="field">Estrelas<input data-boss="${index}" data-boss-field="stars" value="${esc(boss.stars)}" placeholder="0-0"></label><label class="field">Poder<input data-boss="${index}" data-boss-field="power" inputmode="numeric" value="${esc(boss.power)}"></label><label class="field">Taming / Idolizing<input data-boss="${index}" data-boss-field="taming" value="${esc(boss.taming)}"></label></div><div class="boss-skills">${[0, 1, 2].map(skill => `<label class="field">Skill ${skill + 1}<input data-boss-skill="${index}" data-boss-skill-index="${skill}" value="${esc(skills[skill] || '')}" placeholder="Lv"></label>`).join('')}</div><textarea class="boss-note" data-boss-note="${index}" aria-label="Nota sobre ${esc(boss.name)}">${esc(boss.detail)}</textarea><div class="boss-source">Fonte: ${esc(boss.source || 'campo editável')}</div></article>`;
  }

  function renderBossAdvisor() {
    const root = $('bossAdvisor');
    if (!root) return;
    root.innerHTML = state.bosses.length ? state.bosses.map(bossCardHtml).join('') : '<div class="empty">Nenhum Boss importado ainda.</div>';
    document.querySelectorAll('[data-boss]').forEach(input => input.addEventListener('input', () => {
      state.bosses[Number(input.dataset.boss)][input.dataset.bossField] = input.value;
      save(true);
      renderSquadPower();
    }));
    document.querySelectorAll('[data-boss-skill]').forEach(input => input.addEventListener('input', () => {
      const boss = state.bosses[Number(input.dataset.bossSkill)];
      boss.skills[Number(input.dataset.bossSkillIndex)] = input.value;
      save(true);
    }));
    document.querySelectorAll('[data-boss-note]').forEach(input => input.addEventListener('input', () => {
      state.bosses[Number(input.dataset.bossNote)].detail = input.value;
      save(true);
    }));
  }

  function renderAdvice() {
    const current = filledIds();
    const plan = recommend();
    const pool = candidatePool();
    const currentScore = teamScore(current);
    const recommendedScore = teamScore(plan);
    const bonus = elementBonus(current);
    const powerModel = squadModel();
    const missing = plan.filter(id => !current.includes(id));
    const weak = current.filter(id => !plan.includes(id));
    $('decisionTitle').textContent = current.length ? `Seu ${currentTeam().name} pode ganhar ${Math.max(0, recommendedScore - currentScore)} pontos comparativos para ${objectiveLabel()}.` : `Monte ${currentTeam().name} para o advisor calcular a próxima troca.`;
    const gamePower = parsePower(currentTeam().power);
    $('decisionCopy').textContent = $('objective').value !== 'general' && $('objective').value !== 'pvp' && pool.length < 7
      ? `Você tem ${pool.length} Palmons marcados desse elemento. O plano usa somente o seu elenco.`
      : powerModel.currentReference
        ? 'O poder do jogo está ligado à composição atual. Abaixo, a auditoria mostra cada componente da fórmula do APK sem inventar propertypower do servidor.'
        : gamePower
          ? 'O poder do jogo foi preservado como referência da composição anterior. A previsão abaixo é estimativa até você registrar o novo total no jogo.'
          : 'Informe o poder exibido no jogo quando quiser calibrar a fórmula desta composição.';
    const auraLabel = bonus.qualified.length ? bonus.qualified.map(entry => `${entry.element} ${entry.count}`).join(' + ') : 'Sem aura ativa';
    $('stats').innerHTML = `<div class="stat team-power"><b>${gamePower ? fmt(gamePower) : '—'}</b><small>${powerModel.currentReference ? `Poder do ${esc(currentTeam().name)} no jogo` : 'Referência do jogo / composição anterior'}</small></div><div class="stat"><b>${current.length}/7</b><small>Slots ocupados</small></div><div class="stat"><b>${currentScore}</b><small>Score do advisor</small></div><div class="stat"><b>${bonus.bonus ? `+${bonus.bonus}%` : '0%'}</b><small>${esc(auraLabel)}</small></div>`;
    const notes = [];
    if (!current.length) notes.push('<span class="warn-text">Escolha cards nos slots ou use “Aplicar melhor time”.</span>');
    if (missing.length) {
      const pairs = missing.slice(0, 3).map((inId, index) => weak[index] ? `troque <b>${esc(detail(pal(weak[index])).name)}</b> por <b>${esc(detail(pal(inId)).name)}</b>` : `adicione <b>${esc(detail(pal(inId)).name)}</b>`);
      notes.push(`Prioridade: ${pairs.join('; ')}.`);
    } else if (current.length === 7) notes.push('<span class="ok">Nenhuma troca clara no objetivo atual. Use o poder do jogo como medida principal e ajuste os dados dos cards para melhorar a recomendação.</span>');
    if (bonus.count < 3 && current.length >= 3) notes.push(`Seu maior grupo elemental é ${bonus.element} com ${bonus.count}. Três iguais liberam o primeiro bônus de sinergia.`);
    const auraNote = auraSwapAdvice(current);
    const positionNote = positionAdvice(teamSlots());
    if (auraNote) notes.push(auraNote);
    if (positionNote) notes.push(positionNote);
    $('advice').innerHTML = notes.map(note => `<li>${note}</li>`).join('');
  }

  function renderSquadPower() {
    const root = $('squadPowerResult');
    if (!root) return;
    const model = squadModel();
    const bossOptions = ['<option value="">Não informado / nenhum</option>']
      .concat(state.bosses.map(boss => `<option value="${esc(boss.id)}" ${boss.id === model.config.selectedBossId ? 'selected' : ''}>${esc(boss.name)} · ${fmt(parsePower(boss.power))}</option>`));
    $('squadBoss').innerHTML = bossOptions.join('');
    $('armigoPower').value = model.config.armigoPower || '';
    $('jewelPower').value = model.config.jewelPower || '';

    const compositionText = Object.entries(model.aura.counts).map(([element, count]) => `${esc(element)} ${count}`).join(' + ');
    const auraText = model.aura.qualified.length
      ? `${compositionText}: +${model.aura.percent}%`
      : 'Nenhum grupo com 3 Palmons';
    const result = model.displayCalculation;
    const compensatedPower = model.solved.available ? model.solved.value : model.config.calibration?.compensatedPower;
    let status = '<span class="squad-power-status warn">Aguardando poder do jogo</span>';
    if (model.validationPass) status = '<span class="squad-power-status ok">Baseline validado: 243.560.153 · aura 6 Água + 1 Terra</span>';
    else if (model.currentReference && result && model.difference === 0) status = '<span class="squad-power-status ok">Calibrado para a composição atual</span>';
    else if (result) status = '<span class="squad-power-status warn">Estimativa: a composição mudou desde a referência</span>';
    else if (model.officialPower) status = '<span class="squad-power-status warn">Referência antiga: informe o novo poder no jogo para calibrar</span>';

    const cards = model.distribution.map(item => {
      const card = pal(item.id);
      return `<span>${esc(detail(card).name)}: ${fmt(item.power)}</span>`;
    }).join('') || '<span>Sem base individual suficiente para projeção.</span>';
    const expected = result ? fmt(result.total) : '—';
    const difference = model.difference === null ? '—' : `${model.difference >= 0 ? '+' : ''}${fmt(Math.abs(model.difference))}`;
    root.innerHTML = `${status}<div class="squad-power-grid"><div class="squad-power-item"><small>Poder no jogo</small><b>${model.officialPower ? fmt(model.officialPower) : '—'}</b></div><div class="squad-power-item"><small>Aura APK</small><b>+${model.aura.percent}%</b></div><div class="squad-power-item"><small>Boss selecionado</small><b>${model.boss ? fmt(model.bossPower) : 'Não informado'}</b></div><div class="squad-power-item"><small>Armigos pré-aura</small><b>${fmt(model.armigoPower)}</b></div><div class="squad-power-item"><small>Joias pós-aura</small><b>${fmt(model.jewelPower)}</b></div><div class="squad-power-item"><small>Poder compensado</small><b>${compensatedPower === undefined ? '—' : fmt(compensatedPower)}</b></div><div class="squad-power-item"><small>Total pela fórmula</small><b>${expected}</b></div><div class="squad-power-item"><small>Diferença</small><b>${difference}</b></div><div class="squad-power-item"><small>Sinergia</small><b>${auraText}</b></div></div><p class="squad-power-formula">Fórmula do APK: teto((poder compensado + Boss + Armigos) × (1 + aura)) + joias. “Poder compensado” fecha a conta reversa e não afirma o propertypower enviado pelo servidor.</p><div class="squad-power-cards">${cards}</div>`;

    const saveAndRender = () => { if (isCurrentPowerReference()) captureCalibration(); save(true); renderSquadPower(); renderAdvice(); };
    $('squadBoss').onchange = () => { model.config.selectedBossId = $('squadBoss').value; saveAndRender(); };
    $('armigoPower').onchange = () => { model.config.armigoPower = $('armigoPower').value; saveAndRender(); };
    $('jewelPower').onchange = () => { model.config.jewelPower = $('jewelPower').value; saveAndRender(); };
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

  function skillIconHtml(result, skill) {
    const index = skill.index + 1;
    if (index <= 3 && result.heroId) return `<span class="skill-icon"><img src="assets/skill_icons/${esc(result.heroId)}_${index}.png" alt="Icone da skill ${index}"></span>`;
    return '<span class="skill-icon" title="O APK usa a mesma skill passiva generica para este quarto espaco.">IV</span>';
  }

  function skillFields(card, result) {
    if (!result.available) return '';
    const source = card.skillsSource === 'prints-2026-10-19' ? 'Lidas dos seus prints de 19/10.' : card.skillsSource === 'manual' ? 'Editadas manualmente neste perfil.' : 'Não capturada: preencha apenas se aparecer no jogo.';
    return `<div class="skill-list">${result.skills.map(skill => {
      const value = card.skills[skill.index];
      const reading = skill.unknown ? 'não capturada' : skill.locked ? 'bloqueada' : `Lv ${skill.reported}`;
      const max = Math.max(skill.max || 0, Number(skill.reported) || 0, 30);
      return `<label class="skill-field" title="${esc(`ID ${skill.id || '—'} · ${reading}${skill.unknown || skill.locked ? '' : ` · +${fmt(skill.power)} poder`}`)}">${skillIconHtml(result, skill)}<span class="skill-copy"><b>Skill ${skill.index + 1}</b></span><input data-skill="${esc(card.id)}" data-skill-index="${skill.index}" type="number" min="0" max="${max}" value="${value ?? ''}" placeholder="?" aria-label="Nível da skill ${skill.index + 1}"></label>`;
    }).join('')}</div><p class="sub skill-source">${source}</p>`;
  }

  function selectedEvolutionNode(saved, root, index) {
    const selected = Number(saved?.nodes?.[index] || 0);
    return root.nodes.find(node => node.id === selected) || null;
  }

  function evolutionSummary(card) {
    const options = window.PalmonPower.evolutionOptions(card);
    if (!options.length) return '<p class="sub">Sem arvore de evolucao cadastrada no APK para esta forma.</p>';
    const active = options.filter(option => card.evolution?.[option.id]?.active).length;
    const configured = options.reduce((total, option) => {
      const saved = card.evolution?.[option.id];
      return total + option.roots.filter((root, index) => (selectedEvolutionNode(saved, root, index)?.stage || 0) > 0).length;
    }, 0);
    return `<div class="evolution-summary"><span>${active}/${options.length} ramos ativos</span><span>${configured} estagios informados</span><span>O poder entra automaticamente no total</span></div>`;
  }

  function evolutionFields(card) {
    const options = window.PalmonPower.evolutionOptions(card);
    if (!options.length) return '<p class="sub">Este Palmon não possui árvore de evolução na tabela do APK.</p>';
    return options.map((evolution, evolutionIndex) => {
      const saved = card.evolution?.[evolution.id] || {};
      const nodes = evolution.roots.map((root, nodeIndex) => {
        const selected = selectedEvolutionNode(saved, root, nodeIndex);
        const choices = [`<option value="" ${selected ? '' : 'selected'}>Não informado</option>`].concat(root.nodes.map(node => `<option value="${node.id}" ${node.id === selected?.id ? 'selected' : ''}>Estágio ${node.stage} · +${fmt(node.power)}</option>`)).join('');
        return `<label class="field">Escolha ${nodeIndex + 1}<select data-evo-node="${esc(card.id)}" data-evo-id="${evolution.id}" data-evo-index="${nodeIndex}" ${saved.active ? '' : 'disabled'}>${choices}</select></label>`;
      }).join('');
      const configured = evolution.roots.filter((root, index) => (selectedEvolutionNode(saved, root, index)?.stage || 0) > 0).length;
      const summary = saved.active ? `Ramo ${evolutionIndex + 1} ativo · ${configured}/${evolution.roots.length} escolhas` : `Ramo ${evolutionIndex + 1} não usado`;
      return `<details class="evolution-group" data-evolution-branch="${esc(card.id)}:${evolution.id}" ${saved.active ? 'open' : ''}><summary>${summary}</summary><div class="evolution-body"><label class="evolution-toggle"><input data-evo-active="${esc(card.id)}" data-evo-id="${evolution.id}" type="checkbox" ${saved.active ? 'checked' : ''}> Usar este ramo no cálculo</label><button class="evolution-clear" type="button" data-evo-clear="${esc(card.id)}" data-evo-id="${evolution.id}">Limpar ramo</button><p class="sub">Marque o ramo somente se ele estiver ativo no jogo. Depois escolha o estágio visível em cada caminho.</p><div class="mini-fields">${nodes}</div></div></details>`;
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

  function starsPicker(card) {
    const selected = Math.max(0, Math.min(5, Number(card.stars) || 0));
    const stars = Array.from({ length: 5 }, (_, index) => {
      const value = index + 1;
      return `<button type="button" class="star-button ${value <= selected ? 'active' : ''}" data-star-card="${esc(card.id)}" data-star-value="${value}" aria-label="Definir ${value} estrelas" title="${value} estrelas">★</button>`;
    }).join('');
    return `<div class="star-field"><span>Estrelas</span><div class="star-controls" role="group" aria-label="Estrelas de ${esc(detail(card).name)}">${stars}</div></div>`;
  }

  function cardHtml(card) {
    const result = calc(card);
    const info = detail(card);
    const stages = formStages(card).map(stage => `<option value="${stage}" ${info.stage === stage ? 'selected' : ''}>${esc(window.PALMON_KNOWLEDGE.stageLabel(stage))}</option>`).join('');
    const path = info.evolutionPath.join(' → ');
    const portrait = info.image ? `<img src="${esc(info.image)}" alt="${esc(info.name)}">` : '<span class="pill">SP</span>';
    return `<article class="pal"><div class="pal-top">${portrait}<div><div class="pal-title"><b>${esc(info.name)}</b><span class="pill">${esc(info.tier)}</span></div><div class="pal-meta">${esc(card.element)} · ${esc(card.role)} · ${esc(info.stageLabel)}</div><div class="pal-meta">${esc(path)}</div><label class="owned"><input data-owned="${esc(card.id)}" type="checkbox" ${card.owned ? 'checked' : ''}> Eu tenho</label></div></div><div class="pal-fields compact-fields"><label class="field">Nível<input data-roster="${esc(card.id)}" data-field="level" type="number" min="1" value="${Number(card.level || 1)}"></label>${starsPicker(card)}<label class="field">Estágio<select data-roster="${esc(card.id)}" data-field="stage">${stages}</select></label><label class="field">Poder no jogo<input data-roster="${esc(card.id)}" data-field="referencePower" inputmode="numeric" value="${esc(card.referencePower || '')}" placeholder="Ex.: 11925180"></label></div><details class="build-details" data-build-details="${esc(card.id)}"><summary>Editar skills, evolução e equipamento</summary><div class="build-block"><b>Skills</b>${skillFields(card, result)}</div><div class="build-block"><b>Evolução</b>${evolutionSummary(card)}<details class="advanced-evolution" data-evolution-details="${esc(card.id)}"><summary>Preencher ramos de evolução</summary><p class="sub">Abra somente os ramos ativos. O painel permanece aberto após cada alteração.</p>${evolutionFields(card)}</details></div><details class="equipment-editor" data-equipment-details="${esc(card.id)}"><summary>Equipamento (opcional)</summary><p class="sub">Preencha quando quiser auditar esse card pela tabela do jogo.</p><div class="gear-grid">${equipmentFields(card)}</div></details></details></article>`;
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
    document.querySelectorAll('[data-star-card]').forEach(button => button.addEventListener('click', () => {
      const card = pal(button.dataset.starCard); const requested = Number(button.dataset.starValue);
      card.stars = Number(card.stars) === requested ? 0 : requested;
      save(true); render();
    }));
    document.querySelectorAll('[data-skill]').forEach(input => input.addEventListener('change', () => {
      const card = pal(input.dataset.skill); card.skills[Number(input.dataset.skillIndex)] = input.value === '' ? null : Number(input.value); card.skillsSource = 'manual'; save(true); render();
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
      card.evolution[id].nodes[index] = input.value === '' ? null : Number(input.value);
      save(true); render();
    }));
    document.querySelectorAll('[data-evo-clear]').forEach(button => button.addEventListener('click', () => {
      const card = pal(button.dataset.evoClear); const id = button.dataset.evoId;
      card.evolution[id] = { active: false, nodes: [] };
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
    const matches = card => isAdvisorRarity(card) && (elementFilter === 'all' || card.element === elementFilter) && `${detail(card).name} ${detail(card).evolutionPath.join(' ')}`.toLowerCase().includes(search);
    const mine = state.roster.filter(card => card.owned && matches(card)).sort((a, b) => effectivePower(b) - effectivePower(a));
    const missing = state.roster.filter(card => !card.owned && matches(card)).sort((a, b) => a.name.localeCompare(b.name));
    $('rosterCount').textContent = `${mine.length} UR/SP no seu elenco · ${missing.length} UR/SP ainda não obtidos`;
    const grid = list => list.length ? `<div class="roster">${list.map(cardHtml).join('')}</div>` : '<div class="empty">Nenhum Palmon neste filtro.</div>';
    $('roster').innerHTML = `<section class="roster-group"><div class="roster-group-head"><h3>Seu elenco</h3><span class="pill">${mine.length}</span></div>${grid(mine)}</section><section class="roster-group missing"><div class="roster-group-head"><h3>Palmon que faltam</h3><span class="pill">${missing.length}</span></div>${grid(missing)}</section>`;
    bindCardEditors();
  }

  function expansionState() {
    return {
      builds: [...document.querySelectorAll('[data-build-details][open]')].map(node => node.dataset.buildDetails),
      editors: [...document.querySelectorAll('[data-evolution-details][open]')].map(node => node.dataset.evolutionDetails),
      branches: [...document.querySelectorAll('[data-evolution-branch][open]')].map(node => node.dataset.evolutionBranch),
      equipment: [...document.querySelectorAll('[data-equipment-details][open]')].map(node => node.dataset.equipmentDetails),
    };
  }

  function restoreExpansion(expanded) {
    const restore = (selector, attribute, values) => document.querySelectorAll(selector).forEach(node => { if (values.includes(node.dataset[attribute])) node.open = true; });
    restore('[data-build-details]', 'buildDetails', expanded.builds);
    restore('[data-evolution-details]', 'evolutionDetails', expanded.editors);
    restore('[data-evolution-branch]', 'evolutionBranch', expanded.branches);
    restore('[data-equipment-details]', 'equipmentDetails', expanded.equipment);
  }

  function render() {
    const expanded = expansionState();
    const scrollTop = window.scrollY;
    renderTeamPicker(); renderAccount(); renderAdvice(); renderFormation(); renderSquadPower(); renderBossAdvisor(); renderRoster();
    restoreExpansion(expanded);
    requestAnimationFrame(() => window.scrollTo({ top: scrollTop }));
  }

  $('teamPick').addEventListener('change', () => { teamIndex = Number($('teamPick').value); render(); });
  $('teamPower').addEventListener('input', () => {
    currentTeam().power = $('teamPower').value;
    if (parsePower(currentTeam().power)) {
      currentTeam().powerLineupSignature = lineupSignature();
      currentTeam().powerReferenceState = 'current';
      captureCalibration();
    } else {
      currentTeam().powerLineupSignature = '';
      currentTeam().powerReferenceState = '';
    }
    save(true);
    renderAdvice();
    renderSquadPower();
  });
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
  $('exportProfileMd').addEventListener('click', () => {
    const blob = new Blob([profileMarkdown(state)], { type: 'text/markdown;charset=utf-8' });
    const link = document.createElement('a'); link.href = URL.createObjectURL(blob); link.download = 'perfil-palmon-importavel.md'; link.click(); URL.revokeObjectURL(link.href); toast('Perfil exportado em Markdown importável.');
  });
  $('importProfile').addEventListener('change', event => {
    const file = event.target.files?.[0]; if (!file) return;
    const reader = new FileReader();
    reader.onload = () => { try { state = hydrate(parseProfileFile(reader.result)); teamIndex = 0; save(true); render(); toast('Perfil importado.'); } catch (_) { toast('Esse arquivo não é um perfil válido.'); } };
    reader.readAsText(file); event.target.value = '';
  });
  $('resetProfile').addEventListener('click', () => { state = hydrate(clone(BASE)); teamIndex = 0; save(true); render(); toast('Snapshot original restaurado.'); });
  render();
})();
