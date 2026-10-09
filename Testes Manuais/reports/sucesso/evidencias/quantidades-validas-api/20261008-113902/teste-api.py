from datetime import datetime
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo
import json
import shlex
import shutil
import subprocess
import sys

tz = ZoneInfo('America/Fortaleza')
start = datetime.now(tz)
root = Path('reports/evidencias/quantidades-validas-api') / start.strftime('%Y%m%d-%H%M%S')
root.mkdir(parents=True)
Path('/tmp/verzel-quantidades-validas-api-run.txt').write_text(str(root.resolve()))
shutil.copyfile(__file__, root / 'teste-api.py')
client = {'nome': 'Cliente Teste', 'email': 'qa@example.com', 'cep': '01310-100'}
cases = [
    {'pasta': '01-calculo-uma-unidade', 'endpoint': '/api/carrinho/calcular', 'quantidade': 1, 'status': 200, 'subtotal': 50},
    {'pasta': '02-calculo-cinco-unidades', 'endpoint': '/api/carrinho/calcular', 'quantidade': 5, 'status': 200, 'subtotal': 250},
    {'pasta': '03-pedido-uma-unidade', 'endpoint': '/api/pedidos', 'quantidade': 1, 'status': 201, 'subtotal': 50},
    {'pasta': '04-pedido-cinco-unidades', 'endpoint': '/api/pedidos', 'quantidade': 5, 'status': 201, 'subtotal': 250},
]
(root / 'criterios.json').write_text(json.dumps({'cliente': client, 'produtoId': 'P008', 'precoUnitario': 50, 'casos': cases}, ensure_ascii=False, indent=2) + '\n')
records = []
for case in cases:
    folder = root / case['pasta']
    folder.mkdir()
    request = {'cliente': client, 'itens': [{'produtoId': 'P008', 'quantidade': case['quantidade']}]}
    body = json.dumps(request, ensure_ascii=False, separators=(',', ':'))
    (folder / 'corpo-enviado.json').write_text(body + '\n')
    cmd = ['curl', '-i', '-X', 'POST', 'https://verzel-store.qa-test-verzel-store.workers.dev' + case['endpoint'], '-H', 'Content-Type: application/json', '--data-binary', body, '--max-time', '30', '--silent', '--show-error', '--write-out', '\nCURL_HTTP_STATUS:%{http_code}\n']
    (folder / 'comando.txt').write_text(shlex.join(cmd) + '\n')
    phase_start = datetime.now(tz).isoformat(timespec='seconds')
    result = subprocess.run(cmd, capture_output=True)
    (folder / 'resposta-http.txt').write_bytes(result.stdout)
    (folder / 'curl-stderr.txt').write_bytes(result.stderr)
    http, marker, status = result.stdout.decode(errors='replace').rpartition('\nCURL_HTTP_STATUS:')
    status = status.strip()
    raw = http.replace('\r\n', '\n').rsplit('\n\n', 1)[-1].strip() if marker else ''
    (folder / 'corpo-recebido.json').write_text(raw + '\n')
    parse_error = None
    try:
        data = json.loads(raw)
        exact = json.loads(raw, parse_float=Decimal, parse_int=Decimal)
    except ValueError as error:
        data = {}
        exact = {}
        parse_error = str(error)
    checks = []

    def check(label, wanted, found, ok):
        checks.append({'verificacao': label, 'esperado': wanted, 'encontrado': found, 'resultado': 'Aprovado' if ok else 'Bloqueado' if result.returncode else 'Falhou'})

    check('Status final da aplicação', case['status'], status, result.returncode == 0 and status == str(case['status']))
    check('Corpo JSON válido e objeto', 'Objeto JSON', type(data).__name__, parse_error is None and type(data) is dict)
    if not isinstance(data, dict):
        data = {}
        exact = {}
    check('Subtotal', case['subtotal'], data.get('subtotal'), type(data.get('subtotal')) in (int, float) and exact.get('subtotal') == Decimal(str(case['subtotal'])))
    items = data.get('itens')
    check('Produto e quantidade retornados', {'produtoId': 'P008', 'quantidade': case['quantidade']}, items, isinstance(items, list) and len(items) == 1 and isinstance(items[0], dict) and items[0].get('produtoId') == 'P008' and type(items[0].get('quantidade')) is int and items[0]['quantidade'] == case['quantidade'])
    outcome = 'Bloqueado' if result.returncode else 'Aprovado' if all(c['resultado'] == 'Aprovado' for c in checks) else 'Falhou'
    record = {'pasta': case['pasta'], 'endpoint': case['endpoint'], 'quantidade': case['quantidade'], 'inicio': phase_start, 'fim': datetime.now(tz).isoformat(timespec='seconds'), 'comando': cmd, 'curl_exit_code': result.returncode, 'json_parse_error': parse_error, 'resultado': outcome, 'verificacoes': checks}
    (folder / 'validacao-api.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    records.append(record)
    print(json.dumps({'caso': case['pasta'], 'resultado': outcome, 'resposta': data, 'falhas': [c for c in checks if c['resultado'] != 'Aprovado']}, ensure_ascii=False), flush=True)
outcome = 'Falhou' if any(r['resultado'] == 'Falhou' for r in records) else 'Bloqueado' if any(r['resultado'] == 'Bloqueado' for r in records) else 'Aprovado'
summary = {'inicio': start.isoformat(timespec='seconds'), 'fim': datetime.now(tz).isoformat(timespec='seconds'), 'timezone': 'America/Fortaleza', 'resultado': outcome, 'casos': records}
(root / 'resumo-validacao.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'evidencias': str(root), 'resultado': outcome, 'inicio': summary['inicio'], 'fim': summary['fim']}, ensure_ascii=False), flush=True)
sys.exit(0 if outcome == 'Aprovado' else 1)
