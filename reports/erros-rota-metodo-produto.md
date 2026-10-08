# Relatório de teste — Erros de rota, método e produto

**Resultado: Falhou na verificação do formato documentado.** Os cinco casos devolveram os status e códigos de erro esperados. Porém, nenhum incluiu a informação `campo` prevista no exemplo de formato comum da documentação. Não houve bloqueio de execução.

**Data do teste:** 07/10/2026, às 23h15 (horário de Fortaleza).

**Loja:** Verzel Store, ambiente de testes.

**Referência:** VZS-142, versão 2.3.0; cenário em [contrato_api.feature](../features/contrato_api.feature).

## O que foi testado

Verificamos como a loja responde quando se consulta um produto inexistente, um endereço que não existe ou se usa um tipo de solicitação que aquele endereço não aceita.

O objetivo é devolver o motivo correto e manter o formato de erro descrito na documentação. Uma resposta de erro esperada pode representar um teste aprovado: por exemplo, procurar um produto inexistente deve retornar 404, não uma resposta de sucesso.

## Cenário BDD

API é o serviço que recebe as solicitações. Status 404 significa que o recurso não foi encontrado; 405 indica que o tipo de solicitação não é permitido. JSON é o formato dos dados recebidos.

```gherkin
Contexto:
  Dado que as requisições usam o cabeçalho "Content-Type" com valor "application/json"

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
```

## Resultados da conferência

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Execução dos cinco casos | Todas as solicitações concluídas | 5 concluídas, sem erro de conexão | Aprovado |
| Status de cada caso | 404 ou 405 conforme os exemplos | Todos corresponderam aos exemplos | Aprovado |
| Código de cada erro | Código indicado nos exemplos | Todos corresponderam aos exemplos | Aprovado |
| Dados recebidos | Resposta em JSON | JSON válido nos cinco casos | Aprovado |
| Motivo do erro | Objeto erro com codigo e mensagem | Presente nos cinco casos | Aprovado |
| Formato comum documentado | Objeto erro com codigo, mensagem e campo | campo ausente nos cinco casos | Falhou |

### Resultado por caso

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| `GET /api/produtos/INEXISTENTE` | 404 / `PRODUTO_NAO_ENCONTRADO`; erro com codigo, mensagem e campo | 404 / `PRODUTO_NAO_ENCONTRADO`; campo ausente | Falhou |
| `GET /api/rota-inexistente` | 404 / `ROTA_NAO_ENCONTRADA`; erro com codigo, mensagem e campo | 404 / `ROTA_NAO_ENCONTRADA`; campo ausente | Falhou |
| `POST /api/produtos` | 405 / `METODO_NAO_PERMITIDO`; erro com codigo, mensagem e campo | 405 / `METODO_NAO_PERMITIDO`; campo ausente | Falhou |
| `GET /api/carrinho/calcular` | 405 / `METODO_NAO_PERMITIDO`; erro com codigo, mensagem e campo | 405 / `METODO_NAO_PERMITIDO`; campo ausente | Falhou |
| `GET /api/pedidos` | 405 / `METODO_NAO_PERMITIDO`; erro com codigo, mensagem e campo | 405 / `METODO_NAO_PERMITIDO`; campo ausente | Falhou |

### Mensagens recebidas

As mensagens abaixo foram registradas como evidência. O cenário não define seus textos exatos; conferimos que eram textos não vazios.

| Solicitação | Mensagem recebida |
| --- | --- |
| `GET /api/produtos/INEXISTENTE` | Produto INEXISTENTE não encontrado. |
| `GET /api/rota-inexistente` | Rota não encontrada. |
| `POST /api/produtos` | O método POST não é permitido nesta rota. |
| `GET /api/carrinho/calcular` | O método GET não é permitido nesta rota. |
| `GET /api/pedidos` | O método GET não é permitido nesta rota. |

## Falhas encontradas

**F01 — Informação `campo` ausente em todas as respostas.** A documentação afirma “Todo erro segue o mesmo formato” e apresenta um objeto `erro` com `codigo`, `mensagem` e `campo`. As cinco respostas contêm somente `codigo` e `mensagem`.

Essa diferença impede aprovar integralmente o passo “o erro deve seguir o formato documentado”. Uma integração que espere a informação `campo` não a encontrará. Não foi observado problema nos status, códigos ou na identificação textual do motivo.

**Ponto a esclarecer com Produto:** a documentação não explica se `campo` pode ser omitido quando o erro não está ligado a um dado enviado pelo cliente. A classificação acima segue o formato comum apresentado, sem inventar o valor de `campo` para essas situações. Se a omissão for intencional, o contrato e o critério de aceite precisam explicitar essa exceção; se a informação for obrigatória, as respostas precisam ser ajustadas.

## Comprovantes do teste

Cada caso possui o registro integral da resposta, os dados recebidos, a conferência e a saída de erros da ferramenta. Os arquivos de erros da ferramenta estão vazios nesta execução.

| Solicitação | Registro completo | Dados recebidos | Validação detalhada | Erros da ferramenta |
| --- | --- | --- | --- | --- |
| `GET /api/produtos/INEXISTENTE` | [Consulta](evidencias/erros-rota-metodo-produto/20261007-231552/01-produto-inexistente/resposta-http.txt) | [Dados recebidos](evidencias/erros-rota-metodo-produto/20261007-231552/01-produto-inexistente/corpo.json) | [Conferência](evidencias/erros-rota-metodo-produto/20261007-231552/01-produto-inexistente/validacao.json) | [Erros da ferramenta](evidencias/erros-rota-metodo-produto/20261007-231552/01-produto-inexistente/curl-stderr.txt) |
| `GET /api/rota-inexistente` | [Consulta](evidencias/erros-rota-metodo-produto/20261007-231552/02-rota-inexistente/resposta-http.txt) | [Dados recebidos](evidencias/erros-rota-metodo-produto/20261007-231552/02-rota-inexistente/corpo.json) | [Conferência](evidencias/erros-rota-metodo-produto/20261007-231552/02-rota-inexistente/validacao.json) | [Erros da ferramenta](evidencias/erros-rota-metodo-produto/20261007-231552/02-rota-inexistente/curl-stderr.txt) |
| `POST /api/produtos` | [Consulta](evidencias/erros-rota-metodo-produto/20261007-231552/03-metodo-produtos/resposta-http.txt) | [Dados recebidos](evidencias/erros-rota-metodo-produto/20261007-231552/03-metodo-produtos/corpo.json) | [Conferência](evidencias/erros-rota-metodo-produto/20261007-231552/03-metodo-produtos/validacao.json) | [Erros da ferramenta](evidencias/erros-rota-metodo-produto/20261007-231552/03-metodo-produtos/curl-stderr.txt) |
| `GET /api/carrinho/calcular` | [Consulta](evidencias/erros-rota-metodo-produto/20261007-231552/04-metodo-carrinho/resposta-http.txt) | [Dados recebidos](evidencias/erros-rota-metodo-produto/20261007-231552/04-metodo-carrinho/corpo.json) | [Conferência](evidencias/erros-rota-metodo-produto/20261007-231552/04-metodo-carrinho/validacao.json) | [Erros da ferramenta](evidencias/erros-rota-metodo-produto/20261007-231552/04-metodo-carrinho/curl-stderr.txt) |
| `GET /api/pedidos` | [Consulta](evidencias/erros-rota-metodo-produto/20261007-231552/05-metodo-pedidos/resposta-http.txt) | [Dados recebidos](evidencias/erros-rota-metodo-produto/20261007-231552/05-metodo-pedidos/corpo.json) | [Conferência](evidencias/erros-rota-metodo-produto/20261007-231552/05-metodo-pedidos/validacao.json) | [Erros da ferramenta](evidencias/erros-rota-metodo-produto/20261007-231552/05-metodo-pedidos/curl-stderr.txt) |

[Resumo dos cinco casos](evidencias/erros-rota-metodo-produto/20261007-231552/resumo.json).

Para a equipe técnica, estes foram os comandos executados, com verificação de segurança da conexão mantida:

```bash
curl -i -X GET \
  "https://verzel-store.qa-test-verzel-store.workers.dev/api/produtos/INEXISTENTE" \
  -H "Content-Type: application/json" \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X GET \
  "https://verzel-store.qa-test-verzel-store.workers.dev/api/rota-inexistente" \
  -H "Content-Type: application/json" \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  "https://verzel-store.qa-test-verzel-store.workers.dev/api/produtos" \
  -H "Content-Type: application/json" \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X GET \
  "https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular" \
  -H "Content-Type: application/json" \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X GET \
  "https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos" \
  -H "Content-Type: application/json" \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

O marcador `CURL_HTTP_STATUS` é acrescentado pela ferramenta e não faz parte da resposta do serviço. O status final da aplicação foi utilizado na conferência, sem confundir eventuais cabeçalhos de conexão do proxy com o resultado. O comando não usa `--fail`, para preservar os corpos das respostas 404 e 405 esperadas.

## Limite desta avaliação

Foram testados somente os cinco exemplos do cenário, na data indicada. A interface da loja, outros endereços, dados de carrinho, cupons, frete e confirmação de pedidos não foram avaliados. O POST para produtos foi enviado sem corpo, pois o objetivo era testar um método não permitido, sem criar produtos.
