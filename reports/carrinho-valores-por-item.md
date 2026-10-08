# Relatório de teste — Detalhar valores calculados por item

**Resultado: Aprovado.** A loja retornou os valores corretos para uma Calça Jeans Slim e dois Bonés Aba Curva. O cupom BEMVINDO10 veio aplicado, com o código e a mensagem esperados. Nenhuma falha foi encontrada.

**Data do teste:** 08/10/2026, às 01h19min15s (America/Fortaleza).

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao); cenário em [frete_e_totais.feature](../features/frete_e_totais.feature).

## O que foi testado

Enviamos ao serviço de cálculo da loja (API) o carrinho informado: uma unidade de P002, duas unidades de P004 e o cupom BEMVINDO10.

Conferimos os identificadores, nomes, preços unitários, quantidades e totais dos dois produtos. Também verificamos se o cupom estava aplicado e se a mensagem correspondia exatamente à solicitada. O teste foi feito diretamente no serviço, usando o formato de dados JSON apresentado no BDD.

## Cenário BDD

```gherkin
@api
Cenário: Detalhar valores calculados por item
  Quando envio para "POST /api/carrinho/calcular" o JSON:
    """
    {"itens":[{"produtoId":"P002","quantidade":1},{"produtoId":"P004","quantidade":2}],"cupom":"BEMVINDO10"}
    """
  Então a API deve responder com status 200
  E os itens da resposta devem ser:
    | produtoId | nome             | precoUnitario | quantidade | total |
    | P002      | Calça Jeans Slim | 139.9         | 1          | 139.9 |
    | P004      | Boné Aba Curva   | 49.9          | 2          | 99.8  |
  E o campo "cupom.codigo" deve ser "BEMVINDO10"
  E o campo "cupom.aplicado" deve ser verdadeiro
  E o campo "cupom.mensagem" deve ser "Cupom aplicado: 10% de desconto nos produtos."
```

## Resultados da conferência

### Resposta e cupom

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Atendimento da solicitação | Status 200, indicando sucesso | Status 200 da aplicação | Aprovado |
| Formato dos dados | Objeto JSON válido | Objeto JSON válido | Aprovado |
| Produtos retornados | Apenas P002 e P004, uma entrada para cada | Dois itens, sem duplicações nem produtos extras | Aprovado |
| Código do cupom | BEMVINDO10 | BEMVINDO10 | Aprovado |
| Cupom aplicado | Verdadeiro | Verdadeiro | Aprovado |
| Mensagem do cupom | “Cupom aplicado: 10% de desconto nos produtos.” | “Cupom aplicado: 10% de desconto nos produtos.” | Aprovado |

### Calça Jeans Slim — P002

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Identificador | P002 | P002 | Aprovado |
| Nome | Calça Jeans Slim | Calça Jeans Slim | Aprovado |
| Preço de uma unidade | R$ 139,90 | R$ 139,90 | Aprovado |
| Quantidade | 1 | 1 | Aprovado |
| Total do item | R$ 139,90 | R$ 139,90 | Aprovado |

### Boné Aba Curva — P004

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Identificador | P004 | P004 | Aprovado |
| Nome | Boné Aba Curva | Boné Aba Curva | Aprovado |
| Preço de uma unidade | R$ 49,90 | R$ 49,90 | Aprovado |
| Quantidade | 2 | 2 | Aprovado |
| Total do item | R$ 99,80 | R$ 99,80 | Aprovado |

Os totais por item corresponderam ao preço multiplicado pela quantidade: R$ 139,90 × 1 e R$ 49,90 × 2. Os preços e totais foram recebidos como números; as quantidades, como números inteiros; a indicação de cupom aplicado, como verdadeiro. A conferência monetária utilizou valores decimais exatos da resposta.

## Falhas encontradas

Nenhuma falha foi encontrada nesta execução. Todas as 18 verificações registradas nas evidências passaram. Não houve bloqueios nem verificações deixadas sem execução.

## Comprovantes do teste

- [Corpo enviado](evidencias/carrinho-valores-por-item/20261008-011915/corpo-enviado.json) e [valores esperados](evidencias/carrinho-valores-por-item/20261008-011915/esperado.json).
- [Resposta HTTP completa, com status e cabeçalhos](evidencias/carrinho-valores-por-item/20261008-011915/resposta-http.txt) e [dados recebidos](evidencias/carrinho-valores-por-item/20261008-011915/corpo-recebido.json).
- [Comparação de cada campo, resultado, horário e comando](evidencias/carrinho-valores-por-item/20261008-011915/validacao-api.json).
- [Comando executado](evidencias/carrinho-valores-por-item/20261008-011915/comando.txt) e [script do teste](evidencias/carrinho-valores-por-item/20261008-011915/teste-api.py).
- [Registro de erros do curl](evidencias/carrinho-valores-por-item/20261008-011915/curl-stderr.txt): vazio nesta execução. A ferramenta terminou sem erro.

Para a equipe técnica, esta foi a requisição executada:

```bash
curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular' \
  -H 'Content-Type: application/json' \
  --data-binary '{"itens":[{"produtoId":"P002","quantidade":1},{"produtoId":"P004","quantidade":2}],"cupom":"BEMVINDO10"}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

O marcador `CURL_HTTP_STATUS` é acrescentado pela ferramenta e não faz parte da resposta. A avaliação usou o status final da aplicação e manteve a verificação de segurança da conexão ativa.

## Limite desta avaliação

O resultado vale para a requisição informada, com esses dois produtos e BEMVINDO10. Não foram avaliadas a apresentação na interface, outras combinações de itens ou a confirmação de um pedido. Os demais campos do resumo foram preservados na resposta, mas não fazem parte da aprovação deste cenário.
