# Relatório de teste — Confirmar pedidos repetidos sem consumir estoque

**Resultado: Aprovado.** O mesmo pedido de cinco unidades de P005 foi aceito duas vezes. Cada resposta trouxe subtotal e total de R$ 500,00. Depois das confirmações, P005 continuou disponível no catálogo por R$ 100,00.

**Data do teste:** 08/10/2026, das 09h50min32s às 09h50min34s (America/Fortaleza).

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao), ambiente sem armazenamento de pedidos ou controle de estoque; cenário em [isolamento.feature](../../features/isolamento.feature).

## O que foi testado

Verificamos se a loja aceita duas confirmações do mesmo pedido sem impedir a segunda compra ou retirar o produto do catálogo.

Consultamos o catálogo antes, enviamos duas requisições independentes de confirmação com os mesmos dados e consultamos o catálogo novamente. Cada pedido continha cinco Mochilas Urbanas 20L (P005), a R$ 100,00 cada, sem cupom.

Usamos dados fictícios de cliente: nome **Cliente Teste**, e-mail **qa@example.com** e o CEP de exemplo da documentação, **01310-100**. As confirmações foram feitas diretamente no serviço da loja (API), no ambiente de testes.

## Cenário BDD

```gherkin
@api
Cenário: Confirmar pedidos repetidos sem consumir estoque
  Dado um pedido com cliente válido e 5 unidades do produto "P005"
  Quando confirmo esse pedido duas vezes em requisições independentes
  Então cada requisição deve responder com status 201
  E cada resposta deve conter subtotal de R$ 500,00 e total de R$ 500,00
  E o produto "P005" deve continuar disponível no catálogo pelo preço de R$ 100,00
```

## Resultados da conferência

### Primeira confirmação

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Confirmação aceita | Status 201, indicando pedido confirmado | Status 201 da aplicação | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido | Aprovado |
| Produto e quantidade | Apenas P005, com cinco unidades | Apenas Mochila Urbana 20L (P005), com cinco unidades | Aprovado |
| Subtotal | R$ 500,00 | R$ 500,00 | Aprovado |
| Total | R$ 500,00 | R$ 500,00 | Aprovado |

### Segunda confirmação dos mesmos dados

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Confirmação aceita novamente | Status 201, indicando pedido confirmado | Status 201 da aplicação | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido | Aprovado |
| Produto e quantidade | Apenas P005, com cinco unidades | Apenas Mochila Urbana 20L (P005), com cinco unidades | Aprovado |
| Subtotal | R$ 500,00 | R$ 500,00 | Aprovado |
| Total | R$ 500,00 | R$ 500,00 | Aprovado |

As respostas identificaram as confirmações como **VZ-383477** e **VZ-748497**. Esses números são fictícios, conforme a documentação. Foram registrados para identificar os comprovantes; a diferença entre eles não foi usada como requisito de aprovação.

As duas respostas também informaram desconto e frete de R$ 0,00, sem cupom. O total correspondeu às cinco unidades de R$ 100,00.

### Catálogo antes e depois das confirmações

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Consulta inicial | Status 200 e catálogo válido | Status 200 e lista de produtos em JSON | Aprovado |
| P005 antes dos pedidos | Disponível por R$ 100,00 | Uma entrada de Mochila Urbana 20L (P005), por R$ 100,00 | Aprovado |
| Consulta após os dois pedidos | Status 200 e catálogo válido | Status 200 e lista de produtos em JSON | Aprovado |
| P005 após os dois pedidos | Continuar disponível por R$ 100,00 | Uma entrada de Mochila Urbana 20L (P005), por R$ 100,00 | Aprovado |

## Falhas encontradas

Nenhuma falha foi encontrada nesta execução. Os dois pedidos foram aceitos com os valores esperados, e o produto permaneceu no catálogo pelo mesmo preço. Não houve bloqueios nem etapas deixadas sem execução.

## Comprovantes do teste

### Catálogo antes dos pedidos

- [Resposta HTTP completa](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/01-catalogo-antes/resposta-http.txt), [dados recebidos](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/01-catalogo-antes/corpo-recebido.json) e [comparações, horário e comando](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/01-catalogo-antes/validacao-api.json).
- [Comando executado](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/01-catalogo-antes/comando.txt) e [registro de erros](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/01-catalogo-antes/curl-stderr.txt), vazio.

### Primeira confirmação

- [Corpo enviado com dados fictícios](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/02-primeiro-pedido/corpo-enviado.json), [resposta HTTP completa](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/02-primeiro-pedido/resposta-http.txt), [dados recebidos](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/02-primeiro-pedido/corpo-recebido.json) e [comparações, horário e comando](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/02-primeiro-pedido/validacao-api.json).
- [Comando executado](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/02-primeiro-pedido/comando.txt) e [registro de erros](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/02-primeiro-pedido/curl-stderr.txt), vazio.

### Segunda confirmação

- [Corpo enviado, idêntico ao primeiro](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/03-segundo-pedido/corpo-enviado.json), [resposta HTTP completa](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/03-segundo-pedido/resposta-http.txt), [dados recebidos](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/03-segundo-pedido/corpo-recebido.json) e [comparações, horário e comando](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/03-segundo-pedido/validacao-api.json).
- [Comando executado](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/03-segundo-pedido/comando.txt) e [registro de erros](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/03-segundo-pedido/curl-stderr.txt), vazio.

### Catálogo depois dos pedidos

- [Resposta HTTP completa](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/04-catalogo-depois/resposta-http.txt), [dados recebidos](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/04-catalogo-depois/corpo-recebido.json) e [comparações, horário e comando](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/04-catalogo-depois/validacao-api.json).
- [Comando executado](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/04-catalogo-depois/comando.txt) e [registro de erros](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/04-catalogo-depois/curl-stderr.txt), vazio.

### Registros gerais e reprodução

- [Resumo com a ordem das quatro chamadas e seus resultados](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/resumo-validacao.json).
- [Script executado](evidencias/pedidos-repetidos-sem-estoque/20261008-095032/teste-api.py).

Para a equipe técnica, reproduzir nesta ordem:

```bash
# Catálogo antes
curl -i -X GET 'https://verzel-store.qa-test-verzel-store.workers.dev/api/produtos' \
  -H 'Content-Type: application/json' --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

# Primeira confirmação
curl -i -X POST 'https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos' \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"},"itens":[{"produtoId":"P005","quantidade":5}]}' \
  --max-time 30 --silent --show-error --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

# Segunda confirmação, com os mesmos dados
curl -i -X POST 'https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos' \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"},"itens":[{"produtoId":"P005","quantidade":5}]}' \
  --max-time 30 --silent --show-error --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

# Catálogo depois
curl -i -X GET 'https://verzel-store.qa-test-verzel-store.workers.dev/api/produtos' \
  -H 'Content-Type: application/json' --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

O marcador `CURL_HTTP_STATUS` é acrescentado pela ferramenta e não faz parte da resposta. A avaliação considera o status final da aplicação. Todas as chamadas mantiveram a verificação de segurança da conexão ativa e terminaram sem erro de execução do curl. Os valores monetários foram comparados com números decimais exatos.

## Limite desta avaliação

Foram confirmados somente esses dois pedidos idênticos, sem cupom, com cinco unidades de P005 e dados fictícios. Não foram avaliados outros produtos, quantidades, cupons, requisições simultâneas ou a interface.

A aprovação considera a aceitação dos dois pedidos e a presença e o preço de P005 no catálogo após as confirmações. O catálogo não expõe uma quantidade de estoque. A documentação informa que esse ambiente não controla estoque nem armazena pedidos; o teste não inspeciona armazenamento interno ou uma operação comercial real.
