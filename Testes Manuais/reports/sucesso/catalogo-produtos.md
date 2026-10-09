# Relatório de teste — Catálogo de produtos

**Resultado: Aprovado.** Os oito produtos previstos na documentação foram encontrados, com os nomes e preços corretos. Nenhum problema foi identificado neste teste.

**Data do teste:** 07/10/2026, às 21h31 (horário de Fortaleza).

**Loja:** Verzel Store, ambiente de testes.

**Referência:** VZS-142, versão 2.3.0; cenário em [contrato_api.feature](../../features/contrato_api.feature).

## O que foi testado

Conferimos se o serviço que fornece o catálogo da loja entrega todos os produtos esperados, sem repetições, com nome, descrição, categoria e preço preenchidos.

## Cenário BDD

O cenário abaixo descreve o comportamento esperado que foi conferido neste teste. Ele também está em [contrato_api.feature](../../features/contrato_api.feature). Aqui, API significa o serviço que fornece os dados do catálogo; status 200 indica que a consulta foi atendida com sucesso, e JSON é o formato desses dados.

```gherkin
# language: pt
@VZS-142 @api @contrato
Funcionalidade: Catálogo e contrato HTTP da API

  Contexto:
    Dado que as requisições usam o cabeçalho "Content-Type" com valor "application/json"

  Cenário: Listar o catálogo fixo de produtos
    Quando envio uma requisição "GET /api/produtos"
    Então a API deve responder com status 200 e corpo JSON
    E cada produto deve conter id, nome, descricao, categoria e preco
    E os preços devem ser números em reais
    E o catálogo deve conter os produtos:
      | id   | nome                  | preco |
      | P001 | Camiseta Essencial    | 59.9  |
      | P002 | Calça Jeans Slim      | 139.9 |
      | P003 | Tênis Casual Urbano   | 189.9 |
      | P004 | Boné Aba Curva        | 49.9  |
      | P005 | Mochila Urbana 20L    | 100   |
      | P006 | Kit 3 Pares de Meias  | 29.9  |
      | P007 | Jaqueta Corta-Vento   | 229.9 |
      | P008 | Garrafa Térmica 750ml | 50    |
```

## Resultados da conferência

| Verificação | Esperado | Encontrado | Resultado |
| --- | --- | --- | --- |
| Consulta concluída | Consulta sem erros | Consulta sem erros | Aprovado |
| Status da consulta | 200 (sucesso) | 200 (sucesso) | Aprovado |
| Dados recebidos | Lista de produtos em JSON | Lista de produtos em JSON | Aprovado |
| Informações de cada produto | Identificador, nome, descrição, categoria e preço | Todas as informações presentes nos 8 produtos | Aprovado |
| Produtos no catálogo | 8 produtos, de P001 a P008 | 8 produtos, de P001 a P008 | Aprovado |
| Produtos repetidos | Nenhum | Nenhum | Aprovado |
| Formato dos preços | Valores numéricos em reais | Valores numéricos em reais | Aprovado |

### Produtos conferidos

| Produto | Preço esperado | Preço encontrado | Resultado |
| --- | --- | --- | --- |
| Camiseta Essencial | R$ 59,90 | R$ 59,90 | Aprovado |
| Calça Jeans Slim | R$ 139,90 | R$ 139,90 | Aprovado |
| Tênis Casual Urbano | R$ 189,90 | R$ 189,90 | Aprovado |
| Boné Aba Curva | R$ 49,90 | R$ 49,90 | Aprovado |
| Mochila Urbana 20L | R$ 100,00 | R$ 100,00 | Aprovado |
| Kit 3 Pares de Meias | R$ 29,90 | R$ 29,90 | Aprovado |
| Jaqueta Corta-Vento | R$ 229,90 | R$ 229,90 | Aprovado |
| Garrafa Térmica 750ml | R$ 50,00 | R$ 50,00 | Aprovado |

## Falhas encontradas

Nenhuma falha foi encontrada nas verificações deste cenário.

## Comprovantes do teste

Os registros abaixo guardam os dados recebidos e a conferência realizada. São arquivos técnicos disponíveis para consulta da equipe:

- [Registro completo da consulta](evidencias/catalogo-produtos/resposta-http.txt).
- [Dados dos produtos recebidos](evidencias/catalogo-produtos/corpo.json).
- [Conferência detalhada dos resultados](evidencias/catalogo-produtos/validacao.json).
- [Registro de erros da consulta](evidencias/catalogo-produtos/curl-stderr.txt): vazio nesta execução.

Para a equipe técnica, a consulta foi realizada com este comando, sem desativar a verificação de segurança da conexão:

```bash
curl -i -X GET \
  "https://verzel-store.qa-test-verzel-store.workers.dev/api/produtos" \
  -H "Content-Type: application/json" \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

O registro inclui um marcador final acrescentado pela ferramenta para indicar o status da consulta. Ele não faz parte dos dados dos produtos. Eventuais cabeçalhos do túnel de conexão não são usados para avaliar o resultado do serviço.

## Limite desta avaliação

A aprovação vale para os dados do catálogo consultados na data indicada. A aparência dos produtos na tela da loja não foi testada. Pedidos, cupons e frete também não fizeram parte desta avaliação.
