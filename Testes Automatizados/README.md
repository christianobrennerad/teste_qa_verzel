# teste_qa_verzel

Cenários BDD, relatórios de QA e automação da Verzel Store.

Os testes automatizados usam **Playwright com TypeScript**. Para começar com os
cenários de API, veja o [guia de automação](tests/README.md).

```bash
npm ci
npm run test:quantidade-zero
npm run report
```

Use Node.js 20 ou superior. Os exemplos atuais são testes de API e não exigem
instalação de navegadores. Os arquivos BDD continuam em [features](features/README.md)
e os [relatórios de QA](reports/README.md) estão separados em sucesso e falhas,
com as evidências dentro de cada pasta.
