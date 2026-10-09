# language: pt
@VZS-142 @calculo
Funcionalidade: Cálculo do subtotal, desconto, frete e total
  Os cálculos da API devem ser exibidos pela interface sem divergência.

  @CA06 @CA07 @CA11 @api @interface
  Esquema do Cenário: Calcular frete nos limites do subtotal
    Dado um carrinho com os itens "<itens>"
    Quando calculo o carrinho sem cupom
    Então a API deve responder com status 200
    E os valores monetários retornados devem ter precisão de até 2 casas decimais
    E a interface deve exibir os valores com 2 casas decimais
    E a API e a interface devem apresentar o resumo:
      | subtotal | desconto | frete   | freteGratis | valorFaltanteFreteGratis | total   |
      | <subtotal> | 0,00   | <frete> | <gratis>    | <faltante>              | <total> |

    Exemplos:
      | itens          | subtotal | frete | gratis | faltante | total  |
      | P003:1         | 189,90   | 19,90 | falso  | 10,10    | 209,80 |
      | P002:1,P001:1  | 199,80   | 19,90 | falso  | 0,20     | 219,70 |
      | P005:2         | 200,00   | 0,00  | verdadeiro | 0,00 | 200,00 |
      | P007:1         | 229,90   | 0,00  | verdadeiro | 0,00 | 229,90 |

  @CA01 @CA06 @CA08 @CA09 @CA11 @api @interface
  Esquema do Cenário: Calcular frete pelo subtotal anterior ao desconto
    Dado um carrinho com os itens "<itens>"
    Quando calculo o carrinho com o cupom "BEMVINDO10"
    Então a API deve responder com status 200
    E a API e a interface devem apresentar o resumo:
      | subtotal   | desconto   | frete   | freteGratis | valorFaltanteFreteGratis | total   |
      | <subtotal> | <desconto> | <frete> | <gratis>    | <faltante>              | <total> |

    Exemplos:
      | itens         | subtotal | desconto | frete | gratis     | faltante | total  |
      | P005:1        | 100,00   | 10,00    | 19,90 | falso      | 100,00   | 109,90 |
      | P002:1,P001:1 | 199,80   | 19,98    | 19,90 | falso      | 0,20     | 199,72 |
      | P005:2        | 200,00   | 20,00    | 0,00  | verdadeiro | 0,00     | 180,00 |
      | P002:1,P004:2 | 239,70   | 23,97    | 0,00  | verdadeiro | 0,00     | 215,73 |
      | P001:3        | 179,70   | 17,97    | 19,90 | falso      | 20,30    | 181,63 |

  @CA07 @interface
  Cenário: Informar quanto falta para frete grátis
    Dado que o carrinho contém 1 unidade do produto "P003" de R$ 189,90
    Quando visualizo o carrinho
    Então o frete deve ser R$ 19,90
    E o carrinho deve informar que faltam R$ 10,10 para o frete grátis

  @CA06 @CA07 @CA08 @interface
  Cenário: Recalcular frete após alterar a quantidade com cupom aplicado
    Dado que o carrinho contém 1 unidade do produto "P005" de R$ 100,00
    E apliquei o cupom "BEMVINDO10"
    Quando altero a quantidade do produto "P005" para 2
    Então o subtotal deve ser R$ 200,00
    E o desconto deve ser R$ 20,00
    E o frete deve ser R$ 0,00
    E o total deve ser R$ 180,00
    Quando altero a quantidade do produto "P005" para 1
    Então o subtotal deve ser R$ 100,00
    E o desconto deve ser R$ 10,00
    E o frete deve ser R$ 19,90
    E o total deve ser R$ 109,90
    E o carrinho deve informar que faltam R$ 100,00 para o frete grátis

  @api
  Cenário: Detalhar valores calculados por item
    Quando envio para "POST /api/carrinho/calcular" o JSON:
      """
      {"itens":[{"produtoId":"P002","quantidade":1},{"produtoId":"P004","quantidade":2}],"cupom":"BEMVINDO10"}
      """
    Então a API deve responder com status 200
    E os itens da resposta devem ser:
      | produtoId | nome            | precoUnitario | quantidade | total |
      | P002      | Calça Jeans Slim | 139.9        | 1          | 139.9 |
      | P004      | Boné Aba Curva   | 49.9         | 2          | 99.8  |
    E o campo "cupom.codigo" deve ser "BEMVINDO10"
    E o campo "cupom.aplicado" deve ser verdadeiro
    E o campo "cupom.mensagem" deve ser "Cupom aplicado: 10% de desconto nos produtos."
