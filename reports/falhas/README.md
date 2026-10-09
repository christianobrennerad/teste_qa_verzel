# Testes que falharam

Os 9 relatórios abaixo têm resultado **Falhou**. Alguns também contêm exemplos aprovados, mantidos no mesmo relatório para preservar o contexto da execução.

Cada relatório contém o BDD, os resultados e os links dos comprovantes. As evidências ficam em `evidencias/<nome>/`, nesta pasta.

| Teste | Resultado registrado | Evidências |
| --- | --- | --- |
| [Calcular cada chamada sem reutilizar itens ou cupom anteriores](api-isolamento-chamadas.md) | Falhou no total da primeira chamada. | [Comprovantes](evidencias/api-isolamento-chamadas/) |
| [Aplicar desconto apenas aos produtos](cupom-desconto-produtos.md) | Falhou na mensagem exibida. | [Comprovantes](evidencias/cupom-desconto-produtos/) |
| [Erros de rota, método e produto](erros-rota-metodo-produto.md) | Falhou na verificação do formato documentado. | [Comprovantes](evidencias/erros-rota-metodo-produto/) |
| [Recalcular frete após alterar a quantidade com cupom aplicado](frete-alteracao-quantidade.md) | Falhou. | [Comprovantes](evidencias/frete-alteracao-quantidade/) |
| [Frete nos limites do subtotal](frete-limites-subtotal.md) | Falhou. | [Comprovantes](evidencias/frete-limites-subtotal/) |
| [Frete pelo subtotal anterior ao desconto](frete-subtotal-antes-desconto.md) | Falhou em um dos cinco exemplos. | [Comprovantes](evidencias/frete-subtotal-antes-desconto/) |
| [Rejeitar itens inválidos nas duas operações](itens-invalidos-api.md) | Falhou. | [Comprovantes](evidencias/itens-invalidos-api/) |
| [Recusa de corpo JSON inválido](json-invalido.md) | Falhou na verificação do formato documentado. | [Comprovantes](evidencias/json-invalido/) |
| [Manter o resumo do cálculo na confirmação](pedido-resumo-calculo.md) | Falhou. | [Comprovantes](evidencias/pedido-resumo-calculo/) |

As datas, os resultados, as observações adicionais e os comprovantes pertencem às execuções originais. Esta organização não representa uma nova execução.

[Voltar ao índice geral](../README.md)
