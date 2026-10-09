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
root = Path('reports/evidencias/campo-quantidade-invalida') / start.strftime('%Y%m%d-%H%M%S')
root.mkdir(parents=True)
Path('/tmp/verzel-campo-quantidade-invalida-run.txt').write_text(str(root.resolve()))
shutil.copyfile(__file__, root / 'teste-api.py')
body = '{"itens":[{"produtoId":"P001","quantidade":0}]}'
expected = {'codigo': 'QUANTIDADE_INVALIDA', 'mensagem': 'A quantidade deve ser um número inteiro maior ou igual a 1.', 'campo': 'itens[0].quantidade'}
(root / 'criterios.json').write_text(json.dumps({'status': 422, 'erro': expected}, ensure_ascii=False, indent=2) + '\n')
(root / 'corpo-enviado.json').write_text(body + '\n')
cmd = ['curl', '-i', '-X', 'POST', 'https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular', '-H', 'Content-Type: application/json', '--data-binary', body, '--max-time', '30', '--silent', '--show-error', '--write-out', '\nCURL_HTTP_STATUS:%{http_code}\n']
(root / 'comando.txt').write_text(shlex.join(cmd) + '\n')
result = subprocess.run(cmd, capture_output=True)
finish = datetime.now(tz)
(root / 'resposta-http.txt').write_bytes(result.stdout)
(root / 'curl-stderr.txt').write_bytes(result.stderr)
http, marker, status = result.stdout.decode(errors='replace').rpartition('\nCURL_HTTP_STATUS:')
status = status.strip()
raw = http.replace('\r\n', '\n').rsplit('\n\n', 1)[-1].strip() if marker else ''
(root / 'corpo-recebido.json').write_text(raw + '\n')
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
for field, wanted in expected.items():
    check('erro.' + field, wanted, error.get(field), type(error.get(field)) is str and error[field] == wanted)
outcome = 'Bloqueado' if result.returncode else 'Aprovado' if all(c['resultado'] == 'Aprovado' for c in checks) else 'Falhou'
validation = {'inicio': start.isoformat(timespec='seconds'), 'fim': finish.isoformat(timespec='seconds'), 'timezone': 'America/Fortaleza', 'comando': cmd, 'curl_exit_code': result.returncode, 'json_parse_error': parse_error, 'resultado': outcome, 'verificacoes': checks}
(root / 'validacao-api.json').write_text(json.dumps(validation, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'evidencias': str(root), 'resultado': outcome, 'inicio': validation['inicio'], 'fim': validation['fim'], 'resposta': data, 'falhas': [c for c in checks if c['resultado'] != 'Aprovado']}, ensure_ascii=False), flush=True)
sys.exit(0 if outcome == 'Aprovado' else 1)
