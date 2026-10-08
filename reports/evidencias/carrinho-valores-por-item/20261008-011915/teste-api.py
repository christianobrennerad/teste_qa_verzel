from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal
import subprocess,json,shlex,shutil,sys

tz=ZoneInfo('America/Fortaleza');start=datetime.now(tz)
root=Path('reports/evidencias/carrinho-valores-por-item')/start.strftime('%Y%m%d-%H%M%S')
root.mkdir(parents=True,exist_ok=False)
Path('/tmp/verzel-valores-por-item-run.txt').write_text(str(root.resolve()))
shutil.copyfile(__file__,root/'teste-api.py')
body='{"itens":[{"produtoId":"P002","quantidade":1},{"produtoId":"P004","quantidade":2}],"cupom":"BEMVINDO10"}'
expected=[{'produtoId':'P002','nome':'Calça Jeans Slim','precoUnitario':139.9,'quantidade':1,'total':139.9},{'produtoId':'P004','nome':'Boné Aba Curva','precoUnitario':49.9,'quantidade':2,'total':99.8}]
(root/'corpo-enviado.json').write_text(body)
(root/'esperado.json').write_text(json.dumps({'status':200,'itens':expected,'cupom':{'codigo':'BEMVINDO10','aplicado':True,'mensagem':'Cupom aplicado: 10% de desconto nos produtos.'}},ensure_ascii=False,indent=2)+'\n')
cmd=['curl','-i','-X','POST','https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular','-H','Content-Type: application/json','--data-binary',body,'--max-time','30','--silent','--show-error','--write-out','\nCURL_HTTP_STATUS:%{http_code}\n']
(root/'comando.txt').write_text(shlex.join(cmd)+'\n')
r=subprocess.run(cmd,capture_output=True);end=datetime.now(tz)
(root/'resposta-http.txt').write_bytes(r.stdout);(root/'curl-stderr.txt').write_bytes(r.stderr)
response,sep,status=r.stdout.decode(errors='replace').rpartition('\nCURL_HTTP_STATUS:')
raw=response.replace('\r\n','\n').rsplit('\n\n',1)[-1].strip() if sep else ''
(root/'corpo-recebido.json').write_text(raw+'\n')
parse_error=None
try:
    data=json.loads(raw);exact=json.loads(raw,parse_float=Decimal,parse_int=Decimal)
except ValueError as e:
    data={};exact={};parse_error=str(e)
checks=[]
def check(name,want,found,ok):checks.append({'verificacao':name,'esperado':want,'encontrado':found,'resultado':'Aprovado' if ok else ('Bloqueado' if r.returncode else 'Falhou')})
check('Status final da aplicação',200,status.strip(),r.returncode==0 and status.strip()=='200')
check('Corpo JSON válido e objeto','Objeto JSON',type(data).__name__,parse_error is None and type(data) is dict)
if not isinstance(data,dict):data={};exact={}
items=data.get('itens');exact_items=exact.get('itens')
check('Quantidade de itens na resposta',2,len(items) if isinstance(items,list) else None,isinstance(items,list) and len(items)==2)
for want in expected:
    matches=[i for i in (items if isinstance(items,list) else []) if isinstance(i,dict) and i.get('produtoId')==want['produtoId']]
    exact_matches=[i for i in (exact_items if isinstance(exact_items,list) else []) if isinstance(i,dict) and i.get('produtoId')==want['produtoId']]
    check(want['produtoId']+': ocorrência única',1,len(matches),len(matches)==1)
    found=matches[0] if len(matches)==1 else {};found_exact=exact_matches[0] if len(exact_matches)==1 else {}
    for k,v in want.items():
        got=found.get(k)
        ok=(type(got) in (int,float) and found_exact.get(k)==Decimal(str(v))) if k in ('precoUnitario','total') else type(got) is type(v) and got==v
        check(want['produtoId']+'.'+k,v,got,ok)
coupon=data.get('cupom');coupon=coupon if isinstance(coupon,dict) else {}
for k,v in {'codigo':'BEMVINDO10','aplicado':True,'mensagem':'Cupom aplicado: 10% de desconto nos produtos.'}.items():
    got=coupon.get(k);check('cupom.'+k,v,got,type(got) is type(v) and got==v)
outcome='Bloqueado' if r.returncode else ('Aprovado' if all(c['resultado']=='Aprovado' for c in checks) else 'Falhou')
meta={'inicio':start.isoformat(timespec='seconds'),'fim':end.isoformat(timespec='seconds'),'timezone':'America/Fortaleza','ambiente':'https://verzel-store.qa-test-verzel-store.workers.dev','comando':cmd,'curl_exit_code':r.returncode,'json_parse_error':parse_error,'resultado':outcome,'verificacoes':checks}
(root/'validacao-api.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'evidencias':str(root),'inicio':meta['inicio'],'fim':meta['fim'],'resultado':outcome,'verificacoes':len(checks),'falhas':[c for c in checks if c['resultado']!='Aprovado'],'resposta':data},ensure_ascii=False,indent=2))
sys.exit(0 if outcome=='Aprovado' else 1)
