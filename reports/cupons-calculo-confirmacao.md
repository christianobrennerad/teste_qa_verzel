# Relatório de teste — Cupom inválido no cálculo e na confirmação

**Resultado: Aprovado.** Os dois cupons foram recusados corretamente. A loja calculou o carrinho sem desconto e impediu a confirmação do pedido, distinguindo cupom inexistente de cupom expirado.

**Data do teste:** 08/10/2026, das 10h21min23s às 10h21min24s (America/Fortaleza).

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao), critérios CA03 e CA04; cenário em [pedidos.feature](../features/pedidos.feature).

## O que foi testado

Para cada cupom, calculamos um carrinho com uma Mochila Urbana 20L (P005), de R$ 100,00. Em seguida, tentamos confirmar um pedido com o mesmo produto, quantidade e cupom.

As quatro chamadas foram feitas diretamente ao serviço da loja (API). Nas tentativas de confirmação, usamos um cliente fictício válido: Cliente Teste, qa@example.com e CEP 01310-100.

O comportamento esperado é permitir a consulta do valor do carrinho sem aplicar o desconto, mas recusar a confirmação enquanto o cupom inválido ou expirado estiver no pedido.

## Cenário BDD

```gherkin
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
```

## Resultados da conferência

### Cupom INEXISTENTE

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Cálculo atendido | Status 200 | Status 200 | Aprovado |
| Produto no cálculo | Uma unidade de P005 | Uma unidade de P005 | Aprovado |
| Cupom aplicado no cálculo | Falso | Falso | Aprovado |
| Mensagem no cálculo | Cupom inválido. | Cupom inválido. | Aprovado |
| Desconto | R$ 0,00 | R$ 0,00 | Aprovado |
| Total | R$ 119,90 | R$ 119,90 | Aprovado |
| Confirmação recusada | Status 422 | Status 422 | Aprovado |
| Motivo da recusa (`erro.codigo`) | CUPOM_INVALIDO | CUPOM_INVALIDO | Aprovado |
| Pedido não confirmado | Resposta de recusa, sem confirmação | Erro de cupom, sem número ou data de confirmação | Aprovado |

### Cupom VERAO2026

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Cálculo atendido | Status 200 | Status 200 | Aprovado |
| Produto no cálculo | Uma unidade de P005 | Uma unidade de P005 | Aprovado |
| Cupom aplicado no cálculo | Falso | Falso | Aprovado |
| Mensagem no cálculo | Cupom expirado. | Cupom expirado. | Aprovado |
| Desconto | R$ 0,00 | R$ 0,00 | Aprovado |
| Total | R$ 119,90 | R$ 119,90 | Aprovado |
| Confirmação recusada | Status 422 | Status 422 | Aprovado |
| Motivo da recusa (`erro.codigo`) | CUPOM_EXPIRADO | CUPOM_EXPIRADO | Aprovado |
| Pedido não confirmado | Resposta de recusa, sem confirmação | Erro de cupom, sem número ou data de confirmação | Aprovado |

Nos dois cálculos, a loja retornou subtotal de R$ 100,00 e frete de R$ 19,90. Sem desconto, o total foi R$ 119,90. As quatro respostas vieram em JSON válido, o formato de dados usado pela API. As 22 verificações registradas no teste foram aprovadas.

## Falhas encontradas

Nenhuma falha foi encontrada nesta execução. Os retornos 422 nas tentativas de confirmação são o resultado esperado: indicam que a loja recusou o pedido por causa do cupom. Não houve bloqueios nem etapas sem execução.

## Comprovantes do teste

Cada linha abaixo reúne os arquivos da respectiva chamada. As respostas HTTP completas preservam o status e os cabeçalhos recebidos. As validações registram horário, comando e comparação dos resultados.

| Chamada | Envio | Resposta | Validação | Execução |
| --- | --- | --- | --- | --- |
| INEXISTENTE — cálculo | [Corpo enviado](evidencias/cupons-calculo-confirmacao/20261008-102123/01-inexistente/calculo/corpo-enviado.json) | [HTTP completo](evidencias/cupons-calculo-confirmacao/20261008-102123/01-inexistente/calculo/resposta-http.txt) e [JSON recebido](evidencias/cupons-calculo-confirmacao/20261008-102123/01-inexistente/calculo/corpo-recebido.json) | [Conferência](evidencias/cupons-calculo-confirmacao/20261008-102123/01-inexistente/calculo/validacao-api.json) | [Comando](evidencias/cupons-calculo-confirmacao/20261008-102123/01-inexistente/calculo/comando.txt) e [erros da ferramenta](evidencias/cupons-calculo-confirmacao/20261008-102123/01-inexistente/calculo/curl-stderr.txt) |
| INEXISTENTE — confirmação | [Corpo enviado](evidencias/cupons-calculo-confirmacao/20261008-102123/01-inexistente/confirmacao/corpo-enviado.json) | [HTTP completo](evidencias/cupons-calculo-confirmacao/20261008-102123/01-inexistente/confirmacao/resposta-http.txt) e [JSON recebido](evidencias/cupons-calculo-confirmacao/20261008-102123/01-inexistente/confirmacao/corpo-recebido.json) | [Conferência](evidencias/cupons-calculo-confirmacao/20261008-102123/01-inexistente/confirmacao/validacao-api.json) | [Comando](evidencias/cupons-calculo-confirmacao/20261008-102123/01-inexistente/confirmacao/comando.txt) e [erros da ferramenta](evidencias/cupons-calculo-confirmacao/20261008-102123/01-inexistente/confirmacao/curl-stderr.txt) |
| VERAO2026 — cálculo | [Corpo enviado](evidencias/cupons-calculo-confirmacao/20261008-102123/02-expirado/calculo/corpo-enviado.json) | [HTTP completo](evidencias/cupons-calculo-confirmacao/20261008-102123/02-expirado/calculo/resposta-http.txt) e [JSON recebido](evidencias/cupons-calculo-confirmacao/20261008-102123/02-expirado/calculo/corpo-recebido.json) | [Conferência](evidencias/cupons-calculo-confirmacao/20261008-102123/02-expirado/calculo/validacao-api.json) | [Comando](evidencias/cupons-calculo-confirmacao/20261008-102123/02-expirado/calculo/comando.txt) e [erros da ferramenta](evidencias/cupons-calculo-confirmacao/20261008-102123/02-expirado/calculo/curl-stderr.txt) |
| VERAO2026 — confirmação | [Corpo enviado](evidencias/cupons-calculo-confirmacao/20261008-102123/02-expirado/confirmacao/corpo-enviado.json) | [HTTP completo](evidencias/cupons-calculo-confirmacao/20261008-102123/02-expirado/confirmacao/resposta-http.txt) e [JSON recebido](evidencias/cupons-calculo-confirmacao/20261008-102123/02-expirado/confirmacao/corpo-recebido.json) | [Conferência](evidencias/cupons-calculo-confirmacao/20261008-102123/02-expirado/confirmacao/validacao-api.json) | [Comando](evidencias/cupons-calculo-confirmacao/20261008-102123/02-expirado/confirmacao/comando.txt) e [erros da ferramenta](evidencias/cupons-calculo-confirmacao/20261008-102123/02-expirado/confirmacao/curl-stderr.txt) |

- [Resumo dos resultados e horários](evidencias/cupons-calculo-confirmacao/20261008-102123/resumo-validacao.json).
- [Casos e valores esperados](evidencias/cupons-calculo-confirmacao/20261008-102123/casos.json).
- [Script executado](evidencias/cupons-calculo-confirmacao/20261008-102123/teste-api.py).

Os quatro arquivos de erros da ferramenta estão vazios, e o curl terminou sem erro de execução em todas as chamadas. A verificação de segurança da conexão permaneceu ativa.

Para reproduzir as requisições, execute primeiro o cálculo e depois a tentativa de confirmação de cada cupom:

```bash
curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular' \
  -H 'Content-Type: application/json' \
  --data-binary '{"itens":[{"produtoId":"P005","quantidade":1}],"cupom":"INEXISTENTE"}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos' \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"},"itens":[{"produtoId":"P005","quantidade":1}],"cupom":"INEXISTENTE"}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular' \
  -H 'Content-Type: application/json' \
  --data-binary '{"itens":[{"produtoId":"P005","quantidade":1}],"cupom":"VERAO2026"}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos' \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"},"itens":[{"produtoId":"P005","quantidade":1}],"cupom":"VERAO2026"}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

O marcador `CURL_HTTP_STATUS` foi acrescentado pela ferramenta e não faz parte da resposta da loja. A conferência usou o status final da aplicação e comparou desconto e total com números decimais exatos.

## Limite desta avaliação

A aprovação se aplica aos dois cupons e às quatro chamadas desta execução, com uma unidade de P005 e o cliente fictício informado. A apresentação na interface, outros cupons e outros produtos não foram avaliados neste teste.

A recusa da confirmação foi verificada pelo status 422, pelo erro específico de cupom e pela ausência de número e data de confirmação nas respostas. Não houve consulta a armazenamento interno. Segundo a documentação, este ambiente não persiste pedidos nem disponibiliza consulta de pedidos confirmados.
