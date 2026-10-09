# Relatório de teste — Aceitar CEP com ou sem hífen

**Resultado: Aprovado.** A loja confirmou os dois pedidos e devolveu o CEP como texto 01310100, sem hífen e mantendo o zero inicial, nos dois formatos enviados.

**Data do teste:** 09/10/2026, das 16h58min35s às 16h58min35s (America/Fortaleza).

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Execução:** Playwright 1.64.0; chamadas reais de API, sem abrir navegador. Certificados verificados.

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao); [BDD](<../../../Testes Manuais/features/pedidos.feature>); [relatório manual de referência](<../../../Testes Manuais/reports/sucesso/pedido-cep-formatos.md>).

## O que foi testado

A loja confirmou os dois pedidos e devolveu o CEP como texto 01310100, sem hífen e mantendo o zero inicial, nos dois formatos enviados.

Executamos o cenário do relatório manual por meio de testes Playwright. API é o serviço que recebe as requisições da loja; JSON é o formato dos dados enviados e recebidos. Cada comparação foi registrada antes de concluir o resultado.

## Cenário BDD

```gherkin
@api
Esquema do Cenário: Aceitar CEP com ou sem hífen
  Quando confirmo um pedido de uma unidade do produto "P005" com os dados:
    | nome        | email             | cep   |
    | Maria Silva | maria@exemplo.com | <cep> |
  Então a API deve responder com status 201
  E o campo "cliente.cep" deve ser "01310100"

  Exemplos:
    | cep       |
    | 01310-100 |
    | 01310100  |
```

## Resultados da conferência

Foram concluídos 2 caso(s), com 6 verificações aprovadas e 0 com falha. Nenhum caso foi pulado ou ficou bloqueado.

### Pedido com CEP 01310-100

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| API — Pedido confirmado | 201 | 201 | Aprovado |
| API — CEP normalizado, incluindo zero inicial | 01310100 | 01310100 | Aprovado |
| API — Produto e quantidade | [{"produtoId": "P005", "quantidade": 1}] | [{"produtoId": "P005", "quantidade": 1}] | Aprovado |

### Pedido com CEP 01310100

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| API — Pedido confirmado | 201 | 201 | Aprovado |
| API — CEP normalizado, incluindo zero inicial | 01310100 | 01310100 | Aprovado |
| API — Produto e quantidade | [{"produtoId": "P005", "quantidade": 1}] | [{"produtoId": "P005", "quantidade": 1}] | Aprovado |

## Falhas encontradas

Nenhuma falha foi encontrada nas verificações desta execução.

## Comprovantes do teste

- [Resumo e horários](evidencias/pedido-cep-formatos/20261009-165827/resumo-validacao.json).
- [Teste TypeScript](../../tests/api/pedido-cep-formatos.spec.ts).
- [Relatório HTML completo do Playwright](../execucoes/20261009-165827/html/index.html).
- [Saída da execução](../execucoes/20261009-165827/playwright-stdout.txt) e [mensagens da ferramenta](../execucoes/20261009-165827/playwright-stderr.txt).

### Evidências — Pedido com CEP 01310-100

- [Conferência de cada passo](evidencias/pedido-cep-formatos/20261009-165827/com-hifen/validacao.json).
- [api-inicio.json](evidencias/pedido-cep-formatos/20261009-165827/com-hifen/api-inicio.json).
- [api-requisicao.json](evidencias/pedido-cep-formatos/20261009-165827/com-hifen/api-requisicao.json).
- [api-resposta-http.json](evidencias/pedido-cep-formatos/20261009-165827/com-hifen/api-resposta-http.json).
- [api-corpo-recebido.json](evidencias/pedido-cep-formatos/20261009-165827/com-hifen/api-corpo-recebido.json).
- [api-comando.txt](evidencias/pedido-cep-formatos/20261009-165827/com-hifen/api-comando.txt).

### Evidências — Pedido com CEP 01310100

- [Conferência de cada passo](evidencias/pedido-cep-formatos/20261009-165827/sem-hifen/validacao.json).
- [api-inicio.json](evidencias/pedido-cep-formatos/20261009-165827/sem-hifen/api-inicio.json).
- [api-requisicao.json](evidencias/pedido-cep-formatos/20261009-165827/sem-hifen/api-requisicao.json).
- [api-resposta-http.json](evidencias/pedido-cep-formatos/20261009-165827/sem-hifen/api-resposta-http.json).
- [api-corpo-recebido.json](evidencias/pedido-cep-formatos/20261009-165827/sem-hifen/api-corpo-recebido.json).
- [api-comando.txt](evidencias/pedido-cep-formatos/20261009-165827/sem-hifen/api-comando.txt).

Para repetir somente este cenário, execute na pasta `Testes Automatizados`:

```bash
npx playwright test tests/api/pedido-cep-formatos.spec.ts --project=api
```

Os anexos de resposta preservam o status final da aplicação, os cabeçalhos e o corpo recebidos pelo Playwright. Os arquivos de comando mostram as requisições equivalentes em curl; a execução avaliada foi feita pelo Playwright.

O runner terminou com código 1 porque houve comparações reprovadas no conjunto completo, não por bloqueio de ambiente. A primeira execução foi preservada como diagnóstico de uma correção na leitura do desconto pela automação; a avaliação acima usa somente a execução final.

## Limite desta avaliação

O resultado vale para os exemplos deste BDD e para as respostas e telas da data indicada. Não comprova aprovação de toda a loja. Pedidos e dados de cliente são fictícios no ambiente de QA; não houve pagamento real. Os relatórios manuais e suas evidências não foram alterados.
