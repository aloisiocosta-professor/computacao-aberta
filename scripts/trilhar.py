"""Consulta de unidades e validação de registros; não executa código do aprendiz."""
from pathlib import Path
import argparse,json,sys
from aprendizagem import validate_progress
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/"data"/(name+".json")).read_text(encoding="utf-8"))
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest="command",required=True)
    plan=sub.add_parser("plano");plan.add_argument("--disciplina")
    unit=sub.add_parser("unidade");unit.add_argument("id")
    progress=sub.add_parser("verificar-progresso");progress.add_argument("arquivo")
    args=parser.parse_args();skills=read("habilidades")
    if args.command=="plano":
        selected=[s for s in skills if s["disciplina"]==args.disciplina] if args.disciplina else [s for uid in read("trilha-inicial")["unidades"] for s in skills if s["id"]==uid]
        if not selected:parser.error("Disciplina sem unidade cadastrada")
        print(json.dumps(selected,ensure_ascii=False,indent=2))
    elif args.command=="unidade":
        u=next((s for s in skills if s["id"]==args.id),None)
        if u is None:parser.error("Unidade inexistente")
        p=next(p for p in read("perfis-habilidades") if p["id"]==u["perfil"])
        print(json.dumps({"unidade":u,"instrucoes_do_perfil":p,"protocolo":"agentes/PROTOCOLO.md","aviso":"Instruções não certificam aquisição da habilidade nem atualizam pesos de modelos."},ensure_ascii=False,indent=2))
    else:
        try:data=json.loads(Path(args.arquivo).read_text(encoding="utf-8"))
        except (OSError,ValueError) as e:parser.error(str(e))
        errors=validate_progress(data,skills)
        print(json.dumps({"status":"ATENDIDO" if not errors else "NÃO ATENDIDO","erros":errors,"limite":"Integridade do registro; não certifica domínio, autenticidade do artefato ou aprendizagem."},ensure_ascii=False,indent=2))
        return bool(errors)
    return 0
if __name__=="__main__":sys.exit(main())
