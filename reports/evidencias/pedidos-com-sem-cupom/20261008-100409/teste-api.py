from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal
import subprocess,json,re,shlex,shutil,sys

TZ=ZoneInfo('America/Fortaleza');start=datetime.now(TZ)
root=Path('reports/evidencias/pedidos-com-sem-cupom')/start.strftime('%Y%m%d-%H%M%S');root.mkdir(parents=True)
Path('/tmp/verzel-pedidos-com-sem-cupom-run.txt').write_text(str(root.resolve()));shutil.copyfile(__file__,root/'teste-api.py')
cases=[{'slug':'01-sem-cupom','cupom':None,'desconto':0,'total':119.9},{'slug':'02-com-bemvindo10','cupom':'BEMVINDO10','desconto':10,'total':109.9}]
(root/'casos.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n');results=[]
for c in cases:
    folder=root/c['slug'];folder.mkdir()
    request={'cliente':{'nome':'Maria Silva','email':'maria@exemplo.com','cep':'01310-100'},'itens':[{'produtoId':'P005','quantidade':1}]}
    if c['cupom']:request['cupom']=c['cupom']
    body=json.dumps(request,ensure_ascii=False,separators=(',',':'));(folder/'corpo-enviado.json').write_text(body)
    cmd=['curl','-i','-X','POST','https://verzel-store.qa-test-verzel-store.workers.dev/api/pedidos','-H','Content-Type: application/json','--data-binary',body,'--max-time','30','--silent','--show-error','--write-out','\nCURL_HTTP_STATUS:%{http_code}\n']
    (folder/'comando.txt').write_text(shlex.join(cmd)+'\n');stamp=datetime.now(TZ).isoformat(timespec='seconds');r=subprocess.run(cmd,capture_output=True)
    (folder/'resposta-http.txt').write_bytes(r.stdout);(folder/'curl-stderr.txt').write_bytes(r.stderr)
    response,sep,status=r.stdout.decode(errors='replace').rpartition('\nCURL_HTTP_STATUS:')
    raw=response.replace('\r\n','\n').rsplit('\n\n',1)[-1].strip() if sep else '';(folder/'corpo-recebido.json').write_text(raw+'\n');parse_error=None
    try:data=json.loads(raw);exact=json.loads(raw,parse_float=Decimal,parse_int=Decimal)
    except ValueError as e:data={};exact={};parse_error=str(e)
    checks=[]
    def check(label,want,found,ok):checks.append({'verificacao':label,'esperado':want,'encontrado':found,'resultado':'Aprovado' if ok else ('Bloqueado' if r.returncode else 'Falhou')})
    check('Status final da aplicação',201,status.strip(),r.returncode==0 and status.strip()=='201')
    check('Corpo JSON válido e objeto','Objeto JSON',type(data).__name__,parse_error is None and type(data) is dict)
    if not isinstance(data,dict):data={};exact={}
    number=data.get('numero');check('numero','^VZ-[0-9]{6}$',number,isinstance(number,str) and re.fullmatch(r'VZ-[0-9]{6}',number) is not None)
    created=data.get('criadoEm');iso=False
    if isinstance(created,str) and re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:?[0-9]{2})?',created):
        try:datetime.fromisoformat(created.replace('Z','+00:00'));iso=True
        except ValueError:pass
    check('criadoEm','Data e hora ISO 8601 válidas',created,iso)
    customer=data.get('cliente');customer=customer if isinstance(customer,dict) else {}
    for key,want in {'nome':'Maria Silva','email':'maria@exemplo.com','cep':'01310100'}.items():check('cliente.'+key,want,customer.get(key),type(customer.get(key)) is str and customer.get(key)==want)
    for key,want in {'subtotal':100,'desconto':c['desconto'],'frete':19.9,'valorFaltanteFreteGratis':100,'total':c['total']}.items():
        found=data.get(key);check(key,want,found,type(found) in (int,float) and exact.get(key)==Decimal(str(want)))
    check('freteGratis',False,data.get('freteGratis'),data.get('freteGratis') is False)
    items=data.get('itens');check('Uma unidade de P005',{'produtoId':'P005','quantidade':1},items,isinstance(items,list) and len(items)==1 and isinstance(items[0],dict) and items[0].get('produtoId')=='P005' and type(items[0].get('quantidade')) is int and items[0]['quantidade']==1)
    coupon=data.get('cupom');wanted='BEMVINDO10 aplicado' if c['cupom'] else None
    check('Cupom correspondente ao exemplo',wanted,coupon,(isinstance(coupon,dict) and coupon.get('codigo')==c['cupom'] and coupon.get('aplicado') is True) if c['cupom'] else coupon is None)
    outcome='Bloqueado' if r.returncode else 'Aprovado' if all(x['resultado']=='Aprovado' for x in checks) else 'Falhou'
    meta={'caso':c['slug'],'inicio':stamp,'fim':datetime.now(TZ).isoformat(timespec='seconds'),'comando':cmd,'curl_exit_code':r.returncode,'json_parse_error':parse_error,'resultado':outcome,'verificacoes':checks}
    (folder/'validacao-api.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');results.append(meta)
    print(json.dumps({'caso':c['slug'],'resultado':outcome,'resposta':data,'falhas':[x for x in checks if x['resultado']!='Aprovado']},ensure_ascii=False),flush=True)
outcome='Falhou' if any(x['resultado']=='Falhou' for x in results) else 'Bloqueado' if any(x['resultado']=='Bloqueado' for x in results) else 'Aprovado'
summary={'inicio':start.isoformat(timespec='seconds'),'fim':datetime.now(TZ).isoformat(timespec='seconds'),'timezone':'America/Fortaleza','resultado':outcome,'dadosCliente':'Dados de exemplo fornecidos pelo usuário e presentes na documentação','casos':results}
(root/'resumo-validacao.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'evidencias':str(root),'resultado':outcome,'inicio':summary['inicio'],'fim':summary['fim']},ensure_ascii=False))
sys.exit(0 if outcome=='Aprovado' else 1)
