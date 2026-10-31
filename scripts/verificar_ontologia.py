"""Executa o Open Ontologies em armazenamento temporário, com casos positivos e negativos."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from datetime import datetime, timezone, timedelta

ROOT=Path(__file__).resolve().parents[1]


def run(binary, commands, store):
    p=subprocess.run([str(binary),'--no-connect','--data-dir',str(store),'batch','-'],
        input=json.dumps(commands),text=True,encoding='utf-8',capture_output=True,timeout=90)
    rows=[json.loads(line) for line in p.stdout.splitlines() if line.strip()]
    if len(rows)!=len(commands) or any('error' in r or 'error' in r.get('result',{}) for r in rows):
        raise RuntimeError('Comando nativo falhou: '+p.stdout[:2000]+p.stderr[:500])
    return [r['result'] for r in rows]


def verify(binary, checker=None):
    lock=json.loads((ROOT/'ferramentas/open-ontologies.json').read_text(encoding='utf-8'))
    if hashlib.sha256(binary.read_bytes()).hexdigest()!=lock['linux_x86_64_sha256']:
        raise ValueError('SHA256 do motor não corresponde ao binário fixado')
    def command(name,args=None):
        c={'command':name}
        if args is not None:c['args']=args
        return c
    manifest=json.loads((ROOT/'ontologia/manifesto.json').read_text(encoding='utf-8'))
    text=(ROOT/'ontologia/curriculo.ttl').read_text(encoding='utf-8')
    shapes=str(ROOT/'ontologia/formas.ttl')
    queries={p.stem:p.read_text(encoding='utf-8') for p in sorted((ROOT/'ontologia/consultas').glob('*.rq'))}
    with tempfile.TemporaryDirectory(prefix='computacao-ontologia-') as tmp:
        temp=Path(tmp);certificate=temp/'certificado'
        cmds=[command('load',str(ROOT/'ontologia/curriculo.ttl')),command('status'),command('stats'),command('lint',str(ROOT/'ontologia/esquema.ttl')),command('shacl',shapes)]
        names=list(queries)
        cmds += [command('query',queries[n]) for n in names]
        cmds += [command('reason',['--profile','rdfs','--certificate',str(certificate)])]
        out=run(binary,cmds,temp/'principal')
        if out[1]['version']!=lock['versao']:raise ValueError('Versão nativa inesperada')
        if out[2]['individuals']!=manifest['individuos'] or out[4].get('conforms') is not True:raise ValueError('Contagem ou SHACL inválidos')
        results=dict(zip(names,out[5:5+len(names)]))
        counts={r['tipo'].split(':')[-1].rstrip('>'):int(re.search(r'"(\d+)"',r['total']).group(1)) for r in results['contagem']['results']}
        if counts!=manifest['por_classe']:raise ValueError('SPARQL diverge dos JSON de origem')
        expected={'<urn:computacao-aberta:recurso:U-PRG01-0'+str(i)+'>' for i in (1,2,3)}
        if {r['anterior'] for r in results['pre-requisitos']['results']}!=expected:raise ValueError('Fecho transitivo inesperado')
        if len(results['missoes']['results'])!=4:raise ValueError('Missões ausentes')
        if out[3].get('issue_count',0) or out[3].get('issues',[]):raise ValueError('Lint com ocorrências: '+json.dumps(out[3]))
        # Alvo ausente: a forma precisa rejeitar o pré-requisito inválido.
        bad=temp/'invalido.ttl';bad.write_text(text+'\nid:U-PRG01-02 ca:preRequisitoUnidade id:INEXISTENTE .\n',encoding='utf-8')
        negative=run(binary,[command('load',str(bad)),command('shacl',shapes)],temp/'negativo')[-1]
        if negative.get('conforms') is not False or negative.get('violation_count',0)<1:raise ValueError('SHACL não detectou alvo inexistente')
        cycle=temp/'ciclo-invalido.ttl';cycle.write_text(text+'\nid:U-PRG01-01 ca:preRequisitoUnidade id:U-PRG01-04 .\n',encoding='utf-8')
        cyclic=run(binary,[command('load',str(cycle)),command('shacl',shapes)],temp/'ciclo-negativo')[-1]
        if cyclic.get('conforms') is not False:raise ValueError('SHACL não detectou ciclo')
        # Mudança DESEJADA completa para demonstrar remoção, em sandbox descartável.
        proposed=temp/'proposto.ttl';proposed.write_text('\n'.join(line for line in text.splitlines() if not line.startswith('id:U-PRG01-01 '))+'\n',encoding='utf-8')
        lifecycle=run(binary,[command('load',str(ROOT/'ontologia/curriculo.ttl')),command('version','antes'),command('plan',str(proposed)),command('apply',['safe']),command('shacl',shapes),command('rollback','antes'),command('shacl',shapes)],temp/'ciclo')
        if lifecycle[2].get('risk_score') not in ('medium','high'):raise ValueError('Plano não sinalizou risco da remoção')
        if lifecycle[4].get('conforms') is not False or lifecycle[6].get('conforms') is not True:raise ValueError('Remoção/rollback não tiveram efeito esperado')
        formal={'status':'NÃO VERIFICADO','motivo':'Checker não fornecido; certificado gerado não equivale a certificado aceito.'}
        if checker:
            if hashlib.sha256(checker.read_bytes()).hexdigest()!=lock['checker_sha256']:raise ValueError('SHA256 do checker inesperado')
            p=subprocess.run([str(checker),str(certificate/'asserted.tsv'),str(certificate/'derivations.tsv')],capture_output=True,text=True,encoding='utf-8',timeout=30)
            try:answer=json.loads(p.stdout)
            except ValueError:answer=None
            formal=dict(status='CONFIRMADO' if p.returncode==0 and answer and answer.get('ok') is True else 'NÃO VERIFICADO',exit_code=p.returncode,resposta=answer,stderr=p.stderr.strip()[:500])
        if out[-1].get('fixpoint_reached') is not True:raise ValueError('Inferência não alcançou ponto fixo')
        cert=out[-1]['certificate']
        report=dict(data=datetime.now(timezone(timedelta(hours=-3))).isoformat(),status_estrutural='ATENDIDO',motor=lock['versao'],binario_sha256=lock['linux_x86_64_sha256'],
            asserted_triples=out[2]['triples'],individuos=out[2]['individuals'],por_classe=counts,shacl={'conforms':True,'violacoes':out[4]['violation_count']},lint=out[3],
            consultas={n:{'linhas':len(v['results'])} for n,v in results.items()},caso_negativo={'conforms':False,'violacoes':negative['violation_count']},ciclo_negativo={'conforms':False,'violacoes':cyclic['violation_count']},
            ciclo={'risk_score':lifecycle[2]['risk_score'],'blast_radius':lifecycle[2].get('blast_radius'),'conservativity':lifecycle[2].get('conservativity'), 'logic':lifecycle[2].get('logic'),'apos_remocao_conforms':False,'apos_rollback_conforms':True,'escopo':'Somente armazenamento temporário; JSON e TTL do repositório não alterados.'},
            inferencia={'perfil':'rdfs','inferidas':out[-1]['inferred_count'],'fixpoint':out[-1]['fixpoint_reached'],'certificado_asserted':cert['asserted'],'certificado_derivations':cert['derivations'],'checker':formal},
            fontes_sha256=manifest['fontes_sha256'],ttl_sha256=hashlib.sha256((ROOT/'ontologia/curriculo.ttl').read_bytes()).hexdigest(),
            limites=['Validação estrutural não confirma verdade das premissas editoriais ou aprendizagem.','Sem chamadas pagas, credenciais, LLM ou publicação em endpoint externo.','Avaliação científica e aprovação humana NÃO VERIFICADAS.'])
        # Caminhos da sandbox são efêmeros; a informação de escopo permanece.
        return json.loads(json.dumps(report,ensure_ascii=False).replace(str(temp),'<temporario>'))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--bin',required=True,type=Path);p.add_argument('--checker',type=Path);p.add_argument('--saida',type=Path);a=p.parse_args()
    report=verify(a.bin.resolve(),a.checker.resolve() if a.checker else None)
    text=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
    if a.saida:a.saida.parent.mkdir(parents=True,exist_ok=True);a.saida.write_text(text,encoding='utf-8')
    print(text,end='')
