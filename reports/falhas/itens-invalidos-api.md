# Relatório de teste — Rejeitar itens inválidos nas duas operações

**Resultado: Falhou.** Dez dos 14 exemplos passaram nas duas operações. Quatro falharam: itens sem identificador ou sem quantidade foram recusados com códigos diferentes dos esperados; quantidades de 6 e 100 foram aceitas e os pedidos foram confirmados, apesar do limite documentado de cinco unidades por produto.

**Data do teste:** 08/10/2026, das 11h47min09s às 11h47min14s (America/Fortaleza).

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao), seção de códigos de erro e regra de quantidade máxima; cenário em [quantidades_e_itens.feature](../../features/quantidades_e_itens.feature).

## O que foi testado

Enviamos os 14 corpos do cenário ao serviço que calcula o carrinho e ao serviço que confirma pedidos (API), totalizando 28 chamadas independentes.

No cálculo, o corpo foi enviado exatamente como no exemplo. Na confirmação, mantivemos os mesmos dados e tipos dos itens e acrescentamos somente um cliente fictício válido: Cliente Teste, qa@example.com e CEP 01310-100. Campos ausentes continuaram ausentes; texto, números fracionados e valores nulos foram preservados. Não foi enviado cupom.

Conferimos a recusa com status 422, o código esperado, uma mensagem de erro e a indicação do campo relacionado. Como conferência de apoio, verificamos também a ausência de número e data de confirmação nas respostas.

## Cenário BDD

```gherkin
@api
Esquema do Cenário: Rejeitar itens inválidos nas duas operações
  Quando envio para "POST /api/carrinho/calcular" o corpo "<corpo>"
  Então a API deve responder com status 422
  E o campo "erro.codigo" deve ser "<codigo>"
  E o erro deve seguir o formato documentado com código, mensagem e campo relacionado
  Quando envio para "POST /api/pedidos" o mesmo corpo com cliente válido
  Então a API deve responder com status 422
  E o campo "erro.codigo" deve ser "<codigo>"
  E o erro deve seguir o formato documentado com código, mensagem e campo relacionado

  Exemplos:
    | corpo                                                     | codigo                     |
    | {}                                                        | ITENS_OBRIGATORIOS         |
    | {"itens":[]}                                              | ITENS_OBRIGATORIOS         |
    | {"itens":[null]}                                          | ITEM_INVALIDO              |
    | {"itens":["P001"]}                                        | ITEM_INVALIDO              |
    | {"itens":[{"quantidade":1}]}                               | ITEM_INVALIDO              |
    | {"itens":[{"produtoId":"P001"}]}                           | ITEM_INVALIDO              |
    | {"itens":[{"produtoId":"INEXISTENTE","quantidade":1}]}      | PRODUTO_NAO_ENCONTRADO      |
    | {"itens":[{"produtoId":"P001","quantidade":0}]}            | QUANTIDADE_INVALIDA        |
    | {"itens":[{"produtoId":"P001","quantidade":-1}]}           | QUANTIDADE_INVALIDA        |
    | {"itens":[{"produtoId":"P001","quantidade":1.5}]}          | QUANTIDADE_INVALIDA        |
    | {"itens":[{"produtoId":"P001","quantidade":"1"}]}          | QUANTIDADE_INVALIDA        |
    | {"itens":[{"produtoId":"P001","quantidade":null}]}         | QUANTIDADE_INVALIDA        |
    | {"itens":[{"produtoId":"P001","quantidade":6}]}            | QUANTIDADE_MAXIMA_EXCEDIDA  |
    | {"itens":[{"produtoId":"P001","quantidade":100}]}          | QUANTIDADE_MAXIMA_EXCEDIDA  |
```

## Resultados da conferência

Na tabela, “ambas” significa cálculo do carrinho e confirmação do pedido. O esperado para todos os exemplos é status 422, com o código indicado e erro contendo mensagem e campo relacionado.

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| 01 — Lista de itens ausente | 422, ITENS_OBRIGATORIOS e campo relacionado | Ambas: 422, ITENS_OBRIGATORIOS; campo `itens`; mensagem presente | Aprovado |
| 02 — Lista de itens vazia | 422, ITENS_OBRIGATORIOS e campo relacionado | Ambas: 422, ITENS_OBRIGATORIOS; campo `itens`; mensagem presente | Aprovado |
| 03 — Item nulo | 422, ITEM_INVALIDO e campo relacionado | Ambas: 422, ITEM_INVALIDO; campo `itens[0]`; mensagem presente | Aprovado |
| 04 — Item enviado como texto | 422, ITEM_INVALIDO e campo relacionado | Ambas: 422, ITEM_INVALIDO; campo `itens[0]`; mensagem presente | Aprovado |
| 05 — Identificador do produto ausente | 422, ITEM_INVALIDO e campo relacionado | Ambas: 422, **PRODUTO_NAO_ENCONTRADO**; campo `itens[0].produtoId`; mensagem presente | **Falhou** |
| 06 — Quantidade ausente | 422, ITEM_INVALIDO e campo relacionado | Ambas: 422, **QUANTIDADE_INVALIDA**; campo `itens[0].quantidade`; mensagem presente | **Falhou** |
| 07 — Produto INEXISTENTE | 422, PRODUTO_NAO_ENCONTRADO e campo relacionado | Ambas: 422, PRODUTO_NAO_ENCONTRADO; campo `itens[0].produtoId`; mensagem presente | Aprovado |
| 08 — Quantidade zero | 422, QUANTIDADE_INVALIDA e campo relacionado | Ambas: 422, QUANTIDADE_INVALIDA; campo `itens[0].quantidade`; mensagem presente | Aprovado |
| 09 — Quantidade negativa | 422, QUANTIDADE_INVALIDA e campo relacionado | Ambas: 422, QUANTIDADE_INVALIDA; campo `itens[0].quantidade`; mensagem presente | Aprovado |
| 10 — Quantidade fracionada, 1.5 | 422, QUANTIDADE_INVALIDA e campo relacionado | Ambas: 422, QUANTIDADE_INVALIDA; campo `itens[0].quantidade`; mensagem presente | Aprovado |
| 11 — Quantidade como texto, "1" | 422, QUANTIDADE_INVALIDA e campo relacionado | Ambas: 422, QUANTIDADE_INVALIDA; campo `itens[0].quantidade`; mensagem presente | Aprovado |
| 12 — Quantidade nula | 422, QUANTIDADE_INVALIDA e campo relacionado | Ambas: 422, QUANTIDADE_INVALIDA; campo `itens[0].quantidade`; mensagem presente | Aprovado |
| 13 — Quantidade 6 | 422, QUANTIDADE_MAXIMA_EXCEDIDA e campo relacionado | Cálculo: **200**; pedido: **201**; seis unidades aceitas, sem erro | **Falhou** |
| 14 — Quantidade 100 | 422, QUANTIDADE_MAXIMA_EXCEDIDA e campo relacionado | Cálculo: **200**; pedido: **201**; cem unidades aceitas, sem erro | **Falhou** |

O status 422 indica recusa por causa dos dados enviados. Os status 200 e 201 encontrados nos dois últimos exemplos indicam, respectivamente, cálculo atendido e confirmação aceita. JSON é o formato dos dados enviados e recebidos.

O resultado foi de **10 exemplos aprovados e quatro com falha**. Considerando cada operação separadamente, foram **20 chamadas aprovadas e oito com falha**. Das 168 verificações registradas, 144 passaram e 24 falharam. Várias verificações falharam nas chamadas acima do limite porque houve aceitação em vez de resposta de erro; isso não representa 24 defeitos distintos.

Todas as 28 respostas foram objetos JSON válidos. Nas 24 respostas que recusaram a requisição, o erro apresentou código, mensagem e campo relacionado. Isso inclui os exemplos 05 e 06, cujo formato de erro foi correto, mas cujo código divergiu do BDD.

## Falhas encontradas

### Identificador do produto ausente

O corpo `{"itens":[{"quantidade":1}]}` deveria ser recusado com ITEM_INVALIDO. As duas operações retornaram PRODUTO_NAO_ENCONTRADO e a mensagem “Produto undefined não encontrado.”, apontando `itens[0].produtoId`.

A requisição foi recusada, mas a resposta trata um item incompleto como uma referência a produto inexistente. Isso diverge do código esperado no cenário e pode levar quem usa a API a interpretar o motivo da recusa incorretamente.

### Quantidade ausente

O corpo `{"itens":[{"produtoId":"P001"}]}` deveria ser recusado com ITEM_INVALIDO. As duas operações retornaram QUANTIDADE_INVALIDA, com a mensagem “A quantidade deve ser um número inteiro maior ou igual a 1.” e campo `itens[0].quantidade`.

A requisição também foi recusada, mas o código não diferencia o item incompleto como o BDD exige. Os critérios esperados foram mantidos sem alteração.

### Quantidades acima de cinco aceitas pela API

Os pedidos de seis e cem unidades de P001 deveriam receber 422 e QUANTIDADE_MAXIMA_EXCEDIDA. O cálculo retornou 200 e a confirmação retornou 201 nos dois exemplos, sem objeto de erro.

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Recusar seis unidades de P001 | Sem confirmação; 422 e QUANTIDADE_MAXIMA_EXCEDIDA | Pedido VZ-985961 confirmado com seis unidades, subtotal e total de R$ 359,40 | **Falhou** |
| Recusar cem unidades de P001 | Sem confirmação; 422 e QUANTIDADE_MAXIMA_EXCEDIDA | Pedido VZ-327453 confirmado com cem unidades, subtotal e total de R$ 5.990,00 | **Falhou** |

O impacto observado é que as duas operações aceitam quantidades acima do limite documentado. A proteção da interface não comprova a recusa de requisições enviadas diretamente à API. Esta execução avaliou chamadas diretas e registrou as confirmações fictícias acima do limite. A causa interna não foi investigada.

Não houve bloqueios ou falhas de comunicação. As 28 chamadas foram concluídas.

## Comprovantes do teste

- [Índice completo das 28 chamadas](evidencias/itens-invalidos-api/20261008-114709/indice-evidencias.md), com links para cada corpo enviado, resposta HTTP completa, JSON recebido, validação, comando e registro de erros do curl.
- [Resumo dos exemplos e verificações, com horários](evidencias/itens-invalidos-api/20261008-114709/resumo-validacao.json).
- [Casos e critérios esperados](evidencias/itens-invalidos-api/20261008-114709/criterios.json).
- [Script executado](evidencias/itens-invalidos-api/20261008-114709/teste-api.py) e [lista reproduzível dos 28 comandos capturados](evidencias/itens-invalidos-api/20261008-114709/comandos-executados.sh).
- [Comando da execução](evidencias/itens-invalidos-api/20261008-114709/comando-execucao.txt), [código de saída](evidencias/itens-invalidos-api/20261008-114709/registro-execucao.json), [saída das chamadas](evidencias/itens-invalidos-api/20261008-114709/execucao-stdout.txt) e [erros da execução](evidencias/itens-invalidos-api/20261008-114709/execucao-stderr.txt).

| Exemplo | Cálculo do carrinho | Confirmação do pedido |
| --- | --- | --- |
| 01 — Itens ausentes | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/01-itens-ausentes/calculo/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/01-itens-ausentes/calculo/validacao-api.json) | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/01-itens-ausentes/pedido/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/01-itens-ausentes/pedido/validacao-api.json) |
| 02 — Itens vazios | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/02-itens-vazios/calculo/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/02-itens-vazios/calculo/validacao-api.json) | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/02-itens-vazios/pedido/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/02-itens-vazios/pedido/validacao-api.json) |
| 03 — Item nulo | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/03-item-nulo/calculo/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/03-item-nulo/calculo/validacao-api.json) | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/03-item-nulo/pedido/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/03-item-nulo/pedido/validacao-api.json) |
| 04 — Item como texto | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/04-item-texto/calculo/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/04-item-texto/calculo/validacao-api.json) | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/04-item-texto/pedido/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/04-item-texto/pedido/validacao-api.json) |
| 05 — Identificador ausente | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/05-produto-id-ausente/calculo/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/05-produto-id-ausente/calculo/validacao-api.json) | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/05-produto-id-ausente/pedido/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/05-produto-id-ausente/pedido/validacao-api.json) |
| 06 — Quantidade ausente | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/06-quantidade-ausente/calculo/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/06-quantidade-ausente/calculo/validacao-api.json) | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/06-quantidade-ausente/pedido/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/06-quantidade-ausente/pedido/validacao-api.json) |
| 07 — Produto inexistente | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/07-produto-inexistente/calculo/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/07-produto-inexistente/calculo/validacao-api.json) | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/07-produto-inexistente/pedido/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/07-produto-inexistente/pedido/validacao-api.json) |
| 08 — Quantidade zero | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/08-quantidade-zero/calculo/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/08-quantidade-zero/calculo/validacao-api.json) | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/08-quantidade-zero/pedido/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/08-quantidade-zero/pedido/validacao-api.json) |
| 09 — Quantidade negativa | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/09-quantidade-negativa/calculo/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/09-quantidade-negativa/calculo/validacao-api.json) | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/09-quantidade-negativa/pedido/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/09-quantidade-negativa/pedido/validacao-api.json) |
| 10 — Quantidade fracionada | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/10-quantidade-fracionada/calculo/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/10-quantidade-fracionada/calculo/validacao-api.json) | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/10-quantidade-fracionada/pedido/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/10-quantidade-fracionada/pedido/validacao-api.json) |
| 11 — Quantidade como texto | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/11-quantidade-texto/calculo/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/11-quantidade-texto/calculo/validacao-api.json) | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/11-quantidade-texto/pedido/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/11-quantidade-texto/pedido/validacao-api.json) |
| 12 — Quantidade nula | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/12-quantidade-nula/calculo/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/12-quantidade-nula/calculo/validacao-api.json) | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/12-quantidade-nula/pedido/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/12-quantidade-nula/pedido/validacao-api.json) |
| 13 — Quantidade 6 | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/13-quantidade-seis/calculo/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/13-quantidade-seis/calculo/validacao-api.json) | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/13-quantidade-seis/pedido/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/13-quantidade-seis/pedido/validacao-api.json) |
| 14 — Quantidade 100 | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/14-quantidade-cem/calculo/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/14-quantidade-cem/calculo/validacao-api.json) | [HTTP completo](evidencias/itens-invalidos-api/20261008-114709/14-quantidade-cem/pedido/resposta-http.txt) e [conferência](evidencias/itens-invalidos-api/20261008-114709/14-quantidade-cem/pedido/validacao-api.json) |

Todos os registros de erros do curl estão vazios, e a ferramenta terminou com código 0 em cada chamada. O script de teste terminou com código 1 para sinalizar as divergências funcionais encontradas, sem interromper a execução dos demais exemplos.

Como reprodução da aceitação indevida de seis unidades, estas foram as duas requisições executadas:

```bash
curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular' \
  -H 'Content-Type: application/json' \
  --data-binary '{"itens":[{"produtoId":"P001","quantidade":6}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos' \
  -H 'Content-Type: application/json' \
  --data-binary '{"itens":[{"produtoId":"P001","quantidade":6}],"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

Os comandos dos demais exemplos estão no índice e na lista vinculados acima. Para repetir a automação no projeto:

```bash
python reports/falhas/evidencias/itens-invalidos-api/20261008-114709/teste-api.py
```

Uma nova execução salva suas próprias evidências em outra pasta. Os números das confirmações fictícias podem mudar. O marcador `CURL_HTTP_STATUS` é acrescentado pela ferramenta e não faz parte da resposta da loja. A avaliação considerou o status final da aplicação e manteve a verificação de segurança da conexão ativa.

## Limite desta avaliação

O resultado se aplica aos 14 exemplos e às 28 chamadas desta execução. Não foram avaliados a interface, produtos duplicados, outros tipos de itens inválidos ou combinações diferentes das fornecidas.

A confirmação dos pedidos acima do limite foi observada pelo status 201, número, data e itens retornados. Conforme a documentação, os pedidos e seus números são fictícios neste ambiente; não há armazenamento de pedidos, envio de e-mail ou cobrança real. Não foi feita inspeção do armazenamento interno.
