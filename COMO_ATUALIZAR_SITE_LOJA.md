# Atualizar site da loja em 1 clique

Use este arquivo:

`ATUALIZAR_SITE_LOJA_1_CLIQUE.bat`

O que ele faz:

1. Usa o `shop_active_offers_*.json` mais recente.
2. Gera as miniaturas dos pacotes.
3. Reconstrói `palmon_shop_captures.html`.
4. Atualiza o preview da página inicial.
5. Valida se existem ofertas, miniaturas e se não voltou print completo antigo.
6. Faz `git add`, `git commit` e `git push`.
7. Publica no GitHub Pages.

Link final:

`https://marcelo-vian.github.io/palmon-survival-pedia/palmon_shop_captures.html`

Logs:

`logs/update-shop-YYYYMMDD-HHMMSS.log`

Importante:

- Se você apenas tirar prints novos, o botão consegue republicar a base atual, mas não inventa dados novos.
- Quando aparecer pacote novo, preço novo ou item novo, primeiro precisamos transformar os prints em linhas no `shop_active_offers_*.json` e ajustar recortes quando necessário.
- Depois disso, o clique publica tudo sozinho.
