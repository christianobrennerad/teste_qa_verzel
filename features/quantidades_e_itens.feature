# language: pt
@VZS-142 @itens
Funcionalidade: Validação dos itens e limite por produto

  @CA10 @interface
  Cenário: Permitir até 5 unidades de um produto
    Dado que o carrinho contém 4 unidades do produto "P008" de R$ 50,00
    Quando adiciono mais 1 unidade do produto "P008"
    Então o carrinho deve conter 5 unidades do produto "P008"
    E o subtotal deve ser R$ 250,00
    Quando tento adicionar mais 1 unidade do produto "P008"
    Então o carrinho deve continuar contendo 5 unidades do produto "P008"
    E o subtotal deve continuar sendo R$ 250,00

  @CA10 @interface
  Cenário: Limitar cada produto independentemente
    Dado que o carrinho contém 5 unidades do produto "P008" de R$ 50,00
    Quando adiciono 5 unidades do produto "P005" de R$ 100,00
    Então o carrinho deve conter 5 unidades de cada produto
    E o subtotal deve ser R$ 750,00

  @CA10 @api
  Esquema do Cenário: Aceitar os limites válidos de quantidade
    Quando envio para "<endpoint>" uma requisição com cliente válido e os itens:
      """
      [{"produtoId":"P008","quantidade":<quantidade>}]
      """
    Então a API deve responder com status <status>
    E o subtotal deve ser R$ <subtotal>

    Exemplos:
      | endpoint                   | quantidade | status | subtotal |
      | POST /api/carrinho/calcular | 1          | 200    | 50,00    |
      | POST /api/carrinho/calcular | 5          | 200    | 250,00   |
      | POST /api/pedidos           | 1          | 201    | 50,00    |
      | POST /api/pedidos           | 5          | 201    | 250,00   |

  @api
  Esquema do Cenário: Rejeitar itens inválidos nas duas operações
    Quando envio para "POST /api/carrinho/calcular" o corpo "<corpo>"
    Então a API deve responder com status 422
    E o campo "erro.codigo" deve ser "<codigo>"
    E o erro deve seguir o formato documentado com código, mensagem e campo relacionado
    Quando envio para "POST /api/pedidos" o mesmo corpo com cliente válido
    Então a API deve responder com status 422
    E o campo "erro.codigo" deve ser "<codigo>"
    E o erro deve seguir o formato documentado com código, mensagem e campo relacionado

    Exemplos:
      | corpo                                                     | codigo                     |
      | {}                                                        | ITENS_OBRIGATORIOS         |
      | {"itens":[]}                                              | ITENS_OBRIGATORIOS         |
      | {"itens":[null]}                                          | ITEM_INVALIDO              |
      | {"itens":["P001"]}                                        | ITEM_INVALIDO              |
      | {"itens":[{"quantidade":1}]}                               | ITEM_INVALIDO              |
      | {"itens":[{"produtoId":"P001"}]}                           | ITEM_INVALIDO              |
      | {"itens":[{"produtoId":"INEXISTENTE","quantidade":1}]}      | PRODUTO_NAO_ENCONTRADO      |
      | {"itens":[{"produtoId":"P001","quantidade":0}]}            | QUANTIDADE_INVALIDA        |
      | {"itens":[{"produtoId":"P001","quantidade":-1}]}           | QUANTIDADE_INVALIDA        |
      | {"itens":[{"produtoId":"P001","quantidade":1.5}]}          | QUANTIDADE_INVALIDA        |
      | {"itens":[{"produtoId":"P001","quantidade":"1"}]}          | QUANTIDADE_INVALIDA        |
      | {"itens":[{"produtoId":"P001","quantidade":null}]}         | QUANTIDADE_INVALIDA        |
      | {"itens":[{"produtoId":"P001","quantidade":6}]}            | QUANTIDADE_MAXIMA_EXCEDIDA  |
      | {"itens":[{"produtoId":"P001","quantidade":100}]}          | QUANTIDADE_MAXIMA_EXCEDIDA  |

  @api @CA10
  Cenário: Rejeitar produto duplicado em vez de contornar o limite por produto
    Dado o corpo de requisição:
      """
      {"itens":[{"produtoId":"P001","quantidade":3},{"produtoId":"P001","quantidade":3}]}
      """
    Quando envio esse corpo para "POST /api/carrinho/calcular"
    Então a API deve responder com status 422
    E o campo "erro.codigo" deve ser "ITEM_DUPLICADO"
    Quando envio esse corpo para "POST /api/pedidos" com cliente válido
    Então a API deve responder com status 422
    E o campo "erro.codigo" deve ser "ITEM_DUPLICADO"

  @api
  Cenário: Identificar o campo da quantidade inválida
    Quando envio para "POST /api/carrinho/calcular" o JSON:
      """
      {"itens":[{"produtoId":"P001","quantidade":0}]}
      """
    Então a API deve responder com status 422
    E o campo "erro.codigo" deve ser "QUANTIDADE_INVALIDA"
    E o campo "erro.mensagem" deve ser "A quantidade deve ser um número inteiro maior ou igual a 1."
    E o campo "erro.campo" deve ser "itens[0].quantidade"
