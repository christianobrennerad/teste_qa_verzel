# Relatório de teste — Identificar o campo da quantidade inválida

**Resultado: Aprovado.** A loja recusou a quantidade zero e identificou a quantidade do primeiro item como o campo que precisa de correção. O código e a mensagem retornados foram exatamente os esperados.

**Data do teste:** 08/10/2026, das 12h04min55s às 12h04min56s (America/Fortaleza).

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao), seção de códigos de erro; cenário em [quantidades_e_itens.feature](../../features/quantidades_e_itens.feature).

## O que foi testado

Enviamos ao serviço que calcula o carrinho (API) o produto P001, Camiseta Essencial, com quantidade zero. O corpo foi enviado exatamente como no cenário, sem cupom.

Conferimos a recusa com status 422 e comparamos o código, a mensagem completa e a indicação do campo com os valores esperados. O campo `itens[0].quantidade` significa a quantidade do primeiro item da lista.

## Cenário BDD

```gherkin
@api
Cenário: Identificar o campo da quantidade inválida
  Quando envio para "POST /api/carrinho/calcular" o JSON:
    """
    {"itens":[{"produtoId":"P001","quantidade":0}]}
    """
  Então a API deve responder com status 422
  E o campo "erro.codigo" deve ser "QUANTIDADE_INVALIDA"
  E o campo "erro.mensagem" deve ser "A quantidade deve ser um número inteiro maior ou igual a 1."
  E o campo "erro.campo" deve ser "itens[0].quantidade"
```

## Resultados da conferência

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Cálculo recusado | Status 422 | Status 422 | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido | Aprovado |
| Código do erro (`erro.codigo`) | QUANTIDADE_INVALIDA | QUANTIDADE_INVALIDA | Aprovado |
| Mensagem (`erro.mensagem`) | A quantidade deve ser um número inteiro maior ou igual a 1. | A quantidade deve ser um número inteiro maior ou igual a 1. | Aprovado |
| Campo identificado (`erro.campo`) | `itens[0].quantidade` | `itens[0].quantidade` | Aprovado |

As **cinco verificações passaram**. O status 422 indica que a loja recusou os dados enviados; JSON é o formato usado para enviar e receber esses dados. A mensagem orienta a informar uma quantidade inteira de pelo menos uma unidade.

## Falhas encontradas

Nenhuma falha foi encontrada nesta execução. A mensagem, incluindo a pontuação, e o campo identificado corresponderam exatamente ao cenário. Não houve bloqueios nem passos sem execução.

## Comprovantes do teste

- [Corpo enviado, com quantidade zero](evidencias/campo-quantidade-invalida/20261008-120455/corpo-enviado.json).
- [Resposta HTTP completa, com status e cabeçalhos](evidencias/campo-quantidade-invalida/20261008-120455/resposta-http.txt) e [JSON recebido](evidencias/campo-quantidade-invalida/20261008-120455/corpo-recebido.json).
- [Comparação dos cinco critérios, horários e resultado](evidencias/campo-quantidade-invalida/20261008-120455/validacao-api.json).
- [Valores esperados](evidencias/campo-quantidade-invalida/20261008-120455/criterios.json).
- [Comando executado](evidencias/campo-quantidade-invalida/20261008-120455/comando.txt) e [script do teste](evidencias/campo-quantidade-invalida/20261008-120455/teste-api.py).
- [Registro de erros do curl](evidencias/campo-quantidade-invalida/20261008-120455/curl-stderr.txt): vazio. A ferramenta terminou sem erro de comunicação.

Para reproduzir a requisição executada:

```bash
curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular' \
  -H 'Content-Type: application/json' \
  --data-binary '{"itens":[{"produtoId":"P001","quantidade":0}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

A resposta recebida foi:

```json
{
  "erro": {
    "codigo": "QUANTIDADE_INVALIDA",
    "mensagem": "A quantidade deve ser um número inteiro maior ou igual a 1.",
    "campo": "itens[0].quantidade"
  }
}
```

O marcador `CURL_HTTP_STATUS` foi acrescentado pela ferramenta e não faz parte da resposta da loja. A avaliação considerou o status final da aplicação e manteve a verificação de segurança da conexão ativa. Os três campos do erro foram comparados como texto exato.

## Limite desta avaliação

A aprovação se aplica a esta chamada de cálculo com P001 e quantidade zero no primeiro item. Não foram avaliados outros valores de quantidade, outros produtos, erros em posições diferentes da lista, confirmação de pedido ou a interface nesta execução.
