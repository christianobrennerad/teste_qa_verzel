# language: pt
@VZS-142 @pedidos
Funcionalidade: Validação e confirmação do pedido

  @api
  Esquema do Cenário: Confirmar pedido com ou sem cupom
    Quando envio para "POST /api/pedidos" o JSON:
      """
      {"cliente":{"nome":"Maria Silva","email":"maria@exemplo.com","cep":"01310-100"},"itens":[{"produtoId":"P005","quantidade":1}]<campoCupom>}
      """
    Então a API deve responder com status 201
    E o campo "numero" deve corresponder à expressão regular "^VZ-[0-9]{6}$"
    E o campo "criadoEm" deve conter uma data e hora no formato ISO 8601
    E o campo "cliente.nome" deve ser "Maria Silva"
    E o campo "cliente.email" deve ser "maria@exemplo.com"
    E o campo "cliente.cep" deve ser "01310100"
    E o subtotal deve ser R$ 100,00
    E o desconto deve ser R$ <desconto>
    E o frete deve ser R$ 19,90
    E o campo "freteGratis" deve ser falso
    E o campo "valorFaltanteFreteGratis" deve ser 100
    E o total deve ser R$ <total>

    Exemplos:
      | campoCupom              | desconto | total  |
      |                         | 0,00     | 119,90 |
      | ,"cupom":"BEMVINDO10"    | 10,00    | 109,90 |

  @CA02 @api
  Cenário: Normalizar o cupom também na confirmação do pedido
    Quando envio para "POST /api/pedidos" o JSON:
      """
      {"cliente":{"nome":"Maria Silva","email":"maria@exemplo.com","cep":"01310100"},"itens":[{"produtoId":"P005","quantidade":1}],"cupom":"  bemvindo10  "}
      """
    Então a API deve responder com status 201
    E o campo "cupom.codigo" deve ser "BEMVINDO10"
    E o campo "cupom.aplicado" deve ser verdadeiro
    E o total deve ser R$ 109,90

  @CA03 @CA04 @api
  Esquema do Cenário: Diferenciar cupom inválido no cálculo e na confirmação
    Dado os itens de uma unidade do produto "P005"
    Quando calculo o carrinho pela API com o cupom "<cupom>"
    Então a API deve responder com status 200
    E o campo "cupom.aplicado" deve ser falso
    E o campo "cupom.mensagem" deve ser "<mensagem>"
    E o desconto deve ser R$ 0,00
    E o total deve ser R$ 119,90
    Quando confirmo pela API um pedido com os mesmos itens, cliente válido e o cupom "<cupom>"
    Então a API deve responder com status 422
    E o campo "erro.codigo" deve ser "<codigo>"
    E o pedido não deve ser confirmado

    Exemplos:
      | cupom       | mensagem        | codigo         |
      | INEXISTENTE | Cupom inválido. | CUPOM_INVALIDO |
      | VERAO2026   | Cupom expirado. | CUPOM_EXPIRADO |

  @api @CA08 @CA11
  Cenário: Manter o resumo do cálculo na confirmação
    Dado os itens de 2 unidades do produto "P005"
    Quando calculo o carrinho pela API com o cupom "BEMVINDO10"
    Então a API deve responder com status 200
    E o subtotal deve ser R$ 200,00
    E o desconto deve ser R$ 20,00
    E o frete deve ser R$ 0,00
    E o total deve ser R$ 180,00
    Quando confirmo pela API um pedido com os mesmos itens, cliente válido e o cupom "BEMVINDO10"
    Então a API deve responder com status 201
    E os campos de itens, subtotal, desconto, frete, freteGratis, valorFaltanteFreteGratis, total e cupom devem ser iguais aos do cálculo

  @api
  Esquema do Cenário: Aceitar CEP com ou sem hífen
    Quando confirmo um pedido de uma unidade do produto "P005" com os dados:
      | nome        | email             | cep   |
      | Maria Silva | maria@exemplo.com | <cep> |
    Então a API deve responder com status 201
    E o campo "cliente.cep" deve ser "01310100"

    Exemplos:
      | cep       |
      | 01310-100 |
      | 01310100  |

  @api
  Esquema do Cenário: Rejeitar dados inválidos do cliente
    Quando confirmo um pedido de uma unidade do produto "P005" com os dados:
      | nome   | email   | cep   |
      | <nome> | <email> | <cep> |
    Então a API deve responder com status 422
    E o campo "erro.codigo" deve ser "DADOS_INVALIDOS"
    E os detalhes em "campos" devem identificar "<campo>" como inválido
    E o pedido não deve ser confirmado

    Exemplos:
      | nome        | email             | cep       | campo |
      | Maria       | maria@exemplo.com | 01310100  | nome  |
      |             | maria@exemplo.com | 01310100  | nome  |
      | Maria Silva | maria.exemplo.com | 01310100  | email |
      | Maria Silva |                   | 01310100  | email |
      | Maria Silva | maria@exemplo.com | 0131010   | cep   |
      | Maria Silva | maria@exemplo.com | 013101000 | cep   |
      | Maria Silva | maria@exemplo.com | ABCDEFGH  | cep   |
      | Maria Silva | maria@exemplo.com |           | cep   |

  @api
  Cenário: Informar múltiplos dados inválidos do cliente
    Quando confirmo um pedido de uma unidade do produto "P005" com os dados:
      | nome  | email    | cep |
      | Maria | invalido | 123 |
    Então a API deve responder com status 422
    E o campo "erro.codigo" deve ser "DADOS_INVALIDOS"
    E os detalhes em "campos" devem identificar nome, email e cep como inválidos

  @interface
  Cenário: Concluir compra com pagamento na entrega
    Dado que o carrinho contém 1 unidade do produto "P005" de R$ 100,00
    E apliquei o cupom "BEMVINDO10"
    Quando finalizo a compra com nome "Maria Silva", e-mail "maria@exemplo.com" e CEP "01310-100"
    Então deve ser exibida a confirmação com número no formato "VZ-000000"
    E o total confirmado deve ser R$ 109,90
    E o pagamento deve ser na entrega
    E não deve existir etapa de pagamento online
