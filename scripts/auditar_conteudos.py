"""Audita cobertura temática e rastreabilidade; não valida eficácia pedagógica."""
from pathlib import Path
import json
import sys
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
def audit(root=ROOT):
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    skills=read(root/'data/habilidades.json');expected={h['id'] for h in skills}
    titles={i['id']:i['titulo'] for name in ['indices-disciplinas','indices-cursos'] for idx in read(root/'data'/f'{name}.json') for i in idx['itens']}
    byid={h['id']:h for h in skills};lessons=[l for p in sorted((root/'data').glob('conteudos-*.json')) for l in read(p)]
    counts=Counter(l['id'] for l in lessons);present=set(counts)
    errors=[]
    if present!=expected:errors.append({'ausentes':sorted(expected-present),'alheios':sorted(present-expected)})
    if any(c!=1 for c in counts.values()):errors.append({'duplicados':[id for id,c in counts.items() if c!=1]})
    for l in lessons:
        id=l['id']
        if id not in byid:continue
        if l['titulo']!=titles[byid[id]['item']]:errors.append(f'{id}: título diferente do índice')
        if l.get('estado_editorial')!='PROPOSTA_AUTORAL' or l.get('validacao_pedagogica')!='NÃO VERIFICADO':errors.append(f'{id}: estado editorial/pedagógico indevido')
        for key in ['conceito','exemplo','visual','questoes','pratica','projeto','fontes']:
            if not l.get(key):errors.append(f'{id}: falta {key}')
        if l.get('pratica',{}).get('tipo')=='numerica' and len({json.dumps(c['esperado']) for c in l['pratica']['casos']})<2:errors.append(f'{id}: prática aceita constante')
    # Exact copies of full concept/example/question sets would be generic substitutions.
    for field in ['conceito','exemplo','questoes']:
        signatures={}
        for l in lessons:
            sig=json.dumps(l.get(field),sort_keys=True,ensure_ascii=False)
            signatures.setdefault(sig,[]).append(l['id'])
        for ids in signatures.values():
            if len(ids)>1:errors.append({f'{field}_identico':ids})
    report={'status':'ATENDIDO' if not errors else 'NÃO ATENDIDO','unidades_esperadas':len(expected),'unidades_com_conteudo':len(expected&present),'cobertura_percentual':round(100*len(expected&present)/len(expected),2),'questoes':sum(len(l.get('questoes',[])) for l in lessons),'praticas':dict(Counter(l.get('pratica',{}).get('tipo','ausente') for l in lessons)),'erros':errors,'validacao_pedagogica':'NÃO VERIFICADO','escopo':'cobertura editorial e vínculos; fontes, correção científica e eficácia requerem revisão própria'}
    return report
if __name__=='__main__':
    result=audit();print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(bool(result['erros']))
