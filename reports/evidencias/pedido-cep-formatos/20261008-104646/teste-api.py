from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import json
import shlex
import shutil
import subprocess
import sys

tz = ZoneInfo('America/Fortaleza')
start = datetime.now(tz)
root = Path('reports/evidencias/pedido-cep-formatos') / start.strftime('%Y%m%d-%H%M%S')
root.mkdir(parents=True)
Path('/tmp/verzel-pedido-cep-formatos-run.txt').write_text(str(root.resolve()))
shutil.copyfile(__file__, root / 'teste-api.py')
cases = [{'pasta': '01-com-hifen', 'cep': '01310-100'}, {'pasta': '02-sem-hifen', 'cep': '01310100'}]
(root / 'criterios.json').write_text(json.dumps({'casos': cases, 'status': 201, 'cliente.cep': '01310100', 'itens': [{'produtoId': 'P005', 'quantidade': 1}]}, ensure_ascii=False, indent=2) + '\n')
records = []
for case in cases:
    folder = root / case['pasta']
    folder.mkdir()
    request = {'cliente': {'nome': 'Maria Silva', 'email': 'maria@exemplo.com', 'cep': case['cep']}, 'itens': [{'produtoId': 'P005', 'quantidade': 1}]}
    body = json.dumps(request, ensure_ascii=False, separators=(',', ':'))
    (folder / 'corpo-enviado.json').write_text(body + '\n')
    cmd = ['curl', '-i', '-X', 'POST', 'https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos', '-H', 'Content-Type: application/json', '--data-binary', body, '--max-time', '30', '--silent', '--show-error', '--write-out', '\nCURL_HTTP_STATUS:%{http_code}\n']
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
    except ValueError as error:
        data = {}
        parse_error = str(error)
    checks = []

    def check(label, wanted, found, ok):
        checks.append({'verificacao': label, 'esperado': wanted, 'encontrado': found, 'resultado': 'Aprovado' if ok else 'Bloqueado' if result.returncode else 'Falhou'})

    check('Status final da aplicação', 201, status, result.returncode == 0 and status == '201')
    check('Corpo JSON válido e objeto', 'Objeto JSON', type(data).__name__, parse_error is None and type(data) is dict)
    if not isinstance(data, dict):
        data = {}
    client = data.get('cliente') if isinstance(data.get('cliente'), dict) else {}
    check('cliente.cep', '01310100', client.get('cep'), type(client.get('cep')) is str and client['cep'] == '01310100')
    items = data.get('itens')
    check('Uma unidade de P005', {'produtoId': 'P005', 'quantidade': 1}, items, isinstance(items, list) and len(items) == 1 and isinstance(items[0], dict) and items[0].get('produtoId') == 'P005' and type(items[0].get('quantidade')) is int and items[0]['quantidade'] == 1)
    outcome = 'Bloqueado' if result.returncode else 'Aprovado' if all(c['resultado'] == 'Aprovado' for c in checks) else 'Falhou'
    record = {'cepEnviado': case['cep'], 'pasta': case['pasta'], 'inicio': phase_start, 'fim': datetime.now(tz).isoformat(timespec='seconds'), 'comando': cmd, 'curl_exit_code': result.returncode, 'json_parse_error': parse_error, 'resultado': outcome, 'verificacoes': checks}
    (folder / 'validacao-api.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    records.append(record)
    print(json.dumps({'cepEnviado': case['cep'], 'resultado': outcome, 'resposta': data, 'falhas': [c for c in checks if c['resultado'] != 'Aprovado']}, ensure_ascii=False), flush=True)
outcome = 'Falhou' if any(r['resultado'] == 'Falhou' for r in records) else 'Bloqueado' if any(r['resultado'] == 'Bloqueado' for r in records) else 'Aprovado'
summary = {'inicio': start.isoformat(timespec='seconds'), 'fim': datetime.now(tz).isoformat(timespec='seconds'), 'timezone': 'America/Fortaleza', 'resultado': outcome, 'casos': records}
(root / 'resumo-validacao.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'evidencias': str(root), 'resultado': outcome, 'inicio': summary['inicio'], 'fim': summary['fim']}, ensure_ascii=False), flush=True)
sys.exit(0 if outcome == 'Aprovado' else 1)
