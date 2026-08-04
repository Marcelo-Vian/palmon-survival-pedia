# Palmon Survival - Atualizacao Tecnica APK/XAPK 0.5.325

Fonte local: `C:\Users\marce\OneDrive\Área de Trabalho\codex\Palmon_+Survival_0.5.325_APKPure.xapk`, copiado e extraido em 2026-06-18.

Este documento complementa o passo 1 da engenharia feita sobre a versao `0.5.277`. Ele nao substitui o ranking antigo ainda, porque os novos configs de gameplay foram exportados do Unity, mas seguem codificados em `.bytes`.

## 1. Resultado rapido

| Item | Confirmacao |
|---|---|
| Pacote | `com.funfizz.palmon.gp` |
| Versao | `0.5.325` |
| Version code | `241` |
| ResourceVersion | `325` |
| SeasonVersion[0] | `320` |
| LanVer | `424` |
| Target SDK | `36` |
| Split APKs | `base`, `assetLibrary`, `config.arm64_v8a` |

Comparado com `0.5.277`, o novo pacote mudou `ResourceVersion` de `277` para `325`, `SeasonVersion[0]` de `272` para `320`, `LanVer` de `394` para `424` e `VerCode` de `236` para `241`.

## 2. O que mudou

Diff bruto dos configs:

| Medida | Resultado |
|---|---:|
| Arquivos `.ua` antigos | 1130 |
| Arquivos `.ua` novos | 1210 |
| Arquivos adicionados | 80 |
| Arquivos removidos | 0 |
| Arquivos alterados | 434 |

Diff logico por nome de bundle/config:

| Medida | Resultado |
|---|---:|
| Configs logicos antigos | 620 |
| Configs logicos novos | 664 |
| Configs adicionados | 48 |
| Configs removidos | 4 |
| Configs alterados | 134 |

## 3. Novos configs nomeados relevantes

- `gem`
- `gem_power`
- `gem_skill`
- `gem_window`
- `tech_desert`
- `tech_desert_level`
- `desert_reward`
- `desert_pk_preview`
- `s03_resources_worldarea`
- `s03_server_resources_bigworldmap`
- `s03_server_resources_worldarea`
- `s03_till_land_gem`
- `decoration_land_box`
- `decoration_shop`
- `guild_badge_run_npc`
- `guild_badge_run_stage`
- `minigame_reward_center`
- `pyramids_war_pointreward`
- `recharge_gift_window_smart`
- `spectacle_day_buff`
- `tech_amigo`
- `activity_award_ggj`

Leitura pratica: o pacote tem sinal forte de sistemas/expansoes ligados a gemas, deserto, season `s03`, decoracao, guild badge run e novas janelas de recharge/gift. Isso ainda nao confirma periodo ativo nem regra final no servidor.

## 3.1. S02 vs S03 no APK 0.5.325

Conclusao segura: nao e "so S02" nem "so S03". O APK 0.5.325 contem base de S02 e tambem conteudo S03 mais concreto.

| Area | Confirmado no APK | Leitura pratica |
|---|---|---|
| S02 | Token legivel `S2CurseData`, `s02_city_data`, `s02_city_data_part1`, `s02_city_data_part2`, `s02_city_data_reuse` | A S02 continua presente e foi reorganizada em partes. Nome interno mais forte encontrado: `Curse`. |
| S03 | Token legivel novo `S3DesertData`, `s03_city_data`, `s03_guild_furnace`, `s03_home_decor`, `s03_pyramids_data`, `s03_resources_worldarea` | A S03 aparece mais preparada/expandida nesta versao. Nome interno mais forte encontrado: `Desert`. |
| Deserto | `tech_desert`, `tech_desert_level`, `tech_desert_part1` ate `part8`, `desert_reward`, `desert_pk_task`, `desert_pk_preview`, `desert_officials` | Indica tecnologia/arvore sazonal de deserto, recompensas, tarefas e possivel competicao/PK de deserto. |
| Gemas | `gem`, `gem_power`, `gem_skill`, `gem_window`, `s03_till_land_gem` | Indica sistema novo ou expandido de gemas, poder por gemas e skill vinculada a gemas. |
| Piramides | `pyramids_war_pointreward`, `pyramids_war_points_way`, `s03_pyramids_data`, texturas `ipyramidbattle` | Indica sistema/evento de guerra, pontos ou recompensas em piramides. |
| UI de temporada | Paineis `desertcompetition`, `desertmapcity`, `desertstormbattlefield`, `uidesertofficer`; texturas `uigem` | Existem telas especificas para competicao, mapa/cidade de deserto, battlefield, oficiais e gemas. |

Importante: `Curse` e `Desert` sao nomes internos encontrados nos dados do cliente, nao nome oficial publico confirmado. Correcao 2026-08-04: o nome publico confirmado da S02 e **Season 2: Crimson Reign**; S1 e **Dawn of the Ice Age**; a season posterior aparece publicamente como **Conquest Season**. Abertura real da S02/S03, calendario e regras finais dependem de config remota/server-side ou print dentro do jogo.

## 4. Configs criticos alterados

- `hero`
- `hero_evolve`
- `hero_evolve_potency`
- `hero_inborn`
- `skill`
- `card_skill_pal`
- `card_buff_pal`
- `building`
- `home_building`
- `boss_levelup`
- `boss_skill`
- `boss_talent`
- `shop`
- `recharge`
- `recharge_gift`
- `recharge_gift_window`
- `season_recruit`
- `season_open`
- `season_cross_server_team`
- `season_donation_gift`
- `tech`
- `tech_enter`
- `tech_reward`

Regra para nossa base: nao atualizar dano, tier, melhor skill, custo ou melhor composicao com numeros da 0.5.325 ate decodificar e parsear esses configs.

## 5. Arquitetura confirmada

O pacote segue o mesmo desenho tecnico:

- Unity como engine.
- IL2CPP como runtime C# compilado em nativo.
- XLua para ponte/configs Lua.
- AssetBundles para assets e configs.
- SDK Lilith/Farlight para login, pagamento, relatorio e compliance.
- Google Billing no Android.
- Firebase/Huawei/Google services presentes em configs.
- Bibliotecas nativas: `libil2cpp.so`, `libunity.so`, `libxlua.so`, `libllhsdk.so`, `libsigner.so`, `libcheck.so`, `libsodium.so`, `libCrashSight.so`.

## 6. Servidor, compras e protecoes em alto nivel

Confirmado no cliente:

- CDNs de assets globais em `gameconfig.txt`.
- Ambientes `prod` e `qc` nos JSONs de SDK.
- URLs de account center, SDK, H5/QR, diagnostico e upload.
- Modulos `GooglePayModuleLoader`, `PaymentModuleLoader` e `CashierModuleLoader`.
- Permissao Android `com.android.vending.BILLING`.
- Configs de `shop`, `recharge`, `gift` e janelas de oferta.

Leitura correta:

- O APK pode carregar catalogos, textos e estrutura de pacotes.
- A loja ativa do dia e a concessao real de itens dependem de servidor/config remota.
- Compra real deve ser validada com Google Play/App Store e concedida por servidor.
- Estado importante nao deve confiar no cliente.

Para nosso app:

1. Catalogo de ofertas fica no backend/admin.
2. Cliente mostra ofertas recebidas do servidor.
3. Compra usa Google Play Billing/App Store.
4. Cliente envia purchase token/receipt para nosso backend.
5. Backend valida com API oficial.
6. Backend concede item de forma idempotente.
7. Inventario, moeda premium, ranking e eventos ficam autoritativos no servidor.

Nao documentado por seguranca: bypass de compra, quebra de assinatura/protecao, acesso nao autorizado a servidor ou qualquer fluxo para obter item sem validacao legitima.

## 7. O que ainda falta

- Recuperar/reescrever a decodificacao dos `.bytes` da 0.5.325.
- Reparsear `hero`, `skill`, `card_skill_pal`, `card_buff_pal`, `hero_evolve_potency` e `hero_inborn`.
- Gerar ranking 0.5.325 atualizado somente depois do parse.
- Confirmar se novos sistemas de gemas/deserto/s03 estao ativos no servidor ou apenas preparados no cliente.
- Atualizar simulador somente com valores confirmados.

## 8. Arquivos gerados

- `D:\Linkedin\palmon_survival_apk\xapk_0_5_325`
- `D:\Linkedin\palmon_survival_apk\main_0_5_325_extracted`
- `D:\Linkedin\palmon_survival_apk\asset_0_5_325_extracted`
- `D:\Linkedin\palmon_survival_apk\config_arm64_0_5_325_extracted`
- `D:\Linkedin\palmon_survival_apk\analysis_0_5_325\logical_config_diff_0_5_277_to_0_5_325.json`
- `D:\Linkedin\palmon_survival_apk\analysis_0_5_325\config_inventory_diff_0_5_277_to_0_5_325.json`
