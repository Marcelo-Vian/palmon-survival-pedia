(function () {
  const SKILLS = [
    { key: "b_supply_drop", cls: "builder", unlock: 1, pos: 1, max: 5, color: "orange", type: "Ativa", name: "Supply Drop", group: "Recursos", effect: "No max: recebe Gold, Lumber, Steel e Electricity iguais a 20h da produção do Camp. CD 23,5h.", scores: { growth: 66, balanced: 62, combat: 24, map: 38 } },
    { key: "b_amity_boost", cls: "builder", unlock: 1, pos: 2, max: 1, color: "orange", type: "Passiva", name: "Amity Boost", group: "Guilda", effect: "No max: +100% Guild Amity ao doar tecnologia e ajudar aliados.", scores: { growth: 78, balanced: 74, combat: 42, map: 72 } },
    { key: "b_wildborn", cls: "builder", unlock: 1, pos: 3, max: 3, color: "green", type: "Passiva", name: "Wildborn", group: "XP", effect: "No max: +60% Explorer XP ao derrotar Bullymon/Wild Palmon.", scores: { growth: 98, balanced: 96, combat: 64, map: 82 } },
    { key: "b_bonus_ap", cls: "builder", unlock: 5, pos: 1, max: 1, color: "orange", type: "Passiva", name: "Bonus AP", group: "Energia", effect: "No max: +50% AP diario gratis.", scores: { growth: 82, balanced: 78, combat: 48, map: 66 } },
    { key: "b_treasure_hunter", cls: "builder", unlock: 5, pos: 2, max: 5, color: "orange", type: "Passiva", name: "Treasure Hunter", group: "Recursos", effect: "No max: +50% recursos ao derrotar Wild Palmon.", scores: { growth: 72, balanced: 68, combat: 36, map: 54 } },
    { key: "b_builder_instincts", cls: "builder", unlock: 5, pos: 3, max: 3, color: "green", type: "Passiva", name: "Builder Instincts", group: "XP", effect: "No max: +15% Explorer XP ao upar construcoes da season.", scores: { growth: 96, balanced: 94, combat: 58, map: 78 } },
    { key: "b_builders_passion", cls: "builder", unlock: 10, pos: 1, max: 5, color: "orange", type: "Passiva", name: "Builder's Passion", group: "Construcao", effect: "No max: +180 min na duracao do Free Building Speedup.", scores: { growth: 100, balanced: 92, combat: 24, map: 55 } },
    { key: "b_scholarly_passion", cls: "builder", unlock: 10, pos: 2, max: 5, color: "orange", type: "Passiva", name: "Scholarly Passion", group: "Pesquisa", effect: "No max: +180 min na duracao do Free Research Speedup.", scores: { growth: 100, balanced: 92, combat: 24, map: 55 } },
    { key: "b_resource_swap", cls: "builder", unlock: 10, pos: 3, max: 3, color: "green", type: "Ativa", name: "Resource Swap", group: "Recursos", effect: "No max: troca recursos sazonais 2:1, gastando 15.000 para receber metade do outro. CD 47,5h.", scores: { growth: 40, balanced: 42, combat: 24, map: 38 } },
    { key: "b_instant_build", cls: "builder", unlock: 15, pos: 1, max: 5, color: "orange", type: "Ativa", name: "Instant Build", group: "Construcao", effect: "No max: reduz 600 min de todas as filas de construcao. CD 47,5h.", scores: { growth: 99, balanced: 94, combat: 26, map: 58 } },
    { key: "b_instant_research", cls: "builder", unlock: 15, pos: 2, max: 5, color: "orange", type: "Ativa", name: "Instant Research", group: "Pesquisa", effect: "No max: reduz 600 min de todas as filas de pesquisa. CD 47,5h.", scores: { growth: 99, balanced: 94, combat: 26, map: 58 } },
    { key: "b_medal_valor", cls: "builder", unlock: 15, pos: 3, max: 1, color: "green", type: "Passiva", name: "Medal of Valor", group: "XP", effect: "No max: +20% Explorer XP ao participar de Sanctum Sieges.", scores: { growth: 86, balanced: 88, combat: 76, map: 90 } },
    { key: "b_fleet_footed", cls: "builder", unlock: 20, pos: 1, max: 5, color: "orange", type: "Passiva", name: "Fleet-footed", group: "Marcha", effect: "No max: +50% March Speed ao entrar ou voltar de rally.", scores: { growth: 28, balanced: 40, combat: 54, map: 46 } },
    { key: "b_spoils_war", cls: "builder", unlock: 20, pos: 2, max: 5, color: "orange", type: "Passiva", name: "Spoils of War", group: "Raid", effect: "No max: +50% limite de recursos saqueados de Camps inimigos.", scores: { growth: 32, balanced: 44, combat: 58, map: 50 } },
    { key: "b_warrior_instincts", cls: "builder", unlock: 25, pos: 1, max: 3, color: "orange", type: "Passiva", name: "Warrior Instincts", group: "XP", effect: "No max: +60% Explorer XP ao ocupar Sanctums.", scores: { growth: 86, balanced: 88, combat: 78, map: 92 } },
    { key: "b_protector_banner", cls: "builder", unlock: 25, pos: 2, max: 5, color: "orange", type: "Passiva", name: "Protector Banner", group: "Defesa guilda", effect: "No max: reduz em 25% a taxa de ferimento grave de Armigo ao proteger camp aliado.", scores: { growth: 36, balanced: 50, combat: 68, map: 72 } },
    { key: "b_xp_overload", cls: "builder", unlock: 25, pos: 3, max: 5, color: "green", type: "Ativa", name: "XP Overload", group: "XP", effect: "No max: recebe 10% da XP requerida do level atual, ate 100.000 XP. CD 23,5h.", scores: { growth: 94, balanced: 92, combat: 70, map: 86 } },
    { key: "b_construction_aid", cls: "builder", unlock: 30, pos: 1, max: 2, color: "orange", type: "Ativa", name: "Construction Aid", group: "Guilda", effect: "No max: +20% velocidade de construcao por 60 min para voce e um aliado. CD 23,5h.", scores: { growth: 88, balanced: 82, combat: 42, map: 70 } },
    { key: "b_research_aid", cls: "builder", unlock: 30, pos: 2, max: 2, color: "orange", type: "Ativa", name: "Research Aid", group: "Guilda", effect: "No max: +20% velocidade de pesquisa por 60 min para voce e um aliado. CD 23,5h.", scores: { growth: 88, balanced: 82, combat: 42, map: 70 } },
    { key: "b_holy_radiance", cls: "builder", unlock: 30, pos: 3, max: 5, color: "green", type: "Passiva", name: "Holy Radiance", group: "Mapa S2", effect: "No max: Holy Tower reduz Curse Level em 100 quando Empower Mode esta ligado.", scores: { growth: 34, balanced: 56, combat: 58, map: 96 } },
    { key: "b_cost_cutter", cls: "builder", unlock: 35, pos: 1, max: 5, color: "orange", type: "Passiva", name: "Cost Cutter", group: "Economia", effect: "No max: -5% custo de recursos em upgrades de construcao.", scores: { growth: 92, balanced: 86, combat: 26, map: 58 } },
    { key: "b_thrifty_science", cls: "builder", unlock: 35, pos: 2, max: 5, color: "orange", type: "Passiva", name: "Thrifty Science", group: "Economia", effect: "No max: -5% custo de recursos em pesquisa.", scores: { growth: 92, balanced: 86, combat: 26, map: 58 } },
    { key: "b_sacred_blessing", cls: "builder", unlock: 35, pos: 3, max: 1, color: "green", type: "Passiva", name: "Sacred Blessing", group: "Mapa S2", effect: "No max: +100% eficiencia ao enviar Blessings.", scores: { growth: 36, balanced: 58, combat: 54, map: 94 } },
    { key: "b_medical_aid", cls: "builder", unlock: 40, pos: 1, max: 5, color: "orange", type: "Ativa", name: "Medical Aid", group: "Hospital", effect: "No max: +50% capacidade do Hospital por 240 min para voce e aliado. CD 71,5h.", scores: { growth: 36, balanced: 52, combat: 68, map: 70 } },
    { key: "b_guardian_shield", cls: "builder", unlock: 40, pos: 2, max: 3, color: "orange", type: "Ativa", name: "Guardian Shield", group: "Defesa", effect: "No max: concede shield de 3h para voce ou aliado. CD 71,5h.", scores: { growth: 34, balanced: 58, combat: 72, map: 74 } },
    { key: "b_umbra_batfire", cls: "builder", unlock: 40, pos: 3, max: 5, color: "green", type: "Ativa", name: "Umbra Batfire", group: "Mapa S2", effect: "No max: +250 Curse Level em Camps inimigos na area por 10 min. CD 47,5h.", scores: { growth: 24, balanced: 52, combat: 68, map: 98 } },
    { key: "b_class_rewards", cls: "builder", unlock: 45, pos: 1, max: 5, color: "orange", type: "Ativa", name: "Class Rewards", group: "Recompensa", effect: "No max: recompensa Builder nivel 5. CD 23,5h.", scores: { growth: 56, balanced: 60, combat: 34, map: 52 } },
    { key: "b_defensive_tactics", cls: "builder", unlock: 45, pos: 2, max: 5, color: "orange", type: "Passiva", name: "Defensive Tactics", group: "Defesa Palmon", effect: "No max: Palmons ganham +5% ATK, DEF e HP defendendo Camp.", scores: { growth: 38, balanced: 62, combat: 82, map: 74 } },
    { key: "b_gift_life", cls: "builder", unlock: 50, pos: 1, max: 5, color: "orange", type: "Ativa", name: "Gift of Life", group: "Recompensa", effect: "No max: recebe Wreath Chest x5. CD 119,5h.", scores: { growth: 48, balanced: 50, combat: 30, map: 46 } },
    { key: "b_scorched_pepper", cls: "builder", unlock: 50, pos: 2, max: 5, color: "orange", type: "Ativa", name: "Scorched Pepper", group: "Mapa", effect: "No max: armadilha reduz Durability do Camp inimigo e desloca o Camp. Dura 24h, CD 72h.", scores: { growth: 22, balanced: 42, combat: 64, map: 86 } },
    { key: "b_lost_wraith", cls: "builder", unlock: 50, pos: 3, max: 1, color: "green", type: "Ativa", name: "Lost Wraith", group: "Mapa S2", effect: "No max: armadilha aumenta Curse Level em 50 e corrompe o Camp inimigo. Dura 24h, CD 24h.", scores: { growth: 24, balanced: 48, combat: 66, map: 92 } },
    { key: "b_activity_perk", cls: "builder", unlock: 55, pos: 1, max: 5, color: "green", type: "Passiva", name: "Activity Perk", group: "Diarias", effect: "No max: 25% de chance de dobrar recompensa de daily quest.", scores: { growth: 84, balanced: 78, combat: 34, map: 62 } },
    { key: "b_aid_boost", cls: "builder", unlock: 55, pos: 2, max: 5, color: "green", type: "Passiva", name: "Aid Boost", group: "Guilda", effect: "No max: ajudas reduzem +150s de fila.", scores: { growth: 86, balanced: 80, combat: 36, map: 72 } },
    { key: "b_fast_harvest", cls: "builder", unlock: 60, pos: 1, max: 5, color: "green", type: "Passiva", name: "Fast Harvest", group: "Coleta", effect: "No max: +25% velocidade de coleta.", scores: { growth: 82, balanced: 74, combat: 24, map: 52 } },
    { key: "b_emergency_care", cls: "builder", unlock: 60, pos: 2, max: 5, color: "green", type: "Passiva", name: "Emergency Care", group: "Guerra", effect: "No max: -20% taxa de morte de Armigo em combate.", scores: { growth: 42, balanced: 66, combat: 84, map: 80 } },
    { key: "b_enhanced_purification", cls: "builder", unlock: 65, pos: 1, max: 5, color: "green", type: "Passiva", name: "Enhanced Purification", group: "Mapa S2", effect: "No max: +50% efeito de remover corrupcao.", scores: { growth: 40, balanced: 62, combat: 62, map: 92 } },
    { key: "b_master_builder", cls: "builder", unlock: 65, pos: 2, max: 5, color: "green", type: "Passiva", name: "Master Builder", group: "Construcao", effect: "No max: +25% velocidade de construcao.", scores: { growth: 96, balanced: 88, combat: 28, map: 64 } },
    { key: "b_instant_harvest", cls: "builder", unlock: 70, pos: 1, max: 1, color: "green", type: "Ativa", name: "Instant Harvest", group: "Coleta", effect: "Coleta instantaneamente o restante dos nodes ate o limite de carga. CD 119,5h.", scores: { growth: 82, balanced: 76, combat: 24, map: 56 } },
    { key: "b_swift_hunt", cls: "builder", unlock: 70, pos: 2, max: 5, color: "green", type: "Passiva", name: "Swift Hunt", group: "Farm", effect: "No max: +25% March Speed contra NPC.", scores: { growth: 78, balanced: 74, combat: 42, map: 58 } },

    { key: "f_home_beacon", cls: "fighter", unlock: 1, pos: 1, max: 5, color: "orange", type: "Passiva", name: "Home Beacon", group: "Mobilidade", effect: "No max: ao mover Camp, squads despachados retornam; 5 usos por dia.", scores: { growth: 34, balanced: 52, combat: 56, map: 64 } },
    { key: "f_strength_numbers", cls: "fighter", unlock: 1, pos: 2, max: 5, color: "orange", type: "Ativa", name: "Strength in Numbers", group: "Armigo", effect: "No max: recebe 250 Armigo sem passar a capacidade da Hut. CD 23,5h.", scores: { growth: 45, balanced: 62, combat: 70, map: 62 } },
    { key: "f_wildborn", cls: "fighter", unlock: 1, pos: 3, max: 3, color: "green", type: "Passiva", name: "Wildborn", group: "XP", effect: "No max: +60% Explorer XP ao derrotar Bullymon/Wild Palmon.", scores: { growth: 98, balanced: 90, combat: 66, map: 78 } },
    { key: "f_more_merrier", cls: "fighter", unlock: 5, pos: 1, max: 5, color: "orange", type: "Passiva", name: "The More the Merrier", group: "Armigo", effect: "No max: +10% capacidade da Armigo Hut.", scores: { growth: 48, balanced: 64, combat: 74, map: 68 } },
    { key: "f_hospital_wing", cls: "fighter", unlock: 5, pos: 2, max: 5, color: "orange", type: "Passiva", name: "Hospital Wing", group: "Hospital", effect: "No max: +10% capacidade do Hospital.", scores: { growth: 45, balanced: 64, combat: 72, map: 68 } },
    { key: "f_builder_instincts", cls: "fighter", unlock: 5, pos: 3, max: 3, color: "green", type: "Passiva", name: "Builder Instincts", group: "XP", effect: "No max: +15% Explorer XP ao upar construcoes da season.", scores: { growth: 96, balanced: 88, combat: 58, map: 74 } },
    { key: "f_morale_boost", cls: "fighter", unlock: 10, pos: 1, max: 5, color: "orange", type: "Passiva", name: "Morale Boost", group: "Dano", effect: "No max: +5% dano enquanto esta em Frenzy.", scores: { growth: 54, balanced: 88, combat: 99, map: 78 } },
    { key: "f_healing_fruit", cls: "fighter", unlock: 10, pos: 2, max: 5, color: "orange", type: "Ativa", name: "Healing Fruit", group: "Cura", effect: "No max: cura instantaneamente ate 5.000 Armigo feridos fora da fila. CD 71,5h.", scores: { growth: 36, balanced: 58, combat: 68, map: 66 } },
    { key: "f_resource_swap", cls: "fighter", unlock: 10, pos: 3, max: 3, color: "green", type: "Ativa", name: "Resource Swap", group: "Recursos", effect: "No max: troca recursos sazonais 2:1, gastando 15.000 para receber metade do outro. CD 47,5h.", scores: { growth: 38, balanced: 42, combat: 28, map: 38 } },
    { key: "f_breach_point", cls: "fighter", unlock: 15, pos: 1, max: 5, color: "orange", type: "Passiva", name: "Breach Point", group: "Ataque Camp", effect: "No max: ao atacar Camp danificado, +5% taxa de ferimento grave dos Armigo inimigos.", scores: { growth: 28, balanced: 70, combat: 86, map: 76 } },
    { key: "f_intensive_training", cls: "fighter", unlock: 15, pos: 2, max: 5, color: "orange", type: "Passiva", name: "Intensive Training", group: "Treino", effect: "No max: +25% velocidade de treino de Armigo.", scores: { growth: 56, balanced: 64, combat: 68, map: 58 } },
    { key: "f_medal_valor", cls: "fighter", unlock: 15, pos: 3, max: 1, color: "green", type: "Passiva", name: "Medal of Valor", group: "XP", effect: "No max: +20% Explorer XP ao participar de Sanctum Sieges.", scores: { growth: 86, balanced: 88, combat: 78, map: 92 } },
    { key: "f_desolate_march", cls: "fighter", unlock: 20, pos: 1, max: 2, color: "orange", type: "Passiva", name: "Desolate March", group: "Temple", effect: "No max: +50% March Speed no Desolate Lands durante Temple Challenge.", scores: { growth: 36, balanced: 54, combat: 62, map: 68 } },
    { key: "f_spoils_war", cls: "fighter", unlock: 20, pos: 2, max: 5, color: "orange", type: "Passiva", name: "Spoils of War", group: "Raid", effect: "No max: +50% limite de recursos saqueados de Camps inimigos.", scores: { growth: 38, balanced: 58, combat: 66, map: 58 } },
    { key: "f_warrior_instincts", cls: "fighter", unlock: 25, pos: 1, max: 3, color: "orange", type: "Passiva", name: "Warrior Instincts", group: "XP", effect: "No max: +60% Explorer XP ao ocupar Sanctums.", scores: { growth: 86, balanced: 88, combat: 78, map: 94 } },
    { key: "f_swift_banner", cls: "fighter", unlock: 25, pos: 2, max: 5, color: "orange", type: "Passiva", name: "Swift Banner", group: "Reforco", effect: "No max: ao reforcar aliado, +50% March Speed dele.", scores: { growth: 30, balanced: 56, combat: 62, map: 72 } },
    { key: "f_xp_overload", cls: "fighter", unlock: 25, pos: 3, max: 5, color: "green", type: "Ativa", name: "XP Overload", group: "XP", effect: "No max: recebe 10% da XP requerida do level atual, ate 100.000 XP. CD 23,5h.", scores: { growth: 94, balanced: 90, combat: 70, map: 86 } },
    { key: "f_fierce_assault", cls: "fighter", unlock: 30, pos: 1, max: 5, color: "orange", type: "Passiva", name: "Fierce Assault", group: "Rally", effect: "No max: +5% Attack do squad ao iniciar ou entrar em rally.", scores: { growth: 38, balanced: 86, combat: 97, map: 82 } },
    { key: "f_chameleon", cls: "fighter", unlock: 30, pos: 2, max: 1, color: "orange", type: "Ativa", name: "Chameleon", group: "PvP", effect: "Camufla a proxima batalha PvP: detalhes escondidos e sem battle report. CD 47,5h.", scores: { growth: 20, balanced: 54, combat: 68, map: 76 } },
    { key: "f_holy_radiance", cls: "fighter", unlock: 30, pos: 3, max: 5, color: "green", type: "Passiva", name: "Holy Radiance", group: "Mapa S2", effect: "No max: Holy Tower reduz Curse Level em 100 quando Empower Mode esta ligado.", scores: { growth: 34, balanced: 58, combat: 62, map: 96 } },
    { key: "f_ominous_banner", cls: "fighter", unlock: 35, pos: 1, max: 5, color: "orange", type: "Passiva", name: "Ominous Banner", group: "Defesa guilda", effect: "No max: ao proteger camp aliado, +5% taxa de morte dos Armigo atacantes.", scores: { growth: 24, balanced: 70, combat: 84, map: 82 } },
    { key: "f_valiant_banner", cls: "fighter", unlock: 35, pos: 2, max: 5, color: "orange", type: "Passiva", name: "Valiant Banner", group: "Defesa guilda", effect: "No max: +5% ATK, DEF e HP do squad ao defender camp aliado.", scores: { growth: 28, balanced: 74, combat: 86, map: 82 } },
    { key: "f_sacred_blessing", cls: "fighter", unlock: 35, pos: 3, max: 1, color: "green", type: "Passiva", name: "Sacred Blessing", group: "Mapa S2", effect: "No max: +100% eficiencia ao enviar Blessings.", scores: { growth: 36, balanced: 58, combat: 58, map: 94 } },
    { key: "f_defensive_tactics", cls: "fighter", unlock: 40, pos: 1, max: 5, color: "orange", type: "Passiva", name: "Defensive Tactics", group: "Defesa Palmon", effect: "No max: Palmons ganham +5% ATK, DEF e HP defendendo Camp.", scores: { growth: 34, balanced: 86, combat: 92, map: 80 } },
    { key: "f_cheerleader", cls: "fighter", unlock: 40, pos: 2, max: 1, color: "orange", type: "Ativa", name: "Cheerleader", group: "Buff mapa", effect: "No max: Kilohopp concede +2% Attack por 30 min a voce e guildmates na area. CD 71,5h.", scores: { growth: 22, balanced: 72, combat: 84, map: 88 } },
    { key: "f_umbra_batfire", cls: "fighter", unlock: 40, pos: 3, max: 5, color: "green", type: "Ativa", name: "Umbra Batfire", group: "Mapa S2", effect: "No max: +250 Curse Level em Camps inimigos na area por 10 min. CD 47,5h.", scores: { growth: 24, balanced: 54, combat: 72, map: 98 } },
    { key: "f_class_rewards", cls: "fighter", unlock: 45, pos: 1, max: 5, color: "orange", type: "Ativa", name: "Class Rewards", group: "Recompensa", effect: "No max: recompensa Fighter nivel 5. CD 23,5h.", scores: { growth: 48, balanced: 54, combat: 48, map: 50 } },
    { key: "f_rallying_cry", cls: "fighter", unlock: 45, pos: 2, max: 5, color: "orange", type: "Passiva", name: "Rallying Cry", group: "Rally", effect: "No max: em rallies PvP, reduz morte de Armigo em 5% para todos os squads.", scores: { growth: 28, balanced: 84, combat: 91, map: 82 } },
    { key: "f_offensive_tactics", cls: "fighter", unlock: 50, pos: 1, max: 5, color: "orange", type: "Passiva", name: "Offensive Tactics", group: "Ataque Palmon", effect: "No max: +5% ATK, DEF e HP dos Palmons atacando Camp inimigo.", scores: { growth: 26, balanced: 90, combat: 100, map: 84 } },
    { key: "f_stink_bomb", cls: "fighter", unlock: 50, pos: 2, max: 5, color: "orange", type: "Ativa", name: "Stink Bomb", group: "Mapa", effect: "No max: armadilha mata 250 Armigo na Hut inimiga. Dura 24h, CD 72h.", scores: { growth: 18, balanced: 50, combat: 72, map: 88 } },
    { key: "f_lost_wraith", cls: "fighter", unlock: 50, pos: 3, max: 1, color: "green", type: "Ativa", name: "Lost Wraith", group: "Mapa S2", effect: "No max: armadilha aumenta Curse Level em 50 e corrompe o Camp inimigo. Dura 24h, CD 24h.", scores: { growth: 24, balanced: 50, combat: 66, map: 92 } },
    { key: "f_hyper_frenzy", cls: "fighter", unlock: 55, pos: 1, max: 5, color: "green", type: "Passiva", name: "Hyper Frenzy", group: "Dano S2", effect: "No max: +5 min de cap de Frenzy e +5% Palmon Attack em Frenzy. Requer Morale Boost 5/5.", prereq: { key: "f_morale_boost", points: 5 }, scores: { growth: 30, balanced: 92, combat: 99, map: 86 } },
    { key: "f_lethal_strike", cls: "fighter", unlock: 55, pos: 2, max: 5, color: "green", type: "Passiva", name: "Lethal Strike", group: "Rally", effect: "No max: em rally PvP, +5% taxa de ferimento grave nos Armigo inimigos.", scores: { growth: 22, balanced: 80, combat: 94, map: 84 } },
    { key: "f_shield_wall", cls: "fighter", unlock: 60, pos: 1, max: 5, color: "green", type: "Passiva", name: "Shield Wall", group: "Defesa Palmon", effect: "No max: +5% reducao de dano dos Palmons.", scores: { growth: 24, balanced: 88, combat: 96, map: 82 } },
    { key: "f_precision_training", cls: "fighter", unlock: 60, pos: 2, max: 5, color: "green", type: "Passiva", name: "Precision Training", group: "Economia militar", effect: "No max: -5% custo de recurso para treinar Armigo.", scores: { growth: 54, balanced: 62, combat: 66, map: 58 } },
    { key: "f_desert_edge", cls: "fighter", unlock: 65, pos: 1, max: 5, color: "green", type: "Passiva", name: "Desert Edge", group: "Dano S2", effect: "No max: +5% Palmon Attack em batalhas de deserto.", scores: { growth: 22, balanced: 78, combat: 90, map: 78 } },
    { key: "f_expert_cheerer", cls: "fighter", unlock: 65, pos: 2, max: 1, color: "green", type: "Passiva", name: "Expert Cheerer", group: "Buff mapa", effect: "No max: Cheerleader tambem concede +3% Defense. Requer Cheerleader 1/1.", prereq: { key: "f_cheerleader", points: 1 }, scores: { growth: 18, balanced: 72, combat: 82, map: 86 } },
    { key: "f_shelled_armor", cls: "fighter", unlock: 70, pos: 1, max: 5, color: "green", type: "Passiva", name: "Shelled Armor", group: "Anti-critico", effect: "No max: +5% Tenacity dos Palmons.", scores: { growth: 18, balanced: 82, combat: 90, map: 78 } },
    { key: "f_furious_frenzy", cls: "fighter", unlock: 70, pos: 2, max: 1, color: "green", type: "Ativa", name: "Furious Frenzy", group: "Frenzy", effect: "Aplica 3 min de Frenzy em alvo sem shield, max 15 min. CD 71,5h.", scores: { growth: 18, balanced: 78, combat: 88, map: 80 } }
  ];

  const POS = { 1: "esquerda", 2: "meio", 3: "direita" };
  const GOAL_LABEL = {
    growth: "crescimento/F2P/base",
    balanced: "equilibrado",
    combat: "combate/PvP/rally",
    map: "mapa S2"
  };
  const CLASS_LABEL = { builder: "Builder", fighter: "Fighter" };
  const OMITTED_S1 = { builder: 4, fighter: 4 };

  function score(skill, goal) {
    return (skill.scores && (skill.scores[goal] ?? skill.scores.balanced)) || 1;
  }

  function prereqMet(skill, assigned) {
    if (!skill.prereq) return true;
    return (assigned[skill.prereq.key] || 0) >= skill.prereq.points;
  }

  function allocate(eligible, points, goal) {
    const assigned = {};
    let remaining = points;
    const order = [...eligible].sort((a, b) => {
      const diff = score(b, goal) - score(a, goal);
      if (diff) return diff;
      if (a.unlock !== b.unlock) return a.unlock - b.unlock;
      if (a.max !== b.max) return a.max - b.max;
      return a.pos - b.pos;
    });

    let changed = true;
    while (remaining > 0 && changed) {
      changed = false;
      for (const skill of order) {
        if (remaining <= 0) break;
        if (!prereqMet(skill, assigned)) continue;
        const current = assigned[skill.key] || 0;
        if (current >= skill.max) continue;
        const put = Math.min(skill.max - current, remaining);
        assigned[skill.key] = current + put;
        remaining -= put;
        changed = true;
      }
    }

    return { assigned, remaining, order };
  }

  function decision(skill, put, goal, remaining, assigned) {
    const s = score(skill, goal);
    if (put >= skill.max) return "Fechar: alta prioridade para este objetivo.";
    if (put > 0) return "Parcial: recebeu ponto, mas faltou ponto para fechar.";
    if (skill.prereq && !prereqMet(skill, assigned)) return "Bloqueada por pre-requisito.";
    if (s >= 80) return "Boa, mas ficou sem ponto nesta simulacao.";
    if (s >= 60) return "Media: entra depois das prioridades principais.";
    return "Situacional: use so se esse efeito for seu gargalo atual.";
  }

  function runPlanner() {
    const cls = document.getElementById("classPlannerClass")?.value || "builder";
    const goal = document.getElementById("classPlannerGoal")?.value || "growth";
    const level = Math.max(1, Math.min(70, Number(document.getElementById("classPlannerLevel")?.value || 1)));
    const points = Math.max(0, Math.min(140, Number(document.getElementById("classPlannerPoints")?.value || 0)));
    const rows = document.getElementById("classPlannerRows");
    const summary = document.getElementById("classPlannerSummary");
    const warning = document.getElementById("classPlannerWarning");
    const next = document.getElementById("classPlannerNext");
    if (!rows || !summary || !warning || !next) return;

    const eligible = SKILLS.filter((skill) => skill.cls === cls && skill.unlock <= level);
    const locked = SKILLS.filter((skill) => skill.cls === cls && skill.unlock > level).sort((a, b) => a.unlock - b.unlock || a.pos - b.pos);
    const { assigned, remaining, order } = allocate(eligible, points, goal);
    const used = points - remaining;
    const green = eligible.filter((skill) => skill.color === "green").length;
    const orange = eligible.filter((skill) => skill.color === "orange").length;

    const sortedByTree = [...eligible].sort((a, b) => a.unlock - b.unlock || a.pos - b.pos || a.name.localeCompare(b.name));
    rows.innerHTML = sortedByTree.map((skill) => {
      const put = assigned[skill.key] || 0;
      const rowClass = put ? "" : " class=\"planner-row-zero\"";
      const colorLabel = skill.color === "green" ? "Verde/S2" : "Amarela";
      return `<tr${rowClass}>
        <td><span class="planner-lv">Lv ${skill.unlock}</span></td>
        <td><span class="planner-pos">${POS[skill.pos] || skill.pos}</span></td>
        <td><span class="planner-color ${skill.color}">${colorLabel}</span></td>
        <td><b>${skill.name}</b><span class="planner-priority">${skill.type} · ${skill.group}</span><span class="planner-effect">${skill.effect}</span></td>
        <td><b>${put}/${skill.max}</b></td>
        <td>${decision(skill, put, goal, remaining, assigned)}<span class="planner-priority">Score ${score(skill, goal)} no objetivo ${GOAL_LABEL[goal]}.</span></td>
      </tr>`;
    }).join("") || "<tr><td colspan=\"6\">Coloque level e pontos para gerar a distribuicao.</td></tr>";

    const lv1 = sortedByTree.filter((skill) => skill.unlock === 1).map((skill) => `${skill.name} ${assigned[skill.key] || 0}/${skill.max}`).join(" · ");
    const nextUnfinished = order.find((skill) => prereqMet(skill, assigned) && (assigned[skill.key] || 0) < skill.max);
    const nextLocked = locked[0];

    summary.innerHTML = `<b>${CLASS_LABEL[cls]} · objetivo ${GOAL_LABEL[goal]}</b><br>
      Usei <b>${used}</b> de <b>${points}</b> pontos no Explorer Level <b>${level}</b>.
      Considerei <b>${eligible.length}</b> skills liberadas: <b>${orange}</b> amarelas/laranjas e <b>${green}</b> verdes/S2.
      <br><b>Lv1 nesta rota:</b> ${lv1 || "sem skills liberadas"}.`;

    next.innerHTML = `<b>Proxima acao</b><br>
      ${nextUnfinished ? `O proximo ponto novo deve ir em <span class="planner-chip">${nextUnfinished.name}</span>.` : nextLocked ? `Ao chegar no Lv ${nextLocked.unlock}, avalie <span class="planner-chip">${nextLocked.name}</span>.` : "Esta rota fechou tudo que esta liberado para a classe/level informados."}
      <br><small>A tabela abaixo mostra tambem as skills que foram consideradas e adiadas.</small>`;

    const notes = [];
    notes.push(`Modo Season 2: ${OMITTED_S1[cls]} no(s) antigo(s) de Season 1 foram ignorados/substituidos.`);
    if (cls === "builder" && goal === "combat") notes.push("Builder ajuda a sobreviver e apoiar guilda, mas nao substitui Fighter para PvP pesado.");
    if (cls === "fighter" && goal === "growth") notes.push("Fighter em crescimento ainda evolui, mas Builder rende melhor para base/pesquisa.");
    if (level === 50 && points === 57) notes.push("Este bate com seu print novo: Lv50 e 57 pontos totais.");
    warning.innerHTML = `<b>Leitura:</b> ${notes.join(" ")}`;
  }

  function init() {
    ["classPlannerClass", "classPlannerGoal", "classPlannerLevel", "classPlannerPoints"].forEach((id) => {
      document.getElementById(id)?.addEventListener("input", runPlanner);
      document.getElementById(id)?.addEventListener("change", runPlanner);
    });
    runPlanner();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
