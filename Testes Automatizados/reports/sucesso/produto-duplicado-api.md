# Relatório de teste — Rejeitar produto duplicado

**Resultado: Aprovado.** A loja recusou P001 repetido em duas linhas de três unidades, tanto no cálculo quanto na confirmação do pedido. As duas respostas devolveram status 422 e ITEM_DUPLICADO, sem confirmação de pedido.

**Data do teste:** 09/10/2026, das 16h58min35s às 16h58min36s (America/Fortaleza).

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Execução:** Playwright 1.64.0; chamadas reais de API, sem abrir navegador. Certificados verificados.

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao); [BDD](<../../../Testes Manuais/features/quantidades_e_itens.feature>); [relatório manual de referência](<../../../Testes Manuais/reports/sucesso/produto-duplicado-api.md>).

## O que foi testado

A loja recusou P001 repetido em duas linhas de três unidades, tanto no cálculo quanto na confirmação do pedido. As duas respostas devolveram status 422 e ITEM_DUPLICADO, sem confirmação de pedido.

Executamos o cenário do relatório manual por meio de testes Playwright. API é o serviço que recebe as requisições da loja; JSON é o formato dos dados enviados e recebidos. Cada comparação foi registrada antes de concluir o resultado.

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

Foram concluídos 2 caso(s), com 6 verificações aprovadas e 0 com falha. Nenhum caso foi pulado ou ficou bloqueado.

### Produto duplicado: calculo

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| API — Requisição recusada | 422 | 422 | Aprovado |
| API — Código de duplicidade | ITEM_DUPLICADO | ITEM_DUPLICADO | Aprovado |
| API — Sem confirmação de pedido | Não | Não | Aprovado |

### Produto duplicado: pedido

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| API — Requisição recusada | 422 | 422 | Aprovado |
| API — Código de duplicidade | ITEM_DUPLICADO | ITEM_DUPLICADO | Aprovado |
| API — Sem confirmação de pedido | Não | Não | Aprovado |

## Falhas encontradas

Nenhuma falha foi encontrada nas verificações desta execução.

## Comprovantes do teste

- [Resumo e horários](evidencias/produto-duplicado-api/20261009-165827/resumo-validacao.json).
- [Teste TypeScript](../../tests/api/produto-duplicado.spec.ts).
- [Relatório HTML completo do Playwright](../execucoes/20261009-165827/html/index.html).
- [Saída da execução](../execucoes/20261009-165827/playwright-stdout.txt) e [mensagens da ferramenta](../execucoes/20261009-165827/playwright-stderr.txt).

### Evidências — Produto duplicado: calculo

- [Conferência de cada passo](evidencias/produto-duplicado-api/20261009-165827/calculo/validacao.json).
- [api-inicio.json](evidencias/produto-duplicado-api/20261009-165827/calculo/api-inicio.json).
- [api-requisicao.json](evidencias/produto-duplicado-api/20261009-165827/calculo/api-requisicao.json).
- [api-resposta-http.json](evidencias/produto-duplicado-api/20261009-165827/calculo/api-resposta-http.json).
- [api-corpo-recebido.json](evidencias/produto-duplicado-api/20261009-165827/calculo/api-corpo-recebido.json).
- [api-comando.txt](evidencias/produto-duplicado-api/20261009-165827/calculo/api-comando.txt).

### Evidências — Produto duplicado: pedido

- [Conferência de cada passo](evidencias/produto-duplicado-api/20261009-165827/pedido/validacao.json).
- [api-inicio.json](evidencias/produto-duplicado-api/20261009-165827/pedido/api-inicio.json).
- [api-requisicao.json](evidencias/produto-duplicado-api/20261009-165827/pedido/api-requisicao.json).
- [api-resposta-http.json](evidencias/produto-duplicado-api/20261009-165827/pedido/api-resposta-http.json).
- [api-corpo-recebido.json](evidencias/produto-duplicado-api/20261009-165827/pedido/api-corpo-recebido.json).
- [api-comando.txt](evidencias/produto-duplicado-api/20261009-165827/pedido/api-comando.txt).

Para repetir somente este cenário, execute na pasta `Testes Automatizados`:

```bash
npx playwright test tests/api/produto-duplicado.spec.ts --project=api
```

Os anexos de resposta preservam o status final da aplicação, os cabeçalhos e o corpo recebidos pelo Playwright. Os arquivos de comando mostram as requisições equivalentes em curl; a execução avaliada foi feita pelo Playwright.

O runner terminou com código 1 porque houve comparações reprovadas no conjunto completo, não por bloqueio de ambiente. A primeira execução foi preservada como diagnóstico de uma correção na leitura do desconto pela automação; a avaliação acima usa somente a execução final.

## Limite desta avaliação

O resultado vale para os exemplos deste BDD e para as respostas e telas da data indicada. Não comprova aprovação de toda a loja. Pedidos e dados de cliente são fictícios no ambiente de QA; não houve pagamento real. Os relatórios manuais e suas evidências não foram alterados.
