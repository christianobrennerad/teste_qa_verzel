# Relatório de teste — Erros de rota, método e produto

**Resultado: Falhou.** As cinco chamadas devolveram os status e códigos esperados. Todas falharam na conferência do formato comum adotado pelo relatório original, pois não retornaram campo relacionado ao erro. A obrigatoriedade dessa informação em erros de rota e método precisa ser esclarecida com Produto.

**Data do teste:** 09/10/2026, das 16h58min30s às 16h58min34s (America/Fortaleza).

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Execução:** Playwright 1.64.0; chamadas reais de API, sem abrir navegador. Certificados verificados.

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao); [BDD](<../../../Testes Manuais/features/contrato_api.feature>); [relatório manual de referência](<../../../Testes Manuais/reports/falhas/erros-rota-metodo-produto.md>).

## O que foi testado

As cinco chamadas devolveram os status e códigos esperados. Todas falharam na conferência do formato comum adotado pelo relatório original, pois não retornaram campo relacionado ao erro. A obrigatoriedade dessa informação em erros de rota e método precisa ser esclarecida com Produto.

Executamos o cenário do relatório manual por meio de testes Playwright. API é o serviço que recebe as requisições da loja; JSON é o formato dos dados enviados e recebidos. Cada comparação foi registrada antes de concluir o resultado.

## Cenário BDD

```gherkin
Contexto:
  Dado que as requisições usam o cabeçalho "Content-Type" com valor "application/json"

Esquema do Cenário: Retornar erros de rota, método e produto
    Quando envio uma requisição "<requisicao>"
    Então a API deve responder com status <status> e corpo JSON
    E o campo "erro.codigo" deve ser "<codigo>"
    E o erro deve seguir o formato documentado

    Exemplos:
      | requisicao                   | status | codigo                 |
      | GET /api/produtos/INEXISTENTE  | 404    | PRODUTO_NAO_ENCONTRADO  |
      | GET /api/rota-inexistente     | 404    | ROTA_NAO_ENCONTRADA     |
      | POST /api/produtos            | 405    | METODO_NAO_PERMITIDO    |
      | GET /api/carrinho/calcular    | 405    | METODO_NAO_PERMITIDO    |
      | GET /api/pedidos              | 405    | METODO_NAO_PERMITIDO    |
```

## Resultados da conferência

Foram concluídos 5 caso(s), com 20 verificações aprovadas e 5 com falha. Nenhum caso foi pulado ou ficou bloqueado.

### Erros de rota: GET /api/produtos/INEXISTENTE

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| API — Status da resposta | 404 | 404 | Aprovado |
| API — Resposta JSON | Sim | Sim | Aprovado |
| API — Código do erro | PRODUTO_NAO_ENCONTRADO | PRODUTO_NAO_ENCONTRADO | Aprovado |
| API — Mensagem do erro preenchida | Sim | Sim | Aprovado |
| API — Formato documentado inclui campo relacionado | Sim | Não | Falhou |

### Erros de rota: GET /api/rota-inexistente

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| API — Status da resposta | 404 | 404 | Aprovado |
| API — Resposta JSON | Sim | Sim | Aprovado |
| API — Código do erro | ROTA_NAO_ENCONTRADA | ROTA_NAO_ENCONTRADA | Aprovado |
| API — Mensagem do erro preenchida | Sim | Sim | Aprovado |
| API — Formato documentado inclui campo relacionado | Sim | Não | Falhou |

### Erros de rota: POST /api/produtos

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| API — Status da resposta | 405 | 405 | Aprovado |
| API — Resposta JSON | Sim | Sim | Aprovado |
| API — Código do erro | METODO_NAO_PERMITIDO | METODO_NAO_PERMITIDO | Aprovado |
| API — Mensagem do erro preenchida | Sim | Sim | Aprovado |
| API — Formato documentado inclui campo relacionado | Sim | Não | Falhou |

### Erros de rota: GET /api/carrinho/calcular

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| API — Status da resposta | 405 | 405 | Aprovado |
| API — Resposta JSON | Sim | Sim | Aprovado |
| API — Código do erro | METODO_NAO_PERMITIDO | METODO_NAO_PERMITIDO | Aprovado |
| API — Mensagem do erro preenchida | Sim | Sim | Aprovado |
| API — Formato documentado inclui campo relacionado | Sim | Não | Falhou |

### Erros de rota: GET /api/pedidos

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| API — Status da resposta | 405 | 405 | Aprovado |
| API — Resposta JSON | Sim | Sim | Aprovado |
| API — Código do erro | METODO_NAO_PERMITIDO | METODO_NAO_PERMITIDO | Aprovado |
| API — Mensagem do erro preenchida | Sim | Sim | Aprovado |
| API — Formato documentado inclui campo relacionado | Sim | Não | Falhou |

## Falhas encontradas

- Nenhum dos cinco erros trouxe erro.campo, embora essa informação esteja no exemplo de formato comum usado pelo relatório de referência. Código, mensagem e status estavam corretos.
- Ponto a esclarecer com Produto: a documentação não define se campo pode ser omitido quando não há um campo do corpo da requisição relacionado ao problema. A classificação mantém o critério do relatório original; não foi inventado um valor esperado para esse campo.

## Comprovantes do teste

- [Resumo e horários](evidencias/erros-rota-metodo-produto/20261009-165827/resumo-validacao.json).
- [Teste TypeScript](../../tests/api/erros-rota-metodo-produto.spec.ts).
- [Relatório HTML completo do Playwright](../execucoes/20261009-165827/html/index.html).
- [Saída da execução](../execucoes/20261009-165827/playwright-stdout.txt) e [mensagens da ferramenta](../execucoes/20261009-165827/playwright-stderr.txt).

### Evidências — Erros de rota: GET /api/produtos/INEXISTENTE

- [Conferência de cada passo](evidencias/erros-rota-metodo-produto/20261009-165827/1-produto_nao_encontrado/validacao.json).
- [api-inicio.json](evidencias/erros-rota-metodo-produto/20261009-165827/1-produto_nao_encontrado/api-inicio.json).
- [api-requisicao.json](evidencias/erros-rota-metodo-produto/20261009-165827/1-produto_nao_encontrado/api-requisicao.json).
- [api-resposta-http.json](evidencias/erros-rota-metodo-produto/20261009-165827/1-produto_nao_encontrado/api-resposta-http.json).
- [api-corpo-recebido.json](evidencias/erros-rota-metodo-produto/20261009-165827/1-produto_nao_encontrado/api-corpo-recebido.json).
- [api-comando.txt](evidencias/erros-rota-metodo-produto/20261009-165827/1-produto_nao_encontrado/api-comando.txt).
- [error-context](evidencias/erros-rota-metodo-produto/20261009-165827/1-produto_nao_encontrado/error-context).

### Evidências — Erros de rota: GET /api/rota-inexistente

- [Conferência de cada passo](evidencias/erros-rota-metodo-produto/20261009-165827/2-rota_nao_encontrada/validacao.json).
- [api-inicio.json](evidencias/erros-rota-metodo-produto/20261009-165827/2-rota_nao_encontrada/api-inicio.json).
- [api-requisicao.json](evidencias/erros-rota-metodo-produto/20261009-165827/2-rota_nao_encontrada/api-requisicao.json).
- [api-resposta-http.json](evidencias/erros-rota-metodo-produto/20261009-165827/2-rota_nao_encontrada/api-resposta-http.json).
- [api-corpo-recebido.json](evidencias/erros-rota-metodo-produto/20261009-165827/2-rota_nao_encontrada/api-corpo-recebido.json).
- [api-comando.txt](evidencias/erros-rota-metodo-produto/20261009-165827/2-rota_nao_encontrada/api-comando.txt).
- [error-context](evidencias/erros-rota-metodo-produto/20261009-165827/2-rota_nao_encontrada/error-context).

### Evidências — Erros de rota: POST /api/produtos

- [Conferência de cada passo](evidencias/erros-rota-metodo-produto/20261009-165827/3-metodo_nao_permitido/validacao.json).
- [api-inicio.json](evidencias/erros-rota-metodo-produto/20261009-165827/3-metodo_nao_permitido/api-inicio.json).
- [api-requisicao.json](evidencias/erros-rota-metodo-produto/20261009-165827/3-metodo_nao_permitido/api-requisicao.json).
- [api-resposta-http.json](evidencias/erros-rota-metodo-produto/20261009-165827/3-metodo_nao_permitido/api-resposta-http.json).
- [api-corpo-recebido.json](evidencias/erros-rota-metodo-produto/20261009-165827/3-metodo_nao_permitido/api-corpo-recebido.json).
- [api-comando.txt](evidencias/erros-rota-metodo-produto/20261009-165827/3-metodo_nao_permitido/api-comando.txt).
- [error-context](evidencias/erros-rota-metodo-produto/20261009-165827/3-metodo_nao_permitido/error-context).

### Evidências — Erros de rota: GET /api/carrinho/calcular

- [Conferência de cada passo](evidencias/erros-rota-metodo-produto/20261009-165827/4-metodo_nao_permitido/validacao.json).
- [api-inicio.json](evidencias/erros-rota-metodo-produto/20261009-165827/4-metodo_nao_permitido/api-inicio.json).
- [api-requisicao.json](evidencias/erros-rota-metodo-produto/20261009-165827/4-metodo_nao_permitido/api-requisicao.json).
- [api-resposta-http.json](evidencias/erros-rota-metodo-produto/20261009-165827/4-metodo_nao_permitido/api-resposta-http.json).
- [api-corpo-recebido.json](evidencias/erros-rota-metodo-produto/20261009-165827/4-metodo_nao_permitido/api-corpo-recebido.json).
- [api-comando.txt](evidencias/erros-rota-metodo-produto/20261009-165827/4-metodo_nao_permitido/api-comando.txt).
- [error-context](evidencias/erros-rota-metodo-produto/20261009-165827/4-metodo_nao_permitido/error-context).

### Evidências — Erros de rota: GET /api/pedidos

- [Conferência de cada passo](evidencias/erros-rota-metodo-produto/20261009-165827/5-metodo_nao_permitido/validacao.json).
- [api-inicio.json](evidencias/erros-rota-metodo-produto/20261009-165827/5-metodo_nao_permitido/api-inicio.json).
- [api-requisicao.json](evidencias/erros-rota-metodo-produto/20261009-165827/5-metodo_nao_permitido/api-requisicao.json).
- [api-resposta-http.json](evidencias/erros-rota-metodo-produto/20261009-165827/5-metodo_nao_permitido/api-resposta-http.json).
- [api-corpo-recebido.json](evidencias/erros-rota-metodo-produto/20261009-165827/5-metodo_nao_permitido/api-corpo-recebido.json).
- [api-comando.txt](evidencias/erros-rota-metodo-produto/20261009-165827/5-metodo_nao_permitido/api-comando.txt).
- [error-context](evidencias/erros-rota-metodo-produto/20261009-165827/5-metodo_nao_permitido/error-context).

Para repetir somente este cenário, execute na pasta `Testes Automatizados`:

```bash
npx playwright test tests/api/erros-rota-metodo-produto.spec.ts --project=api
```

Os anexos de resposta preservam o status final da aplicação, os cabeçalhos e o corpo recebidos pelo Playwright. Os arquivos de comando mostram as requisições equivalentes em curl; a execução avaliada foi feita pelo Playwright.

O runner terminou com código 1 porque houve comparações reprovadas no conjunto completo, não por bloqueio de ambiente. A primeira execução foi preservada como diagnóstico de uma correção na leitura do desconto pela automação; a avaliação acima usa somente a execução final.

## Limite desta avaliação

O resultado vale para os exemplos deste BDD e para as respostas e telas da data indicada. Não comprova aprovação de toda a loja. Pedidos e dados de cliente são fictícios no ambiente de QA; não houve pagamento real. Os relatórios manuais e suas evidências não foram alterados.
