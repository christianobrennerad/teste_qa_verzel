from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal
import subprocess,json
cases=[{'slug':'01-p003','itens':[{'produtoId':'P003','quantidade':1}],'esperado':{'subtotal':189.9,'desconto':0,'frete':19.9,'freteGratis':False,'valorFaltanteFreteGratis':10.1,'total':209.8}}]
root=Path('reports/evidencias/frete-valor-faltante')/datetime.now(ZoneInfo('America/Fortaleza')).strftime('%Y%m%d-%H%M%S');root.mkdir(parents=True)
Path('/tmp/verzel-frete-valor-faltante-run.txt').write_text(str(root.resolve()));(root/'casos.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
results=[]
for case in cases:
 folder=root/case['slug']/'api';folder.mkdir(parents=True);body=json.dumps({'itens':case['itens']},separators=(',',':'));(folder/'corpo-enviado.json').write_text(body)
 cmd=['curl','-i','-X','POST','https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular','-H','Content-Type: application/json','--data-binary',body,'--max-time','30','--silent','--show-error','--write-out','\nCURL_HTTP_STATUS:%{http_code}\n']
 start=datetime.now(ZoneInfo('America/Fortaleza')).isoformat(timespec='seconds');r=subprocess.run(cmd,capture_output=True)
 (folder/'resposta-http.txt').write_bytes(r.stdout);(folder/'curl-stderr.txt').write_bytes(r.stderr)
 response,sep,status=r.stdout.decode(errors='replace').rpartition('\nCURL_HTTP_STATUS:');raw=response.replace('\r\n','\n').rsplit('\n\n',1)[-1].strip() if sep else '';(folder/'corpo.json').write_text(raw+'\n')
 try:data=json.loads(raw);exact=json.loads(raw,parse_float=Decimal,parse_int=Decimal)
 except ValueError:data={};exact={}
 checks=[]
 def add(name,expected,found,ok):checks.append({'verificacao':name,'esperado':expected,'encontrado':found,'resultado':'Aprovado' if ok else ('Bloqueado' if r.returncode else 'Falhou')})
 add('Status da aplicação',200,status.strip(),r.returncode==0 and status.strip()=='200')
 for key,value in case['esperado'].items():
  found=data.get(key);add(key,value,found,type(found) is bool and found==value if type(value) is bool else type(found) in (int,float) and exact.get(key)==Decimal(str(value)))
 monetary={k:exact.get(k) for k in ['subtotal','desconto','frete','valorFaltanteFreteGratis','total']}
 for idx,item in enumerate(exact.get('itens',[])):
  for key in ['precoUnitario','total']:monetary[f'itens[{idx}].{key}']=item.get(key)
 precision=all(isinstance(v,Decimal) and v==v.quantize(Decimal('0.01')) for v in monetary.values())
 add('Precisão monetária','Até 2 casas decimais',{k:str(v) for k,v in monetary.items()},precision)
 outcome='Bloqueado' if r.returncode else ('Aprovado' if all(c['resultado']=='Aprovado' for c in checks) else 'Falhou')
 meta={'caso':case['slug'],'data':start,'comando':cmd,'curl_exit_code':r.returncode,'resultado':outcome,'verificacoes':checks};(folder/'validacao-api.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');results.append(meta)
 print(json.dumps({'caso':case['slug'],'resultado':outcome,'resumo':data},ensure_ascii=False))
(root/'resumo-api.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
