# Relatório de teste — Cupom com maiúsculas e minúsculas

**Resultado: Aprovado nos dois exemplos executados.** Tanto `bemvindo10` quanto `BeMvInDo10` foram aceitos como BEMVINDO10, com desconto de R$ 10,00 e total de R$ 109,90. Nenhuma falha foi encontrada nessas verificações.

**Data do teste:** 07/10/2026, às 23h53 (horário de Fortaleza). Os horários de cada consulta e interação estão nas evidências.

**Loja:** Verzel Store, ambiente de testes.

**Referência:** VZS-142, versão 2.3.0, critério CA02; cenário em [cupons.feature](../../features/cupons.feature).

## O que foi testado

Conferimos se o cliente consegue usar o cupom sem se preocupar com letras maiúsculas ou minúsculas.

Para cada exemplo, abrimos um contexto novo de navegador, adicionamos uma unidade da Mochila Urbana 20L (P005), de R$ 100,00, e digitamos o código exatamente como informado. Aplicamos o cupom pelo formulário e verificamos a tela e o cálculo recebido. Também consultamos o serviço de cálculo diretamente com cada uma das duas grafias.

## Cenário BDD

O cenário abaixo descreve o comportamento esperado. O contexto prepara o carrinho para cada exemplo, de forma independente.

```gherkin
Contexto:
    Dado que o carrinho contém 1 unidade do produto "P005" de R$ 100,00

@CA02
  Esquema do Cenário: Normalizar maiúsculas, minúsculas e espaços externos
    Quando aplico o cupom "<cupom>"
    Então o cupom "BEMVINDO10" deve estar aplicado
    E o desconto deve ser R$ 10,00
    E o total deve ser R$ 109,90

    Exemplos:
      | cupom          |
      | bemvindo10     |
      | BeMvInDo10     |
```

Apesar de o título citar espaços externos, os dois exemplos fornecidos contêm apenas variações de maiúsculas e minúsculas. Nenhum cupom com espaços foi enviado nesta execução. Espaços usados para alinhar células de uma tabela BDD não fazem parte do código do cupom.

## Resultados da conferência

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| `bemvindo10` — Cupom reconhecido | BEMVINDO10 | BEMVINDO10 | Aprovado |
| `bemvindo10` — Cupom aplicado na tela | Cupom BEMVINDO10 aplicado. | Cupom BEMVINDO10 aplicado. | Aprovado |
| `bemvindo10` — Desconto | R$ 10,00 | R$ 10,00 (abatimento) | Aprovado |
| `bemvindo10` — Total | R$ 109,90 | R$ 109,90 | Aprovado |
| `BeMvInDo10` — Cupom reconhecido | BEMVINDO10 | BEMVINDO10 | Aprovado |
| `BeMvInDo10` — Cupom aplicado na tela | Cupom BEMVINDO10 aplicado. | Cupom BEMVINDO10 aplicado. | Aprovado |
| `BeMvInDo10` — Desconto | R$ 10,00 | R$ 10,00 (abatimento) | Aprovado |
| `BeMvInDo10` — Total | R$ 109,90 | R$ 109,90 | Aprovado |

Nos dois carrinhos, o subtotal permaneceu R$ 100,00 e o frete R$ 19,90. A conta foi **R$ 100,00 − R$ 10,00 + R$ 19,90 = R$ 109,90**. Na tela, o desconto aparece como um abatimento, com sinal negativo.

As duas consultas independentes ao serviço de cálculo também passaram: responderam com status 200, cupom BEMVINDO10 aplicado e os mesmos valores. API significa esse serviço; status 200 indica uma solicitação atendida com sucesso, e JSON é o formato dos dados recebidos.

## Falhas encontradas

Nenhuma falha foi encontrada nos dois exemplos de maiúsculas e minúsculas. Não houve bloqueio de execução.

**Cobertura pendente:** ignorar espaços no início e no fim do cupom não foi avaliado nos exemplos solicitados. Portanto, este resultado não comprova todo o critério CA02; a parte de espaços possui um cenário separado no projeto.

## Comprovantes do teste

### Cupom `bemvindo10`

- [Tela com o cupom digitado](evidencias/cupom-normalizacao/20261007-235309/minusculas/interface/antes-de-aplicar.png) e [tela após aplicação](evidencias/cupom-normalizacao/20261007-235309/minusculas/interface/depois-de-aplicar.png).
- [Código digitado no formulário](evidencias/cupom-normalizacao/20261007-235309/minusculas/interface/cupom-digitado.txt).
- [Texto da tela antes](evidencias/cupom-normalizacao/20261007-235309/minusculas/interface/texto-antes.txt) e [depois](evidencias/cupom-normalizacao/20261007-235309/minusculas/interface/texto-depois.txt).
- [Dados enviados pela interface](evidencias/cupom-normalizacao/20261007-235309/minusculas/interface/corpo-enviado.json), [resposta recebida](evidencias/cupom-normalizacao/20261007-235309/minusculas/interface/corpo-recebido.json) e [status e cabeçalhos](evidencias/cupom-normalizacao/20261007-235309/minusculas/interface/resposta-http.json).
- [Conferência da interface](evidencias/cupom-normalizacao/20261007-235309/minusculas/interface/validacao-interface.json).
- [Consulta independente à API](evidencias/cupom-normalizacao/20261007-235309/minusculas/api/resposta-http.txt), [corpo enviado](evidencias/cupom-normalizacao/20261007-235309/minusculas/api/corpo-enviado.json) e [dados recebidos](evidencias/cupom-normalizacao/20261007-235309/minusculas/api/corpo.json).
- [Conferência da API](evidencias/cupom-normalizacao/20261007-235309/minusculas/api/validacao-api.json) e [erros da ferramenta](evidencias/cupom-normalizacao/20261007-235309/minusculas/api/curl-stderr.txt): arquivo de erros vazio nesta execução.

### Cupom `BeMvInDo10`

- [Tela com o cupom digitado](evidencias/cupom-normalizacao/20261007-235309/maiusculas-e-minusculas/interface/antes-de-aplicar.png) e [tela após aplicação](evidencias/cupom-normalizacao/20261007-235309/maiusculas-e-minusculas/interface/depois-de-aplicar.png).
- [Código digitado no formulário](evidencias/cupom-normalizacao/20261007-235309/maiusculas-e-minusculas/interface/cupom-digitado.txt).
- [Texto da tela antes](evidencias/cupom-normalizacao/20261007-235309/maiusculas-e-minusculas/interface/texto-antes.txt) e [depois](evidencias/cupom-normalizacao/20261007-235309/maiusculas-e-minusculas/interface/texto-depois.txt).
- [Dados enviados pela interface](evidencias/cupom-normalizacao/20261007-235309/maiusculas-e-minusculas/interface/corpo-enviado.json), [resposta recebida](evidencias/cupom-normalizacao/20261007-235309/maiusculas-e-minusculas/interface/corpo-recebido.json) e [status e cabeçalhos](evidencias/cupom-normalizacao/20261007-235309/maiusculas-e-minusculas/interface/resposta-http.json).
- [Conferência da interface](evidencias/cupom-normalizacao/20261007-235309/maiusculas-e-minusculas/interface/validacao-interface.json).
- [Consulta independente à API](evidencias/cupom-normalizacao/20261007-235309/maiusculas-e-minusculas/api/resposta-http.txt), [corpo enviado](evidencias/cupom-normalizacao/20261007-235309/maiusculas-e-minusculas/api/corpo-enviado.json) e [dados recebidos](evidencias/cupom-normalizacao/20261007-235309/maiusculas-e-minusculas/api/corpo.json).
- [Conferência da API](evidencias/cupom-normalizacao/20261007-235309/maiusculas-e-minusculas/api/validacao-api.json) e [erros da ferramenta](evidencias/cupom-normalizacao/20261007-235309/maiusculas-e-minusculas/api/curl-stderr.txt): arquivo de erros vazio nesta execução.

### Registros gerais

- [Resumo dos resultados da API e da interface](evidencias/cupom-normalizacao/20261007-235309/resumo-validacao.json).
- [Script de conferência da interface](evidencias/cupom-normalizacao/20261007-235309/teste-interface.js).
- [Saída da execução do navegador](evidencias/cupom-normalizacao/20261007-235309/navegador-stdout.txt) e [registro de erros](evidencias/cupom-normalizacao/20261007-235309/navegador-stderr.txt): arquivo de erros vazio nesta execução.

### Telas após aplicação

![Carrinho após aplicação de bemvindo10, reconhecido como BEMVINDO10, com desconto de R$ 10,00 e total de R$ 109,90](evidencias/cupom-normalizacao/20261007-235309/minusculas/interface/depois-de-aplicar.png)

![Carrinho após aplicação de BeMvInDo10, reconhecido como BEMVINDO10, com desconto de R$ 10,00 e total de R$ 109,90](evidencias/cupom-normalizacao/20261007-235309/maiusculas-e-minusculas/interface/depois-de-aplicar.png)

Para a equipe técnica, estas foram as consultas independentes executadas com a verificação de segurança da conexão ativa:

```bash
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P005","quantidade":1}],"cupom":"bemvindo10"}' --max-time 30 --silent --show-error --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'

curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P005","quantidade":1}],"cupom":"BeMvInDo10"}' --max-time 30 --silent --show-error --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

Os códigos foram enviados sem alterar suas letras. O marcador `CURL_HTTP_STATUS` é acrescentado pela ferramenta e não faz parte da resposta do serviço. Os registros do navegador preservam o corpo enviado e a resposta recebida durante cada aplicação do cupom. A verificação de certificados permaneceu ativa, usando a confiança no certificado oficial do proxy já autorizada pelo usuário.

## Limite desta avaliação

Foram testados os dois exemplos fornecidos, na API e na interface, com uma unidade de P005. Espaços externos, outros cupons, outros produtos, troca ou remoção do cupom e confirmação de pedidos não foram avaliados. O resultado vale para a execução indicada e para as verificações deste cenário.
