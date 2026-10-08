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
root = Path('reports/evidencias/pedido-cliente-invalido') / start.strftime('%Y%m%d-%H%M%S')
root.mkdir(parents=True)
Path('/tmp/verzel-pedido-cliente-invalido-run.txt').write_text(str(root.resolve()))
shutil.copyfile(__file__, root / 'teste-api.py')
valid = {'nome': 'Maria Silva', 'email': 'maria@exemplo.com', 'cep': '01310100'}
cases = [
    {'pasta': '01-nome-sem-sobrenome', 'campo': 'nome', 'valor': 'Maria'},
    {'pasta': '02-nome-vazio', 'campo': 'nome', 'valor': ''},
    {'pasta': '03-email-sem-arroba', 'campo': 'email', 'valor': 'maria.exemplo.com'},
    {'pasta': '04-email-vazio', 'campo': 'email', 'valor': ''},
    {'pasta': '05-cep-sete-digitos', 'campo': 'cep', 'valor': '0131010'},
    {'pasta': '06-cep-nove-digitos', 'campo': 'cep', 'valor': '013101000'},
    {'pasta': '07-cep-letras', 'campo': 'cep', 'valor': 'ABCDEFGH'},
    {'pasta': '08-cep-vazio', 'campo': 'cep', 'valor': ''},
]
(root / 'criterios.json').write_text(json.dumps({'clienteBase': valid, 'casos': cases, 'status': 422, 'erro.codigo': 'DADOS_INVALIDOS', 'campos': 'Deve indicar o campo inválido do exemplo', 'confirmacao': 'Sem numero ou criadoEm', 'itens': [{'produtoId': 'P005', 'quantidade': 1}]}, ensure_ascii=False, indent=2) + '\n')
records = []
for case in cases:
    folder = root / case['pasta']
    folder.mkdir()
    client = {**valid, case['campo']: case['valor']}
    request = {'cliente': client, 'itens': [{'produtoId': 'P005', 'quantidade': 1}]}
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

    check('Status final da aplicação', 422, status, result.returncode == 0 and status == '422')
    check('Corpo JSON válido e objeto', 'Objeto JSON', type(data).__name__, parse_error is None and type(data) is dict)
    if not isinstance(data, dict):
        data = {}
    error = data.get('erro') if isinstance(data.get('erro'), dict) else {}
    check('erro.codigo', 'DADOS_INVALIDOS', error.get('codigo'), type(error.get('codigo')) is str and error['codigo'] == 'DADOS_INVALIDOS')
    details = data.get('campos')
    path = 'campos'
    if details is None and 'campos' in error:
        details = error['campos']
        path = 'erro.campos'
    field_detail = details.get(case['campo']) if isinstance(details, dict) else None
    check('Campo inválido identificado em campos', case['campo'], {'caminho': path, 'campos': details}, isinstance(details, dict) and case['campo'] in details and bool(field_detail))
    confirmation = {key: data[key] for key in ['numero', 'criadoEm'] if key in data}
    check('Pedido não confirmado na resposta', 'Status 422, erro DADOS_INVALIDOS e ausência de número/data de confirmação', {'status': status, 'erro': error, 'camposConfirmacao': confirmation}, status == '422' and error.get('codigo') == 'DADOS_INVALIDOS' and not confirmation)
    outcome = 'Bloqueado' if result.returncode else 'Aprovado' if all(c['resultado'] == 'Aprovado' for c in checks) else 'Falhou'
    record = {'pasta': case['pasta'], 'clienteEnviado': client, 'campoEsperado': case['campo'], 'inicio': phase_start, 'fim': datetime.now(tz).isoformat(timespec='seconds'), 'comando': cmd, 'curl_exit_code': result.returncode, 'json_parse_error': parse_error, 'resultado': outcome, 'verificacoes': checks}
    (folder / 'validacao-api.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    records.append(record)
    print(json.dumps({'caso': case['pasta'], 'resultado': outcome, 'resposta': data, 'falhas': [c for c in checks if c['resultado'] != 'Aprovado']}, ensure_ascii=False), flush=True)
outcome = 'Falhou' if any(r['resultado'] == 'Falhou' for r in records) else 'Bloqueado' if any(r['resultado'] == 'Bloqueado' for r in records) else 'Aprovado'
summary = {'inicio': start.isoformat(timespec='seconds'), 'fim': datetime.now(tz).isoformat(timespec='seconds'), 'timezone': 'America/Fortaleza', 'resultado': outcome, 'casos': records}
(root / 'resumo-validacao.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'evidencias': str(root), 'resultado': outcome, 'inicio': summary['inicio'], 'fim': summary['fim']}, ensure_ascii=False), flush=True)
sys.exit(0 if outcome == 'Aprovado' else 1)
