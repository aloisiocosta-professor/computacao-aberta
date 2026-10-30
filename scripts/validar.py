"""Validação estrutural offline. Não valida cientificamente o currículo."""
from pathlib import Path
from urllib.parse import urlparse,unquote
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
def check():
    errors=[];checks=0
    def require(ok,msg):
        nonlocal checks
        checks+=1
        if not ok:errors.append(msg)
    def read(n):return json.loads((ROOT/"data"/(n+".json")).read_text(encoding="utf-8"))
    subjects=read("disciplinas");refs=read("referencias");axes=read("eixos");courses=read("cursos");sources=read("fontes");samples=read("amostras-matrizes")
    def index(items,name):
        ids=[x["id"] for x in items]
        require(len(ids)==len(set(ids)),f"IDs duplicados em {name}")
        return {x["id"]:x for x in items}
    sub=index(subjects,"disciplinas");ref=index(refs,"referencias");axis=index(axes,"eixos");course=index(courses,"cursos");source=index(sources,"fontes")
    for c in subjects:
        require(c["eixo"] in axis,"Eixo inexistente: "+c["id"])
        require(bool(c["conhecimentos"]) and bool(c["habilidades"]) and bool(c["metodologia"]),"Ficha vazia: "+c["id"])
        require(c["status_decisao"] in {"PROPOSTO","DECIDIDO","SUPERADO"},"Estado decisório inválido")
        for p in c["pre_requisitos"]:
            require(p in sub,"Pré-requisito inexistente: "+p)
            if p in sub:require(sub[p]["etapa"]<c["etapa"],"Etapa não sucede pré-requisito: "+c["id"]+" / "+p)
        for r in c["referencias_candidatas"]:require(r in ref,"Referência inexistente: "+r)
        for r in c["cursos"]:require(r in course,"Curso inexistente: "+r)
        require((ROOT/"disciplinas"/(c["id"].lower()+".md")).is_file(),"Página ausente: "+c["id"])
    visited=set();active=set()
    def visit(cid):
        if cid in active:
            errors.append("Ciclo em "+cid);return
        if cid in visited:return
        active.add(cid)
        for p in sub[cid]["pre_requisitos"]:
            if p in sub:visit(p)
        active.remove(cid);visited.add(cid)
    for cid in sub:visit(cid)
    require(len(visited)==len(sub),"Grafo não percorrido integralmente")
    expected={"AL","AR","AI","DM","FPL","GIT","HCI","MSF","NC","OS","PDC","SEC","SEP","SDF","SE","SPD","SF"}
    require({a for c in subjects for a in c["cs2023_proposto"]}==expected,"Siglas CS2023 incompletas ou inválidas")
    for r in refs:
        require(bool(r["leitura"]) and bool(r["licenca"]),"Registro de leitura/licença ausente: "+r["id"])
        require(r["correcoes_retratacoes"]["status"] in {"CONFIRMADO","PARCIAL","NÃO VERIFICADO"},"Estado de correção inválido")
        require(urlparse(r["url"]).scheme in {"http","https"},"URL inválida: "+r["id"])
    for s in samples:
        require(s["fonte"] in source,"Fonte de matriz ausente")
        require(s["disciplina_proposta"] in sub,"Ficha de matriz ausente")
        require(bool(s["localizacao"]),"Matriz sem localização")
    link_count=0
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:continue
        text=path.read_text(encoding="utf-8")
        require(text.count("~~~")%2==0 and text.count(chr(96)*3)%2==0,"Cerca de código incompleta: "+str(path))
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)\s]+)\)',text):
            if urlparse(target).scheme or target.startswith("#"):continue
            link_count+=1
            dest=(path.parent/unquote(target.split("#")[0])).resolve()
            require(dest.is_relative_to(ROOT),"Link sai do projeto: "+str(path))
            require(dest.exists(),"Link local quebrado: "+str(path.relative_to(ROOT))+" -> "+target)
    require(not any(p.suffix.lower() in {".pdf",".epub",".mobi"} for p in ROOT.rglob("*") if ".git" not in p.parts),"Obra binária incorporada sem fluxo de licença")
    return {"status":"ATENDIDO" if not errors else "NÃO ATENDIDO","verificacoes":checks,"links_locais":link_count,"disciplinas":len(subjects),"referencias":len(refs),"erros":errors,"escopo":"estrutura offline; URLs externas, conteúdo científico, YAML e licenças integrais não validados"}
if __name__=="__main__":
    result=check()
    print(json.dumps(result,ensure_ascii=False,indent=2))
    sys.exit(bool(result["erros"]))

