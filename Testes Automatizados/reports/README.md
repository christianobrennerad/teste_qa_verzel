# Relatórios dos testes automatizados

**Resultado:** 15 casos executados com Playwright: 6 aprovados e 9 com falha. Nenhum bloqueado ou pulado. As 204 comparações resultaram em 183 aprovações e 21 falhas.

**Execução:** 2026-10-09T16:58:27.772121-03:00 a 2026-10-09T16:58:53.235496-03:00 (America/Fortaleza).

| Relatório | Resultado geral | Casos aprovados | Casos que falharam |
| --- | --- | --- | --- |
| [Erros de rota, método e produto](falhas/erros-rota-metodo-produto.md) | Falhou | 0 | 5 |
| [Aceitar CEP com ou sem hífen](sucesso/pedido-cep-formatos.md) | Aprovado | 2 | 0 |
| [Rejeitar produto duplicado](sucesso/produto-duplicado-api.md) | Aprovado | 2 | 0 |
| [Aplicar desconto apenas aos produtos](falhas/cupom-desconto-produtos.md) | Falhou | 0 | 1 |
| [Recalcular frete após alterar a quantidade com cupom aplicado](falhas/frete-alteracao-quantidade.md) | Falhou | 0 | 1 |
| [Frete nos limites do subtotal](falhas/frete-limites-subtotal.md) | Falhou | 2 | 2 |

Os seis relatórios contêm o BDD integral e evidências próprias em `sucesso/evidencias/` ou `falhas/evidencias/`. O resultado segue o critério registrado no relatório manual de referência.

## Execução e evidências

- [Relatório HTML](execucoes/20261009-165827/html/index.html).
- [Resultado original do runner](execucoes/20261009-165827/resultados.json).
- [Versões, comando, horários e código de saída](execucoes/20261009-165827/execucao.json).
- [Índice de integridade dos anexos](execucoes/20261009-165827/indice-evidencias.json).
- [Diagnóstico da primeira execução](execucoes/20261009-165827/diagnostico-inicial/README.md).
- [Fontes usadas na execução final](execucoes/20261009-165827/fontes).

Para repetir o conjunto na pasta `Testes Automatizados`:

```bash
npm ci
npx playwright install chromium
npm run test:reteste
npm run report
```

Para abrir o HTML desta execução preservada:

```bash
npm run report -- reports/execucoes/20261009-165827/html
```

Na nuvem, foi usado o Chromium instalado em `/usr/bin/chromium`, indicado por `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`, e a confiança no certificado oficial do proxy. A verificação TLS permaneceu ativa. O código 1 do runner corresponde às nove reprovações, sem impedimento de execução.

## Critérios que precisam de esclarecimento

A ausência de erro.campo em erros de rota/método segue a interpretação do formato comum do relatório original. A documentação não esclarece quando esse campo pode ser omitido. A palavra “Grátis” falha somente contra a exigência literal de duas casas decimais do cenário de limites de frete. Essas dúvidas foram mantidas nos relatórios para Produto.

Os relatórios manuais foram preservados. Esta pasta registra a nova execução automatizada de 09/10/2026.
