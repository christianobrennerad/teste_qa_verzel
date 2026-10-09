# Desafio QA — Verzel Store

Projeto de testes para a Verzel Store, baseado na documentação do card **VZS-142, versão 2.3.0**. A entrega reúne cenários BDD, relatórios de testes manuais e automação de API e interface com **Playwright e TypeScript**.

- **Repositório:** [christianobrennerad/teste_qa_verzel](https://github.com/christianobrennerad/teste_qa_verzel).
- **Ambiente testado:** [Verzel Store](https://verzel-store.qa-test-verzel-store.workers.dev).
- **Regras utilizadas:** [Documentação da loja](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao).

## Onde e como usei IA

Usei **ChatGPT/Codex, da OpenAI**, durante a preparação, execução e documentação do desafio. O uso incluiu a criação de código de automação e a execução de testes por meio das ferramentas do ambiente em nuvem.

Forneci a documentação e os cenários a verificar, solicitei as execuções e defini o padrão dos relatórios: linguagem simples para Produto, BDD completo, comparação entre esperado e encontrado e evidências salvas. Também defini a separação entre testes manuais e automatizados e entre resultados aprovados e reprovados.

| Etapa | Como a IA foi utilizada |
| --- | --- |
| Planejamento | Organizou os requisitos da documentação em cenários BDD e arquivos `.feature`. |
| Testes manuais e de API | Executou requisições e interações com a loja pelas ferramentas disponíveis, conferiu respostas e registrou os resultados. |
| Automação | Criou a configuração e os testes Playwright em TypeScript, incluindo dados de entrada, ações na interface e comparações com os valores esperados. |
| Ambiente | Auxiliou na preparação das dependências, configuração do navegador e uso do certificado oficial do proxy, mantendo a validação de certificados ativa. |
| Evidências e relatórios | Salvou requisições, respostas, horários e capturas; escreveu relatórios Markdown e gerou o HTML do Playwright. |
| Organização | Separou os arquivos por resultado e auxiliou nas alterações e publicações no Git, conforme minhas solicitações. |

Um exemplo de correção durante esse processo foi a leitura do desconto na tela: a primeira versão da automação interpretou incorretamente `- R$ 10,00`. A leitura foi corrigida para representar a dedução de R$ 10,00, mantendo o valor esperado do BDD. O diagnóstico inicial foi preservado e os testes foram executados novamente.

As conclusões apresentadas nos relatórios estão ligadas às respostas e telas realmente obtidas nas execuções. As falhas continuam registradas; os critérios não foram alterados para tornar a suíte aprovada. Pontos ambíguos da documentação foram indicados para esclarecimento com Produto.

## O que foi entregue

- [Cenários BDD](<Testes Manuais/features/README.md>) para catálogo, cupons, frete, pedidos, validação de itens e isolamento do carrinho.
- [Relatórios manuais](<Testes Manuais/reports/README.md>) com resultados e evidências das execuções anteriores.
- [Testes automatizados](<Testes Automatizados/tests/README.md>) de API e interface.
- [Relatórios automatizados](<Testes Automatizados/reports/README.md>) organizados em sucesso e falhas, com evidências e histórico das execuções.

```text
teste_qa_verzel/
├── README.md
├── Testes Manuais/
│   ├── features/
│   └── reports/
└── Testes Automatizados/
    ├── tests/
    │   ├── api/
    │   └── interface/
    ├── playwright.config.ts
    ├── package.json
    └── reports/
        ├── sucesso/
        ├── falhas/
        └── execucoes/
```

## Pasta de testes automatizados

A pasta [Testes Automatizados](<Testes Automatizados/README.md>) reúne o código dos testes em Playwright com TypeScript, as configurações para executá-los e os relatórios com evidências.

| Local | Conteúdo |
| --- | --- |
| `Testes Automatizados/tests/api/` | Testes de requisições e respostas da API, incluindo erros de rota, produto duplicado, formatos de CEP e validação de quantidade. |
| `Testes Automatizados/tests/interface/` | Testes das ações na tela, incluindo cupom, limites de frete e alteração de quantidade no carrinho. |
| `Testes Automatizados/reports/sucesso/` | Relatórios dos cenários aprovados e suas evidências. |
| `Testes Automatizados/reports/falhas/` | Relatórios dos cenários reprovados, diferenças encontradas e suas evidências. |
| `Testes Automatizados/reports/execucoes/` | Histórico das execuções, resultados completos, relatórios HTML e capturas de tela. |

O [guia de automação](<Testes Automatizados/tests/README.md>) explica como executar os testes. O [índice dos relatórios](<Testes Automatizados/reports/README.md>) permite consultar os resultados e as evidências.

## Como executar os testes

Requisito: **Node.js 20 ou superior**. Na pasta do repositório, execute:

```bash
cd "Testes Automatizados"
npm ci
npx playwright install chromium
npm test
npm run report
```

`npm test` executa todos os testes configurados. Para rodar somente os seis cenários do reteste, use `npm run test:reteste`. Para um exemplo exclusivamente de API, use `npm run test:quantidade-zero`; esse teste não precisa abrir navegador.

O Playwright executa os arquivos `.spec.ts`. Os arquivos `.feature` documentam os cenários e não são executados automaticamente por essa configuração. O [guia de automação](<Testes Automatizados/tests/README.md>) detalha os comandos e a configuração do ambiente.

## Resultado da última execução completa

Execução em **09/10/2026, das 18h36min57s às 18h37min25s**, no horário de Fortaleza, com Playwright 1.64.0 e Chromium 151.0.7922.173.

| Total de casos | Aprovados | Com falha | Pulados | Bloqueados |
| --- | --- | --- | --- | --- |
| 20 | 11 | 9 | 0 | 0 |

As reprovações envolveram cobrança de frete no subtotal exato de R$ 200,00, mensagem do cupom diferente da prevista, ausência de `erro.campo` e apresentação de “Grátis” em um cenário que exige duas casas decimais. A obrigatoriedade de `erro.campo` em erros de rota/método e o critério de apresentação do frete foram destacados como pontos de esclarecimento com Produto.

- [Relatório HTML](<Testes Automatizados/reports/execucoes/20261009-183657/html/index.html>).
- [Pacote completo do HTML e seus anexos](<Testes Automatizados/reports/execucoes/20261009-183657/relatorio-html.zip>).
- [Captura de tela do relatório](<Testes Automatizados/reports/execucoes/20261009-183657/print-relatorio-html-fortaleza.png>).
- [Resumo dos 20 casos](<Testes Automatizados/reports/execucoes/20261009-183657/resumo.json>).

Para abrir o HTML preservado desta execução, dentro de `Testes Automatizados`:

```bash
npm run report -- reports/execucoes/20261009-183657/html
```

O código de saída 1 da suíte corresponde às nove reprovações registradas. O resultado se aplica aos cenários automatizados e à execução indicada; não representa cobertura de todos os cenários BDD nem aprovação de toda a loja. Os pedidos e dados de cliente usados nos testes são fictícios no ambiente de QA.
