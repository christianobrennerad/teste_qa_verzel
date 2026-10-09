# Relatório de teste — Ignorar espaços externos do cupom

**Resultado: Aprovado.** O cupom foi aceito mesmo com dois espaços no início e dois no fim. A API e a tela reconheceram BEMVINDO10, com desconto de R$ 10,00 e total de R$ 109,90. Nenhuma falha foi encontrada nas verificações deste cenário.

**Data do teste:** 07/10/2026, às 23h58 (horário de Fortaleza). Os horários de cada consulta e interação estão nas evidências.

**Loja:** Verzel Store, ambiente de testes.

**Referência:** VZS-142, versão 2.3.0, critério CA02; cenário em [cupons.feature](../../features/cupons.feature).

## O que foi testado

Conferimos se o cliente consegue aplicar o cupom quando copia ou digita espaços extras antes e depois do código.

Abrimos um carrinho novo com uma unidade da Mochila Urbana 20L (P005), de R$ 100,00. Digitamos dois espaços, `bemvindo10` e mais dois espaços, e aplicamos o cupom pelo formulário. Conferimos o código reconhecido, o desconto e o total na tela. Também enviamos esse mesmo conteúdo diretamente ao serviço de cálculo.

O conteúdo testado possui **14 caracteres**, incluindo os quatro espaços. As aspas do BDD apenas delimitam o texto: não foram enviadas como parte do cupom. Nenhum espaço foi removido pelo script antes de preencher o formulário ou enviar a consulta direta.

## Cenário BDD

O cenário abaixo descreve o comportamento esperado. O contexto prepara o carrinho; o bloco de texto preserva os espaços reais entre as aspas.

```gherkin
Contexto:
    Dado que o carrinho contém 1 unidade do produto "P005" de R$ 100,00

@CA02
  Cenário: Ignorar espaços reais no início e no fim do cupom
    Quando aplico o código de cupom contido entre as aspas do texto:
      """
      "  bemvindo10  "
      """
    Então o cupom "BEMVINDO10" deve estar aplicado
    E o desconto deve ser R$ 10,00
    E o total deve ser R$ 109,90
```

## Resultados da conferência

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Conteúdo digitado no formulário | 2 espaços + bemvindo10 + 2 espaços | Conteúdo completo, com 14 caracteres | Aprovado |
| Conteúdo enviado pelo formulário | Cupom com os quatro espaços preservados | Cupom com os quatro espaços preservados | Aprovado |
| Consulta direta ao serviço | Cupom enviado com espaços e aceito | Resposta 200, cupom aplicado | Aprovado |
| Cupom reconhecido | BEMVINDO10 | BEMVINDO10 | Aprovado |
| Cupom aplicado na tela | BEMVINDO10 aplicado | BEMVINDO10 aplicado, com opção de remover | Aprovado |
| Subtotal | R$ 100,00 | R$ 100,00 | Aprovado |
| Desconto | R$ 10,00 | R$ 10,00, apresentado como abatimento | Aprovado |
| Frete | R$ 19,90 | R$ 19,90 | Aprovado |
| Total | R$ 109,90 | R$ 109,90 | Aprovado |

A conta conferida foi **R$ 100,00 − R$ 10,00 + R$ 19,90 = R$ 109,90**. Os valores recebidos do serviço e exibidos na tela foram iguais.

API significa o serviço que calcula o carrinho. Status 200 indica que a consulta foi atendida com sucesso; JSON é o formato dos dados recebidos. O serviço devolveu o código sem os espaços e em maiúsculas.

## Falhas encontradas

Nenhuma falha foi encontrada na aplicação do cupom, no tratamento dos espaços ou nos valores deste cenário. Não houve bloqueio de execução.

## Comprovantes do teste

### Interface

- [Tela com o cupom digitado](evidencias/cupom-espacos-externos/20261007-235839/espacos-externos/interface/antes-de-aplicar.png).
- [Tela após aplicação](evidencias/cupom-espacos-externos/20261007-235839/espacos-externos/interface/depois-de-aplicar.png).
- [Conteúdo exato do campo de cupom](evidencias/cupom-espacos-externos/20261007-235839/espacos-externos/interface/cupom-digitado.txt): preserva os dois espaços de cada lado.
- [Texto da tela antes](evidencias/cupom-espacos-externos/20261007-235839/espacos-externos/interface/texto-antes.txt) e [depois](evidencias/cupom-espacos-externos/20261007-235839/espacos-externos/interface/texto-depois.txt).
- [Dados enviados pela interface](evidencias/cupom-espacos-externos/20261007-235839/espacos-externos/interface/corpo-enviado.json), [resposta recebida](evidencias/cupom-espacos-externos/20261007-235839/espacos-externos/interface/corpo-recebido.json) e [status e cabeçalhos](evidencias/cupom-espacos-externos/20261007-235839/espacos-externos/interface/resposta-http.json).
- [Conferência detalhada da interface](evidencias/cupom-espacos-externos/20261007-235839/espacos-externos/interface/validacao-interface.json): inclui o comprimento e os caracteres do campo para comprovar os espaços.

### Consulta independente ao serviço

- [Corpo enviado](evidencias/cupom-espacos-externos/20261007-235839/espacos-externos/api/corpo-enviado.json): cupom com espaços preservados.
- [Registro completo da consulta](evidencias/cupom-espacos-externos/20261007-235839/espacos-externos/api/resposta-http.txt).
- [Dados recebidos](evidencias/cupom-espacos-externos/20261007-235839/espacos-externos/api/corpo.json).
- [Conferência detalhada da API](evidencias/cupom-espacos-externos/20261007-235839/espacos-externos/api/validacao-api.json).
- [Registro de erros da consulta](evidencias/cupom-espacos-externos/20261007-235839/espacos-externos/api/curl-stderr.txt): vazio nesta execução.

### Registros gerais

- [Resumo dos resultados](evidencias/cupom-espacos-externos/20261007-235839/resumo-validacao.json).
- [Script da conferência da interface](evidencias/cupom-espacos-externos/20261007-235839/teste-interface.js).
- [Saída da execução do navegador](evidencias/cupom-espacos-externos/20261007-235839/navegador-stdout.txt) e [registro de erros](evidencias/cupom-espacos-externos/20261007-235839/navegador-stderr.txt): arquivo de erros vazio nesta execução.

### Tela conferida

![Carrinho com BEMVINDO10 aplicado após envio do código com espaços; desconto de R$ 10,00 e total de R$ 109,90](evidencias/cupom-espacos-externos/20261007-235839/espacos-externos/interface/depois-de-aplicar.png)

Os espaços no fim do texto não ficam claros em uma imagem. Sua presença foi comprovada pelo conteúdo do campo e pelas requisições salvas, além da captura de tela.

Para a equipe técnica, esta foi a consulta direta executada, com os espaços preservados e a verificação de segurança da conexão ativa:

```bash
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P005","quantidade":1}],"cupom":"  bemvindo10  "}' --max-time 30 --silent --show-error --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

O marcador `CURL_HTTP_STATUS` é acrescentado pela ferramenta e não faz parte da resposta. A conferência utiliza o status final da aplicação. O navegador manteve a verificação de certificados ativa, com a confiança no certificado oficial do proxy já autorizada pelo usuário.

## Limite desta avaliação

Foi testado o código com dois espaços comuns no início e dois no fim, em letras minúsculas, para uma unidade de P005. Não foram avaliados espaços no meio do código, tabulações, quebras de linha, outros cupons, outros produtos ou confirmação de pedidos. A aprovação se aplica ao comportamento e à execução descritos acima.
