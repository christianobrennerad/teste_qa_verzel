from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import hashlib
import json
import shutil

root = Path('/tmp/verzel-pedido-cliente-invalido-run.txt').read_text().strip()
root = Path(root)
shutil.copyfile(__file__, root / 'revisao-validacao.py')
summary_path = root / 'resumo-validacao.json'
summary = json.loads(summary_path.read_text())
archive = root / 'diagnostico-validador-inicial'
archive.mkdir()
shutil.copyfile(summary_path, archive / 'resumo-validacao.json')
raw_files = [p for case in summary['casos'] for p in (root / case['pasta']).iterdir() if p.name != 'validacao-api.json']
hashes_before = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in raw_files}
for case in summary['casos']:
    folder = root / case['pasta']
    shutil.copyfile(folder / 'validacao-api.json', archive / (case['pasta'] + '.json'))
    data = json.loads((folder / 'corpo-recebido.json').read_text())
    error = data.get('erro') if isinstance(data.get('erro'), dict) else {}
    details = error.get('campos')
    expected_field = 'cliente.' + case['campoEsperado']
    matching = [d for d in details if isinstance(d, dict) and d.get('campo') == expected_field and isinstance(d.get('mensagem'), str) and d['mensagem'].strip()] if isinstance(details, list) else []
    for check in case['verificacoes']:
        if check['verificacao'] == 'Campo inválido identificado em campos':
            check['encontrado'] = {'caminho': 'erro.campos', 'campos': details}
            check['resultado'] = 'Aprovado' if matching else 'Falhou'
    case['resultado'] = 'Bloqueado' if case['curl_exit_code'] else 'Aprovado' if all(v['resultado'] == 'Aprovado' for v in case['verificacoes']) else 'Falhou'
    (folder / 'validacao-api.json').write_text(json.dumps(case, ensure_ascii=False, indent=2) + '\n')
summary['resultado'] = 'Falhou' if any(c['resultado'] == 'Falhou' for c in summary['casos']) else 'Bloqueado' if any(c['resultado'] == 'Bloqueado' for c in summary['casos']) else 'Aprovado'
review = {'dataRevisao': datetime.now(ZoneInfo('America/Fortaleza')).isoformat(timespec='seconds'), 'motivo': 'A checagem inicial supôs campos como objeto. A resposta usa erro.campos como lista com identificador cliente.<campo> e mensagem. O cenário não exige um objeto; a leitura foi corrigida sem mudar critérios, requisições ou respostas.', 'novasRequisicoes': 0, 'resultadoFinal': summary['resultado'], 'sha256ArquivosCapturados': hashes_before}
hashes_after = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in raw_files}
assert hashes_before == hashes_after
summary['revisaoValidacao'] = {'arquivo': 'revisao-validacao.json', 'motivo': review['motivo'], 'novasRequisicoes': 0}
summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
(root / 'revisao-validacao.json').write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'resultado': summary['resultado'], 'casos': len(summary['casos']), 'verificacoes': sum(len(c['verificacoes']) for c in summary['casos']), 'arquivosCapturadosInalterados': len(hashes_before), 'novasRequisicoes': 0}, ensure_ascii=False))
