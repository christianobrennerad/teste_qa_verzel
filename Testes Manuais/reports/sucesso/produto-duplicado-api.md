# Relatório de teste — Rejeitar produto duplicado

**Resultado: Aprovado.** A loja recusou P001 enviado em duas linhas de três unidades, tanto no cálculo quanto na confirmação do pedido. As duas respostas retornaram status 422 e código ITEM_DUPLICADO, sem confirmação de pedido.

**Data do teste:** 08/10/2026, às 11h59min13s (America/Fortaleza). As duas chamadas foram iniciadas e concluídas nesse segundo; os registros individuais estão nas evidências.

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao), critério CA10 e código ITEM_DUPLICADO; cenário em [quantidades_e_itens.feature](../../features/quantidades_e_itens.feature).

## O que foi testado

Enviamos a Camiseta Essencial (P001) duas vezes na mesma lista, com três unidades em cada linha. Esse formato representa seis unidades do mesmo produto, distribuídas em duas linhas.

Fizemos duas chamadas independentes ao serviço da loja (API). Primeiro, enviamos o corpo do cenário para calcular o carrinho. Depois, mantivemos as duas linhas e acrescentamos um cliente fictício válido para tentar confirmar o pedido: Cliente Teste, qa@example.com e CEP 01310-100. Não foi enviado cupom.

Conferimos a recusa e o código de duplicidade nas duas operações. Também verificamos o formato dos dados recebidos e a ausência de número e data de confirmação como apoio à conferência.

## Cenário BDD

```gherkin
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
```

## Resultados da conferência

### Cálculo do carrinho

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Requisição recusada | Status 422 | Status 422 | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido | Aprovado |
| Motivo da recusa (`erro.codigo`) | ITEM_DUPLICADO | ITEM_DUPLICADO | Aprovado |
| Resposta sem confirmação | Erro de duplicidade, sem número ou data de confirmação | Erro ITEM_DUPLICADO, sem `numero` ou `criadoEm` | Aprovado |

### Confirmação do pedido

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Pedido recusado | Status 422 | Status 422 | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido | Aprovado |
| Motivo da recusa (`erro.codigo`) | ITEM_DUPLICADO | ITEM_DUPLICADO | Aprovado |
| Resposta sem confirmação | Erro de duplicidade, sem número ou data de confirmação | Erro ITEM_DUPLICADO, sem `numero` ou `criadoEm` | Aprovado |

As **oito verificações passaram**. O status 422 indica que a loja recusou os dados enviados; JSON é o formato usado para enviar e receber esses dados.

As duas respostas informaram “O produto P001 aparece mais de uma vez.” e apontaram `itens[1].produtoId`, o identificador da segunda linha da lista. Esses detalhes foram observados nas respostas e ajudam a localizar a duplicidade.

## Falhas encontradas

Nenhuma falha foi encontrada nesta execução. As duas operações recusaram a duplicidade pelo motivo esperado, e o pedido não foi confirmado na resposta. Não houve bloqueios nem passos sem execução.

## Comprovantes do teste

| Chamada | Envio | Resposta | Validação | Execução |
| --- | --- | --- | --- | --- |
| Cálculo | [Corpo enviado](evidencias/produto-duplicado-api/20261008-115913/calculo/corpo-enviado.json) | [HTTP completo](evidencias/produto-duplicado-api/20261008-115913/calculo/resposta-http.txt) e [JSON recebido](evidencias/produto-duplicado-api/20261008-115913/calculo/corpo-recebido.json) | [Conferência](evidencias/produto-duplicado-api/20261008-115913/calculo/validacao-api.json) | [Comando](evidencias/produto-duplicado-api/20261008-115913/calculo/comando.txt) e [erros da ferramenta](evidencias/produto-duplicado-api/20261008-115913/calculo/curl-stderr.txt) |
| Pedido | [Corpo enviado](evidencias/produto-duplicado-api/20261008-115913/pedido/corpo-enviado.json) | [HTTP completo](evidencias/produto-duplicado-api/20261008-115913/pedido/resposta-http.txt) e [JSON recebido](evidencias/produto-duplicado-api/20261008-115913/pedido/corpo-recebido.json) | [Conferência](evidencias/produto-duplicado-api/20261008-115913/pedido/validacao-api.json) | [Comando](evidencias/produto-duplicado-api/20261008-115913/pedido/comando.txt) e [erros da ferramenta](evidencias/produto-duplicado-api/20261008-115913/pedido/curl-stderr.txt) |

- [Resumo dos resultados e horários](evidencias/produto-duplicado-api/20261008-115913/resumo-validacao.json).
- [Corpo original, cliente fictício e critérios esperados](evidencias/produto-duplicado-api/20261008-115913/criterios.json).
- [Script executado](evidencias/produto-duplicado-api/20261008-115913/teste-api.py).

Os dois registros de erros do curl estão vazios, e a ferramenta terminou sem erro de comunicação. As respostas HTTP completas preservam status e cabeçalhos; as validações registram horários, comandos e comparações.

Para reproduzir as requisições executadas:

```bash
curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular' \
  -H 'Content-Type: application/json' \
  --data-binary '{"itens":[{"produtoId":"P001","quantidade":3},{"produtoId":"P001","quantidade":3}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos' \
  -H 'Content-Type: application/json' \
  --data-binary '{"itens":[{"produtoId":"P001","quantidade":3},{"produtoId":"P001","quantidade":3}],"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

A mesma resposta de erro foi recebida nas duas chamadas:

```json
{
  "erro": {
    "codigo": "ITEM_DUPLICADO",
    "mensagem": "O produto P001 aparece mais de uma vez.",
    "campo": "itens[1].produtoId"
  }
}
```

O marcador `CURL_HTTP_STATUS` foi acrescentado pela ferramenta e não faz parte da resposta da loja. A avaliação considerou o status final da aplicação e manteve a verificação de segurança da conexão ativa.

## Limite desta avaliação

A aprovação se aplica às duas chamadas com P001 repetido em duas linhas de três unidades. Outras combinações de duplicidade, quantidades acima de cinco em uma única linha e a interface não foram avaliadas nesta execução.

A ausência de confirmação foi verificada pelo status 422, pelo código ITEM_DUPLICADO e pela ausência de número e data de confirmação nas respostas. Não houve consulta ao armazenamento interno. Conforme a documentação, este ambiente não armazena pedidos nem permite consultar pedidos confirmados.
