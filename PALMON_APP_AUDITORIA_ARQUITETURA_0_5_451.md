# Auditoria de Arquitetura - Palmon: Survival 0.5.451 + checagem instalada 0.5.465

Data da auditoria: 2026-10-23  
Escopo: leitura estatica do XAPK `0.5.451`, comparacao estrutural com a instalacao `0.5.465` em execucao e inventario limitado por ADB. Nenhuma credencial, token de sessao, pacote de rede ao vivo ou dado privado da conta foi copiado para este documento.

## Objetivo e limite

O objetivo e construir um advisor que represente o perfil real do jogador, explique as recomendacoes e consiga importar uma fotografia fiel do jogo. Esta auditoria mapeia o cliente para isso.

Ela nao tenta se passar pelo aplicativo, chamar servidores do jogo, reutilizar sessoes, alterar recursos ou automatizar acoes no jogo. Esses caminhos nao sao necessarios para o advisor e colocariam a conta em risco.

Quando este documento usa as palavras abaixo, elas tem significado estrito:

| Marca | Significado |
| --- | --- |
| Confirmado | Ha evidencia direta no XAPK/codigo analisado. |
| Inferencia forte | A arquitetura aponta para isso, mas falta observar uma execucao real. |
| Nao confirmado | O APK estatico nao permite afirmar. |

## Artefato auditado

| Item | Valor |
| --- | --- |
| Aplicativo | `com.funfizz.palmon.gp` |
| Nome | Palmon: Survival |
| Versao analisada | `0.5.451` (version code `261`) |
| Formato | XAPK com base, biblioteca de assets e configuracao arm64 |
| SDK minimo / alvo | Android 26 / 36 |
| Tamanho declarado do XAPK | 1.396.955.933 bytes |
| Base APK SHA-256 | `628DCF0391CD1556DB9E52CAC290E13051D44CDFB64D2D22218BCF0A048228F3` |
| Asset library SHA-256 | `3DB5E6105939772EA4FB4F694A1416B60E6B066D4A1CA711F8E7EF856EF31961` |
| Arm64 config SHA-256 | `68859AF059D4115E265C178A8D03806FA4EFB73263B6A4C067E68EB7036EA9E0` |

Importante: a versao do APK e uma fotografia. Um APK posterior pode trocar tabelas, telas, campos, balanceamento, assets e protocolos. O catalogo e as formulas precisam ser revalidados a cada salto de versao relevante.

### Checagem da instalacao ativa

Em 2026-10-23, uma instalacao aberta pelo usuario foi verificada por ADB normal, sem root, sem alterar o jogo e sem ler o armazenamento privado do aplicativo.

| Item | Valor confirmado |
| --- | --- |
| Pacote | `com.funfizz.palmon.gp` |
| Origem da instalacao | Google Play (`com.android.vending`) |
| Versao instalada | `0.5.465` (version code `267`) |
| APK base SHA-256 | `382637BEE2CE8224B967A574750A7E7F1DE5846A6AFFB9F66630B44084CAC187` |
| Split arm64 SHA-256 | `89A26B1F255AFEF230C2CE8939F462C9171EDE312B3A91DE594602CBE285E480` |
| `global-metadata.dat` | 11.710.936 bytes, SHA-256 `113E100810D48B1A8953A372D497822572BD2F94F93F2C08C683E9EAF99C40BF` |
| `libil2cpp.so` | 80.183.352 bytes, SHA-256 `4BD919403903162C2EBB89718DCCBEA8E48C2BAA3471EAAC8B73C29F3F47872A` |
| Metadata IL2CPP | Versao `31`, lida pelo dumper local |

O APK base contem os metadados IL2CPP; o split arm64 contem `libil2cpp`, `libxlua` e as bibliotecas nativas. A geracao do mapa de tipos da `0.5.465` foi concluida localmente. A pausa final do utilitario de analise falhou por nao haver um console interativo, mas aconteceu depois da criacao de `dump.cs`, `script.json`, `stringliteral.json` e das DLLs de referencia; isso nao afeta a leitura feita.

## Resultado da leitura dinamica 0.5.465

### O que a instalacao atual confirma

- A arquitetura continua sendo Unity IL2CPP com xLua. Os tipos nativos `LIMNetManager`, `NetManager`, `FsmLogin` e o modelo de formacao continuam presentes.
- `FormationData`, `FormationNewData`, posicoes, grupos e tipos de formato mantem a mesma estrutura encontrada na `0.5.451`. Isso confirma que posicao e formacao continuam sendo dados reais que o advisor deve registrar, e nao texto decorativo.
- Uma rotina de instanciacao de formacao passou a receber uma colecao somente-leitura de herois e a contagem explicita deles. E uma mudanca de carregamento/visual do grupo; nao e evidencia de uma nova formula de poder e nao deve ser transformada em multiplicador inventado pelo site.
- O conteudo baixado em `Sandbox/versiondata` contem camadas atuais de Lua, UI, modelos, audio, cenas, shader e cache de download. Entre os modulos observados ha fluxos de `worldboss`, `uicardformation` e `mount`, confirmando que Boss, equipe/formacao e montarias fazem parte do conteudo vivo, nao de um catalogo antigo congelado.

### O limite real do ADB normal

O processo do jogo estava em execucao e o armazenamento externo proprio do aplicativo podia ser inventariado. Porem, `run-as com.funfizz.palmon.gp` foi recusado pelo Android. Logo, a area privada onde o aplicativo pode manter preferencias, banco, sessao e cache protegido permanece inacessivel por ADB normal.

O armazenamento externo contem diretorios de cache e registros de jogo, alem do `Sandbox` de recursos. Alguns caches podem relacionar identidade ou sessao. Eles nao foram copiados, abertos, enviados ao repositorio nem usados para preencher o perfil. Forcar acesso a essa area exigiria burlar o isolamento do Android ou manipular autenticacao, o que nao e necessario nem aceitavel para o advisor.

### Consequencia para o importador

Esta leitura fecha uma decisao de arquitetura: o site nao deve tentar importar o perfil bruto a partir de cache do telefone. O caminho robusto e importar um snapshot visivel e editavel, preservando a origem de cada campo, e usar o APK somente para catalogo, imagens, nomes base/evoluido, tabelas e regras verificaveis.

O dado oficial que ainda precisa ser capturado por tela, video ou preenchimento guiado inclui: posse, sete slots e posicoes de cada time, poder exibido por time, Boss, Armigo, joias, equipamentos, arvores de evolucao, skills, buffs e Power Detail. Esses campos devem continuar editaveis e marcados como `print`, `usuario`, `calculado` ou `desconhecido`.

## Mapa geral do cliente

```text
Android / Google Play / SDK nativo
        |
        v
Unity 2019.4 + IL2CPP + xLua
        |
        +-- bootstrap: update de recursos, configuracao remota, SDK e login
        +-- dados estaticos: tabelas, imagens, prefabs e configuracao de jogo
        +-- sessao de jogo: conexao binaria, heartbeat e criptografia negociada
        +-- modulos Lua: HeroData, JewelPowerData, PowerData e outros
        +-- telas: leem os modulos em memoria e os dados estaticos
```

### Camadas confirmadas

1. **Unity IL2CPP com xLua.** O codigo compilado contem `libil2cpp`, `libxlua`, `global-metadata.dat`, wrappers Lua/C# e a maquina de estados `FsmLogin`.
2. **Conteudo estatico no pacote.** O XAPK contem o aplicativo base, uma biblioteca de assets e a configuracao arm64. Tabelas de jogo e scripts Lua sao carregados pelo cliente; parte dos scripts estava em formato protegido e foi analisada apos decodificacao local de leitura.
3. **Estado dinamico vindo do servidor.** Elenco, equipamentos, evolucoes, joias, ranking de poder e atualizacoes do perfil chegam como mensagens e viram objetos em memoria do cliente.
4. **Tela nao e fonte de verdade.** A tela mostra uma projecao de configuracao estatica + estado sincronizado. Ela nao e um banco de dados independente do servidor.

## Inicializacao, SDK e autenticacao

### O que o cliente contem

O `SDKManager` e a ponte Unity/Android concentram o ciclo do SDK. Ha metodos para:

- inicializar configuracao e SDK;
- fazer login e verificar `isSdkLogin`;
- abrir e vincular conta (`OpenAccount`, `IsBindAnyOne`);
- informar usuario ao SDK (`SetUserInfo(uid, serverGroup)`);
- compras e consulta de produtos;
- notificacoes, idioma, suporte, identificadores de dispositivo e telemetria;
- configuracao remota, CDN e Lua remota.

O cliente tambem expoe, para uso interno, propriedades como `appId`, `appUid`, `appToken`, `playerUid`, `appChannel`, `androidId`, `googleAid`, `clientIP`, `pushToken`, `sdkVer` e metadados do dispositivo. Isso confirma que a autenticacao passa por uma camada SDK nativa antes do jogo usar a sessao.

### O que cada dado significa

| Dado | Papel provavel | Deve entrar no advisor? |
| --- | --- | --- |
| `playerUid` | Identificador interno do personagem/conta de jogo. | Somente opcional e mascarado, para associar snapshots. |
| `serverGroup` | Agrupa ou identifica servidor/regiao. | Sim, pois separa perfis. |
| `appUid` | Identidade devolvida pelo SDK/plataforma. | Nao e necessario para recomendacoes. |
| `appToken` | Credencial temporaria ou de sessao do SDK. | Nao. Nunca salvar, mostrar, enviar ou versionar. |
| `pushToken` / FCM token | Endereco para notificacoes push. | Nao. |
| Android ID / Google advertising ID / IP | Identificadores de dispositivo ou rede. | Nao. |
| Compra, recibo e pedido | Dados financeiros e de comprovacao. | Nao. Apenas totais que o jogador quiser informar. |

### Fluxo autenticado que a auditoria suporta

**Confirmado:** existe um estado de login (`FsmLogin`), um `SDKManager.Login`, uma verificacao de login do SDK e campos de identidade usados pelo cliente.

**Inferencia forte:** o SDK autentica a conta/plataforma e entrega identidade ou prova de sessao; em seguida o cliente seleciona/recebe um servidor e abre o canal de jogo.

**Nao confirmado pelo APK estatico:** provedor exato de login do perfil atual, URL de autenticacao, validade/renovacao do token, campos exatos de cada pacote de login e algoritmo de emissao de token.

O advisor nao deve depender desse token. Ele expira, pode dar acesso a conta e nao e necessario para ler um snapshot que o jogador pode conferir e editar.

## Comunicacao com o servidor

### Pilhas de rede encontradas

O binario contem duas abstracoes de transporte:

| Componente | Evidencia | O que prova |
| --- | --- | --- |
| `NetManager` / `NetModel` / `NetChannel` | `ConnectServer(host, port)`, socket, `SendMsg`, `PickMsg`, `NetSendPackage`, `NetReceivePackage` | Ha um canal binario cliente-servidor com host e porta resolvidos em tempo de execucao. |
| `LIMNetManager` | campo `WebSocket`, `ConnectServer(url)`, `SendMsg(byte[])` | Ha tambem suporte a WebSocket. O APK estatico nao prova se ele e o canal principal da conta atual ou um canal complementar. |

O canal de socket tem:

- controle de estado e conectividade;
- heartbeat;
- empacotamento por tipo de mensagem (`ushort`) e corpo binario;
- troca de criptografia (`ExchangeEncrypt`, `OnExchangeCrypt`);
- estados de criptografia `None`, `Exchanging`, `ExchangeEncrypted` e `Done`;
- codificacao de mensagem com nonce (`EncodeWithEncrypy(..., clientTX, nonce)`).

### O que pode e nao pode ser concluido

| Pergunta | Resultado |
| --- | --- |
| O jogo conversa com um servidor depois do login? | Confirmado. |
| O estado do perfil chega em mensagens binaras? | Confirmado. |
| Ha troca de criptografia e nonce? | Confirmado. |
| Qual e o endereco ativo do servidor? | Nao confirmado; host/porta/url sao recebidos em execucao. |
| Qual algoritmo criptografico, chaves e formato integral de pacote? | Nao confirmado. Nao sera extraido nem reproduzido. |
| E possivel usar o advisor sem observar ou reproduzir esse trafego? | Sim. E o caminho recomendado. |

### Ordem funcional observada

```text
SDK / login
  -> configuracao do cliente e recursos
  -> selecao/conexao de servidor em tempo de execucao
  -> negociacao de criptografia + heartbeat
  -> mensagens S2C carregam estado
  -> modulos Lua atualizam modelos em memoria
  -> telas leem esses modelos
```

## Dados de perfil que o servidor entrega ao cliente

### Palmons e elenco

`HeroData` registra, entre outras, mensagens de lista, alteracao e evolucao de Palmons. A carga inicial atribui `msg.herolist` a `heroList`; cada entrada e indexada por `uniqueid` e por `heroid`.

| Area | Mensagens ou operacoes encontradas | Estado |
| --- | --- | --- |
| Elenco completo | `S2C_DseHeroData`, `C2S_DceHeroData` | Confirmado |
| Atualizacao de Palmon | `S2C_DseHeroUpdate` | Confirmado |
| Nivel | `S2C_DseHeroLevelUp` / `C2S_DceHeroLevelUp` | Confirmado |
| Estrelas | `C2S_DceHeroUpgradeStar` e resposta associada | Confirmado |
| Skills | `C2S_DceHeroUpgradeSkill` | Confirmado |
| Evolucao e potencia | mensagens de evolucao, reset e upgrade de potencia | Confirmado |
| Equipamentos | lista, adicionar, remover, vestir, tirar, intensificar, estrelas e exclusivo | Confirmado |
| Skins/cromas | dados, desbloqueio e uso de skin | Confirmado |
| Destino/Fate | leitura, ativacao, melhoria e reset | Confirmado |
| Status de batalha/ferimento | mensagens de status e injury | Confirmado |
| Renascer, breeding e troca inata | comandos e respostas correspondentes | Confirmado |

Campos diretamente demonstrados no fluxo: `uniqueid`, `heroid`, `lv`, `starlv`, `propertypower`, `equipidlist`, `evolveinfo`, status e dados complementares de skin/fate. O conjunto completo de campos de cada mensagem ainda depende do schema binario, que nao foi recuperado do XAPK nesta etapa.

### Poder do Palmon e poder do time

`propertypower` chega no objeto de Palmon sincronizado. O cliente o usa para ordenar elenco e para somar o poder do time. Isso e crucial:

- o poder mostrado de um Palmon nao e derivado somente de nivel e estrelas;
- efeitos globais, evolucao, equipamentos, Fate, habilidades, emblemas, temporada e formacao podem alterar atributos visiveis;
- o advisor deve preservar o valor sincronizado do jogo como referencia enquanto a conta detalhada nao estiver completa;
- um calculo interno so substitui esse valor quando todos os seus componentes forem conhecidos e a validacao bater.

Formula de poder de squad confirmada na logica cliente ja auditada:

```text
ceil((soma propertypower dos 7 Palmons
      + bonus do Boss
      + contribuicao Armigo/soldado)
     * (1 + bonus de aura por elemento))
+ poder de joias do squad
```

Os marcos de aura confirmados sao 3/4/5/6/7 Palmons do mesmo elemento, com 5%/10%/20%/25%/30%. Elementos diferentes que qualificam somam suas auras. Bonus de posicao/formacao pode alterar atributos e deve ser importado para o advisor, mas nao pode ser inventado como se fosse um multiplicador universal de poder.

### Joias

`JewelPowerData` pede a carga completa de joias ao entrar no jogo, recebe mochila, joias equipadas por grade, skill de joia e efeitos. Tambem recebe atualizacoes para compor, decompor, preencher e usar skills.

O advisor precisa separar:

1. joias guardadas na mochila;
2. joias equipadas em cada grade/grupo;
3. habilidades e efeitos de joia;
4. poder de joias que efetivamente participa do squad;
5. valores que pertencem apenas ao poder geral da conta.

### Detalhe de poder da conta

`PowerData` solicita `C2S_DceGetPowerDetailRankInfo` e recebe `S2C_DseGetPowerDetailRankInfo`. A tabela estatica `power_detail_type` enumera categorias de poder geral da conta:

- construcoes;
- tecnologia principal;
- Palmons: nivel, estrelas, skills, equipamentos e evolucao;
- soldados;
- talento;
- tecnologia e skills de guilda;
- VIP;
- politica secreta;
- titulos;
- cidade da alianca;
- spirit;
- equipamento e chips do comandante;
- arma estrategica;
- montarias da base;
- skins de construcao;
- Boss pet;
- emblemas;
- joias;
- tecnologia do deserto;
- decoracao da ilha.

Conclusao: **poder geral da conta e poder de um time sao metricas diferentes**. O perfil completo precisa registrar as duas coisas, com fontes e formulas separadas.

## Dados locais, cache e persistencia

### O que foi comprovado no codigo Lua analisado

No `HeroData.lua`, o uso de `PlayerPrefs` encontrado se limita a preferencias locais de interface:

- flag de Palmon recebido/novo, indexada pelo UID;
- estado visual de exibicao de estrelas por `heroUid`.

Esses usos nao sao o elenco completo, nem a prova de que nivel, poder, equipamentos ou recursos estejam persistidos localmente como fonte de verdade.

### Conclusao sobre arquivos do telefone/emulador

| Hipotese | Resultado atual |
| --- | --- |
| O pacote tem conteudo estatico e configuracoes locais | Confirmado. |
| Ha pequenas preferencias locais de UI | Confirmado. |
| O perfil inteiro fica em arquivo local reutilizavel sem servidor | Nao demonstrado; a logica aponta para dados sincronizados do servidor. |
| Pode existir cache/arquivo privado de sessao ou de perfil | Possivel, mas nao confirmado. |
| Ler esse cache basta para reconstituir tudo | Nao ha evidencia para afirmar. |

Nesta maquina, nao havia `adb` disponivel e o BlueStacks detectado nao expunha uma ponte ADB. Por isso, esta auditoria nao leu o sandbox privado do pacote e nao montou disco virtual de emulador. Isso foi intencional: varrer discos brutos pode misturar dados de outras aplicacoes e segredos de sessao.

Se for feita uma etapa dinamica, ela deve ser **somente leitura**, nesta ordem:

1. inventario de pacote, versao e permissoes;
2. listagem de diretorios e nomes de arquivos, sem abrir valores;
3. classificacao de cada arquivo: cache, configuracao, base local, log, preferencia ou segredo;
4. leitura apenas de arquivos explicitamente aprovados e com redacao automatica de token, identificador e recibo;
5. importacao apenas de campos de jogo aprovados para o perfil do advisor.

O advisor nunca deve guardar `appToken`, token FCM, cookies, recibos, senhas, identificadores de publicidade ou IP.

## O que e suficiente para o advisor

O advisor nao precisa de autenticacao do jogo. Precisa de um snapshot verificavel do estado de jogo.

### Snapshot de conta

| Grupo | Dados necessarios |
| --- | --- |
| Identidade | nome visivel, servidor e UID mascarado opcional |
| Poder | poder geral, detalhamento por categoria e data/hora do snapshot |
| Elenco | posse, forma base/evoluida, nivel, estrelas, poder sincronizado, skills, evolucao, equipamento, skin e Fate relevantes |
| Times 1-4 | sete slots, posicao, Boss, Armigo/soldado, joias e poder oficial de cada time |
| Montarias | todas as montarias possuidas, nivel, skill, recursos investidos e status de reset |
| Boss | posse, nivel, estrelas, skills, equipamentos/atributos e papel por equipe |
| Recursos | comida, ferraduras, orbs, itens de invocacao e materiais que o jogador quiser planejar |
| Aurora/Wishlist | Palmon alvo, afinidade, orbs e banner atual |
| Tecnologia | tecnologias, Desert Tech, emblemas, comandante, arma estrategica e buffs ativos |
| Temporada | servidor, temporada, dia e modificadores ativos |

### Ordem de confianca da importacao

1. Valor exibido pelo jogo em uma tela detalhada e confirmado pelo usuario.
2. Dados importados de um snapshot anterior com mesma versao e mesmo servidor.
3. Valor calculado pelo advisor com todos os componentes conhecidos e validado contra o jogo.
4. Estimativa marcada como estimativa; nunca apresentada como fato.

## Arquitetura recomendada para o importador do perfil

```text
prints/video da conta ou exportacao local aprovada
            |
            v
extrator por tela + OCR + reconhecimento de card
            |
            v
snapshot bruto com origem de cada campo
            |
            v
normalizador: ids, nome base/evoluido, forma, slot e versao
            |
            v
reconciliador: compara com catalogo do APK e pede so campos ausentes
            |
            v
perfil editavel, versionado e salvo no advisor
            |
            v
motor de recomendacao + validacoes de poder e recursos
```

Regras de produto que evitam os erros anteriores:

- Nenhum Palmon aparece como "seu" sem posse confirmada.
- Palmon possuido fica no topo; catalogo restante fica abaixo, em area separada.
- Cada campo editavel informa sua origem: print, usuario, calculado ou desconhecido.
- Nome base e nome evoluido sao duas formas do mesmo registro, nunca dois Palmons inventados.
- Uma troca de equipe recalcula previsao e invalida somente o valor que realmente ficou obsoleto.
- Poder oficial do time e poder calculado ficam lado a lado enquanto houver componente desconhecido.
- O advisor explica cada recomendacao: tier, elemento, aura, posicao, papel, custo e impacto no poder.
- Boss, montaria, Armigo, joia e posicao sao parte do mesmo plano de time; nao podem ser telas isoladas sem efeito no resultado.

## Captura minima para fechar o perfil atual

Para preencher sem adivinhar, a melhor captura e um video curto e continuo, nao dezenas de prints soltos. Ele deve mostrar:

1. perfil da conta e tela de detalhamento de poder;
2. cada um dos Times 1, 2, 3 e 4, incluindo poder, sete slots, posicoes, Boss e Armigo;
3. elenco completo por elemento, abrindo cada Palmon que esta em time ou e candidato de alto tier;
4. em cada detalhe: nivel, estrelas, forma, skills, arvores de evolucao e equipamentos;
5. joias e emblemas equipados;
6. Bosses e suas telas de evolucao/skills/equipamentos;
7. montarias e tela de reset/retorno quando houver;
8. Aurora/Wishlist e recursos de invocacao;
9. Power detail, Tech, Desert Tech, arma estrategica e buffs ativos.

O video deve ser usado apenas para criar um snapshot editavel. O sistema deve manter as imagens como evidencia local do perfil, nao como arte do site e nem como substituto para assets extraidos do APK.

## Lacunas abertas e proxima auditoria

| Tema | Situacao | Como fechar sem risco |
| --- | --- | --- |
| Versao atual do jogo | Checada na instalacao aberta: `0.5.465` (code `267`), com metadados e binario arm64 analisados. O catalogo e o balanceamento continuam sujeitos aos dados de conteudo da temporada. | Revalidar tabelas quando a temporada ou versao relevante mudar. |
| Endpoint ativo e schema binario completo | Nao confirmado estaticamente. | Nao e necessario para o advisor; nao tentar interceptar/reproduzir trafego. |
| Cache privado do aparelho | Deliberadamente nao lido. O Android bloqueou `run-as` para o pacote em ADB normal, e caches podem conter dados de identidade/sessao. | Manter o limite; usar somente capturas visiveis e campos editaveis. |
| Formula completa de cada `propertypower` | Componentes conhecidos, mas campos dinamicos globais ainda faltam. | Importar Power Detail, formacao, joias, equipamentos, tech e buffs e validar por exemplos do jogo. |
| Perfil atual completo | Prints existentes cobrem parte relevante, mas nao substituem todas as telas detalhadas. | Video de inventario conforme checklist acima. |

## Fontes locais de evidencia

Os artefatos abaixo foram usados, mas nao devem ser adicionados ao repositorio nem publicados por conterem material de engenharia e assets brutos:

- `analysis/xapk_0451/manifest.json`
- `analysis/xapk_0451/com.funfizz.palmon.gp.apk`
- `analysis/xapk_0451/assetLibrary.apk`
- `analysis/xapk_0451/config.arm64_v8a.apk`
- `analysis/il2cpp_dump/dump.cs`
- `analysis/working_power/decrypted/HeroData.lua`
- `analysis/working_power/decrypted/JewelPowerData.lua`
- `analysis/working_power/decrypted/PowerData.lua`
- `analysis/working_power/decrypted/UIHeroDescAttributes.lua`
- `analysis/working_power/decrypted/power_detail_type.lua`
- `analysis/apk_0_5_465/com.funfizz.palmon.gp.apk`
- `analysis/apk_0_5_465/config.arm64_v8a.apk`
- `analysis/apk_0_5_465/il2cpp_dump/dump.cs`

## Resultado da auditoria

O jogo usa o servidor como fonte de verdade para o perfil. A comparacao com a instalacao `0.5.465` confirmou que esse desenho continua valido: o APK e o `Sandbox` fornecem catalogo, assets, telas, regras parciais e modelos de dados, mas nao substituem o estado sincronizado da conta.

Portanto, o caminho correto para o site nao e tentar usar uma credencial do jogo. E um importador de perfil baseado em snapshot verificavel, com todos os campos editaveis, valores oficiais preservados, origem explicita, formulas auditadas e reconciliacao guiada dos campos que faltarem.
