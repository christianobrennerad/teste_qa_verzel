# Relatório de teste — Consulta do produto P001

**Resultado: Aprovado.** A consulta funcionou e todos os dados do produto corresponderam ao cenário esperado.

**Data do teste:** 07/10/2026, às 21h45 (horário de Fortaleza).

**Loja:** Verzel Store, ambiente de testes.

**Referência:** VZS-142, versão 2.3.0; cenário em [contrato_api.feature](../features/contrato_api.feature).

## O que foi testado

Consultamos o produto P001, Camiseta Essencial, para conferir seu identificador, nome, descrição, categoria e preço. Foi feita uma consulta direta ao serviço que fornece esses dados.

## Cenário BDD

O cenário abaixo descreve o comportamento esperado. API significa o serviço que fornece os dados; status 200 indica uma consulta bem-sucedida e JSON é o formato da resposta.

```gherkin
Cenário: Consultar produto existente pelo identificador
  Quando envio uma requisição "GET /api/produtos/P001"
  Então a API deve responder com status 200 e corpo JSON
  E o campo "id" deve ser "P001"
  E o campo "nome" deve ser "Camiseta Essencial"
  E o campo "descricao" deve ser "Algodão penteado e corte reto."
  E o campo "categoria" deve ser "Vestuário"
  E o campo "preco" deve ser 59.9
```

## Resultados da conferência

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Consulta concluída | 0 | 0 | Aprovado |
| Status da consulta | 200 | 200 | Aprovado |
| Resposta em JSON com dados de um produto | Objeto JSON | Objeto JSON | Aprovado |
| Formato informado pelo serviço | application/json | application/json | Aprovado |
| Identificador | P001 | P001 | Aprovado |
| Nome | Camiseta Essencial | Camiseta Essencial | Aprovado |
| Descrição | Algodão penteado e corte reto. | Algodão penteado e corte reto. | Aprovado |
| Categoria | Vestuário | Vestuário | Aprovado |
| Preço | R$ 59,90 | R$ 59,90 | Aprovado |

## Falhas encontradas

Nenhuma falha foi encontrada nas verificações deste cenário.

## Comprovantes do teste

- [Registro completo da consulta](evidencias/produto-p001/resposta-http.txt).
- [Dados recebidos do produto](evidencias/produto-p001/corpo.json).
- [Conferência detalhada dos resultados](evidencias/produto-p001/validacao.json).
- [Registro de erros da consulta](evidencias/produto-p001/curl-stderr.txt): vazio nesta execução.

Para a equipe técnica, a consulta foi realizada com este comando, sem desativar a verificação de segurança da conexão:

```bash
curl -i -X GET \
  "https://verzel-store.qa-test-verzel-store.workers.dev/api/produtos/P001" \
  -H "Content-Type: application/json" \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

O registro inclui um marcador final acrescentado pela ferramenta para indicar o status da consulta. Ele não faz parte dos dados do produto. Eventuais cabeçalhos do túnel de conexão não são usados para avaliar o resultado do serviço.

## Limite desta avaliação

O resultado corresponde à consulta feita na data indicada. A aparência do produto na tela, outros produtos, pedidos, cupons e frete não foram avaliados neste teste. O preço numérico `59.9` recebido equivale a R$ 59,90.
