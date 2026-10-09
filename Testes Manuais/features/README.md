# Cenários BDD — Verzel Store

Fonte: documentação fornecida pelo usuário, card **VZS-142**, versão **2.3.0**, publicada em **30/09/2026**. Endereço informado: https://verzel-store.qa-test-verzel-store.workers.dev/documentacao.

Os arquivos usam Gherkin em português (`# language: pt`). São especificações de teste; o projeto ainda não possui runner, definições de passos ou automação de navegador/API. A validação sintática não comprova que a aplicação passa nos cenários.

## Organização e rastreabilidade

| Arquivo | Cobertura |
| --- | --- |
| `cupons.feature` | CA01–CA05, CA09: aplicação, normalização, mensagens, remoção e limite de um cupom |
| `frete_e_totais.feature` | CA01, CA06–CA09, CA11: fórmula, limites do frete, valores por item e atualização do carrinho |
| `quantidades_e_itens.feature` | CA10: limites da interface/API, validação de itens e duplicidade |
| `pedidos.feature` | Confirmação, normalização, consistência com cálculo, erros de cupom e dados do cliente |
| `contrato_api.feature` | Catálogo, consulta, JSON inválido, rotas, métodos e formato de erros |
| `isolamento.feature` | Carrinho por aba/contexto, chamadas independentes e ausência de estoque |

As tags `@api` e `@interface` identificam a camada. Cenários com ambas requerem verificar a resposta da API e sua exibição na interface. As tags `@CA01` a `@CA11` ligam cenários aos critérios de aceite.

## Convenções de execução

- Base da API: `https://verzel-store.qa-test-verzel-store.workers.dev`; requisições e respostas em JSON, com `Content-Type: application/json`.
- Cada cenário começa com estado independente. Prepare um carrinho vazio antes de adicionar os itens indicados, sem depender de outro cenário.
- `P002:1,P004:2` representa uma unidade de P002 e duas de P004. Use somente os preços fixos documentados.
- “Cliente válido” significa `{"nome":"Maria Silva","email":"maria@exemplo.com","cep":"01310-100"}`. Passos de itens compartilhados adicionam `cliente` somente ao confirmar pedidos; não inventam obrigatoriedade desse campo no cálculo.
- Valores com vírgula nos passos representam reais; campos numéricos JSON usam ponto. Compare números decimais, não a presença de zeros finais no JSON: `100` equivale a `100.00`. A interface apresenta duas casas decimais.
- Textos entre aspas nos docstrings de normalização preservam espaços internos às aspas; não aplicar `trim` no dado enviado. As tabelas Gherkin removem espaços externos das células.
- Erros devem conter o objeto `erro` com `codigo` e `mensagem`; valide `campo` nos erros de item e `campos` para dados do cliente, conforme a documentação. Não foram inventadas mensagens ou caminhos específicos não documentados.
- O formato `VZ-000000` significa prefixo `VZ-` seguido de seis dígitos, não um número fixo. Não exigir números únicos, consulta posterior ou persistência do pedido.

## Limites e pontos a esclarecer

Login, cadastro de clientes, pagamento online e consulta de pedidos estão fora do escopo. Nenhum e-mail ou cobrança é realizado; o número de pedido é fictício. Os cenários não pressupõem banco de dados, serviço de e-mail ou controle de estoque.

A documentação fornece apenas um cupom válido. A remoção seguida de reaplicação e a tentativa de outro cupom expirado cobrem o fluxo disponível; testar troca entre dois cupons válidos exige uma segunda massa oficial.

Os preços e o percentual válidos fornecidos geram descontos exatos em centavos. CA11 é coberto pela precisão numérica e apresentação; não há massa documentada para decidir arredondamento de meio centavo. Também não se presume comportamento de cupom vazio, frete de carrinho vazio na interface ou persistência ao recarregar a aba.
