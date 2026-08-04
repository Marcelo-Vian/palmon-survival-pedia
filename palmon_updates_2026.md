# Palmon Survival — Updates e Mudanças 2026

Este arquivo resume o que mudou ou entrou na nossa base. A leitura atual fica alinhada ao servidor do Marcelo: **Season 2: Crimson Reign**.

Regra de atualização: toda entrada nova deve responder:

- O que entrou
- O que muda na decisão de gameplay
- O que fazer primeiro
- Fonte e confiança
- O que ainda não está confirmado

## 2026-08-04 — Correção de seasons e montarias

**O que entrou**

- Correção oficial/local dos nomes de season:
  - **S1: Dawn of the Ice Age**
  - **Season 2: Crimson Reign**
  - **Conquest Season / S3** como season posterior, não aplicável ao servidor atual se a tela mostra S2.
- Print live confirmou `Season 2: Crimson Reign`, versão de tela `0.5.369 (394)`, eventos de S2 e aproximadamente 40 dias restantes.
- A tela live também mostrou o lobo/Skybound Patrol como conteúdo da Season 2 atual do servidor.

**Impacto prático**

- A ferramenta de montarias não usa mais regra genérica de `dia 60/95` para decidir se Bunny/Skybound/Night estão liberadas.
- O que manda é o nome da season na tela + as montarias marcadas como **Tenho**.
- Guias externos por dia de servidor ficam como baixa confiança quando conflitam com print live.

**Faça primeiro**

1. Na tela Season/Eventos, use o nome do topo: `Season 2: Crimson Reign`.
2. No Auditor de Montarias, escolha **Season 2: Crimson Reign**.
3. Marque somente as montarias que você realmente tem; o otimizador redistribui recursos só entre elas.
4. Para tank, priorize Amourphibian e Skybound Patrol; para dano/PvP, Bunny Runny, Night Mare e Skybound Patrol entram no núcleo se você já tem essas montarias.

**Fontes**

- Print live do Marcelo enviado em 2026-08-04: `Season 2: Crimson Reign`.
- APK/localização extraída: `season2_preheating_1_title = "Season 2: Crimson Reign"`, `season_preheating_3_title = "S1: Dawn of the Ice Age"`, `home_mount_7_name = "Skybound Patrol"`.
- Fonte oficial pública: vídeo/canal oficial `Palmon Survival | Season 2: Crimson Reign`.
- Fonte oficial pública indexada: posts Palmon Survival citando `Season I: Dawn of the Ice Age` e `Conquest Season`.

**Não confirmado**

- Datas exatas de início/fim para todos os servidores.
- Uma fórmula confiável para converter número do servidor em dia/season; servidores abrem em ondas e podem ter calendário próprio.

## 2026-07-13 — Correção da árvore de Classes

**O que entrou**

- A calculadora de Class Skills foi refeita para considerar a árvore completa do APK por classe, nível de desbloqueio, posição e cor.
- Agora entram no cálculo os nós amarelos/laranjas e os verdes/S2.
- O exemplo live usado foi **Builder Lv50 com 57/57 pontos**.

**Impacto prático**

- A ferramenta não joga mais pontos só em uma lista manual de prioridades.
- Cada linha da árvore mostra todas as opções liberadas. No Lv1, por exemplo, aparecem as 3 skills e quantos pontos a rota recomenda em cada uma.
- Para Season 2, os nós antigos de Season 1 foram ignorados/substituídos.

**Faça primeiro**

1. Coloque sua classe real, Explorer Level e pontos totais exatamente como aparece no jogo.
2. Se estiver Builder Lv50/57 e quer crescer, use **Crescimento/F2P/base**.
3. Leia a tabela por nível antes de gastar: ela mostra skills fortes, skills adiadas e skills situacionais.

**Fontes**

- APK local: `season_job_tree.lua` e `season_job_skill.lua`.
- Print live de 2026-07-13: Builder Lv50, 57/57 pontos.

**Não confirmado**

- A prioridade estratégica ainda é inferência prática. O APK confirma árvore, max level e efeitos, mas não define uma ordem "melhor" oficial para cada perfil de jogador.

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
