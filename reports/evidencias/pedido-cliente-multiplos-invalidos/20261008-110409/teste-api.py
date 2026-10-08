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
root = Path('reports/evidencias/pedido-cliente-multiplos-invalidos') / start.strftime('%Y%m%d-%H%M%S')
root.mkdir(parents=True)
Path('/tmp/verzel-pedido-cliente-multiplos-invalidos-run.txt').write_text(str(root.resolve()))
shutil.copyfile(__file__, root / 'teste-api.py')
request = {'cliente': {'nome': 'Maria', 'email': 'invalido', 'cep': '123'}, 'itens': [{'produtoId': 'P005', 'quantidade': 1}]}
body = json.dumps(request, ensure_ascii=False, separators=(',', ':'))
(root / 'corpo-enviado.json').write_text(body + '\n')
criteria = {'status': 422, 'erro.codigo': 'DADOS_INVALIDOS', 'camposSolicitados': ['cliente.nome', 'cliente.email'], 'observacaoAdicional': 'Registrar também cliente.cep, esperado pela documentação e pela feature existente; a mensagem atual do usuário exige nome e email.'}
(root / 'criterios.json').write_text(json.dumps(criteria, ensure_ascii=False, indent=2) + '\n')
cmd = ['curl', '-i', '-X', 'POST', 'https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos', '-H', 'Content-Type: application/json', '--data-binary', body, '--max-time', '30', '--silent', '--show-error', '--write-out', '\nCURL_HTTP_STATUS:%{http_code}\n']
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

def check(label, wanted, found, ok, scope='Cenário solicitado'):
    checks.append({'verificacao': label, 'escopo': scope, 'esperado': wanted, 'encontrado': found, 'resultado': 'Aprovado' if ok else 'Bloqueado' if result.returncode else 'Falhou'})

check('Status final da aplicação', 422, status, result.returncode == 0 and status == '422')
check('Corpo JSON válido e objeto', 'Objeto JSON', type(data).__name__, parse_error is None and type(data) is dict)
if not isinstance(data, dict):
    data = {}
error = data.get('erro') if isinstance(data.get('erro'), dict) else {}
check('erro.codigo', 'DADOS_INVALIDOS', error.get('codigo'), type(error.get('codigo')) is str and error['codigo'] == 'DADOS_INVALIDOS')
details = error.get('campos')
for field in criteria['camposSolicitados'] + ['cliente.cep']:
    matching = [d for d in details if isinstance(d, dict) and d.get('campo') == field and isinstance(d.get('mensagem'), str) and d['mensagem'].strip()] if isinstance(details, list) else []
    check('Campo inválido em erro.campos: ' + field, field, matching, bool(matching), 'Conferência adicional' if field == 'cliente.cep' else 'Cenário solicitado')
confirmation = {key: data[key] for key in ['numero', 'criadoEm'] if key in data}
check('Ausência de confirmação na resposta', 'Erro DADOS_INVALIDOS, status 422 e ausência de número/data de confirmação', {'status': status, 'erro': error, 'camposConfirmacao': confirmation}, status == '422' and error.get('codigo') == 'DADOS_INVALIDOS' and not confirmation, 'Conferência adicional')
main_checks = [c for c in checks if c['escopo'] == 'Cenário solicitado']
outcome = 'Bloqueado' if result.returncode else 'Aprovado' if all(c['resultado'] == 'Aprovado' for c in main_checks) else 'Falhou'
validation = {'inicio': start.isoformat(timespec='seconds'), 'fim': finish.isoformat(timespec='seconds'), 'timezone': 'America/Fortaleza', 'comando': cmd, 'curl_exit_code': result.returncode, 'json_parse_error': parse_error, 'resultado': outcome, 'verificacoes': checks}
(root / 'validacao-api.json').write_text(json.dumps(validation, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'evidencias': str(root), 'resultado': outcome, 'inicio': validation['inicio'], 'fim': validation['fim'], 'resposta': data, 'falhas': [c for c in checks if c['resultado'] != 'Aprovado']}, ensure_ascii=False), flush=True)
sys.exit(0 if outcome == 'Aprovado' else 1)
