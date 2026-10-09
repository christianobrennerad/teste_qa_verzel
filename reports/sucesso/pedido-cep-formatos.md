# Relatório de teste — Aceitar CEP com ou sem hífen

**Resultado: Aprovado.** A loja confirmou os dois pedidos, aceitando o CEP com e sem hífen. Nas duas respostas, o CEP foi apresentado como `01310100`, sem hífen e mantendo o zero inicial.

**Data do teste:** 08/10/2026, às 10h46min46s (America/Fortaleza). As duas chamadas foram concluídas nesse segundo; os horários registrados estão nas evidências.

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao); cenário em [pedidos.feature](../../features/pedidos.feature).

## O que foi testado

Confirmamos dois pedidos independentes, cada um com uma Mochila Urbana 20L (P005), de R$ 100,00, sem cupom. Usamos os dados de exemplo do cenário: Maria Silva e maria@exemplo.com. Entre as chamadas, alteramos somente o CEP: primeiro `01310-100`, depois `01310100`.

O teste foi realizado diretamente no serviço da loja (API). Conferimos se os dois formatos eram aceitos e se o CEP retornava como texto de oito dígitos, sem hífen e sem perder o zero inicial.

## Cenário BDD

```gherkin
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
```

## Resultados da conferência

### CEP com hífen: 01310-100

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Confirmação aceita | Status 201 | Status 201 | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido | Aprovado |
| CEP retornado (`cliente.cep`) | Texto `01310100` | Texto `01310100`, com oito dígitos e zero inicial | Aprovado |
| Produto e quantidade | Uma unidade de P005 | Uma unidade de Mochila Urbana 20L (P005) | Aprovado |

A resposta identificou a confirmação como **VZ-891430**.

### CEP sem hífen: 01310100

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Confirmação aceita | Status 201 | Status 201 | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido | Aprovado |
| CEP retornado (`cliente.cep`) | Texto `01310100` | Texto `01310100`, com oito dígitos e zero inicial | Aprovado |
| Produto e quantidade | Uma unidade de P005 | Uma unidade de Mochila Urbana 20L (P005) | Aprovado |

A resposta identificou a confirmação como **VZ-787088**.

O status 201 indica que a loja aceitou a confirmação do pedido. JSON é o formato dos dados recebidos. Os dois exemplos passaram, com oito verificações aprovadas no total.

## Falhas encontradas

Nenhuma falha foi encontrada nesta execução. O CEP com hífen foi convertido para o formato esperado; o CEP sem hífen foi mantido. Ambos preservaram o zero inicial. Não houve bloqueios nem etapas sem execução.

## Comprovantes do teste

| Chamada | Envio | Resposta | Validação | Execução |
| --- | --- | --- | --- | --- |
| CEP com hífen | [Corpo enviado](evidencias/pedido-cep-formatos/20261008-104646/01-com-hifen/corpo-enviado.json) | [HTTP completo](evidencias/pedido-cep-formatos/20261008-104646/01-com-hifen/resposta-http.txt) e [JSON recebido](evidencias/pedido-cep-formatos/20261008-104646/01-com-hifen/corpo-recebido.json) | [Conferência](evidencias/pedido-cep-formatos/20261008-104646/01-com-hifen/validacao-api.json) | [Comando](evidencias/pedido-cep-formatos/20261008-104646/01-com-hifen/comando.txt) e [erros da ferramenta](evidencias/pedido-cep-formatos/20261008-104646/01-com-hifen/curl-stderr.txt) |
| CEP sem hífen | [Corpo enviado](evidencias/pedido-cep-formatos/20261008-104646/02-sem-hifen/corpo-enviado.json) | [HTTP completo](evidencias/pedido-cep-formatos/20261008-104646/02-sem-hifen/resposta-http.txt) e [JSON recebido](evidencias/pedido-cep-formatos/20261008-104646/02-sem-hifen/corpo-recebido.json) | [Conferência](evidencias/pedido-cep-formatos/20261008-104646/02-sem-hifen/validacao-api.json) | [Comando](evidencias/pedido-cep-formatos/20261008-104646/02-sem-hifen/comando.txt) e [erros da ferramenta](evidencias/pedido-cep-formatos/20261008-104646/02-sem-hifen/curl-stderr.txt) |

- [Resumo dos resultados e horários](evidencias/pedido-cep-formatos/20261008-104646/resumo-validacao.json).
- [Casos e valores esperados](evidencias/pedido-cep-formatos/20261008-104646/criterios.json).
- [Script executado](evidencias/pedido-cep-formatos/20261008-104646/teste-api.py).

Os arquivos de erros do curl estão vazios. A ferramenta terminou sem erro de execução nas duas chamadas. As respostas HTTP completas preservam o status e os cabeçalhos recebidos; as validações registram horário, comando e comparação dos campos.

Para reproduzir as chamadas:

```bash
curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos' \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Maria Silva","email":"maria@exemplo.com","cep":"01310-100"},"itens":[{"produtoId":"P005","quantidade":1}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos' \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Maria Silva","email":"maria@exemplo.com","cep":"01310100"},"itens":[{"produtoId":"P005","quantidade":1}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

O marcador `CURL_HTTP_STATUS` foi acrescentado pela ferramenta e não faz parte da resposta da loja. A avaliação considerou o status final da aplicação e manteve a verificação de segurança da conexão ativa. O CEP foi comparado como texto exato.

## Limite desta avaliação

A aprovação se aplica aos dois formatos de CEP apresentados e às duas chamadas desta execução. Não foram avaliados CEPs inválidos, espaços, outros endereços, consulta de endereço ou a interface da loja.

Conforme a documentação, os pedidos e seus números são fictícios neste ambiente; pedidos não são armazenados. A aprovação se refere à aceitação e ao formato do CEP nas respostas observadas.
