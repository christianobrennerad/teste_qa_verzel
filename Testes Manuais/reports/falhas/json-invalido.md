# Relatório de teste — Recusa de corpo JSON inválido

**Resultado: Falhou na verificação do formato documentado.** Os oito casos foram recusados corretamente, com status 400 e código JSON_INVALIDO. Porém, nenhum erro incluiu a informação `campo` apresentada no formato comum da documentação. Não houve bloqueio de execução.

**Data do teste:** 07/10/2026, às 23h24 (horário de Fortaleza).

**Loja:** Verzel Store, ambiente de testes.

**Referência:** VZS-142, versão 2.3.0; cenário em [contrato_api.feature](../../features/contrato_api.feature).

## O que foi testado

Enviamos quatro tipos de conteúdo inadequado para calcular o carrinho e confirmar um pedido: um texto incompleto (`{`), um valor nulo (`null`), uma lista vazia (`[]`) e o texto `"texto"`.

A loja exige um objeto de dados, como `{"itens":[]}`. Os conteúdos `null`, `[]` e `"texto"` são válidos no formato JSON, mas não são objetos. O conteúdo `{` é incompleto. Todos devem ser recusados antes das demais validações de carrinho ou pedido.

## Cenário BDD

API significa o serviço que recebe os dados. Status 400 indica que a solicitação foi recusada por conteúdo inadequado. JSON é o formato dos dados. O código JSON_INVALIDO identifica o motivo da recusa.

```gherkin
Contexto:
  Dado que as requisições usam o cabeçalho "Content-Type" com valor "application/json"

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
```

Os corpos foram enviados literalmente, sem acrescentar campos, corrigir o conteúdo ou remover as aspas de `"texto"`.

## Resultados da conferência

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Execução das solicitações | 8 casos concluídos | 8 casos concluídos, sem erro de conexão | Aprovado |
| Recusa do conteúdo inadequado | Status 400 nos 8 casos | Status 400 nos 8 casos | Aprovado |
| Identificação do motivo | JSON_INVALIDO nos 8 casos | JSON_INVALIDO nos 8 casos | Aprovado |
| Formato dos dados recebidos | Resposta em JSON | JSON válido nos 8 casos | Aprovado |
| Código e mensagem do erro | Presentes no objeto erro | Presentes nos 8 casos | Aprovado |
| Formato comum documentado | Objeto erro com codigo, mensagem e campo | campo ausente nos 8 casos | Falhou |

### Resultado por caso

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| `POST /api/carrinho/calcular` com `{` | 400; JSON_INVALIDO; erro com codigo, mensagem e campo | 400; JSON_INVALIDO; campo ausente | Falhou |
| `POST /api/carrinho/calcular` com `null` | 400; JSON_INVALIDO; erro com codigo, mensagem e campo | 400; JSON_INVALIDO; campo ausente | Falhou |
| `POST /api/carrinho/calcular` com `[]` | 400; JSON_INVALIDO; erro com codigo, mensagem e campo | 400; JSON_INVALIDO; campo ausente | Falhou |
| `POST /api/carrinho/calcular` com `"texto"` | 400; JSON_INVALIDO; erro com codigo, mensagem e campo | 400; JSON_INVALIDO; campo ausente | Falhou |
| `POST /api/pedidos` com `{` | 400; JSON_INVALIDO; erro com codigo, mensagem e campo | 400; JSON_INVALIDO; campo ausente | Falhou |
| `POST /api/pedidos` com `null` | 400; JSON_INVALIDO; erro com codigo, mensagem e campo | 400; JSON_INVALIDO; campo ausente | Falhou |
| `POST /api/pedidos` com `[]` | 400; JSON_INVALIDO; erro com codigo, mensagem e campo | 400; JSON_INVALIDO; campo ausente | Falhou |
| `POST /api/pedidos` com `"texto"` | 400; JSON_INVALIDO; erro com codigo, mensagem e campo | 400; JSON_INVALIDO; campo ausente | Falhou |

A mensagem recebida foi a mesma nos oito casos: **“O corpo da requisição deve ser um objeto JSON válido.”** Seu texto foi registrado como evidência; o cenário não exige uma mensagem exata.

## Falhas encontradas

**F01 — Informação `campo` ausente nas oito respostas.** A documentação afirma “Todo erro segue o mesmo formato” e apresenta um objeto `erro` com `codigo`, `mensagem` e `campo`. As respostas recebidas contêm apenas `codigo` e `mensagem`.

A rejeição dos conteúdos incorretos funcionou. A falha registrada está no passo “o erro deve seguir o formato documentado”. Uma integração que espere a informação `campo` não a encontrará.

**Ponto a esclarecer com Produto:** a documentação não define se `campo` pode ser omitido quando o problema está no corpo inteiro da solicitação. Este relatório segue o formato comum apresentado, sem inventar um valor esperado para `campo`. Se a omissão for intencional, a documentação e o critério de aceite precisam explicitar a exceção; caso a informação seja obrigatória, as respostas precisam ser ajustadas. Essa divergência também foi observada no [teste de erros de rota, método e produto](erros-rota-metodo-produto.md).

## Comprovantes do teste

Cada caso possui o corpo enviado, a resposta integral, os dados recebidos e a conferência detalhada. Os arquivos de erros da ferramenta estão vazios nesta execução.

| Caso | Corpo enviado | Registro completo | Dados recebidos | Validação detalhada | Erros da ferramenta |
| --- | --- | --- | --- | --- | --- |
| `POST /api/carrinho/calcular` com `{` | [Enviado](evidencias/json-invalido/20261007-232411/carrinho-calcular-chave-aberta/corpo-enviado.txt) | [Resposta](evidencias/json-invalido/20261007-232411/carrinho-calcular-chave-aberta/resposta-http.txt) | [Dados recebidos](evidencias/json-invalido/20261007-232411/carrinho-calcular-chave-aberta/corpo.json) | [Conferência](evidencias/json-invalido/20261007-232411/carrinho-calcular-chave-aberta/validacao.json) | [Erros](evidencias/json-invalido/20261007-232411/carrinho-calcular-chave-aberta/curl-stderr.txt) |
| `POST /api/carrinho/calcular` com `null` | [Enviado](evidencias/json-invalido/20261007-232411/carrinho-calcular-nulo/corpo-enviado.txt) | [Resposta](evidencias/json-invalido/20261007-232411/carrinho-calcular-nulo/resposta-http.txt) | [Dados recebidos](evidencias/json-invalido/20261007-232411/carrinho-calcular-nulo/corpo.json) | [Conferência](evidencias/json-invalido/20261007-232411/carrinho-calcular-nulo/validacao.json) | [Erros](evidencias/json-invalido/20261007-232411/carrinho-calcular-nulo/curl-stderr.txt) |
| `POST /api/carrinho/calcular` com `[]` | [Enviado](evidencias/json-invalido/20261007-232411/carrinho-calcular-lista/corpo-enviado.txt) | [Resposta](evidencias/json-invalido/20261007-232411/carrinho-calcular-lista/resposta-http.txt) | [Dados recebidos](evidencias/json-invalido/20261007-232411/carrinho-calcular-lista/corpo.json) | [Conferência](evidencias/json-invalido/20261007-232411/carrinho-calcular-lista/validacao.json) | [Erros](evidencias/json-invalido/20261007-232411/carrinho-calcular-lista/curl-stderr.txt) |
| `POST /api/carrinho/calcular` com `"texto"` | [Enviado](evidencias/json-invalido/20261007-232411/carrinho-calcular-texto/corpo-enviado.txt) | [Resposta](evidencias/json-invalido/20261007-232411/carrinho-calcular-texto/resposta-http.txt) | [Dados recebidos](evidencias/json-invalido/20261007-232411/carrinho-calcular-texto/corpo.json) | [Conferência](evidencias/json-invalido/20261007-232411/carrinho-calcular-texto/validacao.json) | [Erros](evidencias/json-invalido/20261007-232411/carrinho-calcular-texto/curl-stderr.txt) |
| `POST /api/pedidos` com `{` | [Enviado](evidencias/json-invalido/20261007-232411/pedidos-chave-aberta/corpo-enviado.txt) | [Resposta](evidencias/json-invalido/20261007-232411/pedidos-chave-aberta/resposta-http.txt) | [Dados recebidos](evidencias/json-invalido/20261007-232411/pedidos-chave-aberta/corpo.json) | [Conferência](evidencias/json-invalido/20261007-232411/pedidos-chave-aberta/validacao.json) | [Erros](evidencias/json-invalido/20261007-232411/pedidos-chave-aberta/curl-stderr.txt) |
| `POST /api/pedidos` com `null` | [Enviado](evidencias/json-invalido/20261007-232411/pedidos-nulo/corpo-enviado.txt) | [Resposta](evidencias/json-invalido/20261007-232411/pedidos-nulo/resposta-http.txt) | [Dados recebidos](evidencias/json-invalido/20261007-232411/pedidos-nulo/corpo.json) | [Conferência](evidencias/json-invalido/20261007-232411/pedidos-nulo/validacao.json) | [Erros](evidencias/json-invalido/20261007-232411/pedidos-nulo/curl-stderr.txt) |
| `POST /api/pedidos` com `[]` | [Enviado](evidencias/json-invalido/20261007-232411/pedidos-lista/corpo-enviado.txt) | [Resposta](evidencias/json-invalido/20261007-232411/pedidos-lista/resposta-http.txt) | [Dados recebidos](evidencias/json-invalido/20261007-232411/pedidos-lista/corpo.json) | [Conferência](evidencias/json-invalido/20261007-232411/pedidos-lista/validacao.json) | [Erros](evidencias/json-invalido/20261007-232411/pedidos-lista/curl-stderr.txt) |
| `POST /api/pedidos` com `"texto"` | [Enviado](evidencias/json-invalido/20261007-232411/pedidos-texto/corpo-enviado.txt) | [Resposta](evidencias/json-invalido/20261007-232411/pedidos-texto/resposta-http.txt) | [Dados recebidos](evidencias/json-invalido/20261007-232411/pedidos-texto/corpo.json) | [Conferência](evidencias/json-invalido/20261007-232411/pedidos-texto/validacao.json) | [Erros](evidencias/json-invalido/20261007-232411/pedidos-texto/curl-stderr.txt) |

[Resumo dos oito casos](evidencias/json-invalido/20261007-232411/resumo.json).

Para a equipe técnica, estes foram os comandos executados, com verificação de segurança da conexão mantida:

```bash
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{' --max-time 30 --silent --show-error --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary null --max-time 30 --silent --show-error --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '[]' --max-time 30 --silent --show-error --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '"texto"' --max-time 30 --silent --show-error --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '{' --max-time 30 --silent --show-error --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary null --max-time 30 --silent --show-error --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '[]' --max-time 30 --silent --show-error --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '"texto"' --max-time 30 --silent --show-error --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

O uso de `--data-binary` mantém o conteúdo literal de cada exemplo. O marcador `CURL_HTTP_STATUS` é acrescentado pela ferramenta e não faz parte da resposta do serviço. A conferência utiliza o status final da aplicação, sem confundi-lo com cabeçalhos de conexão do proxy. Não foi usado `--fail`, para preservar os corpos das respostas 400 esperadas.

## Limite desta avaliação

Foram testados somente os oito exemplos, na data indicada. Corpos válidos, confirmação de pedidos com dados corretos, cálculos de carrinho, interface, cupons e frete não foram avaliados. Não foi verificado armazenamento de pedidos; a recusa foi confirmada pelo status e pelo erro recebidos.
