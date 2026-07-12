# Palmon Survival — Updates e Mudanças 2026

Este arquivo resume o que mudou ou entrou na nossa base. A leitura atual fica alinhada ao servidor do Marcelo: **Season 2 iniciada agora**.

Regra de atualização: toda entrada nova deve responder:

- O que entrou
- O que muda na decisão de gameplay
- O que fazer primeiro
- Fonte e confiança
- O que ainda não está confirmado

## 2026-07-12 — Achievements e distribuidor automático de Class Skills

**O que entrou**

- Seção nova de **Palmon Achievements** com prioridade de investimento, custos por tier, pré-requisitos e regra de reset.
- Confirmação pelo XAPK local **0.5.346**: o arquivo `hero_fate` é igual ao da 0.5.325 para achievements.
- Regra de fichas excedentes fechada: no APK atual, o caminho `consume1` aparece para **Elemental Guardian**.
- A seção de Classes ganhou um **distribuidor automático de pontos**: classe, objetivo, Explorer Level e pontos totais.

**Impacto prático**

- Super Voltaic Trio, Child of the Sea, Surface Blitz Squad, Burn! My Cosmos!, Critical Hit e It’s Over 9000 usam Omni-Token/Refund normal, não ficha específica excedente.
- Ficha UR específica excedente só deve ser usada quando o achievement/tier aceitar esse consumo. Na tabela atual, isso é **Elemental Guardian**.
- A distribuição de classe deixa de ser uma tabela fixa de 55 pontos e passa a variar conforme seu nível e objetivo.

**Faça primeiro**

1. Em Achievements, priorize **Critical Hit**, depois **It’s Over 9000!**, depois o achievement do elemento do seu time principal.
2. Use ficha excedente só em **Elemental Guardian** e somente se Fingenue, Mantleray, Surveilynx ou Magmolin já estiverem 5 estrelas com fichas sobrando.
3. Na calculadora de classe, informe o segundo número da tela, por exemplo `0/55` significa usar **55 pontos totais**.
4. Para Fighter Lv49/55 pontos, use objetivo equilibrado ou combate; ao Lv50, puxar **Offensive Tactics**.

**Fontes**

- XAPK/APK local 0.5.346 analisado em 2026-07-12.
- `hero_fate.lua` para custos, pré-requisitos e `consume1`.
- `language_en.lua` para regra de reset, Omni-Token Refund, fichas excedentes e limite de reset semanal.
- Prints do jogo enviados em 2026-07-12.

**Não confirmado**

- A fórmula completa de pontos por Explorer Level fora dos valores mostrados no jogo.
- Se o servidor pode alterar temporariamente disponibilidade/custo por evento sem mudar o APK.

## 2026-07-11 — Season 2 / Classes, Explorer Level e Skill Points

**O que entrou**

- Sistema de classes da season mapeado pelo APK/XAPK: **Builder** e **Fighter**.
- Explorer Level da season confirmado até **70**.
- Árvore de skills separada em skills comuns e extensões **Season 2**.
- Texto do jogo confirma que o jogador ganha Explorer XP derrotando Wild Palmon, capturando **Sanctums** e **Sacred Springs**, e melhorando construções exclusivas da season.
- Print live confirmou: **Fighter Lv49**, XP **180.717 / 1.500.000**, **Available Skill Points 0/55**.

**Impacto prático**

- `0/55` quer dizer **0 pontos livres de 55 totais**, não zero pontos na classe.
- Os pontos pertencem ao Explorer Level. Builder e Fighter usam o mesmo banco de pontos; ao trocar classe, o jogo reseta skills e reembolsa pontos.
- Fighter é a classe de PvP/rally/Sanctum. Builder é a classe de crescimento, construção, pesquisa, coleta e suporte.

**Faça primeiro**

1. Se for jogar agressivo: manter Fighter.
2. Em Fighter Lv49, garantir o pacote de XP para subir até Lv55/60 e o pacote de combate: Morale Boost, Fierce Assault, Defensive Tactics e Rallying Cry.
3. Ao chegar Lv50, priorizar **Offensive Tactics 5/5**.
4. Ao chegar Lv55, se tiver Morale Boost 5/5, priorizar **Hyper Frenzy 5/5**.
5. Se o foco for crescer sem guerra pesada, considerar Builder com Builder's Passion, Scholarly Passion, Instant Build, Instant Research, Cost Cutter e Thrifty Science.

**Fontes**

- APK/XAPK local 0.5.325: `season_job.lua`, `season_job_level.lua`, `season_job_tree.lua`, `season_job_skill.lua`.
- Localização do APK: `language_en.lua`.
- Prints do jogo enviados em 2026-07-11.

**Não confirmado**

- A fórmula completa `Explorer Level -> total de Skill Points`; o APK local mostra XP por nível e skill trees, mas não expôs uma tabela clara de pontos por nível.
- Por enquanto, usar sempre o total exibido no jogo em `Available Skill Points: livre/total`.

## 2026-07-11 — Season 2 / Boss Palmon no squad

**O que entrou**

- Correção da leitura de Boss Palmon: o foco atual é **Boss no squad**, não apenas recompensa de evento.
- Boss Palmon tem slot/efeito de squad, upgrade, ascent/star, skills e talentos.
- Titan Totem entra como prédio/sistema de Season 2 ligado a Titan Seals para Boss.
- Boss Tech libera/fortalece uso de Boss em squads.
- A base agora mostra prioridade de skills por Boss com valores Lv.1 -> Lv.5 extraídos do APK decifrado.

**Impacto prático**

- O melhor Boss depende do seu time real.
- Para time Água, Inkuisitor é melhor primeiro investimento.
- Ophidillain tem maior teto por buff universal, mas só compensa como prioridade quando estiver liberado e investido.
- Não faz sentido espalhar Bloom Stones/Titan Seals em vários Boss ao mesmo tempo.

**Faça primeiro**

1. Escolha 1 Boss principal para o seu squad atual.
2. Se seu time principal é Água, foque **Inkuisitor**.
3. Se você já tem Ophidillain bem liberado/investido, ele pode virar o Boss principal universal.
4. Se seu time é Elétrico, foque **Oinkohm**.
5. Se seu time é Terra/tank, foque **Bogolem**.
6. Se seu time é Fogo/burn, foque **Flapnir**.

**Rank prático para Boss no squad**

| Rank | Boss | Melhor caso |
|---:|---|---|
| 1 | Ophidillain | Melhor teto universal quando liberado e investido. |
| 2A | Inkuisitor | Melhor para squad Água, especialmente no seu caso atual. |
| 2B | Oinkohm | Melhor para squad Elétrico e burst. |
| 4 | Bogolem | Melhor para Terra/tank/defesa. |
| 5 | Flapnir | Melhor apenas em Fire/burn. |

**Skills mais importantes**

| Boss | Focar primeiro |
|---|---|
| Ophidillain | Serpent's Shroud > Venomous Instinct > Serpent Elixir |
| Inkuisitor | Midnight Tide > Splash Sprint > Frostbite Bonus |
| Oinkohm | Lightning Conduit > Static Resonance > Quickshock |
| Bogolem | Last Aegis > Mountain Grit > Rocky Fury |
| Flapnir | Dragon's Breath > Flame Splash > Scorch Sensor |

**Fontes**

- APK local decifrado 0.5.277: `boss_skill.lua`, `language_en.lua`, `language_pt_BR.lua`.
- XAPK local 0.5.325: confirmou configs de Boss alterados/criados.
- LDShop Boss Guide, 2026-06-25.
- PalmonGuide 2026: Titan Totem / Season 2.
- Snippets oficiais públicos sobre Boss em Squad Settings e upgrades de Boss afetando Palmons no mesmo squad.

**Não confirmado**

- Se a versão 0.5.325 mudou algum número final das skills no servidor ativo.
- Cooldowns internos completos.
- Fórmula exata de dano final.
- Diferenças por servidor/evento. Validar por print da tela de Boss quando possível.

## 2026-06-18 — XAPK 0.5.325

**O que entrou**

- XAPK 0.5.325 analisado localmente.
- Configs críticos alterados/criados para Boss: `boss_levelup`, `boss_lvup`, `boss_skill`, `boss_star`, `boss_talent`.
- Outros configs gerais também mudaram: `hero`, `skill`, `card_skill_pal`, `card_buff_pal`, `building`, `season_*`, `shop`, `recharge`.

**Impacto prático**

- Confirmou que Boss Palmon virou sistema relevante e ativo para progressão.
- A base não troca número de dano/tier automaticamente sem parse legível ou print live.

**Faça primeiro**

1. Usar o rank de Boss de Season 2 como guia prático.
2. Validar valores atuais de skill por print da tela de Boss.
3. Não atualizar dano/tier/custos sem parse novo ou confirmação visual do jogo.

**Não confirmado**

- Fórmulas e números finais da versão 0.5.325.
- Variações por servidor.

## 2026-06-06 — Pedia inicial consolidada

**O que entrou**

- PalmonDex inicial.
- Tier list estratégica.
- Elementos e counters.
- Slots de batalha.
- Perks por função.
- Guia de screenshot.

**Impacto prático**

- A base passou a responder decisões como: qual Palmon usar, qual skill focar, onde posicionar, qual perk usar e quando evitar gasto.

**Não confirmado**

- Fórmula completa de dano.
- Targeting exato por slot/lado.
- Alguns números dependentes de servidor/evento.
