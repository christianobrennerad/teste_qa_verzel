#!/usr/bin/env bash
# Comandos capturados das 28 chamadas reais. Reexecutar gera novas respostas e confirmações fictícias caso a falha do limite persista.

# 01-itens-ausentes / calculo
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 01-itens-ausentes / pedido
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '{"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 02-itens-vazios / calculo
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":[]}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 02-itens-vazios / pedido
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '{"itens":[],"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 03-item-nulo / calculo
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":[null]}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 03-item-nulo / pedido
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '{"itens":[null],"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 04-item-texto / calculo
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":["P001"]}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 04-item-texto / pedido
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '{"itens":["P001"],"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 05-produto-id-ausente / calculo
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":[{"quantidade":1}]}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 05-produto-id-ausente / pedido
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '{"itens":[{"quantidade":1}],"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 06-quantidade-ausente / calculo
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001"}]}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 06-quantidade-ausente / pedido
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001"}],"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 07-produto-inexistente / calculo
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"INEXISTENTE","quantidade":1}]}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 07-produto-inexistente / pedido
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"INEXISTENTE","quantidade":1}],"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 08-quantidade-zero / calculo
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001","quantidade":0}]}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 08-quantidade-zero / pedido
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001","quantidade":0}],"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 09-quantidade-negativa / calculo
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001","quantidade":-1}]}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 09-quantidade-negativa / pedido
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001","quantidade":-1}],"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 10-quantidade-fracionada / calculo
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001","quantidade":1.5}]}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 10-quantidade-fracionada / pedido
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001","quantidade":1.5}],"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 11-quantidade-texto / calculo
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001","quantidade":"1"}]}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 11-quantidade-texto / pedido
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001","quantidade":"1"}],"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 12-quantidade-nula / calculo
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001","quantidade":null}]}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 12-quantidade-nula / pedido
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001","quantidade":null}],"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 13-quantidade-seis / calculo
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001","quantidade":6}]}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 13-quantidade-seis / pedido
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001","quantidade":6}],"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 14-quantidade-cem / calculo
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001","quantidade":100}]}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'

# 14-quantidade-cem / pedido
curl -i -X POST https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos -H 'Content-Type: application/json' --data-binary '{"itens":[{"produtoId":"P001","quantidade":100}],"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"}}' --max-time 30 --silent --show-error --write-out '
CURL_HTTP_STATUS:%{http_code}
'
