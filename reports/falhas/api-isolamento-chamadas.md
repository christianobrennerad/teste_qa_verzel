# Relatório de teste — Calcular cada chamada sem reutilizar itens ou cupom anteriores

**Resultado: Falhou no total da primeira chamada.** O carrinho com duas unidades de P005 e BEMVINDO10 retornou R$ 199,90, em vez de R$ 180,00. A segunda chamada passou: trouxe apenas uma unidade de P008, sem cupom e com total de R$ 69,90. Não houve reutilização de itens ou cupom nessa sequência.

**Data do teste:** 08/10/2026, das 09h37min46s às 09h37min47s (America/Fortaleza).

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao), regra de cálculo independente por chamada; cenário em [isolamento.feature](../../features/isolamento.feature).

## O que foi testado

Verificamos se o serviço de cálculo da loja (API) considera somente os dados enviados em cada chamada.

Primeiro, enviamos duas Mochilas Urbanas 20L (P005) com BEMVINDO10. Depois, enviamos uma Garrafa Térmica 750ml (P008), sem cupom. As duas requisições foram executadas nessa ordem, na mesma execução da ferramenta curl. A segunda foi realizada mesmo após encontrarmos a divergência no primeiro total.

Conferimos os resultados esperados e verificamos se P005 ou BEMVINDO10 apareciam indevidamente na segunda resposta.

## Cenário BDD

```gherkin
@api
Cenário: Calcular cada chamada sem reutilizar itens ou cupom anteriores
  Quando envio para "POST /api/carrinho/calcular" o JSON:
    """
    {"itens":[{"produtoId":"P005","quantidade":2}],"cupom":"BEMVINDO10"}
    """
  Então a API deve responder com status 200
  E o total deve ser R$ 180,00
  Quando envio para "POST /api/carrinho/calcular" o JSON:
    """
    {"itens":[{"produtoId":"P008","quantidade":1}]}
    """
  Então a API deve responder com status 200
  E a resposta deve conter apenas o produto "P008" com quantidade 1
  E o subtotal deve ser R$ 50,00
  E o desconto deve ser R$ 0,00
  E o frete deve ser R$ 19,90
  E o total deve ser R$ 69,90
```

## Resultados da conferência

### Primeira chamada — duas unidades de P005 com cupom

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Atendimento da solicitação | Status 200, indicando sucesso | Status 200 da aplicação | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido | Aprovado |
| Produto e quantidade enviados | Apenas P005, com duas unidades | Apenas P005, com duas unidades | Aprovado |
| Cupom | BEMVINDO10 aplicado | BEMVINDO10 aplicado | Aprovado |
| Total | R$ 180,00 | R$ 199,90 | Falhou |

O retorno mostrou subtotal de R$ 200,00 e desconto de R$ 20,00, mas manteve frete de R$ 19,90. A documentação prevê frete grátis a partir de R$ 200,00 em produtos, considerando o valor antes do desconto. Portanto, o esperado era R$ 200,00 − R$ 20,00 + R$ 0,00 = R$ 180,00.

### Segunda chamada — uma unidade de P008 sem cupom

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Atendimento da solicitação | Status 200, indicando sucesso | Status 200 da aplicação | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido | Aprovado |
| Produto e quantidade | Apenas P008, com uma unidade | Apenas Garrafa Térmica 750ml (P008), com uma unidade; P005 ausente | Aprovado |
| Cupom da primeira chamada | Nenhum cupom reutilizado | Nenhum cupom na segunda resposta | Aprovado |
| Subtotal | R$ 50,00 | R$ 50,00 | Aprovado |
| Desconto | R$ 0,00 | R$ 0,00 | Aprovado |
| Frete | R$ 19,90 | R$ 19,90 | Aprovado |
| Total | R$ 69,90 | R$ 69,90 | Aprovado |

A segunda resposta correspondeu somente ao carrinho enviado nela. O desconto anterior não foi reutilizado, e o valor foi calculado corretamente: R$ 50,00 + R$ 19,90 = R$ 69,90.

O isolamento observado nesta sequência passou. O cenário completo permanece reprovado porque também exige o total correto na primeira chamada.

## Falhas encontradas

**F01 — Frete cobrado no primeiro carrinho, com R$ 200,00 em produtos.** A primeira resposta retornou frete de R$ 19,90 e total de R$ 199,90, quando deveria conceder frete grátis e total de R$ 180,00.

**Impacto observado:** o total apresentado fica **R$ 19,90 acima do esperado**. Nenhum pedido foi confirmado.

**Como reproduzir:** enviar duas unidades de P005 com BEMVINDO10 ao serviço de cálculo e comparar o total recebido com R$ 180,00. O JSON e o comando estão nas evidências abaixo.

A mesma cobrança no limite exato de R$ 200,00 já foi registrada no teste de [frete pelo subtotal antes do desconto](frete-subtotal-antes-desconto.md). A divergência deste cenário está no cálculo do primeiro carrinho; não foi observado reaproveitamento de itens ou cupom na segunda chamada.

As duas chamadas foram executadas. Não houve bloqueios nem passos deixados sem execução.

## Comprovantes do teste

### Primeira chamada — falhou

- [Corpo enviado](evidencias/api-isolamento-chamadas/20261008-093746/01-p005-com-cupom/corpo-enviado.json).
- [Resposta HTTP completa, com status e cabeçalhos](evidencias/api-isolamento-chamadas/20261008-093746/01-p005-com-cupom/resposta-http.txt) e [dados recebidos](evidencias/api-isolamento-chamadas/20261008-093746/01-p005-com-cupom/corpo-recebido.json).
- [Comparações e resultado de cada verificação](evidencias/api-isolamento-chamadas/20261008-093746/01-p005-com-cupom/validacao-api.json).

### Segunda chamada — aprovada

- [Corpo enviado](evidencias/api-isolamento-chamadas/20261008-093746/02-p008-sem-cupom/corpo-enviado.json).
- [Resposta HTTP completa, com status e cabeçalhos](evidencias/api-isolamento-chamadas/20261008-093746/02-p008-sem-cupom/resposta-http.txt) e [dados recebidos](evidencias/api-isolamento-chamadas/20261008-093746/02-p008-sem-cupom/corpo-recebido.json).
- [Comparações e resultado de cada verificação](evidencias/api-isolamento-chamadas/20261008-093746/02-p008-sem-cupom/validacao-api.json).

### Sequência e reprodução

- [Resumo com ordem das chamadas, horários e comando](evidencias/api-isolamento-chamadas/20261008-093746/resumo-validacao.json) e [corpos e resultados esperados](evidencias/api-isolamento-chamadas/20261008-093746/casos.json).
- [Comando executado](evidencias/api-isolamento-chamadas/20261008-093746/comando.txt) e [script do teste](evidencias/api-isolamento-chamadas/20261008-093746/teste-api.py).
- [Status final e código de saída de cada requisição](evidencias/api-isolamento-chamadas/20261008-093746/curl-stdout.txt). As duas retornaram status 200, e a ferramenta terminou sem erro de execução.
- [Registro de erros do curl](evidencias/api-isolamento-chamadas/20261008-093746/curl-stderr.txt): vazio.

Para a equipe técnica, a sequência pode ser reproduzida assim, usando os mesmos corpos e parâmetros da execução:

```bash
curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular' \
  -H 'Content-Type: application/json' \
  --data-binary '{"itens":[{"produtoId":"P005","quantidade":2}],"cupom":"BEMVINDO10"}' \
  --max-time 30 --silent --show-error \
  --write-out '\nREQUISICAO_1_STATUS:%{http_code};EXIT:%{exitcode}\n' \
  --next \
  -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular' \
  -H 'Content-Type: application/json' \
  --data-binary '{"itens":[{"produtoId":"P008","quantidade":1}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nREQUISICAO_2_STATUS:%{http_code};EXIT:%{exitcode}\n'
```

Na execução registrada, cada resposta foi salva separadamente com `--output`; os caminhos exatos estão no arquivo de comando. `--next` separa as duas chamadas na mesma execução, sem paralelismo. Os marcadores de status e código de saída são acrescentados pelo curl e não fazem parte da resposta da loja. A avaliação considera o status final da aplicação e mantém a verificação de segurança da conexão ativa.

## Limite desta avaliação

Foram testadas somente essas duas chamadas, nessa ordem. O resultado demonstra ausência de reutilização de P005 e BEMVINDO10 na segunda resposta desta sequência, mas não comprova todas as combinações possíveis ou concorrência entre clientes.

Não foram avaliados a interface, a confirmação de pedidos, estoque ou armazenamento interno do serviço. As conclusões se baseiam nas respostas observadas.
