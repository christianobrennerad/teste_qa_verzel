from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import json
import shlex
import shutil
import subprocess
import sys

TZ = ZoneInfo('America/Fortaleza')
start = datetime.now(TZ)
root = Path('reports/evidencias/itens-invalidos-api') / start.strftime('%Y%m%d-%H%M%S')
root.mkdir(parents=True)
Path('/tmp/verzel-itens-invalidos-api-run.txt').write_text(str(root.resolve()))
shutil.copyfile(__file__, root / 'teste-api.py')
client = {'nome': 'Cliente Teste', 'email': 'qa@example.com', 'cep': '01310-100'}
examples = [
    ('01-itens-ausentes', '{}', 'ITENS_OBRIGATORIOS', ['itens']),
    ('02-itens-vazios', '{"itens":[]}', 'ITENS_OBRIGATORIOS', ['itens']),
    ('03-item-nulo', '{"itens":[null]}', 'ITEM_INVALIDO', ['itens[0]']),
    ('04-item-texto', '{"itens":["P001"]}', 'ITEM_INVALIDO', ['itens[0]']),
    ('05-produto-id-ausente', '{"itens":[{"quantidade":1}]}', 'ITEM_INVALIDO', ['itens[0]', 'itens[0].produtoId']),
    ('06-quantidade-ausente', '{"itens":[{"produtoId":"P001"}]}', 'ITEM_INVALIDO', ['itens[0]', 'itens[0].quantidade']),
    ('07-produto-inexistente', '{"itens":[{"produtoId":"INEXISTENTE","quantidade":1}]}', 'PRODUTO_NAO_ENCONTRADO', ['itens[0]', 'itens[0].produtoId']),
    ('08-quantidade-zero', '{"itens":[{"produtoId":"P001","quantidade":0}]}', 'QUANTIDADE_INVALIDA', ['itens[0]', 'itens[0].quantidade']),
    ('09-quantidade-negativa', '{"itens":[{"produtoId":"P001","quantidade":-1}]}', 'QUANTIDADE_INVALIDA', ['itens[0]', 'itens[0].quantidade']),
    ('10-quantidade-fracionada', '{"itens":[{"produtoId":"P001","quantidade":1.5}]}', 'QUANTIDADE_INVALIDA', ['itens[0]', 'itens[0].quantidade']),
    ('11-quantidade-texto', '{"itens":[{"produtoId":"P001","quantidade":"1"}]}', 'QUANTIDADE_INVALIDA', ['itens[0]', 'itens[0].quantidade']),
    ('12-quantidade-nula', '{"itens":[{"produtoId":"P001","quantidade":null}]}', 'QUANTIDADE_INVALIDA', ['itens[0]', 'itens[0].quantidade']),
    ('13-quantidade-seis', '{"itens":[{"produtoId":"P001","quantidade":6}]}', 'QUANTIDADE_MAXIMA_EXCEDIDA', ['itens[0]', 'itens[0].quantidade']),
    ('14-quantidade-cem', '{"itens":[{"produtoId":"P001","quantidade":100}]}', 'QUANTIDADE_MAXIMA_EXCEDIDA', ['itens[0]', 'itens[0].quantidade']),
]
cases = [{'pasta': slug, 'corpo': body, 'codigo': code, 'camposRelacionadosAceitos': fields} for slug, body, code, fields in examples]
(root / 'criterios.json').write_text(json.dumps({'status': 422, 'clientePedidos': client, 'formatoErro': 'Objeto erro com codigo, mensagem e campo relacionado, como texto não vazio.', 'casos': cases}, ensure_ascii=False, indent=2) + '\n')
records = []
for case in cases:
    case_result = {'pasta': case['pasta'], 'corpoOriginal': case['corpo'], 'codigoEsperado': case['codigo'], 'etapas': []}
    for phase, endpoint in [('calculo', '/api/carrinho/calcular'), ('pedido', '/api/pedidos')]:
        folder = root / case['pasta'] / phase
        folder.mkdir(parents=True)
        body = case['corpo']
        if phase == 'pedido':
            request = {**json.loads(body), 'cliente': client}
            body = json.dumps(request, ensure_ascii=False, separators=(',', ':'))
        (folder / 'corpo-enviado.json').write_text(body + '\n')
        cmd = ['curl', '-i', '-X', 'POST', 'https://verzel-store.qa-test-verzel-store.workers.dev' + endpoint, '-H', 'Content-Type: application/json', '--data-binary', body, '--max-time', '30', '--silent', '--show-error', '--write-out', '\nCURL_HTTP_STATUS:%{http_code}\n']
        (folder / 'comando.txt').write_text(shlex.join(cmd) + '\n')
        phase_start = datetime.now(TZ).isoformat(timespec='seconds')
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
        check('erro.codigo', case['codigo'], error.get('codigo'), type(error.get('codigo')) is str and error['codigo'] == case['codigo'])
        check('erro.mensagem', 'Texto não vazio explicando o erro', error.get('mensagem'), isinstance(error.get('mensagem'), str) and bool(error['mensagem'].strip()))
        check('erro.campo relacionado ao problema', case['camposRelacionadosAceitos'], error.get('campo'), isinstance(error.get('campo'), str) and error['campo'] in case['camposRelacionadosAceitos'])
        confirmation = {key: data[key] for key in ['numero', 'criadoEm'] if key in data}
        check('Ausência de confirmação na resposta', 'Resposta de erro com status 422, sem numero ou criadoEm', {'status': status, 'erro': error, 'camposConfirmacao': confirmation}, status == '422' and bool(error) and not confirmation)
        outcome = 'Bloqueado' if result.returncode else 'Aprovado' if all(c['resultado'] == 'Aprovado' for c in checks) else 'Falhou'
        record = {'etapa': phase, 'endpoint': endpoint, 'inicio': phase_start, 'fim': datetime.now(TZ).isoformat(timespec='seconds'), 'comando': cmd, 'curl_exit_code': result.returncode, 'json_parse_error': parse_error, 'resultado': outcome, 'verificacoes': checks}
        (folder / 'validacao-api.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
        case_result['etapas'].append(record)
        print(json.dumps({'caso': case['pasta'], 'etapa': phase, 'resultado': outcome, 'status': status, 'erro': error, 'falhas': [c for c in checks if c['resultado'] != 'Aprovado']}, ensure_ascii=False), flush=True)
    case_result['resultado'] = 'Falhou' if any(r['resultado'] == 'Falhou' for r in case_result['etapas']) else 'Bloqueado' if any(r['resultado'] == 'Bloqueado' for r in case_result['etapas']) else 'Aprovado'
    records.append(case_result)
outcome = 'Falhou' if any(r['resultado'] == 'Falhou' for r in records) else 'Bloqueado' if any(r['resultado'] == 'Bloqueado' for r in records) else 'Aprovado'
summary = {'inicio': start.isoformat(timespec='seconds'), 'fim': datetime.now(TZ).isoformat(timespec='seconds'), 'timezone': 'America/Fortaleza', 'resultado': outcome, 'casos': records}
(root / 'resumo-validacao.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'evidencias': str(root), 'resultado': outcome, 'inicio': summary['inicio'], 'fim': summary['fim']}, ensure_ascii=False), flush=True)
sys.exit(0 if outcome == 'Aprovado' else 1)
