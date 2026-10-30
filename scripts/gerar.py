"""Gera a documentação editorial; usa somente a biblioteca padrão."""
from pathlib import Path
import json,csv,io
from relacoes import render_relations
ROOT=Path(__file__).resolve().parents[1]
def read(n): return json.loads((ROOT/"data"/(n+".json")).read_text(encoding="utf-8"))
def write(n,s):
    p=ROOT/n
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(s.rstrip()+"\n",encoding="utf-8")
def table(headers,rows):
    return "| "+" | ".join(headers)+" |\n|"+"|".join("---" for _ in headers)+"|\n"+"\n".join("| "+" | ".join(str(x).replace("|","/").replace("\n"," ") if x is not None else "—" for x in row)+" |" for row in rows)+"\n"
def export(n,fields,rows):
    f=io.StringIO(newline="")
    w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader()
    for r in rows:w.writerow({k:";".join(r[k]) if isinstance(r.get(k),list) else r.get(k) for k in fields})
    write(n,f.getvalue())
def generate():
    subs,axes,refs,courses,sources,filters,samples=[read(x) for x in ("disciplinas","eixos","referencias","cursos","fontes","filtro-ebooks","amostras-matrizes")]
    sub={x["id"]:x for x in subs}; ax={x["id"]:x for x in axes}; ref={x["id"]:x for x in refs}; course={x["id"]:x for x in courses}
    def sl(c,p="../disciplinas/"):return f'[{c["id"]} — {c["nome"]}]({p}{c["id"].lower()}.md)'
    write("curriculo/catalogo.md","# Catálogo de disciplinas\n\nProposta editorial v0.2.0. Não é uma matriz oficial nem uma enumeração universal de todas as disciplinas existentes. Pré-requisitos e habilidades são propostas; revisão especializada pendente.\n\n"+table(["ID","Disciplina","Eixo","Percursos","Etapa lógica"],[(c["id"],sl(c),c["eixo"],", ".join(c["percursos"]) or "eletiva",c["etapa"]) for c in subs]))
    for c in subs:
        s=f'# {c["id"]} — {c["nome"]}\n\nEixo: **{ax[c["eixo"]]["nome"]}**. Percursos: {", ".join(c["percursos"]) or "eletiva"}. Etapa lógica: {c["etapa"]}.\n\n'
        s+="Estado: **PROPOSTO**. Avaliação científica: **NÃO VERIFICADO**. Ficha elaborada com assistência de IA; revisão humana pendente. O vínculo com fontes é temático, sem certificação de equivalência.\n\n## Conhecimentos\n\n"+"\n".join("- "+v for v in c["conhecimentos"])
        s+="\n\n## Habilidade e resultado observável\n\n"+c["habilidades"][0].capitalize()+".\n\n## Pré-requisitos propostos\n\n"
        s+="\n".join("- "+sl(sub[p],"") for p in c["pre_requisitos"]) if c["pre_requisitos"] else "Sem disciplina anterior exigida nesta proposta; diagnosticar conhecimentos escolares básicos."
        s+="\n\n## Metodologia sugerida\n\n"+c["metodologia"].capitalize()+". Adaptar ao diagnóstico do estudante; ver [protocolo pedagógico](../docs/metodologia.md).\n\n## Atividade e avaliação\n\n"+c["evidencia"]+"\n\nVerificar correção, justificativas, casos limite e possibilidade de reprodução. A ficha não atribui carga horária oficial.\n\n## Cursos e aulas\n\n"
        s+="\n".join(f'- [{course[i]["titulo"]}]({course[i]["url"]}) — {course[i]["nota"]}.' for i in c["cursos"]) if c["cursos"] else "Curso específico ainda não selecionado e auditado. Consultar a [UBL](https://github.com/Universidade-Livre/ciencia-da-computacao) e o [catálogo](../bibliografia/cursos.md); não presumir cobertura integral."
        s+="\n\n## Referências candidatas para seleção de capítulos\n\n"
        for i in c["referencias_candidatas"]:
            r=ref[i];s+=f'- [{i}: {r["titulo"]}]({r["url"]}) — {r["autores"]}. Escopo: {r["escopo"]}. Acesso: {r["acesso"]}. Leitura integral NÃO VERIFICADA.\n'
        s+="\nReferência candidata não significa que todo o livro seja obrigatório ou cubra toda a disciplina. Seleção de capítulos e aderência às habilidades requerem revisão. Ver [catálogo bibliográfico](../bibliografia/catalogo.md).\n\n## Correspondência curricular\n\n"
        s+=("Áreas CS2023 propostas: "+", ".join(c["cs2023_proposto"])+". Aproximação editorial por área; unidades de conhecimento e resultados de aprendizagem ainda não auditados." if c["cs2023_proposto"] else "Conteúdo de engenharia e ciências básicas. Relacionamento detalhado com CE2016 e SBC pendente.")
        s+="\n\n## Lacunas\n\n"+"\n".join("- "+x for x in c["lacunas"])+"\n\n[Voltar ao catálogo](../curriculo/catalogo.md)\n"
        s+="\n## Fontes, limitações e sugestões de pesquisa\n\nVer [relações detalhadas desta disciplina](../bibliografia/relacoes/"+c["id"].lower()+".md), com funções propostas, justificativa, acesso, licença, limites de leitura e autoria das sugestões. Vínculo temático não comprova suporte a uma alegação.\n"
        write("disciplinas/"+c["id"].lower()+".md",s)
    write("curriculo/eixos.md","# Eixos temáticos\n\nOrganização autoral proposta; os 16 eixos locais são diferentes das 17 áreas do CS2023.\n\n"+table(["ID","Eixo","Relação proposta CS2023","Metodologia"],[(a["id"],a["nome"],", ".join(a["cs2023"]) or "engenharia/ciências básicas",a["metodologia"]) for a in axes]))
    for track,name in [("CC","Ciência da Computação"),("EC","Engenharia de Computação")]:
        selected={c["id"] for c in subs if track in c["percursos"]};added=set()
        def include(cid):
            for p in sub[cid]["pre_requisitos"]:
                if p not in selected:selected.add(p);added.add(p)
                include(p)
        for cid in list(selected):include(cid)
        rows=sorted((sub[i] for i in selected),key=lambda c:(c["etapa"],c["id"]))
        s=f"# Percurso proposto — {name}\n\nEstado: **PROPOSTO**. Estudo independente: etapas são camadas de pré-requisitos, não semestres nem promessa de duração. Não atribui diploma, grau, registro profissional ou créditos universitários.\n\n"
        if added:s+="Pré-requisitos adicionais: "+", ".join(sorted(added))+".\n\n"
        s+=table(["Etapa lógica","Disciplina","Pré-requisitos"],[(c["etapa"],sl(c),", ".join(c["pre_requisitos"]) or "—") for c in rows])
        s+="\nEletivas no [catálogo](catalogo.md). Estágio, extensão, laboratórios e trabalho final possuem exigências institucionais próprias; sua presença aqui não substitui supervisão e aprovação institucional.\n"
        write(f"curriculo/percurso-{track.lower()}.md",s)
    areas=sorted({a for c in subs for a in c["cs2023_proposto"]})
    write("matrizes/correspondencias-cs2023.md","# Correspondências temáticas com CS2023\n\nFonte: [CS2023 — Knowledge Areas](https://csed.acm.org/knowledge-areas/). Mapeamento: PROPOSTO.\n\n"+table(["Área","Disciplinas propostas"],[(a,", ".join(c["id"] for c in subs if a in c["cs2023_proposto"])) for a in areas])+"\nA presença de siglas não comprova cobertura de tópicos, horas ou competências. Auditoria por unidade de conhecimento: NÃO VERIFICADO. Mapeamentos detalhados CE2016 e SBC pendentes.\n")
    write("matrizes/fontes-institucionais.md","# Matrizes e fontes institucionais\n\nConsulta: 30/10/2026. Amostra exploratória; a versão identificada permanece ligada à fonte. Não representa todas as instituições.\n\n"+table(["ID","Documento","Tipo","Versão","Estado","Limite"],[(s["id"],f'[{s["titulo"]}]({s["url"]})',s["tipo"],s["versao"],s["status"],s["limite"]) for s in sources]))
    write("matrizes/amostras-rastreaveis.md","# Amostras rastreáveis de matrizes\n\nComponentes localizados em quatro matrizes, sem transcrição integral. Correspondência temática proposta; equivalência formal NÃO VERIFICADA. Horas institucionais não são atribuídas às nossas fichas.\n\n"+table(["Fonte","Código","Nome na fonte","CH","Período","Ficha","Localização"],[(x["fonte"],x["codigo"],x["nome"],x["carga_horaria"],x["periodo"],sl(sub[x["disciplina_proposta"]]),x["localizacao"]) for x in samples])+"\nURLs e versões no [registro de fontes](fontes-institucionais.md).\n")
    s="# Bibliografia especializada — catálogo inicial\n\nSeleção exploratória, não revisão sistemática. Metadados e sumários consultados não equivalem à leitura integral. Obras candidatas para seleção de capítulos; adequação por disciplina pendente. Clássicos e obras recentes podem coexistir neste currículo sem importar o recorte temporal de outro projeto.\n\n"
    s+=table(["ID","Título","Autoria","Edição/ano","Tipo","Escopo","Acesso"],[(r["id"],f'[{r["titulo"]}]({r["url"]})',r["autores"],f'{r["edicao"] or "a conferir"} / {r["ano"] or "a conferir"}',r["tipo"],r["escopo"],r["acesso"]) for r in refs])
    s+="\n## Leitura e direitos\n\n"+table(["ID","Leitura realizada","Metadados","Licença da obra","Correções/retratações"],[(r["id"],r["leitura"],r["status_metadados"],r["licenca"],r["correcoes_retratacoes"]["status"]) for r in refs])
    s+="\nA licença do repositório não se aplica aos livros vinculados. Para citar em artigo, registrar edição realmente lida, suporte em página/seção/tabela e verificação de correções. Não há certificação de conformidade ABNT nesta versão.\n"
    s+="\nConsulte também o [índice por fonte](por-fonte.md), as [relações com disciplinas](relacoes.md), as [funções acadêmicas](funcoes.md) e as [limitações e sugestões de pesquisa](limitacoes-e-pesquisa.md).\n"
    write("bibliografia/catalogo.md",s)
    write("bibliografia/cursos.md","# Cursos e conjuntos de aulas\n\nPáginas de apresentação e programa consultadas; aulas, exercícios e certificação não auditados. Acesso gratuito a partes não garante gratuidade integral.\n\n"+table(["ID","Título","Instituição","Idioma","Limites"],[(c["id"],f'[{c["titulo"]}]({c["url"]})',c["instituicao"],c["idioma"],c["nota"]) for c in courses]))
    write("bibliografia/filtro-ebooks.md","# Filtro de fontes complementares\n\nPonto de partida: [gist indicado](https://gist.github.com/baiwfg2/af827b8b75eebf8ab29f5531a0d265ce?permalink_comment_id=3896162). Corpo e comentários visíveis examinados; comentário 3896162 não isolado na resposta recuperada. Comentários fora de tema não foram tratados como recomendações.\n\nCritério: localizar a obra em autor/editora/universidade/repositório autorizado e verificar condições por título. Leitura gratuita é diferente de autorização de redistribuição. Ausência de verificação não é acusação de irregularidade.\n\n"+table(["Fonte","Decisão","Estado","Motivo"],[(f'[{x["nome"]}]({x["url"]})' if x["url"] else x["nome"],x["decisao"],x["status"],x["motivo"]) for x in filters])+"\nTriagem inicial dos principais candidatos, não auditoria de todos os domínios/comentários. Não houve download de livros, cadastro, compra ou tentativa de contornar acesso.\n")
    export("data/disciplinas.csv",["id","nome","eixo","etapa","percursos","natureza","pre_requisitos","conhecimentos","habilidades","referencias_candidatas","status_decisao"],subs)
    export("data/referencias.csv",["id","titulo","autores","edicao","ano","url","tipo","acesso","licenca","status","leitura"],refs)
    export("data/matrizes.csv",["fonte","codigo","nome","carga_horaria","periodo","disciplina_proposta","localizacao","equivalencia_formal"],samples)
    bib=[]
    for r in refs:
        fields={"title":r["titulo"],"author":" and ".join(r["autores"].split("; ")),"url":r["url"],"urldate":"2026-10-30","note":"Registro de descoberta. Conferir edição antes de citar; leitura integral não verificada."}
        if r["ano"]:fields["year"]=str(r["ano"])
        if r["doi"]:fields["doi"]=r["doi"]
        bib.append("@"+("article" if r["id"].startswith("P") else "misc")+"{"+r["id"]+",\n"+",\n".join("  "+k+" = {"+v+"}" for k,v in fields.items())+"\n}")
    write("bibliografia/referencias.bib","\n\n".join(bib))
    relations,functions=read("relacoes-fontes"),read("funcoes-fontes")
    render_relations(subs,refs,functions,relations,table,write,export)
    print(json.dumps({"disciplinas":len(subs),"eixos":len(axes),"referencias":len(refs),"cursos":len(courses),"areas_cs2023":len(areas),"amostras":len(samples),"relacoes_fontes":len(relations),"funcoes":len(functions)},ensure_ascii=False))
if __name__=="__main__":generate()

