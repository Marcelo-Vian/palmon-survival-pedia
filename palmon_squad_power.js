/* Squad-power math transcribed from LegionData.GetLegionTotalPower in the APK.
 * This module intentionally separates server propertypower from the editable
 * game-power reference used by the profile advisor. */
(() => {
  const RATE = 10000;
  const numeric = value => Number(String(value ?? '').replace(/[^0-9.-]/g, '')) || 0;

  function auraBpsForCount(count) {
    const value = Number(count) || 0;
    if (value >= 7) return 3000;
    if (value >= 6) return 2500;
    if (value >= 5) return 2000;
    if (value >= 4) return 1000;
    if (value >= 3) return 500;
    return 0;
  }

  function auraForElements(elements) {
    const counts = {};
    (elements || []).filter(Boolean).forEach(element => { counts[element] = (counts[element] || 0) + 1; });
    const qualified = Object.entries(counts)
      .map(([element, count]) => ({ element, count, bps: auraBpsForCount(count) }))
      .filter(entry => entry.bps > 0);
    const bps = qualified.reduce((total, entry) => total + entry.bps, 0);
    return { counts, qualified, bps, percent: bps / 100, multiplier: (RATE + bps) / RATE };
  }

  function calculate({ propertyPower = 0, bossPower = 0, armigoPower = 0, jewelPower = 0, auraBps = 0 } = {}) {
    const preAura = Math.max(0, Math.round(numeric(propertyPower)))
      + Math.max(0, Math.round(numeric(bossPower)))
      + Math.max(0, Math.round(numeric(armigoPower)));
    const beforeJewels = Math.ceil(preAura * (RATE + Math.max(0, numeric(auraBps))) / RATE);
    const jewels = Math.max(0, Math.round(numeric(jewelPower)));
    return { preAura, beforeJewels, jewelPower: jewels, total: beforeJewels + jewels };
  }

  function solveCompensatedProperty({ officialPower = 0, bossPower = 0, armigoPower = 0, jewelPower = 0, auraBps = 0 } = {}) {
    const official = Math.max(0, Math.round(numeric(officialPower)));
    const jewels = Math.max(0, Math.round(numeric(jewelPower)));
    const knownPreAura = Math.max(0, Math.round(numeric(bossPower))) + Math.max(0, Math.round(numeric(armigoPower)));
    const targetBeforeJewels = official - jewels;
    const divisor = RATE + Math.max(0, Math.round(numeric(auraBps)));
    if (!official || targetBeforeJewels < 0 || !divisor) return { available: false, value: 0, min: 0, max: 0, total: 0 };

    // ceil(inner * divisor / RATE) === targetBeforeJewels. Keep the full
    // integer interval so the UI can say it is a compensation, not a server value.
    const minInner = Math.floor((targetBeforeJewels - 1) * RATE / divisor) + 1;
    const maxInner = Math.floor(targetBeforeJewels * RATE / divisor);
    const min = Math.max(0, minInner - knownPreAura);
    const max = Math.max(0, maxInner - knownPreAura);
    const value = min;
    const calculated = calculate({ propertyPower: value, bossPower, armigoPower, jewelPower, auraBps });
    return { available: calculated.total === official, value, min, max, total: calculated.total };
  }

  function distributeCompensation(cards, total) {
    const safeCards = (cards || []).filter(Boolean);
    const safeTotal = Math.max(0, Math.round(numeric(total)));
    const referenceTotal = safeCards.reduce((sum, card) => sum + Math.max(0, Math.round(numeric(card.referencePower))), 0);
    let remainder = safeTotal;
    return safeCards.map((card, index) => {
      const amount = index === safeCards.length - 1
        ? remainder
        : referenceTotal
          ? Math.round(safeTotal * Math.max(0, numeric(card.referencePower)) / referenceTotal)
          : Math.floor(safeTotal / Math.max(1, safeCards.length));
      remainder -= amount;
      return { id: card.id, power: Math.max(0, amount) };
    });
  }

  window.PALMON_SQUAD_POWER = { RATE, auraBpsForCount, auraForElements, calculate, solveCompensatedProperty, distributeCompensation };
})();
