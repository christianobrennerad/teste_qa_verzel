# Relatórios dos testes automatizados

## Última execução — suíte completa

Em **09/10/2026, das 18h36min57s às 18h37min25s (America/Fortaleza)**, executamos todos os 20 testes configurados: **11 aprovados e 9 com falhas**, sem casos pulados ou bloqueados. O comando foi `npm test`, com Playwright 1.64.0 e Chromium 151.0.7922.173, mantendo a validação de certificados ativa.

- [Relatório HTML desta execução](execucoes/20261009-183657/html/index.html).
- [Captura de tela do relatório HTML](execucoes/20261009-183657/print-relatorio-html-fortaleza.png).
- [Pacote completo do HTML e seus anexos](execucoes/20261009-183657/relatorio-html.zip).
- [Resumo dos 20 casos](execucoes/20261009-183657/resumo.json).
- [Resultado original do Playwright](execucoes/20261009-183657/resultados.json).
- [Índice e integridade dos 169 anexos](execucoes/20261009-183657/indice-evidencias.json).
- [Versões, horários e comando executado](execucoes/20261009-183657/execucao.json).

Para abrir o relatório com todas as evidências, execute dentro de `Testes Automatizados`:

```bash
npm run report -- reports/execucoes/20261009-183657/html
```

As reprovações continuam concentradas nos erros de rota/método, na mensagem do cupom e nos cenários de frete. A ausência de `erro.campo` e a apresentação de “Grátis” seguem os critérios dos relatórios de referência e os pontos de esclarecimento descritos abaixo. O código 1 do runner indica as nove reprovações; a execução foi concluída.

## Reteste anterior — seis relatórios

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
