# language: pt
@VZS-142 @isolamento
Funcionalidade: Isolamento do carrinho e ausência de persistência da API
  O ambiente compartilhado não deve ser tratado como uma loja com pedidos persistidos ou estoque.

  @interface
  Esquema do Cenário: Iniciar outro contexto de navegação com carrinho vazio
    Dado que adicionei o produto "P005" ao carrinho da aba atual
    Quando abro a loja em "<contexto>"
    Então o carrinho do novo contexto deve estar vazio
    E o carrinho da aba original deve continuar contendo o produto "P005"

    Exemplos:
      | contexto        |
      | outra aba       |
      | outro navegador |
      | janela anônima  |

  @api
  Cenário: Calcular cada chamada sem reutilizar itens ou cupom anteriores
    Quando envio para "POST /api/carrinho/calcular" o JSON:
      """
      {"itens":[{"produtoId":"P005","quantidade":2}],"cupom":"BEMVINDO10"}
      """
    Então a API deve responder com status 200
    E o total deve ser R$ 180,00
    Quando envio para "POST /api/carrinho/calcular" o JSON:
      """
      {"itens":[{"produtoId":"P008","quantidade":1}]}
      """
    Então a API deve responder com status 200
    E a resposta deve conter apenas o produto "P008" com quantidade 1
    E o subtotal deve ser R$ 50,00
    E o desconto deve ser R$ 0,00
    E o frete deve ser R$ 19,90
    E o total deve ser R$ 69,90

  @api
  Cenário: Confirmar pedidos repetidos sem consumir estoque
    Dado um pedido com cliente válido e 5 unidades do produto "P005"
    Quando confirmo esse pedido duas vezes em requisições independentes
    Então cada requisição deve responder com status 201
    E cada resposta deve conter subtotal de R$ 500,00 e total de R$ 500,00
    E o produto "P005" deve continuar disponível no catálogo pelo preço de R$ 100,00
