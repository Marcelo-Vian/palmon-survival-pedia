# Atualizar Site Da Loja Em 1 Clique

## Onde Colocar O ZIP

Coloque o ZIP exportado pelo Android Helper nesta pasta:

`D:\Linkedin\palmon_survival_pedia\COLOQUE_O_ZIP_AQUI`

Depois volte para a pasta principal e clique em:

`D:\Linkedin\palmon_survival_pedia\ATUALIZAR_SITE_LOJA_1_CLIQUE.bat`

Tambem funciona arrastar o ZIP diretamente em cima do arquivo `.bat`.

## O Que O Clique Faz

1. Importa o ZIP da pasta `COLOQUE_O_ZIP_AQUI`, se existir.
2. Copia as imagens para `D:\Linkedin\palmon_survival_prints\loja\prints`.
3. Usa o `shop_active_offers_*.json` mais recente.
4. Gera as miniaturas dos pacotes.
5. Reconstrói `palmon_shop_captures.html`.
6. Atualiza o preview da página inicial.
7. Valida ofertas, miniaturas e links.
8. Faz `git add`, `git commit` e `git push`.
9. Publica no GitHub Pages.

Link final:

`https://marcelo-vian.github.io/palmon-survival-pedia/palmon_shop_captures.html`

Logs:

`D:\Linkedin\palmon_survival_pedia\logs`

## Importante

Se o ZIP tiver pacotes novos, a rotina importa os prints, mas esses pacotes ainda precisam ser transformados em linhas da base de dados antes de aparecerem como ofertas calculadas no site.

Se clicar e parecer que nada aconteceu, confira se voce clicou no `.bat`, nao no `.ps1`. O `.bat` deixa a janela aberta e mostra o caminho do log.
