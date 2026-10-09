# language: pt
@VZS-142 @interface @cupons
Funcionalidade: Aplicação e remoção de cupom no carrinho
  Como cliente da Verzel Store
  Quero aplicar um cupom válido ao carrinho
  Para obter desconto sobre os produtos

  Contexto:
    Dado que o carrinho contém 1 unidade do produto "P005" de R$ 100,00

  @CA01 @CA09
  Cenário: Aplicar desconto apenas aos produtos
    Quando aplico o cupom "BEMVINDO10"
    Então o subtotal deve ser R$ 100,00
    E o desconto deve ser R$ 10,00
    E o frete deve ser R$ 19,90
    E o total deve ser R$ 109,90
    E deve ser exibida a mensagem "Cupom aplicado: 10% de desconto nos produtos."

  @CA02
  Esquema do Cenário: Normalizar maiúsculas, minúsculas e espaços externos
    Quando aplico o cupom "<cupom>"
    Então o cupom "BEMVINDO10" deve estar aplicado
    E o desconto deve ser R$ 10,00
    E o total deve ser R$ 109,90

    Exemplos:
      | cupom          |
      | bemvindo10     |
      | BeMvInDo10     |

  @CA02
  Cenário: Ignorar espaços reais no início e no fim do cupom
    Quando aplico o código de cupom contido entre as aspas do texto:
      """
      "  bemvindo10  "
      """
    Então o cupom "BEMVINDO10" deve estar aplicado
    E o desconto deve ser R$ 10,00
    E o total deve ser R$ 109,90

  @CA03 @CA04
  Esquema do Cenário: Recusar cupom inexistente ou expirado
    Quando aplico o cupom "<cupom>"
    Então deve ser exibida a mensagem "<mensagem>"
    E nenhum cupom deve estar aplicado
    E o desconto deve ser R$ 0,00
    E o total deve ser R$ 119,90

    Exemplos:
      | cupom       | mensagem        |
      | INEXISTENTE | Cupom inválido. |
      | VERAO2026   | Cupom expirado. |

  @CA05
  Cenário: Manter apenas um cupom aplicado
    Dado que apliquei o cupom "BEMVINDO10"
    Quando tento aplicar novamente o cupom "BEMVINDO10" sem remover o atual
    Então deve continuar existindo apenas um cupom aplicado
    E o desconto deve continuar sendo R$ 10,00
    E o total deve continuar sendo R$ 109,90

  @CA05
  Cenário: Remover o cupom e recalcular o carrinho
    Dado que apliquei o cupom "BEMVINDO10"
    Quando removo o cupom atual
    Então nenhum cupom deve estar aplicado
    E o desconto deve ser R$ 0,00
    E o frete deve ser R$ 19,90
    E o total deve ser R$ 119,90
    Quando aplico o cupom "BEMVINDO10"
    Então o desconto deve ser R$ 10,00
    E deve existir apenas um cupom aplicado

  @CA05 @CA04
  Cenário: Remover o cupom válido antes de tentar aplicar outro
    Dado que apliquei o cupom "BEMVINDO10"
    Quando removo o cupom atual
    E aplico o cupom "VERAO2026"
    Então deve ser exibida a mensagem "Cupom expirado."
    E nenhum cupom deve estar aplicado
    E o desconto deve ser R$ 0,00
    E o total deve ser R$ 119,90
