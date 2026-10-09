# Como executar os cenários com Playwright

A automação foi iniciada em TypeScript com dois cenários que você já testou:

- [Identificar o campo da quantidade inválida](api/campo-quantidade-invalida.spec.ts): um teste com quantidade zero.
- [Aceitar os limites válidos de quantidade](api/quantidades-validas.spec.ts): quatro testes, um para cada linha da tabela de exemplos.

Os cinco testes usam a API da loja. Eles não abrem navegador nem precisam de
`npx playwright install`. As confirmações de pedido usam dados fictícios no
ambiente de QA descrito pela documentação.

## Preparar o projeto

Abra o terminal na pasta deste repositório. Use Node.js 20 ou superior e execute:

```bash
npm ci
```

Mesmo que o Playwright esteja instalado em outro projeto ou globalmente, este
comando instala as versões registradas em `package-lock.json` neste projeto.

## Executar um cenário

Comece pelo cenário de quantidade zero:

```bash
npm run test:quantidade-zero
```

A mesma execução pode ser feita diretamente pelo Playwright:

```bash
npx playwright test tests/api/campo-quantidade-invalida.spec.ts --project=api
```

O teste envia P001 com quantidade zero e compara a resposta com os valores do
BDD: status 422, código QUANTIDADE_INVALIDA, mensagem completa e campo
`itens[0].quantidade`. Uma comparação diferente faz o teste falhar.

## Executar os quatro exemplos da tabela

```bash
npx playwright test tests/api/quantidades-validas.spec.ts --project=api
```

Cada objeto em `exemplos` corresponde a uma linha da tabela do BDD. O laço cria
um teste independente para cada combinação de operação e quantidade. Assim,
você consegue identificar qual exemplo passou ou falhou.

Para executar os cinco testes:

```bash
npm run test:api
```

Para conferir os tipos do TypeScript:

```bash
npm run typecheck
```

## Ver os resultados e as evidências

Depois da execução, abra o relatório:

```bash
npm run report
```

O Playwright também mostra o resultado no terminal. No relatório HTML, abra um
teste para consultar os anexos `requisicao.json`, `resposta-http.json` e
`corpo-recebido.json`. Eles registram os dados enviados, horários, status,
cabeçalhos e corpo recebido antes das comparações, inclusive quando uma
comparação falha.

Os arquivos gerados ficam em:

- `playwright-report/`: relatório HTML.
- `test-results/`: anexos e resumo `resultados.json`.

Essas pastas estão no `.gitignore`. Cada execução substitui os resultados
anteriores nessas pastas. Para guardar uma execução histórica, copie os
resultados para uma pasta nova de evidências antes de executar novamente.
O relatório automático é HTML/JSON; relatórios de QA em Markdown continuam
seguindo o padrão de `AGENTS.md`. Guarde relatórios e evidências aprovados em
`reports/sucesso/` e os que falharam em `reports/falhas/`, conforme o
[índice dos relatórios](../reports/README.md). Quando um esquema do cenário
contiver exemplos aprovados e reprovados, preserve a execução completa na
pasta de falhas, identificando cada resultado no relatório.

## Transformar outro BDD em teste

Crie um arquivo `tests/api/nome-do-cenario.spec.ts`, seguindo o exemplo existente:

```typescript
import { test, expect } from '../suporte/fixtures';
import { enviarPost } from '../suporte/http';

test('Nome do cenário', async ({ request }, testInfo) => {
  // Dado: prepare os dados exatamente como no BDD.
  const corpo = { itens: [{ produtoId: 'P008', quantidade: 1 }] };

  // Quando: faça a requisição real.
  const resposta = await enviarPost(
    request,
    testInfo,
    '/api/carrinho/calcular',
    corpo,
  );

  // Então: compare o resultado com o esperado.
  expect(resposta.status()).toBe(200);
  const dados = await resposta.json();
  expect(dados.subtotal).toBe(50);
});
```

O Playwright executa os arquivos `.spec.ts`. Os arquivos `.feature` são a
referência dos cenários e não são executados automaticamente por esta
configuração. Os passos são traduzidos em dados, requisições e comparações nos
testes TypeScript.

## Configuração do ambiente

A URL da loja está em `playwright.config.ts`. Para outro ambiente autorizado,
defina `BASE_URL` antes de executar. Os testes usam as mesmas rotas.

Quando `HTTPS_PROXY` ou `https_proxy` estiver definido, a configuração de apoio
usa esse proxy sem gravar suas credenciais nos anexos. A verificação de
certificados permanece ativa. Se o ambiente fornecer uma autoridade de
certificação oficial, o Node pode usá-la por `NODE_EXTRA_CA_CERTS`.

Este projeto ainda não tem testes de interface do Playwright. Os exemplos
atuais demonstram o fluxo de API; testes de interface também exigirão o
navegador correspondente instalado pelo Playwright.
