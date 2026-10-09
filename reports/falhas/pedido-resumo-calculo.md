# Relatório de teste — Manter o resumo do cálculo na confirmação

**Resultado: Falhou.** O cálculo e a confirmação mantiveram os mesmos valores, mas ambos cobraram R$ 19,90 de frete indevidamente. Para o subtotal de R$ 200,00, o esperado era frete grátis e total de R$ 180,00; a loja retornou R$ 199,90 e confirmou o pedido com esse valor.

**Data do teste:** 08/10/2026, das 10h38min18s às 10h38min19s (America/Fortaleza).

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao), critérios CA08 e CA11; cenário em [pedidos.feature](../../features/pedidos.feature).

## O que foi testado

Calculamos um carrinho com duas Mochilas Urbanas 20L (P005), de R$ 100,00 cada, e o cupom BEMVINDO10. Depois, confirmamos um pedido enviando os mesmos itens, quantidade e cupom.

O teste foi feito diretamente no serviço da loja (API). Para a confirmação, usamos um cliente fictício válido: Cliente Teste, qa@example.com e CEP 01310-100.

Conferimos se o subtotal de R$ 200,00 recebia desconto de R$ 20,00 e frete grátis, resultando em R$ 180,00. Também comparamos todos os oito campos solicitados entre o cálculo e a confirmação. Mesmo após encontrar a divergência no cálculo, executamos a confirmação para verificar o cenário completo.

## Cenário BDD

```gherkin
@api @CA08 @CA11
Cenário: Manter o resumo do cálculo na confirmação
  Dado os itens de 2 unidades do produto "P005"
  Quando calculo o carrinho pela API com o cupom "BEMVINDO10"
  Então a API deve responder com status 200
  E o subtotal deve ser R$ 200,00
  E o desconto deve ser R$ 20,00
  E o frete deve ser R$ 0,00
  E o total deve ser R$ 180,00
  Quando confirmo pela API um pedido com os mesmos itens, cliente válido e o cupom "BEMVINDO10"
  Então a API deve responder com status 201
  E os campos de itens, subtotal, desconto, frete, freteGratis, valorFaltanteFreteGratis, total e cupom devem ser iguais aos do cálculo
```

## Resultados da conferência

### Valores esperados no cálculo

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Cálculo atendido | Status 200 | Status 200 | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido | Aprovado |
| Produto e quantidade | Duas unidades de P005 | Duas unidades de Mochila Urbana 20L (P005) | Aprovado |
| Cupom | BEMVINDO10 aplicado | BEMVINDO10 aplicado | Aprovado |
| Subtotal | R$ 200,00 | R$ 200,00 | Aprovado |
| Desconto | R$ 20,00 | R$ 20,00 | Aprovado |
| Frete | R$ 0,00 | R$ 19,90 | **Falhou** |
| Total | R$ 180,00 | R$ 199,90 | **Falhou** |

JSON é o formato de dados usado pela API. O status 200 indica que a consulta foi atendida; os valores retornados ainda precisam seguir as regras da loja.

### Resposta da confirmação

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Confirmação aceita | Status 201 | Status 201; confirmação VZ-349645 | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido | Aprovado |

A loja retornou o número **VZ-349645** e a data `2026-10-08T13:38:19.620Z`. O total dessa confirmação foi R$ 199,90, reproduzindo a cobrança incorreta do cálculo.

### Comparação entre cálculo e confirmação

Nesta tabela, o esperado é que cada campo permaneça igual ao cálculo. Isso verifica a consistência entre as respostas; os valores corretos do cenário foram avaliados na primeira tabela.

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Itens (`itens`) | Mesmo conteúdo completo | Uma linha de P005, nome Mochila Urbana 20L, preço unitário R$ 100,00, quantidade 2 e total R$ 200,00 em ambas | Aprovado |
| Subtotal (`subtotal`) | Mesmo valor | R$ 200,00 em ambas | Aprovado |
| Desconto (`desconto`) | Mesmo valor | R$ 20,00 em ambas | Aprovado |
| Frete (`frete`) | Mesmo valor | R$ 19,90 em ambas, embora o valor esteja incorreto | Aprovado |
| Frete grátis (`freteGratis`) | Mesmo indicador | Falso em ambas | Aprovado |
| Valor faltante (`valorFaltanteFreteGratis`) | Mesmo valor | R$ 0,00 em ambas | Aprovado |
| Total (`total`) | Mesmo valor | R$ 199,90 em ambas, embora o valor esteja incorreto | Aprovado |
| Cupom (`cupom`) | Mesmo conteúdo completo | Código BEMVINDO10, aplicado verdadeiro e mensagem “Cupom aplicado: 10% de desconto nos produtos.” em ambas | Aprovado |

Das 18 verificações registradas, 16 passaram e duas falharam: frete e total esperados no cálculo. Os oito campos comparados estavam presentes nas duas respostas e foram iguais, incluindo o conteúdo completo de itens e cupom. Essa igualdade não elimina a falha nos valores.

## Falhas encontradas

**Cobrança de frete no limite de R$ 200,00.** O subtotal atingiu o valor necessário para frete grátis antes do desconto, mas a loja retornou frete de R$ 19,90. O desconto de R$ 20,00 foi aplicado corretamente.

**Total acima do esperado e mantido na confirmação.** O esperado era R$ 200,00 − R$ 20,00 + R$ 0,00 = R$ 180,00. A loja calculou R$ 199,90 e confirmou esse mesmo total, uma diferença de R$ 19,90. Neste ambiente de testes, isso representa uma confirmação fictícia com valor incorreto.

Além disso, as duas respostas indicaram `freteGratis: false` e valor faltante de R$ 0,00. Essa combinação reforça a divergência observada no limite do frete grátis. A causa interna não foi investigada. O comportamento também foi observado no [teste anterior de frete pelo subtotal antes do desconto](frete-subtotal-antes-desconto.md).

Não houve bloqueios de execução. As duas chamadas foram realizadas e comparadas.

## Comprovantes do teste

| Chamada | Envio | Resposta | Validação | Execução |
| --- | --- | --- | --- | --- |
| Cálculo | [Corpo enviado](evidencias/pedido-resumo-calculo/20261008-103818/calculo/corpo-enviado.json) | [HTTP completo](evidencias/pedido-resumo-calculo/20261008-103818/calculo/resposta-http.txt) e [JSON recebido](evidencias/pedido-resumo-calculo/20261008-103818/calculo/corpo-recebido.json) | [Conferência dos valores](evidencias/pedido-resumo-calculo/20261008-103818/calculo/validacao-api.json) | [Comando](evidencias/pedido-resumo-calculo/20261008-103818/calculo/comando.txt) e [erros da ferramenta](evidencias/pedido-resumo-calculo/20261008-103818/calculo/curl-stderr.txt) |
| Confirmação | [Corpo enviado](evidencias/pedido-resumo-calculo/20261008-103818/confirmacao/corpo-enviado.json) | [HTTP completo](evidencias/pedido-resumo-calculo/20261008-103818/confirmacao/resposta-http.txt) e [JSON recebido](evidencias/pedido-resumo-calculo/20261008-103818/confirmacao/corpo-recebido.json) | [Comparação dos oito campos](evidencias/pedido-resumo-calculo/20261008-103818/confirmacao/validacao-api.json) | [Comando](evidencias/pedido-resumo-calculo/20261008-103818/confirmacao/comando.txt) e [erros da ferramenta](evidencias/pedido-resumo-calculo/20261008-103818/confirmacao/curl-stderr.txt) |

- [Resumo das verificações e horários](evidencias/pedido-resumo-calculo/20261008-103818/resumo-validacao.json).
- [Critérios e valores esperados](evidencias/pedido-resumo-calculo/20261008-103818/criterios.json).
- [Script executado](evidencias/pedido-resumo-calculo/20261008-103818/teste-api.py).

Os dois arquivos de erros do curl estão vazios, e a ferramenta terminou sem erro de comunicação. O script sinalizou falha porque os valores de frete e total divergiram do cenário.

Para reproduzir, execute primeiro o cálculo e depois a confirmação:

```bash
curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular' \
  -H 'Content-Type: application/json' \
  --data-binary '{"itens":[{"produtoId":"P005","quantidade":2}],"cupom":"BEMVINDO10"}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos' \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"},"itens":[{"produtoId":"P005","quantidade":2}],"cupom":"BEMVINDO10"}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

O marcador `CURL_HTTP_STATUS` foi acrescentado pela ferramenta e não faz parte da resposta da loja. A avaliação considerou o status final da aplicação, preservou a verificação de segurança da conexão e comparou os valores monetários com números decimais exatos.

## Limite desta avaliação

O resultado se aplica a estas duas chamadas, com duas unidades de P005, cupom BEMVINDO10 e o cliente fictício informado. Não foram avaliados a interface, outros produtos ou outros valores de subtotal nesta execução.

A confirmação foi verificada pela resposta da API. Conforme a documentação, os pedidos e seus números são fictícios neste ambiente; não há persistência de pedidos nem cobrança real. Não foi feita inspeção do armazenamento interno.
