from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal
import subprocess,json,shlex,shutil,re,sys

TZ=ZoneInfo('America/Fortaleza');start=datetime.now(TZ)
root=Path('reports/evidencias/api-isolamento-chamadas')/start.strftime('%Y%m%d-%H%M%S');root.mkdir(parents=True)
Path('/tmp/verzel-isolamento-api-run.txt').write_text(str(root.resolve()));shutil.copyfile(__file__,root/'teste-api.py')
cases=[{'slug':'01-p005-com-cupom','corpo':'{"itens":[{"produtoId":"P005","quantidade":2}],"cupom":"BEMVINDO10"}','esperado':{'total':180},'produto':'P005','quantidade':2},{'slug':'02-p008-sem-cupom','corpo':'{"itens":[{"produtoId":"P008","quantidade":1}]}','esperado':{'subtotal':50,'desconto':0,'frete':19.9,'total':69.9},'produto':'P008','quantidade':1}]
cmd=['curl'];URL='https://verzel-store.qa-test-verzel-store.workers.dev/api/carrinho/calcular'
for idx,c in enumerate(cases,1):
    folder=root/c['slug'];folder.mkdir();(folder/'corpo-enviado.json').write_text(c['corpo'])
    if idx>1:cmd.append('--next')
    cmd.extend(['-i','-X','POST',URL,'-H','Content-Type: application/json','--data-binary',c['corpo'],'--max-time','30','--silent','--show-error','--output',str((folder/'resposta-http.txt').resolve()),'--write-out',f'REQUISICAO_{idx}_STATUS:%{{http_code}};EXIT:%{{exitcode}}\n'])
(root/'comando.txt').write_text(shlex.join(cmd)+'\n')
(root/'casos.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
r=subprocess.run(cmd,capture_output=True);end=datetime.now(TZ)
(root/'curl-stdout.txt').write_bytes(r.stdout);(root/'curl-stderr.txt').write_bytes(r.stderr)
markers={int(i):(status,int(code)) for i,status,code in re.findall(r'REQUISICAO_(\d+)_STATUS:(\d+);EXIT:(\d+)',r.stdout.decode(errors='replace'))};results=[]
for idx,c in enumerate(cases,1):
    folder=root/c['slug'];status,exitcode=markers.get(idx,('000',-1))
    http=(folder/'resposta-http.txt').read_text(errors='replace') if (folder/'resposta-http.txt').exists() else ''
    raw=http.replace('\r\n','\n').rsplit('\n\n',1)[-1].strip();(folder/'corpo-recebido.json').write_text(raw+'\n')
    parse_error=None
    try:data=json.loads(raw);exact=json.loads(raw,parse_float=Decimal,parse_int=Decimal)
    except ValueError as e:data={};exact={};parse_error=str(e)
    checks=[]
    def check(label,want,found,ok):checks.append({'verificacao':label,'esperado':want,'encontrado':found,'resultado':'Aprovado' if ok else ('Bloqueado' if exitcode!=0 else 'Falhou')})
    check('Status final da aplicação',200,status,exitcode==0 and status=='200')
    check('Corpo JSON válido e objeto','Objeto JSON',type(data).__name__,parse_error is None and type(data) is dict)
    if not isinstance(data,dict):data={};exact={}
    for k,v in c['esperado'].items():check(k,v,data.get(k),type(data.get(k)) in (int,float) and exact.get(k)==Decimal(str(v)))
    items=data.get('itens');check('Apenas o produto e a quantidade enviados',{'produtoId':c['produto'],'quantidade':c['quantidade']},items,isinstance(items,list) and len(items)==1 and isinstance(items[0],dict) and items[0].get('produtoId')==c['produto'] and type(items[0].get('quantidade')) is int and items[0]['quantidade']==c['quantidade'])
    coupon=data.get('cupom')
    if idx==1:check('Cupom da primeira chamada aplicado','BEMVINDO10 aplicado',coupon,isinstance(coupon,dict) and coupon.get('codigo')=='BEMVINDO10' and coupon.get('aplicado') is True)
    else:check('Nenhum cupom herdado da primeira chamada',None,coupon,coupon is None)
    meta={'ordem':idx,'inicioDaSequencia':start.isoformat(timespec='seconds'),'fimDaSequencia':end.isoformat(timespec='seconds'),'statusAplicacao':status,'curl_exit_code':exitcode,'json_parse_error':parse_error,'resultado':'Bloqueado' if exitcode!=0 else ('Aprovado' if all(x['resultado']=='Aprovado' for x in checks) else 'Falhou'),'verificacoes':checks}
    (folder/'validacao-api.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');results.append(meta)
    print(json.dumps({'chamada':idx,'resultado':meta['resultado'],'resposta':data,'falhas':[x for x in checks if x['resultado']!='Aprovado']},ensure_ascii=False),flush=True)
outcome='Falhou' if any(x['resultado']=='Falhou' for x in results) else 'Bloqueado' if any(x['resultado']=='Bloqueado' for x in results) else 'Aprovado'
summary={'inicio':start.isoformat(timespec='seconds'),'fim':end.isoformat(timespec='seconds'),'timezone':'America/Fortaleza','metodo':'Uma execução do curl; duas requisições sequenciais, separadas por --next; sem paralelismo','comando':cmd,'curl_exit_code':r.returncode,'resultado':outcome,'chamadas':results}
(root/'resumo-validacao.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'evidencias':str(root),'inicio':summary['inicio'],'fim':summary['fim'],'resultado':outcome},ensure_ascii=False))
sys.exit(0 if outcome=='Aprovado' else 1)
