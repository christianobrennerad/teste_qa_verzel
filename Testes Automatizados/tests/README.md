# Como executar os cenários com Playwright

A automação foi iniciada em TypeScript com dois cenários de API:

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

Para executar todos os testes de API disponíveis:

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

Essas pastas estão no `.gitignore`. Cada execução padrão substitui os resultados
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

## Retestar os seis relatórios solicitados

Execute os comandos dentro de `Testes Automatizados`:

```bash
npm ci
npx playwright install chromium
npm run test:reteste
npm run report
```

O conjunto possui 15 testes independentes:

| Cenário | Casos | Arquivo |
| --- | --- | --- |
| Frete nos limites do subtotal | 4 | [Teste](interface/frete-limites-subtotal.spec.ts) |
| Frete após alterar a quantidade | 1, com os passos 1 → 2 → 1 | [Teste](interface/frete-alteracao-quantidade.spec.ts) |
| Erros de rota, método e produto | 5 | [Teste](api/erros-rota-metodo-produto.spec.ts) |
| Cupom de desconto apenas nos produtos | 1 | [Teste](interface/cupom-desconto-produtos.spec.ts) |
| Produto duplicado | 2 | [Teste](api/produto-duplicado.spec.ts) |
| CEP com ou sem hífen | 2 | [Teste](api/pedido-cep-formatos.spec.ts) |

Os testes de interface usam Chromium. Cada teste começa em um contexto novo,
monta o carrinho pelos botões da loja e salva telas, valores, requisições e
respostas. As comparações continuam após uma reprovação para conferir os
demais passos do BDD. O teste permanece reprovado quando uma comparação falha.

Para repetir apenas um arquivo, por exemplo:

```bash
npx playwright test tests/interface/frete-alteracao-quantidade.spec.ts --project=interface-chromium
npx playwright test tests/api/pedido-cep-formatos.spec.ts --project=api
```

As requisições são reais e usam somente o ambiente de QA. O desconto exibido
como `- R$ 10,00` é comparado como uma dedução de R$ 10,00. A palavra `Grátis`
representa frete zero nos cenários de valor; no cenário que exige literalmente
duas casas decimais, a apresentação também é comparada com o texto exigido.

Os [relatórios preservados](../reports/README.md) documentam a execução com
6 casos aprovados e 9 reprovados em 09/10/2026. Para abrir esse HTML:

```bash
npm run report -- reports/execucoes/20261009-165827/html
```

Na nuvem, foi usado o navegador em `/usr/bin/chromium`. Para reutilizá-lo em
um ambiente com esse arquivo e a confiança no certificado oficial já
configurada, execute:

```bash
PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium \
NODE_EXTRA_CA_CERTS=/usr/local/share/ca-certificates/environment-proxy-ca.crt \
npm run test:reteste
```

`NODE_EXTRA_CA_CERTS` configura a confiança das chamadas Node. O navegador
também precisa confiar no certificado oficial do ambiente; essa variável não
substitui a configuração de confiança do Chromium. Os testes mantêm a
verificação de certificados ativa.
