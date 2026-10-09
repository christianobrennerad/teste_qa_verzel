# Testes com sucesso

Os 24 relatórios abaixo têm resultado **Aprovado** no escopo descrito em cada documento.

Cada relatório contém o BDD, os resultados e os links dos comprovantes. As evidências ficam em `evidencias/<nome>/`, nesta pasta.

| Teste | Resultado registrado | Evidências |
| --- | --- | --- |
| [Identificar o campo da quantidade inválida](campo-quantidade-invalida.md) | Aprovado. | [Comprovantes](evidencias/campo-quantidade-invalida/) |
| [Iniciar outro contexto de navegação com carrinho vazio](carrinho-isolamento-contextos.md) | Aprovado — os três exemplos passaram com Firefox. | [Comprovantes](evidencias/carrinho-isolamento-contextos/) |
| [Detalhar valores calculados por item](carrinho-valores-por-item.md) | Aprovado. | [Comprovantes](evidencias/carrinho-valores-por-item/) |
| [Catálogo de produtos](catalogo-produtos.md) | Aprovado. | [Comprovantes](evidencias/catalogo-produtos/) |
| [Concluir compra com pagamento na entrega](compra-pagamento-entrega.md) | Aprovado. | [Comprovantes](evidencias/compra-pagamento-entrega/) |
| [Ignorar espaços externos do cupom](cupom-espacos-externos.md) | Aprovado. | [Comprovantes](evidencias/cupom-espacos-externos/) |
| [Cupom com maiúsculas e minúsculas](cupom-normalizacao.md) | Aprovado nos dois exemplos executados. | [Comprovantes](evidencias/cupom-normalizacao/) |
| [Remover o cupom e recalcular o carrinho](cupom-remocao-reaplicacao.md) | Aprovado. | [Comprovantes](evidencias/cupom-remocao-reaplicacao/) |
| [Remover cupom válido e tentar cupom expirado](cupom-troca-expirado.md) | Aprovado. | [Comprovantes](evidencias/cupom-troca-expirado/) |
| [Manter apenas um cupom aplicado](cupom-unico.md) | Aprovado para a proteção oferecida pela interface. | [Comprovantes](evidencias/cupom-unico/) |
| [Cupom inválido no cálculo e na confirmação](cupons-calculo-confirmacao.md) | Aprovado. | [Comprovantes](evidencias/cupons-calculo-confirmacao/) |
| [Recusar cupom inexistente ou expirado](cupons-inexistente-expirado.md) | Aprovado nos dois exemplos. | [Comprovantes](evidencias/cupons-inexistente-expirado/) |
| [Informar quanto falta para frete grátis](frete-valor-faltante.md) | Aprovado. | [Comprovantes](evidencias/frete-valor-faltante/) |
| [Permitir até cinco unidades de um produto](limite-cinco-unidades.md) | Aprovado para o cenário de quantidade. | [Comprovantes](evidencias/limite-cinco-unidades/) |
| [Limitar cada produto independentemente](limites-independentes-produtos.md) | Aprovado. | [Comprovantes](evidencias/limites-independentes-produtos/) |
| [Aceitar CEP com ou sem hífen](pedido-cep-formatos.md) | Aprovado. | [Comprovantes](evidencias/pedido-cep-formatos/) |
| [Rejeitar dados inválidos do cliente](pedido-cliente-invalido.md) | Aprovado. | [Comprovantes](evidencias/pedido-cliente-invalido/) |
| [Informar múltiplos dados inválidos do cliente](pedido-cliente-multiplos-invalidos.md) | Aprovado. | [Comprovantes](evidencias/pedido-cliente-multiplos-invalidos/) |
| [Normalizar o cupom na confirmação do pedido](pedido-cupom-normalizacao.md) | Aprovado. | [Comprovantes](evidencias/pedido-cupom-normalizacao/) |
| [Confirmar pedido com ou sem cupom](pedidos-com-sem-cupom.md) | Aprovado — os dois exemplos passaram. | [Comprovantes](evidencias/pedidos-com-sem-cupom/) |
| [Confirmar pedidos repetidos sem consumir estoque](pedidos-repetidos-sem-estoque.md) | Aprovado. | [Comprovantes](evidencias/pedidos-repetidos-sem-estoque/) |
| [Rejeitar produto duplicado](produto-duplicado-api.md) | Aprovado. | [Comprovantes](evidencias/produto-duplicado-api/) |
| [Consulta do produto P001](produto-p001.md) | Aprovado. | [Comprovantes](evidencias/produto-p001/) |
| [Aceitar os limites válidos de quantidade](quantidades-validas-api.md) | Aprovado. | [Comprovantes](evidencias/quantidades-validas-api/) |

As datas, os resultados, as observações adicionais e os comprovantes pertencem às execuções originais. Esta organização não representa uma nova execução.

[Voltar ao índice geral](../README.md)
