from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal
import subprocess,json,shlex,shutil,sys

TZ=ZoneInfo('America/Fortaleza');start=datetime.now(TZ)
root=Path('reports/evidencias/pedido-cupom-normalizacao')/start.strftime('%Y%m%d-%H%M%S');root.mkdir(parents=True)
Path('/tmp/verzel-pedido-cupom-normalizacao-run.txt').write_text(str(root.resolve()));shutil.copyfile(__file__,root/'teste-api.py')
body='{"cliente":{"nome":"Maria Silva","email":"maria@exemplo.com","cep":"01310100"},"itens":[{"produtoId":"P005","quantidade":1}],"cupom":"  bemvindo10  "}'
coupon=json.loads(body)['cupom'];assert coupon=='  bemvindo10  ' and len(coupon)==14
(root/'corpo-enviado.json').write_text(body)
input_evidence={'cupomLiteral':coupon,'comprimento':len(coupon),'espacosNoInicio':len(coupon)-len(coupon.lstrip(' ')),'espacosNoFim':len(coupon)-len(coupon.rstrip(' ')),'codigosDosCaracteres':[ord(x) for x in coupon],'observacao':'Enviado com --data-binary, sem remover espaços ou alterar letras localmente'}
(root/'cupom-enviado.json').write_text(json.dumps(input_evidence,ensure_ascii=False,indent=2)+'\n')
cmd=['curl','-i','-X','POST','https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos','-H','Content-Type: application/json','--data-binary',body,'--max-time','30','--silent','--show-error','--write-out','\nCURL_HTTP_STATUS:%{http_code}\n']
(root/'comando.txt').write_text(shlex.join(cmd)+'\n');r=subprocess.run(cmd,capture_output=True);end=datetime.now(TZ)
(root/'resposta-http.txt').write_bytes(r.stdout);(root/'curl-stderr.txt').write_bytes(r.stderr)
response,sep,status=r.stdout.decode(errors='replace').rpartition('\nCURL_HTTP_STATUS:');raw=response.replace('\r\n','\n').rsplit('\n\n',1)[-1].strip() if sep else ''
(root/'corpo-recebido.json').write_text(raw+'\n');parse_error=None
try:data=json.loads(raw);exact=json.loads(raw,parse_float=Decimal,parse_int=Decimal)
except ValueError as e:data={};exact={};parse_error=str(e)
checks=[]
def check(label,want,found,ok):checks.append({'verificacao':label,'esperado':want,'encontrado':found,'resultado':'Aprovado' if ok else ('Bloqueado' if r.returncode else 'Falhou')})
check('Cupom enviado com espaços reais e letras minúsculas','  bemvindo10  ',coupon,coupon=='  bemvindo10  ' and input_evidence['espacosNoInicio']==2 and input_evidence['espacosNoFim']==2)
check('Status final da aplicação',201,status.strip(),r.returncode==0 and status.strip()=='201')
check('Corpo JSON válido e objeto','Objeto JSON',type(data).__name__,parse_error is None and type(data) is dict)
if not isinstance(data,dict):data={};exact={}
applied=data.get('cupom');applied=applied if isinstance(applied,dict) else {}
check('cupom.codigo','BEMVINDO10',applied.get('codigo'),type(applied.get('codigo')) is str and applied.get('codigo')=='BEMVINDO10')
check('cupom.aplicado',True,applied.get('aplicado'),applied.get('aplicado') is True)
for key,want in {'total':109.9,'subtotal':100,'desconto':10,'frete':19.9}.items():check(key,want,data.get(key),type(data.get(key)) in (int,float) and exact.get(key)==Decimal(str(want)))
items=data.get('itens');check('Uma unidade de P005',{'produtoId':'P005','quantidade':1},items,isinstance(items,list) and len(items)==1 and isinstance(items[0],dict) and items[0].get('produtoId')=='P005' and type(items[0].get('quantidade')) is int and items[0]['quantidade']==1)
outcome='Bloqueado' if r.returncode else 'Aprovado' if all(c['resultado']=='Aprovado' for c in checks) else 'Falhou'
meta={'inicio':start.isoformat(timespec='seconds'),'fim':end.isoformat(timespec='seconds'),'timezone':'America/Fortaleza','comando':cmd,'curl_exit_code':r.returncode,'json_parse_error':parse_error,'resultado':outcome,'verificacoes':checks}
(root/'validacao-api.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'evidencias':str(root),'inicio':meta['inicio'],'fim':meta['fim'],'resultado':outcome,'resposta':data,'falhas':[c for c in checks if c['resultado']!='Aprovado']},ensure_ascii=False,indent=2))
sys.exit(0 if outcome=='Aprovado' else 1)
