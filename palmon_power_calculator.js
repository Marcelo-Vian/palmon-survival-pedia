/* Exact client-side rules extracted from XAPK 0.5.451. */
window.PalmonPower = (() => {
  const source = () => window.PALMON_POWER;
  const number = value => Number(value) || 0;
  const key = value => String(value);

  function resolveHeroId(palmon) {
    if (palmon.gameId && source().heroes[key(palmon.gameId)]) return key(palmon.gameId);
    const code = String(palmon.image || '').match(/_(\d{4})(?:_|\.)/);
    if (!code) return null;
    return Object.keys(source().heroes).find(id => Number(id) % 100000 === Number(code[1])) || null;
  }

  function configForSkill(id, level) {
    const base = number(id);
    if (level === null || level === undefined || level === '') return { id: base, config: null, unknown: true };
    const reported = number(level);
    if (reported <= 0) return { id: base, config: null, locked: true };
    const wanted = Math.max(1, reported);
    for (let offset = wanted - 1; offset >= 0; offset--) {
      const skill = source().skills[key(base + offset)];
      if (skill && number(skill[0]) === wanted) return { id: base + offset, config: skill };
    }
    return { id: base, config: source().skills[key(base)] || null };
  }

  function maxPotencyStage(rootId) {
    let node = source().potencies[key(rootId)];
    let last = rootId;
    while (node && number(node[1]) !== -1) {
      last = number(node[1]);
      node = source().potencies[key(last)];
    }
    return last;
  }

  function potencyPower(rootId, selectedId) {
    let nodeId = number(rootId);
    let node = source().potencies[key(nodeId)];
    const target = number(selectedId) || number(rootId);
    const root = node;
    let total = 0;
    while (node && number(node[2]) <= number(root[3])) {
      if (nodeId > target) break;
      total += number(node[0]);
      if (number(node[1]) === -1) break;
      nodeId = number(node[1]);
      node = source().potencies[key(nodeId)];
    }
    return total;
  }

  function evolutionDetails(hero, palmon) {
    const selected = palmon.evolution || {};
    const evolutionIds = Array.isArray(hero[4]) ? hero[4] : [];
    const breakdown = [];
    let total = 0;
    let configured = !evolutionIds.length;
    evolutionIds.forEach(evolutionId => {
      const evolution = source().evolutions[key(evolutionId)];
      const saved = selected[key(evolutionId)];
      if (!evolution || !saved || saved.active !== true) {
        breakdown.push({ id: evolutionId, power: 0, configured: false });
        return;
      }
      configured = true;
      let value = number(evolution[1]);
      const chosen = saved.nodes || [];
      evolution[2].forEach((rootId, index) => {
        value += potencyPower(rootId, chosen[index]);
      });
      total += value;
      breakdown.push({ id: evolutionId, power: value, configured: true });
    });
    return { total, configured, breakdown };
  }

  function findEquipment(quality, slot) {
    return Object.entries(source().equipment)
      .map(([id, value]) => ({ id, value }))
      .find(item => number(item.value[0]) === number(quality) && number(item.value[1]) === number(slot));
  }

  function findStrength(type, level, fallbackId) {
    const target = Math.max(0, number(level));
    const matching = Object.entries(source().equipmentStrength)
      .map(([id, value]) => ({ id, value }))
      .filter(item => number(item.value[0]) === number(type));
    return matching.find(item => number(item.value[1]) === target)
      || matching.find(item => key(item.id) === key(fallbackId))
      || null;
  }

  function findEquipmentStar(type, stars, fallbackId) {
    const target = Math.max(0, number(stars));
    const matching = Object.entries(source().equipmentStars)
      .map(([id, value]) => ({ id, value }))
      .filter(item => number(item.value[0]) === number(type));
    return matching.find(item => number(item.value[1]) === target)
      || matching.find(item => key(item.id) === key(fallbackId))
      || null;
  }

  function equipmentDetails(hero, palmon) {
    if (!hero[5]) return { total: 0, configured: true, breakdown: [] };
    const slots = palmon.equipment || [];
    const breakdown = [];
    let total = 0;
    let configured = slots.length >= 4;
    for (let slot = 1; slot <= 4; slot++) {
      const item = slots[slot - 1];
      if (!item || item.quality === undefined || item.quality === null) {
        configured = false;
        breakdown.push({ slot, power: 0, configured: false });
        continue;
      }
      if (number(item.quality) === 0) {
        breakdown.push({ slot, power: 0, configured: true });
        continue;
      }
      const equipment = findEquipment(item.quality, slot);
      if (!equipment) {
        configured = false;
        breakdown.push({ slot, power: 0, configured: false });
        continue;
      }
      const strength = findStrength(equipment.value[2], item.level, equipment.value[3]);
      const star = findEquipmentStar(equipment.value[2], item.stars, equipment.value[4]);
      if (!strength || !star) {
        configured = false;
        breakdown.push({ slot, power: 0, configured: false });
        continue;
      }
      const power = Math.floor((number(equipment.value[5]) + number(strength.value[2])) * (1 + number(star.value[2]) / 10000) + number(star.value[3]));
      total += power;
      breakdown.push({ slot, power, configured: true, quality: number(item.quality), level: number(strength.value[1]), stars: number(star.value[1]) });
    }
    return { total, configured, breakdown };
  }

  function calculate(palmon) {
    const heroId = resolveHeroId(palmon);
    const hero = heroId && source().heroes[heroId];
    if (!hero) return { available: false, total: 0, missing: ['Palmon sem ID confirmado no APK.'], components: {} };

    const levelPower = number(source().levels[`${hero[1]}:${number(palmon.level)}`]);
    const starPower = number(source().stars[`${hero[2]}:${number(palmon.stars)}`]);
    const skillLevels = palmon.skills || [];
    const skills = hero[3].map((skillId, index) => {
      const resolved = configForSkill(skillId, skillLevels[index]);
      return { index, id: resolved.id, reported: skillLevels[index], level: resolved.config ? resolved.config[0] : (resolved.locked ? 0 : null), max: resolved.config ? resolved.config[1] : 0, power: number(resolved.config?.[2]), unknown: !!resolved.unknown, locked: !!resolved.locked };
    });
    const skillPower = skills.reduce((total, skill) => total + skill.power, 0);
    const evolution = evolutionDetails(hero, palmon);
    const equipment = equipmentDetails(hero, palmon);
    const missing = [];
    if (!levelPower) missing.push('nível fora da curva do APK');
    if (!starPower && number(palmon.stars) > 0) missing.push('estrela fora da curva do APK');
    const skillsRead = skillLevels.length === hero[3].length && skillLevels.every(level => level !== null && level !== undefined && level !== '' && Number.isInteger(Number(level)) && Number(level) >= 0);
    if (!skillsRead) missing.push('níveis das skills');
    if (!evolution.configured) missing.push('progresso de evolução');
    if (!equipment.configured) missing.push('equipamentos');
    const components = { base: number(hero[0]), level: levelPower, stars: starPower, skills: skillPower, evolution: evolution.total, equipment: equipment.total };
    return {
      available: true,
      heroId,
      total: Object.values(components).reduce((total, value) => total + value, 0),
      exact: missing.length === 0,
      missing,
      components,
      skills,
      evolution,
      equipment,
    };
  }

  function defaults(palmon) {
    const heroId = resolveHeroId(palmon);
    const hero = heroId && source().heroes[heroId];
    if (!hero) return palmon;
    const skills = Array.isArray(palmon.skills) && palmon.skills.length === hero[3].length ? palmon.skills : hero[3].map(() => null);
    const equipment = Array.isArray(palmon.equipment) && palmon.equipment.length === 4 ? palmon.equipment : [null, null, null, null];
    return { ...palmon, gameId: number(heroId), skills, equipment, evolution: palmon.evolution || {} };
  }

  function evolutionOptions(palmon) {
    const heroId = resolveHeroId(palmon);
    const hero = heroId && source().heroes[heroId];
    if (!hero) return [];
    const evolutionIds = Array.isArray(hero[4]) ? hero[4] : [];
    return evolutionIds.map(evolutionId => {
      const evolution = source().evolutions[key(evolutionId)];
      return {
        id: evolutionId,
        roots: (evolution?.[2] || []).map(rootId => {
          const nodes = [];
          let id = number(rootId);
          while (id > 0) {
            const potency = source().potencies[key(id)];
            if (!potency) break;
            nodes.push({ id, stage: number(potency[2]), power: number(potency[0]) });
            if (number(potency[1]) === -1) break;
            id = number(potency[1]);
          }
          return { rootId, nodes };
        }),
      };
    });
  }

  return { calculate, defaults, evolutionOptions, maxPotencyStage, resolveHeroId };
})();
