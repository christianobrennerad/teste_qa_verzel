# Relatório de teste — Recalcular frete após alterar a quantidade com cupom aplicado

**Resultado: Falhou.** Ao aumentar P005 de uma para duas unidades com BEMVINDO10, a loja cobrou R$ 19,90 de frete e mostrou total de R$ 199,90; o esperado era frete grátis e R$ 180,00. Ao voltar para uma unidade, os valores e o aviso de frete ficaram corretos.

**Data do teste:** 09/10/2026, das 16h58min40s às 16h58min43s (America/Fortaleza).

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Execução:** Playwright 1.64.0; Chromium 151.0.7922.173 e chamadas reais de API. Certificados verificados.

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao); [BDD](<../../../Testes Manuais/features/frete_e_totais.feature>); [relatório manual de referência](<../../../Testes Manuais/reports/falhas/frete-alteracao-quantidade.md>).

## O que foi testado

Ao aumentar P005 de uma para duas unidades com BEMVINDO10, a loja cobrou R$ 19,90 de frete e mostrou total de R$ 199,90; o esperado era frete grátis e R$ 180,00. Ao voltar para uma unidade, os valores e o aviso de frete ficaram corretos.

Executamos o cenário do relatório manual por meio de testes Playwright. API é o serviço que recebe as requisições da loja; JSON é o formato dos dados enviados e recebidos. Cada comparação foi registrada antes de concluir o resultado.

## Cenário BDD

```gherkin
@CA06 @CA07 @CA08 @interface
Cenário: Recalcular frete após alterar a quantidade com cupom aplicado
  Dado que o carrinho contém 1 unidade do produto "P005" de R$ 100,00
  E apliquei o cupom "BEMVINDO10"
  Quando altero a quantidade do produto "P005" para 2
  Então o subtotal deve ser R$ 200,00
  E o desconto deve ser R$ 20,00
  E o frete deve ser R$ 0,00
  E o total deve ser R$ 180,00
  Quando altero a quantidade do produto "P005" para 1
  Então o subtotal deve ser R$ 100,00
  E o desconto deve ser R$ 10,00
  E o frete deve ser R$ 19,90
  E o total deve ser R$ 109,90
  E o carrinho deve informar que faltam R$ 100,00 para o frete grátis
```

## Resultados da conferência

Foram concluídos 1 caso(s), com 27 verificações aprovadas e 4 com falha. Nenhum caso foi pulado ou ficou bloqueado.

### Frete após alterar quantidade com cupom: 1 para 2 e volta para 1

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| API 1-quantidade-1 — subtotal | R$ 100,00 | R$ 100,00 | Aprovado |
| API 1-quantidade-1 — desconto | R$ 10,00 | R$ 10,00 | Aprovado |
| API 1-quantidade-1 — frete | R$ 19,90 | R$ 19,90 | Aprovado |
| API 1-quantidade-1 — total | R$ 109,90 | R$ 109,90 | Aprovado |
| Interface 1-quantidade-1 — Quantidade de P005 | 1 | 1 | Aprovado |
| Interface 1-quantidade-1 — Um único cupom BEMVINDO10 | Sim | Sim | Aprovado |
| Interface 1-quantidade-1 — subtotal | R$ 100,00 | R$ 100,00 | Aprovado |
| Interface 1-quantidade-1 — desconto | R$ 10,00 | R$ 10,00 | Aprovado |
| Interface 1-quantidade-1 — frete | R$ 19,90 | R$ 19,90 | Aprovado |
| Interface 1-quantidade-1 — total | R$ 109,90 | R$ 109,90 | Aprovado |
| API 2-quantidade-2 — subtotal | R$ 200,00 | R$ 200,00 | Aprovado |
| API 2-quantidade-2 — desconto | R$ 20,00 | R$ 20,00 | Aprovado |
| API 2-quantidade-2 — frete | R$ 0,00 | R$ 19,90 | Falhou |
| API 2-quantidade-2 — total | R$ 180,00 | R$ 199,90 | Falhou |
| Interface 2-quantidade-2 — Quantidade de P005 | 2 | 2 | Aprovado |
| Interface 2-quantidade-2 — Um único cupom BEMVINDO10 | Sim | Sim | Aprovado |
| Interface 2-quantidade-2 — subtotal | R$ 200,00 | R$ 200,00 | Aprovado |
| Interface 2-quantidade-2 — desconto | R$ 20,00 | R$ 20,00 | Aprovado |
| Interface 2-quantidade-2 — frete | R$ 0,00 | R$ 19,90 | Falhou |
| Interface 2-quantidade-2 — total | R$ 180,00 | R$ 199,90 | Falhou |
| API 3-quantidade-1 — subtotal | R$ 100,00 | R$ 100,00 | Aprovado |
| API 3-quantidade-1 — desconto | R$ 10,00 | R$ 10,00 | Aprovado |
| API 3-quantidade-1 — frete | R$ 19,90 | R$ 19,90 | Aprovado |
| API 3-quantidade-1 — total | R$ 109,90 | R$ 109,90 | Aprovado |
| Interface 3-quantidade-1 — Quantidade de P005 | 1 | 1 | Aprovado |
| Interface 3-quantidade-1 — Um único cupom BEMVINDO10 | Sim | Sim | Aprovado |
| Interface 3-quantidade-1 — subtotal | R$ 100,00 | R$ 100,00 | Aprovado |
| Interface 3-quantidade-1 — desconto | R$ 10,00 | R$ 10,00 | Aprovado |
| Interface 3-quantidade-1 — frete | R$ 19,90 | R$ 19,90 | Aprovado |
| Interface 3-quantidade-1 — total | R$ 109,90 | R$ 109,90 | Aprovado |
| Interface ao voltar para uma unidade — Aviso de frete | Faltam R$ 100,00 para o frete grátis. | Faltam R$ 100,00 para o frete grátis. | Aprovado |

## Falhas encontradas

- A alteração para duas unidades preservou o cupom e calculou desconto de R$ 20,00, mas manteve frete de R$ 19,90 e total de R$ 199,90. O comprador pagaria R$ 19,90 a mais que o previsto no cenário.
- O retorno para uma unidade passou: subtotal R$ 100,00, desconto R$ 10,00, frete R$ 19,90, total R$ 109,90 e aviso de R$ 100,00 faltantes.

## Comprovantes do teste

- [Resumo e horários](evidencias/frete-alteracao-quantidade/20261009-165827/resumo-validacao.json).
- [Teste TypeScript](../../tests/interface/frete-alteracao-quantidade.spec.ts).
- [Relatório HTML completo do Playwright](../execucoes/20261009-165827/html/index.html).
- [Saída da execução](../execucoes/20261009-165827/playwright-stdout.txt) e [mensagens da ferramenta](../execucoes/20261009-165827/playwright-stderr.txt).

### Evidências — Frete após alterar quantidade com cupom: 1 para 2 e volta para 1

- [Conferência de cada passo](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/validacao.json).
- [1-quantidade-1-api-requisicao.json](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/1-quantidade-1-api-requisicao.json).
- [1-quantidade-1-api-resposta-http.json](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/1-quantidade-1-api-resposta-http.json).
- [1-quantidade-1-api-corpo-recebido.json](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/1-quantidade-1-api-corpo-recebido.json).
- [1-quantidade-1-api-comando.txt](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/1-quantidade-1-api-comando.txt).
- [1-quantidade-1-estado-interface.json](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/1-quantidade-1-estado-interface.json).
- [1-quantidade-1-texto-tela.txt](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/1-quantidade-1-texto-tela.txt).
- [1-quantidade-1-tela.png](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/1-quantidade-1-tela.png).
- [2-quantidade-2-api-requisicao.json](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/2-quantidade-2-api-requisicao.json).
- [2-quantidade-2-api-resposta-http.json](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/2-quantidade-2-api-resposta-http.json).
- [2-quantidade-2-api-corpo-recebido.json](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/2-quantidade-2-api-corpo-recebido.json).
- [2-quantidade-2-api-comando.txt](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/2-quantidade-2-api-comando.txt).
- [2-quantidade-2-estado-interface.json](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/2-quantidade-2-estado-interface.json).
- [2-quantidade-2-texto-tela.txt](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/2-quantidade-2-texto-tela.txt).
- [2-quantidade-2-tela.png](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/2-quantidade-2-tela.png).
- [3-quantidade-1-api-requisicao.json](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/3-quantidade-1-api-requisicao.json).
- [3-quantidade-1-api-resposta-http.json](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/3-quantidade-1-api-resposta-http.json).
- [3-quantidade-1-api-corpo-recebido.json](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/3-quantidade-1-api-corpo-recebido.json).
- [3-quantidade-1-api-comando.txt](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/3-quantidade-1-api-comando.txt).
- [3-quantidade-1-estado-interface.json](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/3-quantidade-1-estado-interface.json).
- [3-quantidade-1-texto-tela.txt](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/3-quantidade-1-texto-tela.txt).
- [3-quantidade-1-tela.png](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/3-quantidade-1-tela.png).
- [error-context](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/error-context).

![Tela registrada durante o teste](evidencias/frete-alteracao-quantidade/20261009-165827/quantidade-1-2-1/1-quantidade-1-tela.png)

Para repetir somente este cenário, execute na pasta `Testes Automatizados`:

```bash
npx playwright test tests/interface/frete-alteracao-quantidade.spec.ts --project=interface-chromium
```

Os anexos de resposta preservam o status final da aplicação, os cabeçalhos e o corpo recebidos pelo Playwright. Os arquivos de comando mostram as requisições equivalentes em curl; a execução avaliada foi feita pelo Playwright.

O runner terminou com código 1 porque houve comparações reprovadas no conjunto completo, não por bloqueio de ambiente. A primeira execução foi preservada como diagnóstico de uma correção na leitura do desconto pela automação; a avaliação acima usa somente a execução final.

## Limite desta avaliação

O resultado vale para os exemplos deste BDD e para as respostas e telas da data indicada. Não comprova aprovação de toda a loja. Pedidos e dados de cliente são fictícios no ambiente de QA; não houve pagamento real. Os relatórios manuais e suas evidências não foram alterados.
