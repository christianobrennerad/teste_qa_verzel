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
root = Path('reports/evidencias/produto-duplicado-api') / start.strftime('%Y%m%d-%H%M%S')
root.mkdir(parents=True)
Path('/tmp/verzel-produto-duplicado-api-run.txt').write_text(str(root.resolve()))
shutil.copyfile(__file__, root / 'teste-api.py')
body_original = '{"itens":[{"produtoId":"P001","quantidade":3},{"produtoId":"P001","quantidade":3}]}'
client = {'nome': 'Cliente Teste', 'email': 'qa@example.com', 'cep': '01310-100'}
(root / 'criterios.json').write_text(json.dumps({'corpoOriginal': body_original, 'clientePedidos': client, 'status': 422, 'erro.codigo': 'ITEM_DUPLICADO'}, ensure_ascii=False, indent=2) + '\n')
records = []
for phase, endpoint in [('calculo', '/api/carrinho/calcular'), ('pedido', '/api/pedidos')]:
    folder = root / phase
    folder.mkdir()
    body = body_original
    if phase == 'pedido':
        body = json.dumps({**json.loads(body), 'cliente': client}, ensure_ascii=False, separators=(',', ':'))
    (folder / 'corpo-enviado.json').write_text(body + '\n')
    cmd = ['curl', '-i', '-X', 'POST', 'https://verzel-store.qa-test-verzel-store.workers.dev' + endpoint, '-H', 'Content-Type: application/json', '--data-binary', body, '--max-time', '30', '--silent', '--show-error', '--write-out', '\nCURL_HTTP_STATUS:%{http_code}\n']
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

    check('Status final da aplicação', 422, status, result.returncode == 0 and status == '422')
    check('Corpo JSON válido e objeto', 'Objeto JSON', type(data).__name__, parse_error is None and type(data) is dict)
    if not isinstance(data, dict):
        data = {}
    error = data.get('erro') if isinstance(data.get('erro'), dict) else {}
    check('erro.codigo', 'ITEM_DUPLICADO', error.get('codigo'), type(error.get('codigo')) is str and error['codigo'] == 'ITEM_DUPLICADO')
    confirmation = {key: data[key] for key in ['numero', 'criadoEm'] if key in data}
    check('Recusa sem confirmação na resposta', 'Status 422, erro ITEM_DUPLICADO e ausência de número/data de confirmação', {'status': status, 'erro': error, 'camposConfirmacao': confirmation}, status == '422' and error.get('codigo') == 'ITEM_DUPLICADO' and not confirmation)
    outcome = 'Bloqueado' if result.returncode else 'Aprovado' if all(c['resultado'] == 'Aprovado' for c in checks) else 'Falhou'
    record = {'etapa': phase, 'endpoint': endpoint, 'inicio': phase_start, 'fim': datetime.now(tz).isoformat(timespec='seconds'), 'comando': cmd, 'curl_exit_code': result.returncode, 'json_parse_error': parse_error, 'resultado': outcome, 'verificacoes': checks}
    (folder / 'validacao-api.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    records.append(record)
    print(json.dumps({'etapa': phase, 'resultado': outcome, 'resposta': data, 'falhas': [c for c in checks if c['resultado'] != 'Aprovado']}, ensure_ascii=False), flush=True)
outcome = 'Falhou' if any(r['resultado'] == 'Falhou' for r in records) else 'Bloqueado' if any(r['resultado'] == 'Bloqueado' for r in records) else 'Aprovado'
summary = {'inicio': start.isoformat(timespec='seconds'), 'fim': datetime.now(tz).isoformat(timespec='seconds'), 'timezone': 'America/Fortaleza', 'resultado': outcome, 'etapas': records}
(root / 'resumo-validacao.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'evidencias': str(root), 'resultado': outcome, 'inicio': summary['inicio'], 'fim': summary['fim']}, ensure_ascii=False), flush=True)
sys.exit(0 if outcome == 'Aprovado' else 1)
