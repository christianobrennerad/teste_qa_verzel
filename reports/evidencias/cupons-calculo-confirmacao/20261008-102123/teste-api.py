from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal
import subprocess,json,shlex,shutil,sys

TZ=ZoneInfo('America/Fortaleza');start=datetime.now(TZ)
root=Path('reports/evidencias/cupons-calculo-confirmacao')/start.strftime('%Y%m%d-%H%M%S');root.mkdir(parents=True)
Path('/tmp/verzel-cupons-calculo-confirmacao-run.txt').write_text(str(root.resolve()));shutil.copyfile(__file__,root/'teste-api.py')
cases=[{'slug':'01-inexistente','cupom':'INEXISTENTE','mensagem':'Cupom inválido.','codigo':'CUPOM_INVALIDO'},{'slug':'02-expirado','cupom':'VERAO2026','mensagem':'Cupom expirado.','codigo':'CUPOM_EXPIRADO'}]
(root/'casos.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n');results=[]
for c in cases:
    case_result={'cupom':c['cupom'],'etapas':[]}
    for phase in ['calculo','confirmacao']:
        folder=root/c['slug']/phase;folder.mkdir(parents=True)
        request={'itens':[{'produtoId':'P005','quantidade':1}],'cupom':c['cupom']}
        if phase=='confirmacao':request={'cliente':{'nome':'Cliente Teste','email':'qa@example.com','cep':'01310-100'},**request}
        body=json.dumps(request,ensure_ascii=False,separators=(',',':'));(folder/'corpo-enviado.json').write_text(body)
        endpoint='/api/carrinho/calcular' if phase=='calculo' else '/api/pedidos';wanted_status=200 if phase=='calculo' else 422
        cmd=['curl','-i','-X','POST','https://verzel-store.qa-test-verzel-store.workers.dev'+endpoint,'-H','Content-Type: application/json','--data-binary',body,'--max-time','30','--silent','--show-error','--write-out','\nCURL_HTTP_STATUS:%{http_code}\n']
        (folder/'comando.txt').write_text(shlex.join(cmd)+'\n');stamp=datetime.now(TZ).isoformat(timespec='seconds');r=subprocess.run(cmd,capture_output=True)
        (folder/'resposta-http.txt').write_bytes(r.stdout);(folder/'curl-stderr.txt').write_bytes(r.stderr)
        response,sep,status=r.stdout.decode(errors='replace').rpartition('\nCURL_HTTP_STATUS:');raw=response.replace('\r\n','\n').rsplit('\n\n',1)[-1].strip() if sep else ''
        (folder/'corpo-recebido.json').write_text(raw+'\n');parse_error=None
        try:data=json.loads(raw);exact=json.loads(raw,parse_float=Decimal,parse_int=Decimal)
        except ValueError as e:data={};exact={};parse_error=str(e)
        checks=[]
        def check(label,want,found,ok):checks.append({'verificacao':label,'esperado':want,'encontrado':found,'resultado':'Aprovado' if ok else ('Bloqueado' if r.returncode else 'Falhou')})
        check('Status final da aplicação',wanted_status,status.strip(),r.returncode==0 and status.strip()==str(wanted_status))
        check('Corpo JSON válido e objeto','Objeto JSON',type(data).__name__,parse_error is None and type(data) is dict)
        if not isinstance(data,dict):data={};exact={}
        if phase=='calculo':
            coupon=data.get('cupom');coupon=coupon if isinstance(coupon,dict) else {}
            check('cupom.aplicado',False,coupon.get('aplicado'),coupon.get('aplicado') is False)
            check('cupom.mensagem',c['mensagem'],coupon.get('mensagem'),type(coupon.get('mensagem')) is str and coupon.get('mensagem')==c['mensagem'])
            for key,want in {'desconto':0,'total':119.9}.items():check(key,want,data.get(key),type(data.get(key)) in (int,float) and exact.get(key)==Decimal(str(want)))
            items=data.get('itens');check('Uma unidade de P005',{'produtoId':'P005','quantidade':1},items,isinstance(items,list) and len(items)==1 and isinstance(items[0],dict) and items[0].get('produtoId')=='P005' and type(items[0].get('quantidade')) is int and items[0]['quantidade']==1)
        else:
            error=data.get('erro');error=error if isinstance(error,dict) else {}
            check('erro.codigo',c['codigo'],error.get('codigo'),type(error.get('codigo')) is str and error.get('codigo')==c['codigo'])
            confirmation={key:data[key] for key in ['numero','criadoEm'] if key in data}
            check('Pedido não confirmado na resposta','Status 422, erro de cupom e ausência de número/data de confirmação',{'status':status.strip(),'erro':error,'camposConfirmacao':confirmation},status.strip()=='422' and error.get('codigo')==c['codigo'] and not confirmation)
        outcome='Bloqueado' if r.returncode else 'Aprovado' if all(x['resultado']=='Aprovado' for x in checks) else 'Falhou'
        meta={'cupom':c['cupom'],'etapa':phase,'inicio':stamp,'fim':datetime.now(TZ).isoformat(timespec='seconds'),'comando':cmd,'curl_exit_code':r.returncode,'json_parse_error':parse_error,'resultado':outcome,'verificacoes':checks}
        (folder/'validacao-api.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');case_result['etapas'].append(meta)
        print(json.dumps({'cupom':c['cupom'],'etapa':phase,'resultado':outcome,'resposta':data,'falhas':[x for x in checks if x['resultado']!='Aprovado']},ensure_ascii=False),flush=True)
    case_result['resultado']='Falhou' if any(x['resultado']=='Falhou' for x in case_result['etapas']) else 'Bloqueado' if any(x['resultado']=='Bloqueado' for x in case_result['etapas']) else 'Aprovado';results.append(case_result)
outcome='Falhou' if any(x['resultado']=='Falhou' for x in results) else 'Bloqueado' if any(x['resultado']=='Bloqueado' for x in results) else 'Aprovado'
summary={'inicio':start.isoformat(timespec='seconds'),'fim':datetime.now(TZ).isoformat(timespec='seconds'),'timezone':'America/Fortaleza','resultado':outcome,'cliente':'Dados fictícios: Cliente Teste, qa@example.com; CEP de exemplo da documentação','casos':results}
(root/'resumo-validacao.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'evidencias':str(root),'resultado':outcome,'inicio':summary['inicio'],'fim':summary['fim']},ensure_ascii=False))
sys.exit(0 if outcome=='Aprovado' else 1)
