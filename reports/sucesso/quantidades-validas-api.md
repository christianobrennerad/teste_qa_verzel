# Relatório de teste — Aceitar os limites válidos de quantidade

**Resultado: Aprovado.** A loja aceitou uma e cinco unidades de P008 tanto no cálculo do carrinho quanto na confirmação do pedido. Os subtotais foram R$ 50,00 e R$ 250,00, conforme o cenário.

**Data do teste:** 08/10/2026, das 11h39min02s às 11h39min04s (America/Fortaleza).

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao), critério CA10; cenário em [quantidades_e_itens.feature](../../features/quantidades_e_itens.feature).

## O que foi testado

Fizemos quatro chamadas independentes ao serviço da loja (API), usando a Garrafa Térmica 750ml (P008), de R$ 50,00. Calculamos carrinhos com uma e cinco unidades e depois confirmamos pedidos com essas mesmas quantidades.

As quatro requisições incluíram um cliente fictício válido: Cliente Teste, qa@example.com e CEP 01310-100. Os itens foram enviados dentro de `itens`, junto aos dados de `cliente`, conforme o formato da API. Não foi enviado cupom.

Conferimos o status de cada resposta, o subtotal e se o produto e a quantidade retornados correspondiam ao envio.

## Cenário BDD

```gherkin
@CA10 @api
Esquema do Cenário: Aceitar os limites válidos de quantidade
  Quando envio para "<endpoint>" uma requisição com cliente válido e os itens:
    """
    [{"produtoId":"P008","quantidade":<quantidade>}]
    """
  Então a API deve responder com status <status>
  E o subtotal deve ser R$ <subtotal>

  Exemplos:
    | endpoint                   | quantidade | status | subtotal |
    | POST /api/carrinho/calcular | 1          | 200    | 50,00    |
    | POST /api/carrinho/calcular | 5          | 200    | 250,00   |
    | POST /api/pedidos           | 1          | 201    | 50,00    |
    | POST /api/pedidos           | 5          | 201    | 250,00   |
```

## Resultados da conferência

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Calcular carrinho com uma unidade de P008 | Status 200 e subtotal de R$ 50,00 | Status 200 e subtotal de R$ 50,00 | Aprovado |
| Calcular carrinho com cinco unidades de P008 | Status 200 e subtotal de R$ 250,00 | Status 200 e subtotal de R$ 250,00 | Aprovado |
| Confirmar pedido com uma unidade de P008 | Status 201 e subtotal de R$ 50,00 | Status 201 e subtotal de R$ 50,00 | Aprovado |
| Confirmar pedido com cinco unidades de P008 | Status 201 e subtotal de R$ 250,00 | Status 201 e subtotal de R$ 250,00 | Aprovado |
| Dados recebidos nas quatro chamadas | Objetos JSON válidos | Objetos JSON válidos nas quatro respostas | Aprovado |
| Produto e quantidade retornados | Apenas P008, na quantidade enviada em cada exemplo | Apenas P008, com uma ou cinco unidades, conforme o envio | Aprovado |

O status 200 indica que o cálculo foi atendido; o status 201 indica que a confirmação foi aceita. JSON é o formato usado para enviar e receber os dados. As **16 verificações passaram**: status, formato dos dados, subtotal e produto/quantidade em cada um dos quatro exemplos.

O subtotal corresponde a uma unidade × R$ 50,00 = R$ 50,00 ou cinco unidades × R$ 50,00 = R$ 250,00. As confirmações retornaram os números **VZ-655301** para uma unidade e **VZ-426171** para cinco unidades.

## Falhas encontradas

Nenhuma falha foi encontrada nesta execução. Os quatro exemplos retornaram os status e subtotais esperados, com o produto e a quantidade corretos. Não houve bloqueios nem exemplos sem execução.

## Comprovantes do teste

| Chamada | Envio | Resposta | Validação | Execução |
| --- | --- | --- | --- | --- |
| Cálculo — uma unidade | [Corpo enviado](evidencias/quantidades-validas-api/20261008-113902/01-calculo-uma-unidade/corpo-enviado.json) | [HTTP completo](evidencias/quantidades-validas-api/20261008-113902/01-calculo-uma-unidade/resposta-http.txt) e [JSON recebido](evidencias/quantidades-validas-api/20261008-113902/01-calculo-uma-unidade/corpo-recebido.json) | [Conferência](evidencias/quantidades-validas-api/20261008-113902/01-calculo-uma-unidade/validacao-api.json) | [Comando](evidencias/quantidades-validas-api/20261008-113902/01-calculo-uma-unidade/comando.txt) e [erros da ferramenta](evidencias/quantidades-validas-api/20261008-113902/01-calculo-uma-unidade/curl-stderr.txt) |
| Cálculo — cinco unidades | [Corpo enviado](evidencias/quantidades-validas-api/20261008-113902/02-calculo-cinco-unidades/corpo-enviado.json) | [HTTP completo](evidencias/quantidades-validas-api/20261008-113902/02-calculo-cinco-unidades/resposta-http.txt) e [JSON recebido](evidencias/quantidades-validas-api/20261008-113902/02-calculo-cinco-unidades/corpo-recebido.json) | [Conferência](evidencias/quantidades-validas-api/20261008-113902/02-calculo-cinco-unidades/validacao-api.json) | [Comando](evidencias/quantidades-validas-api/20261008-113902/02-calculo-cinco-unidades/comando.txt) e [erros da ferramenta](evidencias/quantidades-validas-api/20261008-113902/02-calculo-cinco-unidades/curl-stderr.txt) |
| Pedido — uma unidade | [Corpo enviado](evidencias/quantidades-validas-api/20261008-113902/03-pedido-uma-unidade/corpo-enviado.json) | [HTTP completo](evidencias/quantidades-validas-api/20261008-113902/03-pedido-uma-unidade/resposta-http.txt) e [JSON recebido](evidencias/quantidades-validas-api/20261008-113902/03-pedido-uma-unidade/corpo-recebido.json) | [Conferência](evidencias/quantidades-validas-api/20261008-113902/03-pedido-uma-unidade/validacao-api.json) | [Comando](evidencias/quantidades-validas-api/20261008-113902/03-pedido-uma-unidade/comando.txt) e [erros da ferramenta](evidencias/quantidades-validas-api/20261008-113902/03-pedido-uma-unidade/curl-stderr.txt) |
| Pedido — cinco unidades | [Corpo enviado](evidencias/quantidades-validas-api/20261008-113902/04-pedido-cinco-unidades/corpo-enviado.json) | [HTTP completo](evidencias/quantidades-validas-api/20261008-113902/04-pedido-cinco-unidades/resposta-http.txt) e [JSON recebido](evidencias/quantidades-validas-api/20261008-113902/04-pedido-cinco-unidades/corpo-recebido.json) | [Conferência](evidencias/quantidades-validas-api/20261008-113902/04-pedido-cinco-unidades/validacao-api.json) | [Comando](evidencias/quantidades-validas-api/20261008-113902/04-pedido-cinco-unidades/comando.txt) e [erros da ferramenta](evidencias/quantidades-validas-api/20261008-113902/04-pedido-cinco-unidades/curl-stderr.txt) |

- [Resumo dos resultados e horários](evidencias/quantidades-validas-api/20261008-113902/resumo-validacao.json).
- [Casos, cliente fictício e valores esperados](evidencias/quantidades-validas-api/20261008-113902/criterios.json).
- [Script executado](evidencias/quantidades-validas-api/20261008-113902/teste-api.py).

Os quatro arquivos de erros do curl estão vazios, e a ferramenta terminou sem erro de comunicação em todas as chamadas. As respostas HTTP completas preservam o status e os cabeçalhos; as validações registram horários, comandos e comparações.

Para reproduzir as quatro requisições executadas:

```bash
curl -i -X POST \
  https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"},"itens":[{"produtoId":"P008","quantidade":1}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"},"itens":[{"produtoId":"P008","quantidade":5}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"},"itens":[{"produtoId":"P008","quantidade":1}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST \
  https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"},"itens":[{"produtoId":"P008","quantidade":5}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

O marcador `CURL_HTTP_STATUS` foi acrescentado pela ferramenta e não faz parte da resposta da loja. A avaliação considerou o status final da aplicação, manteve a verificação de segurança da conexão ativa e comparou os subtotais com números decimais exatos.

## Limite desta avaliação

A aprovação se aplica às quatro chamadas, ao produto P008 e às quantidades de uma e cinco unidades. Não foram avaliadas quantidades intermediárias, acima do limite, outros produtos, cupom ou a interface nesta execução.

O cenário avaliou subtotal, status e a correspondência dos itens. Frete e total não fazem parte dos critérios deste relatório. Segundo a documentação, os pedidos e seus números são fictícios neste ambiente; pedidos não são armazenados e nenhuma cobrança real é feita.
