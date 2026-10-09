# teste_qa_verzel

Automação e relatórios de QA da Verzel Store.

Os testes automatizados usam **Playwright com TypeScript**. Para começar com os
cenários de API e interface, veja o [guia de automação](tests/README.md).

```bash
npm ci
npx playwright install chromium
npm run test:reteste
npm run report
```

Execute os comandos nesta pasta, `Testes Automatizados`, com Node.js 20 ou
superior. O conjunto de reteste executa os seis cenários solicitados: frete nos
limites, alteração de quantidade, erros de rota e método, desconto com cupom,
produto duplicado e formatos de CEP.

Os [relatórios automatizados](reports/README.md) estão separados em sucesso e
falhas, com as evidências dentro de cada pasta. Os cenários BDD e relatórios
manuais continuam em [Testes Manuais](<../Testes Manuais/features/README.md>).

Os testes exclusivamente de API, como `npm run test:quantidade-zero`, não
precisam de navegador. Na nuvem, também é possível usar o Chromium já instalado
indicando `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`, conforme o guia.
