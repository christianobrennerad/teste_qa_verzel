from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal
import subprocess,json,shlex,shutil,sys

TZ=ZoneInfo('America/Fortaleza');BASE='https://verzel-store.qa-test-verzel-store.workers.dev'
start=datetime.now(TZ);root=Path('reports/evidencias/pedidos-repetidos-sem-estoque')/start.strftime('%Y%m%d-%H%M%S');root.mkdir(parents=True)
Path('/tmp/verzel-pedidos-repetidos-run.txt').write_text(str(root.resolve()));shutil.copyfile(__file__,root/'teste-api.py')
body='{"cliente":{"nome":"Cliente Teste","email":"qa@example.com","cep":"01310-100"},"itens":[{"produtoId":"P005","quantidade":5}]}'
calls=[('01-catalogo-antes','GET','/api/produtos',None,200),('02-primeiro-pedido','POST','/api/pedidos',body,201),('03-segundo-pedido','POST','/api/pedidos',body,201),('04-catalogo-depois','GET','/api/produtos',None,200)]
results=[]
for order,(slug,method,endpoint,payload,wanted_status) in enumerate(calls,1):
    folder=root/slug;folder.mkdir();cmd=['curl','-i','-X',method,BASE+endpoint,'-H','Content-Type: application/json']
    if payload is not None:
        (folder/'corpo-enviado.json').write_text(payload);cmd.extend(['--data-binary',payload])
    cmd.extend(['--max-time','30','--silent','--show-error','--write-out','\nCURL_HTTP_STATUS:%{http_code}\n'])
    (folder/'comando.txt').write_text(shlex.join(cmd)+'\n');stamp=datetime.now(TZ).isoformat(timespec='seconds');r=subprocess.run(cmd,capture_output=True)
    (folder/'resposta-http.txt').write_bytes(r.stdout);(folder/'curl-stderr.txt').write_bytes(r.stderr)
    response,sep,status=r.stdout.decode(errors='replace').rpartition('\nCURL_HTTP_STATUS:')
    raw=response.replace('\r\n','\n').rsplit('\n\n',1)[-1].strip() if sep else '';(folder/'corpo-recebido.json').write_text(raw+'\n');parse_error=None
    try:data=json.loads(raw);exact=json.loads(raw,parse_float=Decimal,parse_int=Decimal)
    except ValueError as e:data=None;exact=None;parse_error=str(e)
    checks=[]
    def check(label,want,found,ok):checks.append({'verificacao':label,'esperado':want,'encontrado':found,'resultado':'Aprovado' if ok else ('Bloqueado' if r.returncode else 'Falhou')})
    check('Status final da aplicação',wanted_status,status.strip(),r.returncode==0 and status.strip()==str(wanted_status))
    if method=='POST':
        check('Resposta JSON válida e objeto','Objeto JSON',type(data).__name__,parse_error is None and type(data) is dict)
        data=data if isinstance(data,dict) else {};exact=exact if isinstance(exact,dict) else {}
        for k in ['subtotal','total']:check(k,500,data.get(k),type(data.get(k)) in (int,float) and exact.get(k)==Decimal('500'))
        items=data.get('itens');check('Pedido contém cinco unidades de P005',{'produtoId':'P005','quantidade':5},items,isinstance(items,list) and len(items)==1 and isinstance(items[0],dict) and items[0].get('produtoId')=='P005' and type(items[0].get('quantidade')) is int and items[0]['quantidade']==5)
    else:
        check('Resposta JSON válida e lista','Lista JSON',type(data).__name__,parse_error is None and isinstance(data,list))
        products=[p for p in (data if isinstance(data,list) else []) if isinstance(p,dict) and p.get('id')=='P005']
        check('P005 disponível no catálogo','Uma entrada de P005',len(products),len(products)==1)
        product=products[0] if len(products)==1 else {};exact_products=[p for p in (exact if isinstance(exact,list) else []) if isinstance(p,dict) and p.get('id')=='P005']
        price=exact_products[0].get('preco') if len(exact_products)==1 else None
        check('Preço de P005',100,product.get('preco'),type(product.get('preco')) in (int,float) and price==Decimal('100'))
    outcome='Bloqueado' if r.returncode else 'Aprovado' if all(c['resultado']=='Aprovado' for c in checks) else 'Falhou'
    meta={'ordem':order,'inicio':stamp,'fim':datetime.now(TZ).isoformat(timespec='seconds'),'metodo':method,'endpoint':endpoint,'comando':cmd,'curl_exit_code':r.returncode,'json_parse_error':parse_error,'resultado':outcome,'verificacoes':checks}
    (folder/'validacao-api.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');results.append(meta)
    print(json.dumps({'chamada':slug,'resultado':outcome,'resposta':data if method=='POST' else products,'falhas':[c for c in checks if c['resultado']!='Aprovado']},ensure_ascii=False),flush=True)
overall='Falhou' if any(r['resultado']=='Falhou' for r in results) else 'Bloqueado' if any(r['resultado']=='Bloqueado' for r in results) else 'Aprovado'
summary={'inicio':start.isoformat(timespec='seconds'),'fim':datetime.now(TZ).isoformat(timespec='seconds'),'timezone':'America/Fortaleza','resultado':overall,'cliente':'Dados fictícios: Cliente Teste, qa@example.com; CEP de exemplo da documentação','sequencia':'Catálogo antes; duas confirmações independentes e idênticas; catálogo depois','verificacoes':results}
(root/'resumo-validacao.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'evidencias':str(root),'resultado':overall,'inicio':summary['inicio'],'fim':summary['fim']},ensure_ascii=False))
sys.exit(0 if overall=='Aprovado' else 1)
