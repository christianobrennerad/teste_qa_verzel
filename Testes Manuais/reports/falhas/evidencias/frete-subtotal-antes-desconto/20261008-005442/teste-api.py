from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal
import subprocess,json
cases=[
 {'slug':'01-subtotal-100-00','itens':[{'produtoId':'P005','quantidade':1}],'esperado':{'subtotal':100,'desconto':10,'frete':19.9,'freteGratis':False,'valorFaltanteFreteGratis':100,'total':109.9}},
 {'slug':'02-subtotal-199-80','itens':[{'produtoId':'P002','quantidade':1},{'produtoId':'P001','quantidade':1}],'esperado':{'subtotal':199.8,'desconto':19.98,'frete':19.9,'freteGratis':False,'valorFaltanteFreteGratis':0.2,'total':199.72}},
 {'slug':'03-subtotal-200-00','itens':[{'produtoId':'P005','quantidade':2}],'esperado':{'subtotal':200,'desconto':20,'frete':0,'freteGratis':True,'valorFaltanteFreteGratis':0,'total':180}},
 {'slug':'04-subtotal-239-70','itens':[{'produtoId':'P002','quantidade':1},{'produtoId':'P004','quantidade':2}],'esperado':{'subtotal':239.7,'desconto':23.97,'frete':0,'freteGratis':True,'valorFaltanteFreteGratis':0,'total':215.73}},
 {'slug':'05-subtotal-179-70','itens':[{'produtoId':'P001','quantidade':3}],'esperado':{'subtotal':179.7,'desconto':17.97,'frete':19.9,'freteGratis':False,'valorFaltanteFreteGratis':20.3,'total':181.63}}
]
root=Path('reports/evidencias/frete-subtotal-antes-desconto')/datetime.now(ZoneInfo('America/Fortaleza')).strftime('%Y%m%d-%H%M%S');root.mkdir(parents=True)
Path('/tmp/verzel-frete-desconto-run.txt').write_text(str(root.resolve()));(root/'casos.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
results=[]
for case in cases:
 folder=root/case['slug']/'api';folder.mkdir(parents=True);body=json.dumps({'itens':case['itens'],'cupom':'BEMVINDO10'},separators=(',',':'));(folder/'corpo-enviado.json').write_text(body)
 cmd=['curl','-i','-X','POST','https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular','-H','Content-Type: application/json','--data-binary',body,'--max-time','30','--silent','--show-error','--write-out','\nCURL_HTTP_STATUS:%{http_code}\n']
 start=datetime.now(ZoneInfo('America/Fortaleza')).isoformat(timespec='seconds');r=subprocess.run(cmd,capture_output=True)
 (folder/'resposta-http.txt').write_bytes(r.stdout);(folder/'curl-stderr.txt').write_bytes(r.stderr)
 response,sep,status=r.stdout.decode(errors='replace').rpartition('\nCURL_HTTP_STATUS:');raw=response.replace('\r\n','\n').rsplit('\n\n',1)[-1].strip() if sep else '';(folder/'corpo.json').write_text(raw+'\n')
 try:data=json.loads(raw);exact=json.loads(raw,parse_float=Decimal,parse_int=Decimal)
 except ValueError:data={};exact={}
 checks=[]
 def add(name,expected,found,ok):checks.append({'verificacao':name,'esperado':expected,'encontrado':found,'resultado':'Aprovado' if ok else ('Bloqueado' if r.returncode else 'Falhou')})
 add('Status da aplicação',200,status.strip(),r.returncode==0 and status.strip()=='200')
 add('Cupom válido aplicado','BEMVINDO10 aplicado',data.get('cupom'),data.get('cupom',{}).get('codigo')=='BEMVINDO10' and data.get('cupom',{}).get('aplicado') is True)
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
