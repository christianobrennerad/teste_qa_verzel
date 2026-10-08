# Relatório de teste — Normalizar o cupom na confirmação do pedido

**Resultado: Aprovado.** A loja aceitou o cupom em letras minúsculas, com dois espaços no início e dois no fim. A confirmação retornou BEMVINDO10 aplicado e total de R$ 109,90.

**Data do teste:** 08/10/2026, das 10h14min15s às 10h14min16s (America/Fortaleza).

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao), critério CA02; cenário em [pedidos.feature](../features/pedidos.feature).

## O que foi testado

Confirmamos um pedido de uma Mochila Urbana 20L (P005), a R$ 100,00, enviando o cupom exatamente como `"  bemvindo10  "`. Os espaços dentro das aspas fazem parte do código enviado: são dois antes e dois depois de `bemvindo10`.

O teste foi feito diretamente no serviço da loja (API), usando os dados de cliente apresentados no cenário e na documentação. O cupom foi enviado sem remover espaços ou alterar as letras antes da requisição. Conferimos se a loja reconhecia BEMVINDO10, aplicava o cupom e confirmava o total esperado.

## Cenário BDD

```gherkin
@CA02 @api
Cenário: Normalizar o cupom também na confirmação do pedido
  Quando envio para "POST /api/pedidos" o JSON:
    """
    {"cliente":{"nome":"Maria Silva","email":"maria@exemplo.com","cep":"01310100"},"itens":[{"produtoId":"P005","quantidade":1}],"cupom":"  bemvindo10  "}
    """
  Então a API deve responder com status 201
  E o campo "cupom.codigo" deve ser "BEMVINDO10"
  E o campo "cupom.aplicado" deve ser verdadeiro
  E o total deve ser R$ 109,90
```

## Resultados da conferência

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Cupom enviado | `"  bemvindo10  "`, com espaços reais e letras minúsculas | Exatamente esse valor, com dois espaços em cada extremidade | Aprovado |
| Confirmação aceita | Status 201, indicando pedido confirmado | Status 201 da aplicação | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido | Aprovado |
| Código reconhecido | BEMVINDO10 | BEMVINDO10 | Aprovado |
| Cupom aplicado | Verdadeiro | Verdadeiro | Aprovado |
| Total | R$ 109,90 | R$ 109,90 | Aprovado |
| Produto e quantidade | Uma unidade de P005 | Uma unidade de Mochila Urbana 20L (P005) | Aprovado |
| Subtotal | R$ 100,00 | R$ 100,00 | Aprovado |
| Desconto | R$ 10,00 | R$ 10,00 | Aprovado |
| Frete | R$ 19,90 | R$ 19,90 | Aprovado |

A resposta identificou a confirmação como **VZ-891116**. O total correspondeu a R$ 100,00 − R$ 10,00 + R$ 19,90 = R$ 109,90. O cupom recebido na resposta foi BEMVINDO10, sem os espaços e com letras maiúsculas.

## Falhas encontradas

Nenhuma falha foi encontrada nesta execução. O cupom foi reconhecido e aplicado com o total esperado. Não houve bloqueios nem passos deixados sem execução.

## Comprovantes do teste

- [Corpo enviado, com os espaços originais](evidencias/pedido-cupom-normalizacao/20261008-101415/corpo-enviado.json).
- [Comprovação do cupom enviado](evidencias/pedido-cupom-normalizacao/20261008-101415/cupom-enviado.json): 14 caracteres, incluindo dois espaços no início e dois no fim; os espaços têm código de caractere 32.
- [Resposta HTTP completa, com status e cabeçalhos](evidencias/pedido-cupom-normalizacao/20261008-101415/resposta-http.txt) e [dados recebidos](evidencias/pedido-cupom-normalizacao/20261008-101415/corpo-recebido.json).
- [Comparação de cada campo, horários e resultado](evidencias/pedido-cupom-normalizacao/20261008-101415/validacao-api.json).
- [Comando executado](evidencias/pedido-cupom-normalizacao/20261008-101415/comando.txt) e [script do teste](evidencias/pedido-cupom-normalizacao/20261008-101415/teste-api.py).
- [Registro de erros do curl](evidencias/pedido-cupom-normalizacao/20261008-101415/curl-stderr.txt): vazio. A ferramenta terminou sem erro de execução.

Para a equipe técnica, esta foi a requisição executada:

```bash
curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos' \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Maria Silva","email":"maria@exemplo.com","cep":"01310100"},"itens":[{"produtoId":"P005","quantidade":1}],"cupom":"  bemvindo10  "}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

O marcador `CURL_HTTP_STATUS` é acrescentado pela ferramenta e não faz parte da resposta. A avaliação considera o status final da aplicação e manteve a verificação de segurança da conexão ativa. O valor de total e os demais valores monetários conferidos foram comparados com números decimais exatos.

## Limite desta avaliação

Foi testada somente a confirmação deste pedido, com uma unidade de P005 e o cupom indicado. Não foram avaliadas outras combinações de letras, espaços internos, tabulações, outros produtos ou a apresentação na interface.

Conforme a documentação, as confirmações e seus números são fictícios neste ambiente; pedidos não são armazenados. A aprovação se refere à resposta observada nesta execução.
