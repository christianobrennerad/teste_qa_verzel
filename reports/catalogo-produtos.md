# Relatório de teste — Catálogo de produtos

**Resultado: SUCESSO.** A execução independente confirmou o cenário “Listar o catálogo fixo de produtos”: HTTP 200, corpo JSON, campos obrigatórios presentes e os oito produtos com nomes e preços correspondentes à documentação.

- **Execução:** 2026-10-07T21:31:46-03:00 (America/Fortaleza, UTC−03:00).
- **Referência:** VZS-142, versão 2.3.0; `features/contrato_api.feature`.
- **Ambiente:** Verzel Store de QA, API pública acessada a partir do ambiente de desenvolvimento na nuvem.
- **Escopo:** somente `GET /api/produtos`. Não foram testados pedidos, cupons, frete ou interface nesta execução.

## Procedimento

Foi enviada uma requisição GET com o cabeçalho definido no contexto do cenário. A resposta integral foi salva e o JSON foi analisado para verificar status, estrutura, tipos e dados de cada produto. O curl preservou TLS e não seguiu redirecionamentos.

```bash
curl -i -X GET \
  "https://verzel-store.qa-test-verzel-store.workers.dev/api/produtos" \
  -H "Content-Type: application/json" \
  --max-time 30 --silent --show-error \
  --write-out '\nCURL_HTTP_STATUS:%{http_code}\n'
```

O marcador final `CURL_HTTP_STATUS` é metadado acrescentado pelo curl para registrar o status final; não faz parte do corpo da API. O arquivo HTTP pode incluir o cabeçalho de estabelecimento do túnel do proxy. A validação considera o status da resposta da aplicação.

## Verificações

| Verificação | Resultado | Evidência |
| --- | --- | --- |
| Execução da requisição | PASSOU | curl retornou código 0 |
| Status da aplicação | PASSOU | HTTP 200 |
| Tipo e formato da resposta | PASSOU | application/json; charset=utf-8; JSON analisado com sucesso |
| Campos de cada produto | PASSOU | id, nome, descricao, categoria e preco presentes nos 8 itens |
| Tipo dos preços | PASSOU | Todos os preços são números JSON, com os valores documentados em reais |
| Composição do catálogo | PASSOU | 8 produtos, IDs P001–P008 sem duplicidade |

| ID | Nome esperado | Preço esperado (R$) | Nome recebido | Preço recebido (R$) | Resultado |
| --- | --- | --- | --- | --- | --- |
| P001 | Camiseta Essencial | 59.9 | Camiseta Essencial | 59.9 | PASSOU |
| P002 | Calça Jeans Slim | 139.9 | Calça Jeans Slim | 139.9 | PASSOU |
| P003 | Tênis Casual Urbano | 189.9 | Tênis Casual Urbano | 189.9 | PASSOU |
| P004 | Boné Aba Curva | 49.9 | Boné Aba Curva | 49.9 | PASSOU |
| P005 | Mochila Urbana 20L | 100 | Mochila Urbana 20L | 100 | PASSOU |
| P006 | Kit 3 Pares de Meias | 29.9 | Kit 3 Pares de Meias | 29.9 | PASSOU |
| P007 | Jaqueta Corta-Vento | 229.9 | Jaqueta Corta-Vento | 229.9 | PASSOU |
| P008 | Garrafa Térmica 750ml | 50 | Garrafa Térmica 750ml | 50 | PASSOU |

Os preços `100` e `50` são números válidos e equivalem a R$ 100,00 e R$ 50,00. Zeros decimais finais não são exigidos no JSON. A ordem dos produtos não foi usada como critério de aprovação, pois o cenário exige sua presença, sem definir ordenação.

## Evidências

- [Resposta HTTP integral](evidencias/catalogo-produtos/resposta-http.txt): cabeçalhos e corpo originais da execução registrada.
- [Corpo JSON](evidencias/catalogo-produtos/corpo.json): corpo extraído da mesma resposta, sem nova consulta.
- [Validação detalhada](evidencias/catalogo-produtos/validacao.json): horário, comando, status e resultado de cada comparação.
- [Saída de erro do curl](evidencias/catalogo-produtos/curl-stderr.txt): vazia nesta execução.

## Conclusão

**Cenário aprovado nesta execução.** Nenhuma divergência foi encontrada nas verificações descritas. O resultado representa a resposta observada neste momento e não comprova disponibilidade futura nem aprovação das demais funcionalidades.
