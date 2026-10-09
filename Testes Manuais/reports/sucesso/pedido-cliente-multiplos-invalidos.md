# Relatório de teste — Informar múltiplos dados inválidos do cliente

**Resultado: Aprovado.** A loja recusou o pedido e informou, na mesma resposta, que nome e e-mail eram inválidos. Também indicou o CEP inválido e não retornou confirmação de pedido.

**Data do teste:** 08/10/2026, às 11h04min09s (America/Fortaleza). A chamada foi iniciada e concluída nesse segundo, conforme o registro de execução.

**Loja:** [Verzel Store — ambiente de testes](https://verzel-store.qa-test-verzel-store.workers.dev).

**Referência:** [Documentação VZS-142, versão 2.3.0](https://verzel-store.qa-test-verzel-store.workers.dev/documentacao); cenário relacionado em [pedidos.feature](../../features/pedidos.feature).

## O que foi testado

Tentamos confirmar um pedido com uma Mochila Urbana 20L (P005), de R$ 100,00, sem cupom. Enviamos exatamente os dados do cenário: nome `Maria`, e-mail `invalido` e CEP `123`.

O teste foi feito diretamente no serviço da loja (API). Conferimos se a loja recusava o pedido e identificava nome e e-mail inválidos juntos, sem interromper a validação após encontrar o primeiro problema.

O BDD abaixo preserva a solicitação atual, que exige identificar nome e e-mail. A versão existente no arquivo `.feature` também inclui o CEP. Por isso, registramos a indicação do CEP e a ausência de confirmação como conferências adicionais.

## Cenário BDD

```gherkin
@api
Cenário: Informar múltiplos dados inválidos do cliente
  Quando confirmo um pedido de uma unidade do produto "P005" com os dados:
    | nome  | email    | cep |
    | Maria | invalido | 123 |
  Então a API deve responder com status 422
  E o campo "erro.codigo" deve ser "DADOS_INVALIDOS"
  E os detalhes em "campos" devem identificar nome, email
```

## Resultados da conferência

### Conferência do cenário solicitado

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Pedido recusado | Status 422 | Status 422 | Aprovado |
| Dados recebidos | Objeto JSON válido | Objeto JSON válido | Aprovado |
| Motivo da recusa (`erro.codigo`) | DADOS_INVALIDOS | DADOS_INVALIDOS | Aprovado |
| Identificação do nome inválido | Nome indicado nos detalhes de campos | `cliente.nome`: “Informe nome e sobrenome.” | Aprovado |
| Identificação do e-mail inválido | E-mail indicado nos detalhes da mesma resposta | `cliente.email`: “Informe um e-mail válido.” | Aprovado |

O status 422 indica que a loja recusou o pedido por causa dos dados enviados. JSON é o formato usado para enviar e receber esses dados. Os detalhes vieram em `erro.campos`, uma lista que reúne o campo e a mensagem de correção para cada problema.

### Conferências adicionais

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Identificação do CEP inválido | CEP indicado nos detalhes | `cliente.cep`: “Informe um CEP com 8 dígitos.” | Aprovado |
| Ausência de confirmação | Resposta de recusa, sem número ou data de confirmação | Erro DADOS_INVALIDOS, sem `numero` ou `criadoEm` | Aprovado |

As cinco verificações do cenário e as duas conferências adicionais passaram. A mesma resposta informou os três campos inválidos. As mensagens acima foram observadas na execução; o cenário exige a identificação dos campos, sem definir o texto dessas mensagens.

## Falhas encontradas

Nenhuma falha foi encontrada nesta execução. A loja apresentou nome e e-mail inválidos juntos e também identificou o CEP inválido. Não houve bloqueios nem passos sem execução.

## Comprovantes do teste

- [Corpo enviado, com os três dados inválidos](evidencias/pedido-cliente-multiplos-invalidos/20261008-110409/corpo-enviado.json).
- [Resposta HTTP completa, com status e cabeçalhos](evidencias/pedido-cliente-multiplos-invalidos/20261008-110409/resposta-http.txt) e [JSON recebido](evidencias/pedido-cliente-multiplos-invalidos/20261008-110409/corpo-recebido.json).
- [Comparação de cada campo, horários e resultado](evidencias/pedido-cliente-multiplos-invalidos/20261008-110409/validacao-api.json).
- [Critérios esperados e distinção das conferências adicionais](evidencias/pedido-cliente-multiplos-invalidos/20261008-110409/criterios.json).
- [Comando executado](evidencias/pedido-cliente-multiplos-invalidos/20261008-110409/comando.txt) e [script do teste](evidencias/pedido-cliente-multiplos-invalidos/20261008-110409/teste-api.py).
- [Registro de erros do curl](evidencias/pedido-cliente-multiplos-invalidos/20261008-110409/curl-stderr.txt): vazio. A ferramenta terminou sem erro de comunicação.

Para reproduzir a requisição executada:

```bash
curl -i -X POST \
  'https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos' \
  -H 'Content-Type: application/json' \
  --data-binary '{"cliente":{"nome":"Maria","email":"invalido","cep":"123"},"itens":[{"produtoId":"P005","quantidade":1}]}' \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

A resposta recebida foi:

```json
{
  "erro": {
    "codigo": "DADOS_INVALIDOS",
    "mensagem": "Existem campos inválidos no pedido.",
    "campos": [
      {"campo": "cliente.nome", "mensagem": "Informe nome e sobrenome."},
      {"campo": "cliente.email", "mensagem": "Informe um e-mail válido."},
      {"campo": "cliente.cep", "mensagem": "Informe um CEP com 8 dígitos."}
    ]
  }
}
```

O marcador `CURL_HTTP_STATUS` foi acrescentado pela ferramenta e não faz parte da resposta da loja. A avaliação considerou o status final da aplicação e manteve a verificação de segurança da conexão ativa.

## Limite desta avaliação

A aprovação se aplica a esta chamada, com uma unidade de P005 e os três dados informados. Outras combinações de dados inválidos, campos ausentes e a apresentação na interface não foram avaliadas nesta execução.

A ausência de confirmação foi verificada pelo status 422, pelo erro DADOS_INVALIDOS e pela ausência de número e data de confirmação na resposta. Não houve consulta ao armazenamento interno. Conforme a documentação, este ambiente não armazena pedidos nem permite consultar pedidos confirmados.
