(function () {
  const STORAGE_KEY = 'palmon_lang';
  const LANGS = new Set(['pt', 'en']);
  const textOriginals = new WeakMap();
  const attrOriginals = new WeakMap();
  let applying = false;
  let observer = null;

  const phrases = [
    ['Pedia, simuladores e ferramentas do jogo em um só lugar', 'Pedia, simulators, and game tools in one place'],
    ['Este hub reúne a enciclopédia consolidada, o montador de time, o simulador de batalha e o analisador de loja. A base mistura dados extraídos do APK, cruzamento com fontes oficiais e regras práticas de gameplay organizadas para consulta rápida.', 'This hub brings together the consolidated encyclopedia, team builder, battle simulator, and shop analyzer. The knowledge base combines APK-extracted data, official sources, and practical gameplay rules organized for quick consultation.'],
    ['Entre pela Pedia para estudar o jogo, depois use os simuladores para decidir time, perks, skills e prioridades de progressão.', 'Start with the Pedia to study the game, then use the simulators to decide team layout, perks, skills, and progression priorities.'],
    ['Abrir Pedia Completa', 'Open Full Pedia'],
    ['Abrir Pedia', 'Open Pedia'],
    ['Pedia Completa', 'Full Pedia'],
    ['Montar Time', 'Build Team'],
    ['Montador de Time', 'Team Builder'],
    ['Simular Batalha', 'Simulate Battle'],
    ['Simulador de Batalha', 'Battle Simulator'],
    ['Loja offline por enquanto', 'Shop offline for now'],
    ['Shop Analyzer (offline)', 'Shop Analyzer (offline)'],
    ['Ferramentas', 'Tools'],
    ['Enciclopédia', 'Encyclopedia'],
    ['Mecânicas', 'Mechanics'],
    ['Resumo executivo, combate, elementos, perks, tier list, PalmonDex e regras práticas em uma leitura só.', 'Executive summary, combat, elements, perks, tier list, PalmonDex, and practical rules in a single read.'],
    ['Use o mesmo motor do simulador para arrastar, trocar, otimizar só o seu elenco atual e ajustar evolução, perks e skills por Palmon.', 'Use the same simulator engine to drag, swap, optimize only your current roster, and adjust evolution, perks, and skills for each Palmon.'],
    ['Teste distribuição frente/fundo, pressão de dano, resistência e impacto estimado das combinações do seu time.', 'Test front/back distribution, damage pressure, survivability, and the estimated impact of your team combinations.'],
    ['Módulo de bundles e loja deixado offline por enquanto, até a leitura do lado servidor ficar melhor amarrada com o que está ativo no dia.', 'Bundles and shop module is offline for now until server-side reading is better aligned with what is active each day.'],
    ['Publicação preparada para GitHub Pages. Alguns dados vêm do cliente/APK e outros de fontes oficiais e da comunidade verificadas em 2026.', 'Publication prepared for GitHub Pages. Some data comes from the client/APK and other parts come from official and community sources verified in 2026.'],

    ['Palmon Survival Pedia 2026 - Enciclopédia Completa', 'Palmon Survival Pedia 2026 - Complete Encyclopedia'],
    ['Enciclopédia consolidada com tudo que temos até agora: dados extraídos do APK/XAPK, ranking estratégico, habilidades, elementos, posições de batalha, perks, breeding, progressão, eventos e guia para responder prints. Onde não há confirmação de 2026, está marcado como lacuna.', 'Consolidated encyclopedia with everything we have so far: APK/XAPK data, strategic ranking, skills, elements, battle positions, perks, breeding, progression, events, and a screenshot-analysis guide. Anything not confirmed in 2026 is marked as a gap.'],
    ['Base consolidada 2026', 'Consolidated 2026 base'],
    ['Voltar ao hub', 'Back to hub'],
    ['Leitura rápida', 'Quick read'],
    ['Faça primeiro', 'Do first'],
    ['Evite', 'Avoid'],
    ['Melhor base atual', 'Best current baseline'],
    ['Nota de confiança:', 'Confidence note:'],
    ['Ferramentas novas:', 'New tools:'],
    ['Fontes e confiabilidade', 'Sources and reliability'],
    ['A Pedia prioriza APK/config local e fontes oficiais. Guias de comunidade entram como recomendação, não como regra oficial.', 'The Pedia prioritizes local APK/config data and official sources. Community guides are used as recommendations, not official rules.'],
    ['Fonte', 'Source'],
    ['Tipo', 'Type'],
    ['Confiabilidade', 'Reliability'],
    ['Uso na Pedia', 'Use in the Pedia'],
    ['Loop de gameplay e progressão', 'Gameplay loop and progression'],
    ['Loop principal', 'Core loop'],
    ['Prioridade de investimento', 'Investment priority'],
    ['Mecânicas de combate', 'Combat mechanics'],
    ['Funções', 'Roles'],
    ['Rank bruto APK', 'Raw APK rank'],
    ['Elementos e counters', 'Elements and counters'],
    ['Counter confirmado:', 'Confirmed counter:'],
    ['dano causado +10% e dano recebido -10%', 'damage dealt +10% and damage taken -10%'],
    ['Forte contra:', 'Strong against:'],
    ['Fraco contra:', 'Weak against:'],
    ['Formação e 7 posições', 'Formation and 7 positions'],
    ['Regra prática', 'Practical rule'],
    ['O que ainda não é 100% fechado', 'What is not 100% confirmed yet'],
    ['Perks e breeding', 'Perks and breeding'],
    ['Melhor configuração padrão por função', 'Best default setup by role'],
    ['Tier list', 'Tier list'],
    ['PalmonDex completa', 'Complete PalmonDex'],
    ['Estratégias práticas', 'Practical strategies'],
    ['Iniciante', 'Beginner'],
    ['Meio de jogo', 'Mid game'],
    ['Avançado/competitivo', 'Advanced/competitive'],
    ['Free-to-play', 'Free-to-play'],
    ['Pagante leve', 'Light spender'],
    ['Guia para analisar prints', 'Screenshot analysis guide'],
    ['O que olhar primeiro', 'What to check first'],
    ['Como responder decisão', 'How to answer decisions'],
    ['Incertezas e lacunas', 'Uncertainties and gaps'],

    ['Simulador tatico', 'Tactical simulator'],
    ['Simulador tático', 'Tactical simulator'],
    ['Montar time inteligente', 'Smart team builder'],
    ['7 slots confirmados', '7 confirmed slots'],
    ['perks, skills e evolucao', 'perks, skills, and evolution'],
    ['perks, skills e evolução', 'perks, skills, and evolution'],
    ['Simulador de Batalha - Palmon Survival', 'Battle Simulator - Palmon Survival'],
    ['Montar Time - Palmon Survival', 'Team Builder - Palmon Survival'],
    ['Monte o time que voce tem no jogo e o time inimigo, escolha forma base/evoluida, preencha o nivel de cada skill e perks, e rode uma simulacao estimada por turnos. O botao Otimizar meu time so realoca os Palmons ja colocados em Meu Time.', 'Build the team you actually have in the game and the enemy team, choose base/evolved form, enter each skill level and perks, then run an estimated turn simulation. The Optimize my team button only rearranges Palmons already placed in My Team.'],
    ['Monte somente o time que voce tem no jogo, arraste para trocar posicoes, ajuste forma base/evoluida, niveis individuais de skill e perks, e receba sugestoes praticas do mesmo motor usado no simulador completo.', 'Build only the team you have in the game, drag to swap positions, adjust base/evolved form, individual skill levels and perks, then get practical suggestions from the same engine used by the full simulator.'],
    ['Abrir modo montar time', 'Open team builder mode'],
    ['Abrir simulador completo', 'Open full simulator'],
    ['Meu melhor time', 'My best team'],
    ['Gerar inimigo forte', 'Generate strong enemy'],
    ['Otimizar meu time contra inimigo', 'Optimize my team against enemy'],
    ['Otimizar meu time', 'Optimize my team'],
    ['Simular agora', 'Simulate now'],
    ['Limpar tudo', 'Clear all'],
    ['Meu Time', 'My Team'],
    ['Time Inimigo', 'Enemy Team'],
    ['Clique num slot para selecionar', 'Click a slot to select'],
    ['Monte o adversario do print', 'Build the opponent from the screenshot'],
    ['Monte o adversário do print', 'Build the opponent from the screenshot'],
    ['Resultado estimado', 'Estimated result'],
    ['Resumo do meu time', 'My team summary'],
    ['Configuração dos Palmons em campo', 'Palmon field configuration'],
    ['Sugestões', 'Suggestions'],
    ['Melhorias recomendadas', 'Recommended improvements'],
    ['Alertas', 'Alerts'],
    ['Log da simulação', 'Simulation log'],
    ['Como o cálculo funciona', 'How the calculation works'],
    ['Dica: arraste um Palmon da lista para um slot.', 'Tip: drag a Palmon from the list into a slot.'],
    ['Otimizar nao adiciona Palmon novo: ele so reorganiza o time atual.', 'Optimize does not add new Palmons: it only rearranges the current team.'],
    ['Otimizar não adiciona Palmon novo: ele só reorganiza o time atual.', 'Optimize does not add new Palmons: it only rearranges the current team.'],
    ['Arraste para qualquer slot do seu time ou do inimigo.', 'Drag to any slot on your team or the enemy team.'],
    ['Tambem da para arrastar Palmon ja colocado para outro slot.', 'You can also drag an already placed Palmon to another slot.'],
    ['Também dá para arrastar Palmon já colocado para outro slot.', 'You can also drag an already placed Palmon to another slot.'],
    ['Monte o time que voce tem no jogo e o time inimigo', 'Build the team you have in the game and the enemy team'],
    ['Monte o time que você tem no jogo e o time inimigo', 'Build the team you have in the game and the enemy team'],
    ['escolha forma base ou evoluida', 'choose base or evolved form'],
    ['escolha forma base ou evoluída', 'choose base or evolved form'],
    ['preencha o nivel de cada skill e perks', 'enter each skill level and perks'],
    ['preencha o nível de cada skill e perks', 'enter each skill level and perks'],
    ['rode uma simulacao estimada por turnos', 'run an estimated turn simulation'],
    ['rode uma simulação estimada por turnos', 'run an estimated turn simulation'],
    ['O botao', 'The button'],
    ['O botão', 'The button'],
    ['so realoca os Palmons ja colocados em', 'only rearranges the Palmons already placed in'],
    ['só realoca os Palmons já colocados em', 'only rearranges the Palmons already placed in'],
    ['Depois de colocado, clique nele e depois clique no slot de destino', 'After placing it, click it and then click the destination slot'],
    ['ou arraste o proprio slot preenchido', 'or drag the filled slot itself'],
    ['ou arraste o próprio slot preenchido', 'or drag the filled slot itself'],
    ['para mover ou trocar de posicao inclusive entre My Team e Enemy Team', 'to move or swap positions, including between My Team and Enemy Team'],
    ['para mover/trocar de posicao inclusive entre My Team e Enemy Team', 'to move/swap positions, including between My Team and Enemy Team'],
    ['Foco:', 'Focus:'],

    ['Todas funções', 'All roles'],
    ['Todas funÃ§Ãµes', 'All roles'],
    ['Todas funções', 'All roles'],
    ['Todos elementos', 'All elements'],
    ['Todos tiers', 'All tiers'],
    ['Frente/Fundo', 'Front/Back'],
    ['Buscar Palmon ou skill', 'Search Palmon or skill'],
    ['Buscar Palmon', 'Search Palmon'],
    ['Palmons visíveis', 'visible Palmons'],
    ['Palmons catalogados', 'cataloged Palmons'],
    ['Imagens locais', 'local images'],
    ['UR no ranking', 'UR in ranking'],
    ['DPS fundo', 'Backline DPS'],
    ['DPS frente/bruiser', 'Front DPS/bruiser'],
    ['Suporte/controle', 'Support/control'],
    ['Tank', 'Tank'],
    ['Frente esquerda', 'front left'],
    ['Frente meio', 'front center'],
    ['Frente direita', 'front right'],
    ['Fundo esquerda', 'back left'],
    ['Fundo meio-esquerda', 'back mid-left'],
    ['Fundo meio-direita', 'back mid-right'],
    ['Fundo direita', 'back right'],
    ['Frente', 'Front'],
    ['Fundo', 'Back'],
    ['Água', 'Water'],
    ['Agua', 'Water'],
    ['Fogo', 'Fire'],
    ['Terra', 'Earth'],
    ['Elétrico', 'Electric'],
    ['Eletrico', 'Electric'],
    ['forte contra', 'strong against'],
    ['fraco contra', 'weak against'],
    ['Bônus', 'Bonus'],
    ['Bonus', 'Bonus'],
    ['sem bônus', 'no bonus'],
    ['sem bonus', 'no bonus'],
    ['Dano meu time', 'My team damage'],
    ['Dano inimigo', 'Enemy damage'],
    ['Bônus meu time', 'My team bonus'],
    ['Bônus inimigo', 'Enemy bonus'],
    ['Dano', 'Damage'],
    ['Vida efetiva', 'Effective life'],
    ['Sobrevivência estimada', 'Estimated survivability'],
    ['Dano estimado', 'Estimated damage'],
    ['Palmons no time', 'Palmons on team'],
    ['Skill para focar:', 'Skill to focus:'],
    ['Habilidades completas', 'Full skills'],
    ['Evolução:', 'Evolution:'],
    ['Evolucao:', 'Evolution:'],
    ['não confirmada', 'not confirmed'],
    ['Função:', 'Role:'],
    ['Funcao:', 'Role:'],
    ['Elemento:', 'Element:'],
    ['Melhor slot:', 'Best slot:'],
    ['Alternativas:', 'Alternatives:'],
    ['Stats APK:', 'APK stats:'],
    ['Valor:', 'Value:'],
    ['Alvo APK:', 'APK target:'],
    ['principal', 'main'],
    ['total bruto se todos os hits conectarem', 'raw total if all hits connect'],
    ['Causa', 'Deals'],
    ['dano a um único inimigo', 'damage to a single enemy'],
    ['dano a um Ãºnico inimigo', 'damage to a single enemy'],
    ['dano a todos os inimigos próximos', 'damage to all nearby enemies'],
    ['dano a todos os inimigos prÃ³ximos', 'damage to all nearby enemies'],
    ['Ganha', 'Gains'],
    ['Ataque', 'Attack'],
    ['Defesa', 'Defense'],
    ['PV', 'HP'],
    ['máximo', 'maximum'],
    ['mÃ¡ximo', 'maximum'],
    ['enquanto está em combate', 'while in combat'],
    ['enquanto estÃ¡ em combate', 'while in combat'],
    ['ao trabalhar em uma tarefa de', 'when working on a'],
    ['produção', 'production'],
    ['produÃ§Ã£o', 'production'],
    ['Plantio', 'Planting task'],
    ['Carga', 'Charging task'],
    ['Mineração', 'Mining task'],
    ['MineraÃ§Ã£o', 'Mining task'],
    ['Serragem', 'Sawing task'],
    ['Fundição', 'Smelting task'],
    ['FundiÃ§Ã£o', 'Smelting task'],
    ['tarefa de', 'task of'],
    ['Slot', 'Slot'],
    ['limpar', 'clear'],
    ['Limpar', 'Clear'],
    ['Forma', 'Form'],
    ['Base', 'Base'],
    ['Evoluído', 'Evolved'],
    ['Evoluido', 'Evolved'],
    ['Estrelas', 'Stars'],
    ['Perfil', 'Profile'],
    ['Nível', 'Level'],
    ['Nivel', 'Level'],
    ['Otimizar skills', 'Optimize skills'],
    ['Sugerir foco', 'Suggest focus'],
    ['proxima skill para focar e', 'next skill to focus is'],
    ['próxima skill para focar é', 'next skill to focus is'],
    ['Coloque seu melhor tank no Slot 2.', 'Put your best tank in Slot 2.'],
    ['Nenhum alerta grave encontrado.', 'No severe alert found.'],
    ['Sem alertas fortes.', 'No strong alerts.'],
    ['Sem melhoria óbvia pelo modelo atual.', 'No obvious improvement in the current model.'],
    ['Time coerente; refine perks e skill focus para extrair mais dano.', 'Coherent team; refine perks and skill focus to extract more damage.'],

    ['Palmon Survival - Shop Analyzer', 'Palmon Survival - Shop Analyzer'],
    ['Analisador de Loja', 'Shop Analyzer'],
    ['Voltar ao hub', 'Back to hub'],
    ['Pacotes', 'Packages'],
    ['Ofertas', 'Offers'],
    ['resultados', 'results'],
    ['Nenhuma oferta confirmada para este filtro.', 'No confirmed offer for this filter.'],
    ['Nenhum pacote relacionado por nome/tema para este filtro.', 'No package related by name/theme for this filter.'],
    ['preco BRL nao confirmado', 'BRL price not confirmed'],
    ['preço BRL não confirmado', 'BRL price not confirmed'],
    ['sem icone', 'no icon'],
    ['icone real', 'real icon'],
    ['icone provavel', 'likely icon'],
    ['icone provável', 'likely icon'],
    ['Descricao nao confirmada nas localizacoes extraidas.', 'Description not confirmed in extracted localizations.'],
    ['Descrição não confirmada nas localizações extraídas.', 'Description not confirmed in extracted localizations.']
  ];

  phrases.push(
    ['Resumo', 'Summary'],
    ['Montador de time', 'Team Builder'],
    ['Simulador de batalha', 'Battle Simulator'],
    ['Loop e progressão', 'Loop and progression'],
    ['Loop e progressÃ£o', 'Loop and progression'],
    ['Combate', 'Combat'],
    ['Elementos', 'Elements'],
    ['7 posições', '7 positions'],
    ['7 posiÃ§Ãµes', '7 positions'],
    ['Estratégias', 'Strategies'],
    ['EstratÃ©gias', 'Strategies'],
    ['Prints', 'Screenshots'],
    ['Lacunas', 'Gaps'],
    ['Monte 1 tank central, 2-3 DPS protegidos e 1 controle/suporte.', 'Build 1 central tank, 2-3 protected DPS, and 1 control/support unit.'],
    ['Use o bônus de elemento se conseguir 3+ Palmons do mesmo tipo sem destruir a função do time.', 'Use the element bonus if you can reach 3+ Palmons of the same type without breaking the team roles.'],
    ['Use o bÃ´nus de elemento se conseguir 3+ Palmons do mesmo tipo sem destruir a funÃ§Ã£o do time.', 'Use the element bonus if you can reach 3+ Palmons of the same type without breaking the team roles.'],
    ['Antes de evoluir, defina as 4 perks do Palmon.', 'Before evolving, lock in the Palmon’s 4 perks.'],
    ['Gastar Skillfruit/Omni Token em Palmon que vai sair do time.', 'Spending Skillfruit/Omni Token on a Palmon that will leave the team.'],
    ['Colocar DPS frágil no Slot 2.', 'Putting fragile DPS in Slot 2.'],
    ['Colocar DPS frÃ¡gil no Slot 2.', 'Putting fragile DPS in Slot 2.'],
    ['Breedar com pais cheios de traits ruins, porque aumenta o RNG.', 'Breeding with parents full of bad traits, because it increases RNG.'],
    ['Mammolith ou Embergeist; Ghillant/Statchew como alternativas.', 'Mammolith or Embergeist; Ghillant/Statchew as alternatives.'],
    ['tank no 2; carries no 4/5; agressivos nos 1/6.', 'tank in 2; carries in 4/5; aggressive units in 1/6.'],
    ['Palmons, stats, skills, elementos, linhas, slots e traits vêm do APK/XAPK.', 'Palmons, stats, skills, elements, lines, slots, and traits come from the APK/XAPK.'],
    ['Palmons, stats, skills, elementos, linhas, slots e traits vÃªm do APK/XAPK.', 'Palmons, stats, skills, elements, lines, slots, and traits come from the APK/XAPK.'],
    ['Estratégia de rank/perks é inferência prática baseada nesses dados + fontes 2026.', 'Rank/perk strategy is a practical inference based on this data + 2026 sources.'],
    ['EstratÃ©gia de rank/perks Ã© inferÃªncia prÃ¡tica baseada nesses dados + fontes 2026.', 'Rank/perk strategy is a practical inference based on this data + 2026 sources.'],
    ['use o Team Builder para montar seu elenco com drag and drop, o Battle Simulator para testar matchups completos e deixe o Shop Analyzer offline por enquanto, ate a leitura do lado servidor ficar mais confiavel.', 'use the Team Builder to assemble your roster with drag and drop, the Battle Simulator to test full matchups, and keep the Shop Analyzer offline for now until server-side reading becomes more reliable.'],
    ['use o Team Builder para montar seu elenco com drag and drop, o Battle Simulator para testar matchups completos e deixe o Shop Analyzer offline por enquanto, até a leitura do lado servidor ficar mais confiável.', 'use the Team Builder to assemble your roster with drag and drop, the Battle Simulator to test full matchups, and keep the Shop Analyzer offline for now until server-side reading becomes more reliable.'],
    ['use o Team Builder para montar seu elenco com drag and drop, o Battle Simulator para testar matchups completos e deixe o Shop Analyzer offline por enquanto, atÃ© a leitura do lado servidor ficar mais confiÃ¡vel.', 'use the Team Builder to assemble your roster with drag and drop, the Battle Simulator to test full matchups, and keep the Shop Analyzer offline for now until server-side reading becomes more reliable.'],
    ['use o Team Builder', 'use the Team Builder'],
    ['use o ', 'use the '],
    [', o ', ', the '],
    [' o ', ' the '],
    ['o Battle Simulator', 'the Battle Simulator'],
    [' o Battle Simulator', ' the Battle Simulator'],
    ['o Battle Simulator to', 'the Battle Simulator to'],
    [' e keep ', ' and keep '],
    ['Bonus de mesma composição', 'Same-composition bonus'],
    ['Bônus de mesma composição', 'Same-composition bonus'],
    ['3 Palmons do mesmo tipo', '3 Palmons of the same type'],
    ['Não force 7 do mesmo elemento se isso destruir tank/DPS/controle.', 'Do not force 7 of the same element if it breaks tank/DPS/control balance.'],
    ['NÃ£o force 7 do mesmo elemento se isso destruir tank/DPS/controle.', 'Do not force 7 of the same element if it breaks tank/DPS/control balance.'],
    ['Cuidado:', 'Warning:'],
    ['páginas individuais públicas não confirmam as 4 perks perfeitas de todos os Palmons.', 'public individual pages do not confirm the perfect 4 perks for every Palmon.'],
    ['pÃ¡ginas individuais pÃºblicas nÃ£o confirmam as 4 perks perfeitas de todos os Palmons.', 'public individual pages do not confirm the perfect 4 perks for every Palmon.'],
    ['Por isso a Pedia usa perfil por função e marca como recomendação prática.', 'That is why the Pedia uses role-based profiles and marks them as practical recommendations.'],
    ['Por isso a Pedia usa perfil por funÃ§Ã£o e marca como recomendaÃ§Ã£o prÃ¡tica.', 'That is why the Pedia uses role-based profiles and marks them as practical recommendations.'],
    ['para montar seu elenco com drag and drop', 'to assemble your roster with drag and drop'],
    ['para testar matchups completos', 'to test full matchups'],
    ['deixe o Shop Analyzer offline por enquanto', 'keep the Shop Analyzer offline for now'],
    ['ate a leitura do lado servidor ficar mais confiavel', 'until server-side reading becomes more reliable'],
    ['até a leitura do lado servidor ficar mais confiável', 'until server-side reading becomes more reliable'],
    ['atÃ© a leitura do lado servidor ficar mais confiÃ¡vel', 'until server-side reading becomes more reliable'],
    ['dados extraídos do APK/XAPK', 'APK/XAPK-extracted data'],
    ['dados extraÃ­dos do APK/XAPK', 'APK/XAPK-extracted data'],
    ['ranking estratégico', 'strategic ranking'],
    ['ranking estratÃ©gico', 'strategic ranking'],
    ['habilidades', 'skills'],
    ['posições de batalha', 'battle positions'],
    ['posiÃ§Ãµes de batalha', 'battle positions'],
    ['progressão', 'progression'],
    ['progressÃ£o', 'progression'],
    ['eventos', 'events'],
    ['guia para responder prints', 'screenshot-answering guide'],
    ['Onde não há confirmação de 2026, está marcado como lacuna.', 'Anything not confirmed in 2026 is marked as a gap.'],
    ['Onde nÃ£o hÃ¡ confirmaÃ§Ã£o de 2026, estÃ¡ marcado como lacuna.', 'Anything not confirmed in 2026 is marked as a gap.']
  );

  try {
    const dataNode = document.getElementById('palmon-data');
    if (dataNode) {
      const data = JSON.parse(dataNode.textContent || '{}');
      (data.palmons || []).forEach((palmon) => {
        (palmon.skills || []).forEach((skill) => {
          if (skill.name && skill.nameEn && skill.name !== skill.nameEn) {
            phrases.push([skill.name, skill.nameEn]);
          }
        });
      });
    }
  } catch {
    // Optional page data. If it is absent or malformed, the generic UI translation still works.
  }

  const sortedPhrases = phrases
    .filter(([from]) => from && from.trim())
    .sort((a, b) => b[0].length - a[0].length);

  function currentLang() {
    const queryLang = new URLSearchParams(window.location.search).get('lang');
    if (LANGS.has(queryLang)) return queryLang;
    const stored = localStorage.getItem(STORAGE_KEY);
    return LANGS.has(stored) ? stored : 'pt';
  }

  function translateText(text) {
    if (!text || !text.trim()) return text;
    if (text.trim() === 'o') return text.replace('o', 'the');
    if (text.trim() === 'O') return text.replace('O', 'The');
    let output = text;
    for (const [from, to] of sortedPhrases) {
      output = output.split(from).join(to);
    }
    return output;
  }

  function shouldSkipNode(node) {
    const parent = node.parentElement;
    if (!parent) return true;
    return !!parent.closest('script, style, noscript, code, pre, textarea, [data-no-i18n]');
  }

  function translateTextNode(node, lang) {
    if (shouldSkipNode(node)) return;
    if (!textOriginals.has(node)) textOriginals.set(node, node.nodeValue);
    const original = textOriginals.get(node);
    node.nodeValue = lang === 'en' ? translateText(original) : original;
  }

  function translateAttributes(element, lang) {
    if (!element || element.closest('script, style, noscript, [data-no-i18n]')) return;
    const attrs = ['placeholder', 'title', 'alt', 'aria-label'];
    let saved = attrOriginals.get(element);
    if (!saved) {
      saved = {};
      attrOriginals.set(element, saved);
    }
    for (const attr of attrs) {
      if (!element.hasAttribute(attr)) continue;
      if (!(attr in saved)) saved[attr] = element.getAttribute(attr);
      const original = saved[attr];
      element.setAttribute(attr, lang === 'en' ? translateText(original) : original);
    }
  }

  function applyTextTranslation(lang) {
    if (window.PALMON_SKIP_TEXT_TRANSLATION && typeof window.setLang === 'function') {
      window.setLang(lang);
      return;
    }
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach((node) => translateTextNode(node, lang));
    document.querySelectorAll('[placeholder], [title], [alt], [aria-label]').forEach((el) => translateAttributes(el, lang));
    document.title = lang === 'en' ? translateText(document.title) : (document.title || '').replace('Complete Encyclopedia', 'Enciclopédia Completa').replace('Battle Simulator', 'Simulador de Batalha').replace('Team Builder', 'Montar Time');
  }

  function internalUrl(url) {
    if (!url) return null;
    if (url.startsWith('#') || url.startsWith('javascript:') || url.startsWith('mailto:') || url.startsWith('tel:')) return null;
    try {
      const parsed = new URL(url, window.location.href);
      if (parsed.origin !== window.location.origin) return null;
      return parsed;
    } catch {
      return null;
    }
  }

  function updateLinks(lang) {
    document.querySelectorAll('a[href]').forEach((link) => {
      const parsed = internalUrl(link.getAttribute('href'));
      if (!parsed) return;
      parsed.searchParams.set('lang', lang);
      link.setAttribute('href', parsed.pathname.split('/').pop() + parsed.search + parsed.hash);
    });
  }

  function ensureLanguagePanel() {
    let pt = document.getElementById('langPt');
    let en = document.getElementById('langEn');
    if (pt && en) return { pt, en };

    const style = document.createElement('style');
    style.textContent = `
      .palmon-floating-lang{position:fixed;right:16px;top:14px;z-index:9999;display:flex;align-items:center;gap:10px;padding:9px 10px;border:1px solid #bfd8fb;border-radius:12px;background:#ffffffee;box-shadow:0 10px 22px rgba(23,32,51,.14);backdrop-filter:blur(8px)}
      .palmon-floating-lang span{font-size:12px;font-weight:800;color:#172033}
      .palmon-floating-lang button{border:1px solid #cfe0f5;background:#fff;color:#5b7188;border-radius:9px;padding:7px 10px;font-weight:900;cursor:pointer;min-width:auto}
      .palmon-floating-lang button.active{background:linear-gradient(135deg,#2563eb,#5fd0ff);border-color:#2563eb;color:#fff}
      @media(max-width:760px){.palmon-floating-lang{position:static;margin:10px 14px;width:fit-content}}
    `;
    document.head.appendChild(style);

    const panel = document.createElement('div');
    panel.className = 'palmon-floating-lang';
    panel.innerHTML = '<span>Idioma / Language</span><button id="langPt" type="button">PT</button><button id="langEn" type="button">EN</button>';
    document.body.prepend(panel);
    return { pt: panel.querySelector('#langPt'), en: panel.querySelector('#langEn') };
  }

  function applyLanguage(lang) {
    if (!LANGS.has(lang)) lang = 'pt';
    if (applying) return;
    applying = true;
    localStorage.setItem(STORAGE_KEY, lang);
    document.documentElement.lang = lang === 'en' ? 'en' : 'pt-BR';
    const buttons = ensureLanguagePanel();
    buttons.pt.classList.toggle('active', lang === 'pt');
    buttons.en.classList.toggle('active', lang === 'en');
    applyTextTranslation(lang);
    updateLinks(lang);
    applying = false;
  }

  function setLanguage(lang, updateUrl = true) {
    applyLanguage(lang);
    if (updateUrl) {
      const url = new URL(window.location.href);
      url.searchParams.set('lang', lang);
      window.history.replaceState(null, '', url);
    }
  }

  function observeDynamicText() {
    if (observer) observer.disconnect();
    observer = new MutationObserver(() => {
      if (applying || currentLang() !== 'en') return;
      window.requestAnimationFrame(() => applyLanguage('en'));
    });
    observer.observe(document.body, { childList: true, subtree: true, characterData: true });
  }

  function bindButtons() {
    const buttons = ensureLanguagePanel();
    buttons.pt.addEventListener('click', () => setLanguage('pt'));
    buttons.en.addEventListener('click', () => setLanguage('en'));
  }

  function init() {
    bindButtons();
    applyLanguage(currentLang());
    observeDynamicText();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.PalmonI18n = { setLanguage, applyLanguage };
})();
