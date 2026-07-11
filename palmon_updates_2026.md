# Palmon Survival — Updates e Mudanças 2026

Este arquivo resume o que mudou ou entrou na nossa base. A leitura atual fica alinhada ao servidor do Marcelo: **Season 2 iniciada agora**.

Regra de atualização: toda entrada nova deve responder:

- O que entrou
- O que muda na decisão de gameplay
- O que fazer primeiro
- Fonte e confiança
- O que ainda não está confirmado

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
