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
root = Path('reports/evidencias/pedido-resumo-calculo') / start.strftime('%Y%m%d-%H%M%S')
root.mkdir(parents=True)
Path('/tmp/verzel-pedido-resumo-calculo-run.txt').write_text(str(root.resolve()))
shutil.copyfile(__file__, root / 'teste-api.py')
items = [{'produtoId': 'P005', 'quantidade': 2}]
client = {'nome': 'Cliente Teste', 'email': 'qa@example.com', 'cep': '01310-100'}
expected = {'subtotal': 200, 'desconto': 20, 'frete': 0, 'total': 180}
fields = ['itens', 'subtotal', 'desconto', 'frete', 'freteGratis', 'valorFaltanteFreteGratis', 'total', 'cupom']
(root / 'criterios.json').write_text(json.dumps({'itens': items, 'cupom': 'BEMVINDO10', 'valoresEsperadosCalculo': expected, 'camposIguais': fields}, ensure_ascii=False, indent=2) + '\n')
records = []
responses = {}
exact_responses = {}

for phase, endpoint, status_expected in [('calculo', '/api/carrinho/calcular', 200), ('confirmacao', '/api/pedidos', 201)]:
    folder = root / phase
    folder.mkdir()
    request = {'itens': items, 'cupom': 'BEMVINDO10'}
    if phase == 'confirmacao':
        request = {'cliente': client, **request}
    body = json.dumps(request, ensure_ascii=False, separators=(',', ':'))
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
        exact = json.loads(raw, parse_float=Decimal, parse_int=Decimal)
    except ValueError as error:
        data = {}
        exact = {}
        parse_error = str(error)
    checks = []

    def check(label, wanted, found, ok):
        checks.append({'verificacao': label, 'esperado': wanted, 'encontrado': found, 'resultado': 'Aprovado' if ok else 'Bloqueado' if result.returncode else 'Falhou'})

    check('Status final da aplicação', status_expected, status, result.returncode == 0 and status == str(status_expected))
    check('Corpo JSON válido e objeto', 'Objeto JSON', type(data).__name__, parse_error is None and type(data) is dict)
    if not isinstance(data, dict):
        data = {}
        exact = {}
    if phase == 'calculo':
        for field, wanted in expected.items():
            check(field, wanted, data.get(field), type(data.get(field)) in (int, float) and exact.get(field) == Decimal(str(wanted)))
        actual_items = data.get('itens')
        check('Duas unidades de P005', items, actual_items, isinstance(actual_items, list) and len(actual_items) == 1 and isinstance(actual_items[0], dict) and actual_items[0].get('produtoId') == 'P005' and type(actual_items[0].get('quantidade')) is int and actual_items[0]['quantidade'] == 2)
        coupon = data.get('cupom') if isinstance(data.get('cupom'), dict) else {}
        check('Cupom BEMVINDO10 aplicado', {'codigo': 'BEMVINDO10', 'aplicado': True}, coupon, coupon.get('codigo') == 'BEMVINDO10' and coupon.get('aplicado') is True)
    else:
        calculation = responses['calculo']
        exact_calculation = exact_responses['calculo']
        for field in fields:
            present = field in calculation and field in data
            if field in ['subtotal', 'desconto', 'frete', 'valorFaltanteFreteGratis', 'total']:
                same = present and type(calculation[field]) in (int, float) and type(data[field]) in (int, float) and exact_calculation[field] == exact[field]
            elif field == 'freteGratis':
                same = present and type(calculation[field]) is bool and type(data[field]) is bool and calculation[field] is data[field]
            else:
                same = present and type(calculation[field]) is type(data[field]) and calculation[field] == data[field]
            check('Igualdade de ' + field, calculation.get(field), data.get(field), same)
    outcome = 'Bloqueado' if result.returncode else 'Aprovado' if all(c['resultado'] == 'Aprovado' for c in checks) else 'Falhou'
    record = {'etapa': phase, 'inicio': phase_start, 'fim': datetime.now(tz).isoformat(timespec='seconds'), 'comando': cmd, 'curl_exit_code': result.returncode, 'json_parse_error': parse_error, 'resultado': outcome, 'verificacoes': checks}
    (folder / 'validacao-api.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    responses[phase] = data
    exact_responses[phase] = exact
    records.append(record)
    print(json.dumps({'etapa': phase, 'resultado': outcome, 'resposta': data, 'falhas': [c for c in checks if c['resultado'] != 'Aprovado']}, ensure_ascii=False), flush=True)

outcome = 'Falhou' if any(r['resultado'] == 'Falhou' for r in records) else 'Bloqueado' if any(r['resultado'] == 'Bloqueado' for r in records) else 'Aprovado'
summary = {'inicio': start.isoformat(timespec='seconds'), 'fim': datetime.now(tz).isoformat(timespec='seconds'), 'timezone': 'America/Fortaleza', 'resultado': outcome, 'etapas': records, 'camposIguais': fields}
(root / 'resumo-validacao.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'evidencias': str(root), 'resultado': outcome, 'inicio': summary['inicio'], 'fim': summary['fim']}, ensure_ascii=False), flush=True)
sys.exit(0 if outcome == 'Aprovado' else 1)
