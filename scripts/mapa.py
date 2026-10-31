"""Exportação pedagógica determinística para Understand Anything, sem LLM."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ('eixos', 'disciplinas', 'habilidades', 'referencias', 'cursos',
          'missoes', 'indices-disciplinas', 'indices-cursos', 'trilha-inicial')


def build_graph(root=ROOT):
    data = {name: json.loads((root / 'data' / (name + '.json')).read_text())
            for name in INPUTS}
    digest = hashlib.sha256()
    for name in INPUTS:
        digest.update(name.encode())
        digest.update((root / 'data' / (name + '.json')).read_bytes())
    nodes, edges = [], []
    layers = {a['id']: dict(id=a['id'], name=a['nome'],
              description='Eixo editorial proposto', nodeIds=[])
              for a in data['eixos']}
    layers['fontes'] = dict(id='fontes', name='Fontes candidatas',
                           description='Não comprovam cobertura integral', nodeIds=[])
    layers['missoes'] = dict(id='missoes', name='Missões interdisciplinares',
                            description='Aplicar, explicar e decidir', nodeIds=[])

    def node(id_, type_, name, summary, path, layer, tags):
        nodes.append(dict(id=id_, type=type_, name=name, summary=summary,
                          filePath=path, tags=tags, complexity='moderate'))
        layers[layer]['nodeIds'].append(id_)

    def edge(source, target, type_, description):
        edges.append(dict(source=source, target=target, type=type_,
                          direction='forward', weight=1.0, description=description))

    subjects = {s['id']: s for s in data['disciplinas']}
    items = {i['id']: i for index in data['indices-disciplinas'] + data['indices-cursos']
             for i in index['itens']}
    for a in data['eixos']:
        node('eixo:' + a['id'], 'topic', a['nome'], a['metodologia'],
             'curriculo/eixos.md', a['id'], ['eixo', 'PROPOSTO'])
    for s in subjects.values():
        sid = 'disciplina:' + s['id']
        node(sid, 'topic', s['id'] + ' — ' + s['nome'],
             'Disciplina proposta. ' + s['habilidades'][0],
             'disciplinas/' + s['id'].lower() + '.md', s['eixo'], ['disciplina', 'PROPOSTO'])
        edge(sid, 'eixo:' + s['eixo'], 'categorized_under', 'Organização editorial')
        for p in s['pre_requisitos']:
            edge(sid, 'disciplina:' + p, 'depends_on', 'Pré-requisito proposto; diagnosticar')
    for h in data['habilidades']:
        sid = 'habilidade:' + h['id']
        node(sid, 'article', h['id'] + ' — ' + items[h['item']]['titulo'],
             h['resultado_observavel'] + ' Estado: ' + h['estado_editorial'] +
             '; validação científica: ' + h['validacao_cientifica'],
             h['aula_local'] or 'unidades/por-disciplina/' + h['disciplina'].lower() + '.md',
             subjects[h['disciplina']]['eixo'], ['habilidade', h['estado_editorial']])
        edge('disciplina:' + h['disciplina'], sid, 'contains', 'Item registrado de índice')
        for p in h['pre_requisitos']:
            edge(sid, 'habilidade:' + p, 'depends_on', 'Pré-requisito editorial proposto')
        for r in h['referencias_candidatas']:
            edge(sid, 'fonte:' + r, 'related', 'Referência CANDIDATA; capítulo/aderência NÃO VERIFICADOS')
        if h['curso']:
            edge(sid, 'curso:' + h['curso'], 'related', 'Item de índice externo; aula não declarada assistida')
    for r in data['referencias']:
        node('fonte:' + r['id'], 'source', r['id'] + ' — ' + r['titulo'],
             r['autores'] + '. Leitura: ' + r['leitura'] + '. ' + r['url'],
             'bibliografia/catalogo.md', 'fontes', ['referencia_candidata', r['status']])
    for c in data['cursos']:
        node('curso:' + c['id'], 'source', c['id'] + ' — ' + c['titulo'],
             c['leitura'] + '. ' + c['url'], 'unidades/indices/' + c['id'].lower() + '.md',
             'fontes', ['curso', 'PARCIAL'])
    for m in data['missoes']:
        mid = 'missao:' + m['id']
        node(mid, 'article', m['id'] + ' — ' + m['titulo'],
             m['problema'] + ' Limite: ' + m['limite'],
             'missoes/' + m['id'].lower() + '.md', 'missoes', ['missao', 'PROPOSTO'])
        for h in m['habilidades_requeridas']:
            edge(mid, 'habilidade:' + h, 'depends_on', 'Praticar antes da missão')
        for h in m['habilidades_introduzidas']:
            edge(mid, 'habilidade:' + h, 'related', 'Introdução; não certifica domínio')
        for s in m['disciplinas']:
            edge(mid, 'disciplina:' + s, 'related', m['contribuicoes'][s])
    tour = [dict(order=i+1, title='Praticar: ' + items[next(h['item'] for h in data['habilidades'] if h['id']==uid)]['titulo'],
                 description='Abra a aula, preveja o resultado e faça a tentativa. Registre o apoio recebido; navegar não é dominar.',
                 nodeIds=['habilidade:' + uid])
            for i, uid in enumerate(data['trilha-inicial']['unidades'])]
    tour.append(dict(order=len(tour)+1, title='Integrar e transferir',
                     description='Faça a missão M01, explique a decisão e teste casos limite.', nodeIds=['missao:M01']))
    graph = dict(version='1.0.0', kind='knowledge', project=dict(
        name='Computação Aberta — mapa pedagógico', languages=['Português', 'Python', 'JSON'],
        frameworks=[], description='Exportação editorial determinística; sem inferências semânticas, progresso pessoal ou certificação. SHA256 dos dados: ' + digest.hexdigest(),
        analyzedAt='2026-10-31T00:00:00-03:00', gitCommitHash=''),
        nodes=nodes, edges=edges, layers=list(layers.values()), tour=tour)
    validate_graph(graph, root)
    return graph


def validate_graph(graph, root=ROOT):
    ids = [n['id'] for n in graph['nodes']]
    if len(ids) != len(set(ids)):
        raise ValueError('ID duplicado')
    ids = set(ids)
    for e in graph['edges']:
        if e['source'] not in ids or e['target'] not in ids:
            raise ValueError('Aresta sem nó')
    assigned = [id_ for layer in graph['layers'] for id_ in layer['nodeIds']]
    if len(assigned) != len(ids) or set(assigned) != ids:
        raise ValueError('Camada ausente ou duplicada')
    for step in graph['tour']:
        if not set(step['nodeIds']) <= ids:
            raise ValueError('Tour sem nó')
    for n in graph['nodes']:
        p = Path(n['filePath'])
        if p.is_absolute() or '..' in p.parts or not (root / p).is_file():
            raise ValueError('Caminho inválido: ' + str(p))


def compose_graph(pedagogical, structure):
    """Preserva os dois mapas e conecta cada habilidade ao documento que a descreve."""
    graph = json.loads(json.dumps(structure))
    graph['project']['name'] = 'Computação Aberta — estrutura e aprendizagem'
    graph['project']['description'] += ' Inclui camada pedagógica editorial; referências continuam candidatas.'
    graph['nodes'].extend(pedagogical['nodes'])
    graph['edges'].extend(pedagogical['edges'])
    graph['layers'].extend(pedagogical['layers'])
    documents = {n['filePath']: n['id'] for n in structure['nodes']
                 if n['type'] == 'document' and 'filePath' in n}
    for n in pedagogical['nodes']:
        if n['filePath'] in documents:
            graph['edges'].append(dict(source=documents[n['filePath']], target=n['id'],
                type='documents', direction='forward', weight=0.5,
                description='Documento local que apresenta este item editorial; não comprova domínio.'))
    # O tour principal ensina a arquitetura; a prática tem tour próprio no mapa pedagógico.
    return graph


def generate_map(root=ROOT):
    pedagogical = build_graph(root)
    out = root / '.ua'
    out.mkdir(exist_ok=True)
    (out / 'pedagogical-graph.json').write_text(json.dumps(pedagogical, ensure_ascii=False, indent=2) + '\n')
    snapshot = out / 'structural-graph.json'
    graph = compose_graph(pedagogical, json.loads(snapshot.read_text())) if snapshot.exists() else pedagogical
    validate_graph(graph, root)
    (out / 'knowledge-graph.json').write_text(json.dumps(graph, ensure_ascii=False, indent=2) + '\n')
    return graph


if __name__ == '__main__':
    graph = generate_map()
    print(json.dumps({'nos': len(graph['nodes']), 'arestas': len(graph['edges']), 'etapas_tour': len(graph['tour'])}))
