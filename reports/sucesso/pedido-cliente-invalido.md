# Relatório de teste — Rejeitar dados inválidos do cliente

**Resultado: Aprovado.** A loja recusou os oito pedidos com dados inválidos, informou qual campo precisava de correção e não retornou confirmação de pedido.

**Data do teste:** 08/10/2026, das 10h57min01s às 10h57min03s (America/Fortaleza). O horário da revisão da checagem automática está registrado separadamente nas evidências.

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao); cenário em [pedidos.feature](../../features/pedidos.feature).

## O que foi testado

Tentamos confirmar oito pedidos independentes, cada um com uma Mochila Urbana 20L (P005), de R$ 100,00, sem cupom. Usamos os dados de exemplo do cenário e alteramos um campo por vez: nome, e-mail ou CEP.

Foram testados nome sem sobrenome, nome vazio, e-mail sem arroba, e-mail vazio, CEP com sete dígitos, CEP com nove dígitos, CEP com letras e CEP vazio. Os campos vazios foram enviados como texto vazio (`""`), mantendo o campo na requisição.

As chamadas foram feitas diretamente ao serviço da loja (API). Conferimos a recusa, o código DADOS_INVALIDOS, a identificação do campo e a ausência de número e data de confirmação.

## Cenário BDD

```gherkin
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
```

## Resultados da conferência

### Verificações realizadas em cada um dos oito exemplos

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Pedido recusado | Status 422 | Status 422 nas oito chamadas | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido nas oito respostas | Aprovado |
| Motivo da recusa (`erro.codigo`) | DADOS_INVALIDOS | DADOS_INVALIDOS nos oito exemplos | Aprovado |
| Pedido não confirmado | Resposta de recusa, sem número ou data de confirmação | Erro de dados inválidos, sem `numero` ou `criadoEm` nas oito respostas | Aprovado |

O status 422 indica que a loja recusou o pedido por causa dos dados enviados. JSON é o formato usado para enviar e receber esses dados. As recusas são o comportamento esperado deste teste.

### Identificação do campo inválido em cada exemplo

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Nome sem sobrenome: `Maria` | Identificar nome inválido | `cliente.nome`: “Informe nome e sobrenome.” | Aprovado |
| Nome vazio | Identificar nome inválido | `cliente.nome`: “Informe o nome completo.” | Aprovado |
| E-mail sem arroba: `maria.exemplo.com` | Identificar e-mail inválido | `cliente.email`: “Informe um e-mail válido.” | Aprovado |
| E-mail vazio | Identificar e-mail inválido | `cliente.email`: “Informe o e-mail.” | Aprovado |
| CEP com sete dígitos: `0131010` | Identificar CEP inválido | `cliente.cep`: “Informe um CEP com 8 dígitos.” | Aprovado |
| CEP com nove dígitos: `013101000` | Identificar CEP inválido | `cliente.cep`: “Informe um CEP com 8 dígitos.” | Aprovado |
| CEP com letras: `ABCDEFGH` | Identificar CEP inválido | `cliente.cep`: “Informe um CEP com 8 dígitos.” | Aprovado |
| CEP vazio | Identificar CEP inválido | `cliente.cep`: “Informe o CEP.” | Aprovado |

Os detalhes vieram em `erro.campos`, uma lista que informa o campo e a mensagem de correção. As mensagens acima foram observadas nas respostas; o cenário exige a identificação do campo inválido. Os oito exemplos passaram, com 40 verificações aprovadas na conferência final.

## Falhas encontradas

Nenhuma falha do produto foi encontrada. Todos os pedidos foram recusados pelo motivo correto, com indicação do campo inválido. Não houve bloqueios nem exemplos sem execução.

## Comprovantes do teste

| Exemplo | Envio | Resposta | Validação | Execução |
| --- | --- | --- | --- | --- |
| Nome sem sobrenome | [Corpo enviado](evidencias/pedido-cliente-invalido/20261008-105701/01-nome-sem-sobrenome/corpo-enviado.json) | [HTTP completo](evidencias/pedido-cliente-invalido/20261008-105701/01-nome-sem-sobrenome/resposta-http.txt) e [JSON recebido](evidencias/pedido-cliente-invalido/20261008-105701/01-nome-sem-sobrenome/corpo-recebido.json) | [Conferência final](evidencias/pedido-cliente-invalido/20261008-105701/01-nome-sem-sobrenome/validacao-api.json) | [Comando](evidencias/pedido-cliente-invalido/20261008-105701/01-nome-sem-sobrenome/comando.txt) e [erros da ferramenta](evidencias/pedido-cliente-invalido/20261008-105701/01-nome-sem-sobrenome/curl-stderr.txt) |
| Nome vazio | [Corpo enviado](evidencias/pedido-cliente-invalido/20261008-105701/02-nome-vazio/corpo-enviado.json) | [HTTP completo](evidencias/pedido-cliente-invalido/20261008-105701/02-nome-vazio/resposta-http.txt) e [JSON recebido](evidencias/pedido-cliente-invalido/20261008-105701/02-nome-vazio/corpo-recebido.json) | [Conferência final](evidencias/pedido-cliente-invalido/20261008-105701/02-nome-vazio/validacao-api.json) | [Comando](evidencias/pedido-cliente-invalido/20261008-105701/02-nome-vazio/comando.txt) e [erros da ferramenta](evidencias/pedido-cliente-invalido/20261008-105701/02-nome-vazio/curl-stderr.txt) |
| E-mail sem arroba | [Corpo enviado](evidencias/pedido-cliente-invalido/20261008-105701/03-email-sem-arroba/corpo-enviado.json) | [HTTP completo](evidencias/pedido-cliente-invalido/20261008-105701/03-email-sem-arroba/resposta-http.txt) e [JSON recebido](evidencias/pedido-cliente-invalido/20261008-105701/03-email-sem-arroba/corpo-recebido.json) | [Conferência final](evidencias/pedido-cliente-invalido/20261008-105701/03-email-sem-arroba/validacao-api.json) | [Comando](evidencias/pedido-cliente-invalido/20261008-105701/03-email-sem-arroba/comando.txt) e [erros da ferramenta](evidencias/pedido-cliente-invalido/20261008-105701/03-email-sem-arroba/curl-stderr.txt) |
| E-mail vazio | [Corpo enviado](evidencias/pedido-cliente-invalido/20261008-105701/04-email-vazio/corpo-enviado.json) | [HTTP completo](evidencias/pedido-cliente-invalido/20261008-105701/04-email-vazio/resposta-http.txt) e [JSON recebido](evidencias/pedido-cliente-invalido/20261008-105701/04-email-vazio/corpo-recebido.json) | [Conferência final](evidencias/pedido-cliente-invalido/20261008-105701/04-email-vazio/validacao-api.json) | [Comando](evidencias/pedido-cliente-invalido/20261008-105701/04-email-vazio/comando.txt) e [erros da ferramenta](evidencias/pedido-cliente-invalido/20261008-105701/04-email-vazio/curl-stderr.txt) |
| CEP com sete dígitos | [Corpo enviado](evidencias/pedido-cliente-invalido/20261008-105701/05-cep-sete-digitos/corpo-enviado.json) | [HTTP completo](evidencias/pedido-cliente-invalido/20261008-105701/05-cep-sete-digitos/resposta-http.txt) e [JSON recebido](evidencias/pedido-cliente-invalido/20261008-105701/05-cep-sete-digitos/corpo-recebido.json) | [Conferência final](evidencias/pedido-cliente-invalido/20261008-105701/05-cep-sete-digitos/validacao-api.json) | [Comando](evidencias/pedido-cliente-invalido/20261008-105701/05-cep-sete-digitos/comando.txt) e [erros da ferramenta](evidencias/pedido-cliente-invalido/20261008-105701/05-cep-sete-digitos/curl-stderr.txt) |
| CEP com nove dígitos | [Corpo enviado](evidencias/pedido-cliente-invalido/20261008-105701/06-cep-nove-digitos/corpo-enviado.json) | [HTTP completo](evidencias/pedido-cliente-invalido/20261008-105701/06-cep-nove-digitos/resposta-http.txt) e [JSON recebido](evidencias/pedido-cliente-invalido/20261008-105701/06-cep-nove-digitos/corpo-recebido.json) | [Conferência final](evidencias/pedido-cliente-invalido/20261008-105701/06-cep-nove-digitos/validacao-api.json) | [Comando](evidencias/pedido-cliente-invalido/20261008-105701/06-cep-nove-digitos/comando.txt) e [erros da ferramenta](evidencias/pedido-cliente-invalido/20261008-105701/06-cep-nove-digitos/curl-stderr.txt) |
| CEP com letras | [Corpo enviado](evidencias/pedido-cliente-invalido/20261008-105701/07-cep-letras/corpo-enviado.json) | [HTTP completo](evidencias/pedido-cliente-invalido/20261008-105701/07-cep-letras/resposta-http.txt) e [JSON recebido](evidencias/pedido-cliente-invalido/20261008-105701/07-cep-letras/corpo-recebido.json) | [Conferência final](evidencias/pedido-cliente-invalido/20261008-105701/07-cep-letras/validacao-api.json) | [Comando](evidencias/pedido-cliente-invalido/20261008-105701/07-cep-letras/comando.txt) e [erros da ferramenta](evidencias/pedido-cliente-invalido/20261008-105701/07-cep-letras/curl-stderr.txt) |
| CEP vazio | [Corpo enviado](evidencias/pedido-cliente-invalido/20261008-105701/08-cep-vazio/corpo-enviado.json) | [HTTP completo](evidencias/pedido-cliente-invalido/20261008-105701/08-cep-vazio/resposta-http.txt) e [JSON recebido](evidencias/pedido-cliente-invalido/20261008-105701/08-cep-vazio/corpo-recebido.json) | [Conferência final](evidencias/pedido-cliente-invalido/20261008-105701/08-cep-vazio/validacao-api.json) | [Comando](evidencias/pedido-cliente-invalido/20261008-105701/08-cep-vazio/comando.txt) e [erros da ferramenta](evidencias/pedido-cliente-invalido/20261008-105701/08-cep-vazio/curl-stderr.txt) |

- [Resumo final dos resultados e horários](evidencias/pedido-cliente-invalido/20261008-105701/resumo-validacao.json).
- [Casos e critérios esperados](evidencias/pedido-cliente-invalido/20261008-105701/criterios.json).
- [Script que executou as oito chamadas](evidencias/pedido-cliente-invalido/20261008-105701/teste-api.py).
- [Script da revisão das respostas salvas](evidencias/pedido-cliente-invalido/20261008-105701/revisao-validacao.py) e [registro da revisão e integridade dos arquivos](evidencias/pedido-cliente-invalido/20261008-105701/revisao-validacao.json).
- [Diagnóstico inicial da ferramenta](evidencias/pedido-cliente-invalido/20261008-105701/diagnostico-validador-inicial/resumo-validacao.json), preservado para rastreabilidade.

**Ajuste da ferramenta de conferência:** a primeira checagem automática esperava que `campos` fosse um objeto. A API retornou uma lista em `erro.campos`, identificando corretamente `cliente.nome`, `cliente.email` ou `cliente.cep`. Corrigimos a leitura dessa lista e revisamos as mesmas respostas, sem novas chamadas nem mudanças nos critérios. As verificações iniciais estão preservadas na pasta de diagnóstico; os resultados finais estão nos arquivos de validação vinculados acima. O registro de revisão comprova que os 40 arquivos capturados — envios, comandos, respostas e registros de erros — permaneceram inalterados.

Os oito arquivos de erros do curl estão vazios, e todas as chamadas terminaram sem erro de comunicação. As respostas HTTP completas preservam o status e os cabeçalhos. A revisão da ferramenta não representa uma falha do produto.

Para reproduzir as oito requisições executadas:

```bash
curl -i -X POST \
  https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Maria","email":"maria@exemplo.com","cep":"01310100"},"itens":[{"produtoId":"P005","quantidade":1}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"","email":"maria@exemplo.com","cep":"01310100"},"itens":[{"produtoId":"P005","quantidade":1}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Maria Silva","email":"maria.exemplo.com","cep":"01310100"},"itens":[{"produtoId":"P005","quantidade":1}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Maria Silva","email":"","cep":"01310100"},"itens":[{"produtoId":"P005","quantidade":1}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Maria Silva","email":"maria@exemplo.com","cep":"0131010"},"itens":[{"produtoId":"P005","quantidade":1}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Maria Silva","email":"maria@exemplo.com","cep":"013101000"},"itens":[{"produtoId":"P005","quantidade":1}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Maria Silva","email":"maria@exemplo.com","cep":"ABCDEFGH"},"itens":[{"produtoId":"P005","quantidade":1}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Maria Silva","email":"maria@exemplo.com","cep":""},"itens":[{"produtoId":"P005","quantidade":1}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

O marcador `CURL_HTTP_STATUS` foi acrescentado pela ferramenta e não faz parte da resposta da loja. A avaliação considerou o status final da aplicação e manteve a verificação de segurança da conexão ativa. Os campos vazios e os CEPs foram enviados como texto, exatamente como nos exemplos.

## Limite desta avaliação

A aprovação se aplica aos oito exemplos e às respostas desta execução, com uma unidade de P005 e sem cupom. Não foram testados vários campos inválidos ao mesmo tempo, campos ausentes, outros tipos de dados ou a apresentação na interface.

A ausência de confirmação foi verificada pelo status 422, pelo erro DADOS_INVALIDOS e pela ausência de número e data de confirmação nas respostas. Não houve consulta ao armazenamento interno. Conforme a documentação, este ambiente não armazena pedidos nem permite consultar pedidos confirmados.
