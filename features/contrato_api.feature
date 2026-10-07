# language: pt
@VZS-142 @api @contrato
Funcionalidade: Catálogo e contrato HTTP da API

  Contexto:
    Dado que as requisições usam o cabeçalho "Content-Type" com valor "application/json"

  Cenário: Listar o catálogo fixo de produtos
    Quando envio uma requisição "GET /api/produtos"
    Então a API deve responder com status 200 e corpo JSON
    E cada produto deve conter id, nome, descricao, categoria e preco
    E os preços devem ser números em reais
    E o catálogo deve conter os produtos:
      | id   | nome                  | preco |
      | P001 | Camiseta Essencial    | 59.9  |
      | P002 | Calça Jeans Slim      | 139.9 |
      | P003 | Tênis Casual Urbano   | 189.9 |
      | P004 | Boné Aba Curva        | 49.9  |
      | P005 | Mochila Urbana 20L    | 100   |
      | P006 | Kit 3 Pares de Meias  | 29.9  |
      | P007 | Jaqueta Corta-Vento   | 229.9 |
      | P008 | Garrafa Térmica 750ml | 50    |

  Cenário: Consultar produto existente pelo identificador
    Quando envio uma requisição "GET /api/produtos/P001"
    Então a API deve responder com status 200 e corpo JSON
    E o campo "id" deve ser "P001"
    E o campo "nome" deve ser "Camiseta Essencial"
    E o campo "descricao" deve ser "Algodão penteado e corte reto."
    E o campo "categoria" deve ser "Vestuário"
    E o campo "preco" deve ser 59.9

  Esquema do Cenário: Retornar erros de rota, método e produto
    Quando envio uma requisição "<requisicao>"
    Então a API deve responder com status <status> e corpo JSON
    E o campo "erro.codigo" deve ser "<codigo>"
    E o erro deve seguir o formato documentado

    Exemplos:
      | requisicao                   | status | codigo                 |
      | GET /api/produtos/INEXISTENTE  | 404    | PRODUTO_NAO_ENCONTRADO  |
      | GET /api/rota-inexistente     | 404    | ROTA_NAO_ENCONTRADA     |
      | POST /api/produtos            | 405    | METODO_NAO_PERMITIDO    |
      | GET /api/carrinho/calcular    | 405    | METODO_NAO_PERMITIDO    |
      | GET /api/pedidos              | 405    | METODO_NAO_PERMITIDO    |

  Esquema do Cenário: Recusar corpo que não seja um objeto JSON válido
    Quando envio para "<endpoint>" o corpo literal "<corpo>"
    Então a API deve responder com status 400 e corpo JSON
    E o campo "erro.codigo" deve ser "JSON_INVALIDO"
    E o erro deve seguir o formato documentado

    Exemplos:
      | endpoint                   | corpo    |
      | POST /api/carrinho/calcular | {        |
      | POST /api/carrinho/calcular | null     |
      | POST /api/carrinho/calcular | []       |
      | POST /api/carrinho/calcular | "texto"  |
      | POST /api/pedidos           | {        |
      | POST /api/pedidos           | null     |
      | POST /api/pedidos           | []       |
      | POST /api/pedidos           | "texto"  |
