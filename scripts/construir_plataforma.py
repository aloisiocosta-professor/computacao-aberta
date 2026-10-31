"""Empacota apenas arquivos públicos da plataforma para GitHub Pages."""
from pathlib import Path
import argparse
import json
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=('index.html','styles.css','app.mjs','engine.mjs','missions.mjs','simulation.mjs','icon.svg','catalogo.json','laboratorio.html','academia.css','academia.mjs','jornada.mjs','jornada.json')


def catalog(root=ROOT):
    def read(name):return json.loads((root/'data'/(name+'.json')).read_text(encoding='utf-8'))
    axes={x['id']:x['nome'] for x in read('eixos')}
    items={i['id']:i['titulo'] for x in read('indices-disciplinas')+read('indices-cursos') for i in x['itens']}
    skills=read('habilidades')
    rows=[dict(id=s['id'],nome=s['nome'],eixo=axes[s['eixo']],unidades=[dict(id=h['id'],titulo=items[h['item']],estado=h['estado_editorial']) for h in skills if h['disciplina']==s['id']]) for s in read('disciplinas')]
    (root/'plataforma/catalogo.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    missions=read('desafios-plataforma')
    module='// Gerado de data/desafios-plataforma.json.\nexport const missions='+json.dumps(missions,ensure_ascii=False,indent=2)+';\nexport const byId=id=>missions.find(m=>m.id===id)||missions[0];\n'
    (root/'plataforma/missions.mjs').write_text(module,encoding='utf-8')
    profiles={x['id']:x for x in read('perfis-habilidades')}
    refs={x['id']:x for x in read('referencias')}
    courses={x['id']:x for x in read('cursos')}
    models=read('gamificacao')
    journey=dict(versao=models['versao'],estado_pedagogico=models['status_pedagogico'],eixos=read('eixos'),modelos=models['modelos'],disciplinas=[])
    for d in read('disciplinas'):
        profile=profiles[next(h['perfil'] for h in skills if h['disciplina']==d['id'])]
        units=[]
        for h in skills:
            if h['disciplina']!=d['id']:continue
            resources=[dict(id=r,titulo=refs[r]['titulo'],url=refs[r]['url'],leitura=refs[r]['leitura'],tipo='Livro/referência candidata') for r in h['referencias_candidatas'] if r in refs]
            if h.get('curso') in courses:
                c=courses[h['curso']];resources.insert(0,dict(id=c['id'],titulo=c['titulo'],url=c['url'],leitura=c['leitura'],tipo='Curso de origem'))
            units.append(dict(id=h['id'],titulo=items[h['item']],item=h['item'],indice=h['indice'],estado=h['estado_editorial'],objetivo=h['resultado_observavel'],pre_requisitos=h['pre_requisitos'],modelo=d['eixo'],recursos=resources,tarefa=profile['visualizacao']['tarefa'],representacao=profile['visualizacao']['representacao'],criterios=profile['criterios'],evidencias=profile['evidencias_esperadas'],transferencia=profile['transferencia'],julgamento=profile['julgamento_pratico'],aula=h.get('aula_local')))
        journey['disciplinas'].append(dict(id=d['id'],nome=d['nome'],eixo=d['eixo'],etapa=d['etapa'],percursos=d['percursos'],pre_requisitos=d['pre_requisitos'],metodologia=d['metodologia'],unidades=units))
    # Share repeated profiles and references: keep the initial download compact.
    journey['perfis']={}
    journey['recursos']={}
    shared=('tarefa','representacao','criterios','evidencias','transferencia','julgamento')
    for d in journey['disciplinas']:
        for u in d['unidades']:
            journey['perfis'].setdefault(d['eixo'],{key:u[key] for key in shared})
            for key in shared:u.pop(key)
            for resource in u['recursos']:journey['recursos'][resource['id']]=resource
            u['recursos']=[resource['id'] for resource in u['recursos']]
    (root/'plataforma/jornada.json').write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return rows


def build(destination,root=ROOT):
    destination=destination.resolve()
    if destination==root.resolve() or destination==root/'plataforma' or not destination.is_relative_to(root):
        raise ValueError('Escolha uma pasta de saída dedicada dentro do projeto, como dist.')
    allowed=set(PUBLIC)|{'release.json','.nojekyll'}
    if destination.exists() and any(p.name not in allowed for p in destination.iterdir()):
        raise ValueError('A pasta de saída contém arquivos não esperados. Use uma pasta dedicada e vazia.')
    rows=catalog(root);destination.mkdir(parents=True,exist_ok=True)
    for filename in PUBLIC:shutil.copyfile(root/'plataforma'/filename,destination/filename)
    try:commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True,stderr=subprocess.DEVNULL).strip()
    except (OSError,subprocess.CalledProcessError):commit='development'
    (destination/'release.json').write_text(json.dumps(dict(version='0.2.0',commit=commit),indent=2)+'\n',encoding='utf-8')
    (destination/'.nojekyll').write_text('',encoding='utf-8')
    return dict(version='0.2.0',commit=commit,files=list(PUBLIC)+['release.json','.nojekyll'],disciplinas=len(rows),desafios=len(json.loads((root/'data/desafios-plataforma.json').read_text(encoding='utf-8'))))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,default=ROOT/'dist');args=p.parse_args()
    print(json.dumps(build(args.out),ensure_ascii=False,indent=2))
