# Relatório de teste — Confirmar pedido com ou sem cupom

**Resultado: Aprovado — os dois exemplos passaram.** O pedido sem cupom foi confirmado por R$ 119,90. Com BEMVINDO10, recebeu R$ 10,00 de desconto e foi confirmado por R$ 109,90. Os dados do cliente, o número e a data da confirmação vieram conforme esperado.

**Data do teste:** 08/10/2026, das 10h04min09s às 10h04min10s (America/Fortaleza).

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao); cenário em [pedidos.feature](../features/pedidos.feature).

## O que foi testado

Enviamos duas confirmações de pedido diretamente ao serviço da loja (API). Cada pedido continha uma Mochila Urbana 20L (P005), a R$ 100,00. A primeira chamada não enviou cupom; a segunda enviou BEMVINDO10.

Usamos os dados de exemplo fornecidos no cenário e na documentação: Maria Silva, e-mail maria@exemplo.com e CEP 01310-100. Conferimos a confirmação de cada pedido, os dados devolvidos e os valores da compra. Também verificamos se o CEP foi devolvido sem hífen.

## Cenário BDD

```gherkin
Funcionalidade: Validação e confirmação do pedido

  @api
  Esquema do Cenário: Confirmar pedido com ou sem cupom
    Quando envio para "POST /api/pedidos" o JSON:
      """
      {"cliente":{"nome":"Maria Silva","email":"maria@exemplo.com","cep":"01310-100"},"itens":[{"produtoId":"P005","quantidade":1}]<campoCupom>}
      """
    Então a API deve responder com status 201
    E o campo "numero" deve corresponder à expressão regular "^VZ-[0-9]{6}$"
    E o campo "criadoEm" deve conter uma data e hora no formato ISO 8601
    E o campo "cliente.nome" deve ser "Maria Silva"
    E o campo "cliente.email" deve ser "maria@exemplo.com"
    E o campo "cliente.cep" deve ser "01310100"
    E o subtotal deve ser R$ 100,00
    E o desconto deve ser R$ <desconto>
    E o frete deve ser R$ 19,90
    E o campo "freteGratis" deve ser falso
    E o campo "valorFaltanteFreteGratis" deve ser 100
    E o total deve ser R$ <total>

    Exemplos:
      | campoCupom           | desconto | total  |
      |                      | 0,00     | 119,90 |
      | ,"cupom":"BEMVINDO10" | 10,00    | 109,90 |
```

O campo vazio na primeira linha significa que a requisição não contém cupom.

## Resultados da conferência

### Pedido sem cupom

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Confirmação aceita | Status 201, indicando pedido confirmado | Status 201 da aplicação | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido | Aprovado |
| Número da confirmação | VZ- seguido de seis dígitos | VZ-075471 | Aprovado |
| Data e hora da confirmação | Data e hora válidas em ISO 8601 | `2026-10-08T13:04:10.364Z`, formato válido | Aprovado |
| Nome | Maria Silva | Maria Silva | Aprovado |
| E-mail | maria@exemplo.com | maria@exemplo.com | Aprovado |
| CEP sem hífen | 01310100 | 01310100 | Aprovado |
| Produto e quantidade | Uma unidade de P005 | Uma unidade de Mochila Urbana 20L (P005) | Aprovado |
| Cupom | Nenhum | Nenhum | Aprovado |
| Subtotal | R$ 100,00 | R$ 100,00 | Aprovado |
| Desconto | R$ 0,00 | R$ 0,00 | Aprovado |
| Frete | R$ 19,90 | R$ 19,90 | Aprovado |
| Frete grátis | Não | Não | Aprovado |
| Quanto falta para frete grátis | R$ 100,00 | R$ 100,00 | Aprovado |
| Total | R$ 119,90 | R$ 119,90 | Aprovado |

### Pedido com BEMVINDO10

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Confirmação aceita | Status 201, indicando pedido confirmado | Status 201 da aplicação | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido | Aprovado |
| Número da confirmação | VZ- seguido de seis dígitos | VZ-706939 | Aprovado |
| Data e hora da confirmação | Data e hora válidas em ISO 8601 | `2026-10-08T13:04:10.797Z`, formato válido | Aprovado |
| Nome | Maria Silva | Maria Silva | Aprovado |
| E-mail | maria@exemplo.com | maria@exemplo.com | Aprovado |
| CEP sem hífen | 01310100 | 01310100 | Aprovado |
| Produto e quantidade | Uma unidade de P005 | Uma unidade de Mochila Urbana 20L (P005) | Aprovado |
| Cupom | BEMVINDO10 aplicado | BEMVINDO10 aplicado | Aprovado |
| Subtotal | R$ 100,00 | R$ 100,00 | Aprovado |
| Desconto | R$ 10,00 | R$ 10,00 | Aprovado |
| Frete | R$ 19,90 | R$ 19,90 | Aprovado |
| Frete grátis | Não | Não | Aprovado |
| Quanto falta para frete grátis | R$ 100,00 | R$ 100,00 | Aprovado |
| Total | R$ 109,90 | R$ 109,90 | Aprovado |

Sem cupom, o total foi R$ 100,00 + R$ 19,90 = R$ 119,90. Com o cupom, foi R$ 100,00 − R$ 10,00 + R$ 19,90 = R$ 109,90. O frete permaneceu igual nos dois pedidos.

As datas retornadas terminam em `Z`, que indica horário UTC. As duas correspondem a 10h04min10s no horário de Fortaleza. A validação conferiu tanto a escrita do formato quanto a existência de uma data e hora válidas.

## Falhas encontradas

Nenhuma falha foi encontrada nesta execução. Todas as 30 verificações dos dois exemplos passaram. Não houve bloqueios nem exemplos deixados sem execução.

## Comprovantes do teste

### Sem cupom

- [Corpo enviado](evidencias/pedidos-com-sem-cupom/20261008-100409/01-sem-cupom/corpo-enviado.json), [resposta HTTP completa](evidencias/pedidos-com-sem-cupom/20261008-100409/01-sem-cupom/resposta-http.txt) e [dados recebidos](evidencias/pedidos-com-sem-cupom/20261008-100409/01-sem-cupom/corpo-recebido.json).
- [Comparação de cada campo, horário e resultado](evidencias/pedidos-com-sem-cupom/20261008-100409/01-sem-cupom/validacao-api.json), [comando executado](evidencias/pedidos-com-sem-cupom/20261008-100409/01-sem-cupom/comando.txt) e [registro de erros](evidencias/pedidos-com-sem-cupom/20261008-100409/01-sem-cupom/curl-stderr.txt), vazio.

### Com BEMVINDO10

- [Corpo enviado](evidencias/pedidos-com-sem-cupom/20261008-100409/02-com-bemvindo10/corpo-enviado.json), [resposta HTTP completa](evidencias/pedidos-com-sem-cupom/20261008-100409/02-com-bemvindo10/resposta-http.txt) e [dados recebidos](evidencias/pedidos-com-sem-cupom/20261008-100409/02-com-bemvindo10/corpo-recebido.json).
- [Comparação de cada campo, horário e resultado](evidencias/pedidos-com-sem-cupom/20261008-100409/02-com-bemvindo10/validacao-api.json), [comando executado](evidencias/pedidos-com-sem-cupom/20261008-100409/02-com-bemvindo10/comando.txt) e [registro de erros](evidencias/pedidos-com-sem-cupom/20261008-100409/02-com-bemvindo10/curl-stderr.txt), vazio.

### Registros gerais e reprodução

- [Valores esperados dos exemplos](evidencias/pedidos-com-sem-cupom/20261008-100409/casos.json), [resumo dos resultados](evidencias/pedidos-com-sem-cupom/20261008-100409/resumo-validacao.json) e [script executado](evidencias/pedidos-com-sem-cupom/20261008-100409/teste-api.py).

Para a equipe técnica, estas foram as requisições executadas:

```bash
# Sem cupom
curl -i -X POST 'https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos' \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Maria Silva","email":"maria@exemplo.com","cep":"01310-100"},"itens":[{"produtoId":"P005","quantidade":1}]}' \
  --max-time 30 --silent --show-error --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

# Com BEMVINDO10
curl -i -X POST 'https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos' \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Maria Silva","email":"maria@exemplo.com","cep":"01310-100"},"itens":[{"produtoId":"P005","quantidade":1}],"cupom":"BEMVINDO10"}' \
  --max-time 30 --silent --show-error --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

O marcador `CURL_HTTP_STATUS` é acrescentado pela ferramenta e não faz parte da resposta. A avaliação considera o status final da aplicação. As duas chamadas mantiveram a verificação de segurança da conexão ativa e terminaram sem erro de execução do curl. Os valores monetários foram comparados com números decimais exatos, e a indicação de frete grátis foi conferida como falso.

## Limite desta avaliação

Foram executados somente esses dois exemplos, com uma unidade de P005 e os dados de cliente informados. Não foram testados outros produtos, cupons, dados inválidos, a interface ou os limites para conceder frete grátis.

Conforme a documentação, as confirmações e seus números são fictícios neste ambiente; pedidos não são armazenados. A aprovação se refere às respostas observadas, sem avaliar armazenamento interno ou uma operação comercial real.
