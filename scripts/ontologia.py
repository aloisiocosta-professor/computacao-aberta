"""Exporta os dados editoriais em RDF; não infere proficiência nem suporte científico."""
from pathlib import Path
import hashlib
import json
import argparse

ROOT = Path(__file__).resolve().parents[1]
PREFIXES = '''@prefix ca: <urn:computacao-aberta:ontologia:> .
@prefix id: <urn:computacao-aberta:recurso:> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
'''
SOURCES = ('eixos', 'disciplinas', 'habilidades', 'referencias', 'cursos', 'missoes',
           'relacoes-fontes', 'funcoes-fontes')


def literal(value):
    return json.dumps(str(value), ensure_ascii=False)


def export(root=ROOT):
    meta = json.loads((root / 'data/ontologia.json').read_text(encoding='utf-8'))
    data = {s: json.loads((root / 'data' / (s+'.json')).read_text(encoding='utf-8')) for s in SOURCES}
    schema = [PREFIXES, 'ca: a owl:Ontology ; rdfs:label "Ontologia editorial Computação Aberta"@pt ; owl:versionInfo "0.1.0-proposta" .']
    for c in meta['classes']:
        text = f"ca:{c['id']} a owl:Class ; rdfs:label {literal(c['nome'])}@pt ; rdfs:comment {literal(c['descricao'])}@pt"
        if c.get('superclasse'): text += ' ; rdfs:subClassOf ca:' + c['superclasse']
        schema.append(text + ' .')
    for p in meta['propriedades']:
        schema.append(f"ca:{p['id']} a owl:{p['tipo']} ; rdfs:label {literal(p['nome'])}@pt ; rdfs:comment {literal(p['descricao'])}@pt ; rdfs:domain ca:{p['dominio']} ; rdfs:range {p['alcance']} .")
    triples = [PREFIXES]
    counts = {}

    def add(s, p, o): triples.append(f'id:{s} {p} {o} .')

    def entity(s, kind, name, source, description):
        counts[kind] = counts.get(kind, 0) + 1
        add(s, 'a', 'ca:'+kind)
        add(s, 'rdfs:label', literal(name)+'@pt')
        add(s, 'rdfs:comment', literal(description)+'@pt')
        add(s, 'ca:idLocal', literal(s))
        path = 'data/'+source+'.json'
        add(s, 'ca:arquivoOrigem', literal(path))
        add(s, 'ca:hashOrigem', literal(hashlib.sha256((root/path).read_bytes()).hexdigest()))

    for a in data['eixos']:
        entity(a['id'], 'Eixo', a['nome'], 'eixos', a['metodologia'])
    for d in data['disciplinas']:
        entity(d['id'], 'Disciplina', d['nome'], 'disciplinas', 'Proposta editorial: '+d['habilidades'][0])
        add(d['id'], 'ca:pertenceEixo', 'id:'+d['eixo'])
        for p in d['pre_requisitos']: add(d['id'], 'ca:preRequisitoDisciplina', 'id:'+p)
    for h in data['habilidades']:
        entity(h['id'], 'UnidadeHabilidade', h['id'], 'habilidades', h['resultado_observavel'])
        add(h['id'], 'ca:daDisciplina', 'id:'+h['disciplina'])
        add(h['disciplina'], 'ca:contemUnidade', 'id:'+h['id'])
        add(h['id'], 'ca:estadoEditorial', literal(h['estado_editorial']))
        add(h['id'], 'ca:estadoEvidencia', literal(h['validacao_cientifica']))
        for p in h['pre_requisitos']: add(h['id'], 'ca:preRequisitoUnidade', 'id:'+p)
        for p in h['referencias_candidatas']: add(h['id'], 'ca:referenciaCandidata', 'id:'+p)
        if h['curso']: add(h['id'], 'ca:temCurso', 'id:'+h['curso'])
    for r in data['referencias']:
        entity(r['id'], 'Referencia', r['titulo'], 'referencias', r['leitura'])
        add(r['id'], 'rdfs:seeAlso', '<'+r['url']+'>')
    for c in data['cursos']:
        entity(c['id'], 'Curso', c['titulo'], 'cursos', c['leitura'])
        add(c['id'], 'rdfs:seeAlso', '<'+c['url']+'>')
    for m in data['missoes']:
        entity(m['id'], 'Missao', m['titulo'], 'missoes', m['problema']+' Limite: '+m['limite'])
        for h in m['habilidades_requeridas']: add(m['id'], 'ca:requerHabilidade', 'id:'+h)
        for h in m['habilidades_introduzidas']: add(m['id'], 'ca:introduzHabilidade', 'id:'+h)
        for d in m['disciplinas']: add(m['id'], 'ca:integraDisciplina', 'id:'+d)
    for f in data['funcoes-fontes']:
        entity('funcao-'+f['id'], 'FuncaoAcademica', f['nome'], 'funcoes-fontes', f['finalidade'])
    for r in data['relacoes-fontes']:
        sid = 'relacao-'+r['id']
        entity(sid, 'RelacaoFonte', r['id'], 'relacoes-fontes', r['justificativa'])
        add(sid, 'ca:disciplinaDaRelacao', 'id:'+r['disciplina'])
        add(sid, 'ca:fonteDaRelacao', 'id:'+r['referencia'])
        add(sid, 'ca:estadoDecisao', literal(r['status_decisao']))
        add(sid, 'ca:estadoEvidencia', literal(r['status_evidencia']))
        for f in r['funcoes_propostas']: add(sid, 'ca:funcaoProposta', 'id:funcao-'+f)
    out = root/'ontologia';out.mkdir(exist_ok=True)
    (out/'esquema.ttl').write_text('\n'.join(schema)+'\n', encoding='utf-8')
    (out/'dados.ttl').write_text('\n'.join(triples)+'\n', encoding='utf-8')
    (out/'curriculo.ttl').write_text('\n'.join(schema+triples)+'\n', encoding='utf-8')
    manifest = dict(status_decisao='PROPOSTO', validacao_cientifica='NÃO VERIFICADO',
        individuos=sum(counts.values()), por_classe=counts,
        fontes_sha256={s:hashlib.sha256((root/'data'/(s+'.json')).read_bytes()).hexdigest() for s in SOURCES},
        limite='Exportação das relações editoriais; não registra proficiência humana/IA ou suporte científico confirmado.')
    (out/'manifesto.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return manifest


def impact(unit, root=ROOT):
    """Dependência editorial transitiva; não é plano semântico do motor OWL."""
    skills=json.loads((root/'data/habilidades.json').read_text(encoding='utf-8'))
    missions=json.loads((root/'data/missoes.json').read_text(encoding='utf-8'))
    if unit not in {h['id'] for h in skills}: raise ValueError('Unidade inexistente')
    affected={unit}
    while True:
        more={h['id'] for h in skills if set(h['pre_requisitos']) & affected}
        if more <= affected: break
        affected |= more
    return dict(unidade=unit, unidades_dependentes=sorted(affected-{unit}),
        missoes_requeridas=[m['id'] for m in missions if set(m['habilidades_requeridas']) & affected],
        missoes_introducao=[m['id'] for m in missions if set(m['habilidades_introduzidas']) & affected],
        limite='Dependência transitiva local. Não equivale a blast radius ou conservatividade calculados pelo Open Ontologies.')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--impacto');a=p.parse_args()
    try: result=impact(a.impacto) if a.impacto else export()
    except ValueError as e:p.error(str(e))
    print(json.dumps(result,ensure_ascii=False,indent=2))
