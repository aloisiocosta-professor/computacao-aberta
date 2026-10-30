"""Habilidades por item de índice, sem equiparar consumo de conteúdo a domínio."""
from collections import Counter,defaultdict
from datetime import date
STAGES=["diagnostico","modelo_visual","exemplo_guiado","pratica_assistida","pratica_independente","transferencia","retencao"]
PROGRESS={"nao_iniciado","exposicao","pratica_assistida","desempenho_independente","transferencia_demonstrada","retencao_verificada"}
def validate_learning(subjects,courses,indices,skills,profiles,missions):
    errors=[];sub={c["id"]:c for c in subjects};course={c["id"] for c in courses};units={u["id"]:u for u in skills};prof={p["id"]:p for p in profiles}
    if len(units)!=len(skills):errors.append("ID de habilidade duplicado")
    index={x["id"]:x for x in indices}
    if len(index)!=len(indices):errors.append("ID de índice duplicado")
    itemmap={}
    for ix in indices:
        if ix["tipo"]=="curso_externo" and ix.get("curso") not in course:errors.append("Curso de índice inexistente")
        if ix["tipo"]=="curso_externo" and (not ix.get("fonte_url") or not ix.get("consulta_em") or not ix.get("escopo")):errors.append("Índice externo sem origem, data ou escopo")
        for item in ix["itens"]:
            key=(ix["id"],item["id"])
            if key in itemmap:errors.append("Item duplicado no índice")
            itemmap[key]=item
            if not item.get("titulo") or not item.get("numero_original"):errors.append("Item sem título ou número/origem")
    coverage=Counter((u["indice"],u["item"]) for u in skills)
    for key in itemmap:
        if coverage[key]!=1:errors.append("Cada item precisa de exatamente uma unidade: "+"/".join(key))
    for key in coverage:
        if key not in itemmap:errors.append("Habilidade vinculada a item inexistente: "+str(key))
    for c in subjects:
        ix=index.get("IDX-"+c["id"])
        if not ix or [i["titulo"] for i in ix["itens"]]!=c["conhecimentos"]:errors.append("Índice autoral não corresponde aos tópicos: "+c["id"])
    for u in skills:
        if u["disciplina"] not in sub:errors.append("Disciplina da habilidade inexistente")
        if not u.get("resultado_observavel"):errors.append("Unidade sem resultado observável")
        if u.get("estado_editorial") not in {"ROTEIRO","AULA_INICIAL","REVISADA"}:errors.append("Estado editorial inválido")
        if u.get("estado_editorial")!="ROTEIRO" and not u.get("aula_local"):errors.append("Aula sem arquivo indicado")
        if u.get("validacao_cientifica") not in {"NÃO VERIFICADO","PARCIAL","CONFIRMADO"}:errors.append("Estado científico inválido")
        if u.get("perfil") not in prof:errors.append("Perfil pedagógico inexistente")
        for p in u["pre_requisitos"]:
            if p not in units:errors.append("Pré-requisito de habilidade inexistente: "+p)
    seen=set();active=set()
    def visit(uid):
        if uid in active:errors.append("Ciclo nas habilidades: "+uid);return
        if uid in seen:return
        active.add(uid)
        for p in units[uid]["pre_requisitos"]:
            if p in units:visit(p)
        active.remove(uid);seen.add(uid)
    for uid in units:visit(uid)
    for p in profiles:
        if [s["etapa"] for s in p["ciclo"]]!=STAGES:errors.append("Ciclo de aprendizagem incompleto: "+p["id"])
        if not p["visualizacao"].get("alternativa_textual"):errors.append("Visual sem alternativa textual")
        if not p.get("julgamento_pratico") or not p.get("criterios"):errors.append("Perfil sem critérios ou julgamento")
    for m in missions:
        if len(set(m["disciplinas"]))<2:errors.append("Missão sem integração interdisciplinar")
        if set(m["contribuicoes"])!=set(m["disciplinas"]):errors.append("Missão sem explicar contribuição por disciplina")
        for uid in m["habilidades_requeridas"]+m["habilidades_introduzidas"]:
            if uid not in units:errors.append("Missão aponta habilidade inexistente: "+uid)
    return errors

def validate_progress(data,skills):
    if not isinstance(data,dict) or not isinstance(data.get("registros"),list):
        return ["Progresso deve conter uma lista de registros"]
    errors=[];units={s["id"] for s in skills};records={}
    for r in data.get("registros",[]):
        if not isinstance(r,dict):errors.append("Registro de progresso deve ser objeto");continue
        rid=r.get("id");uid=r.get("unidade");state=r.get("estado")
        if not rid or rid in records:errors.append("ID de progresso ausente ou duplicado")
        if uid not in units:errors.append("Unidade de progresso inexistente")
        if state not in PROGRESS:errors.append("Estado de progresso inválido")
        try:day=date.fromisoformat(r.get("data",""))
        except (ValueError,TypeError):errors.append("Data de progresso inválida");day=None
        if state not in {"nao_iniciado","exposicao"}:
            if not r.get("artefatos") or not r.get("avaliador") or not r.get("justificativa"):
                errors.append("Prática exige artefato, avaliador e justificativa")
        if r.get("apoio") not in {"nenhum","pista","exemplo","solucao","nao_informado"}:errors.append("Apoio não registrado")
        if state in {"desempenho_independente","transferencia_demonstrada","retencao_verificada"}:
            if r.get("apoio")!="nenhum":errors.append("Desempenho independente não pode usar pista/exemplo/solução")
            if set(r.get("criterios_atendidos",[]))!={"correcao","explicacao","representacao","limites"}:
                errors.append("Critérios de desempenho incompletos")
        if state in {"transferencia_demonstrada","retencao_verificada"}:
            previous=records.get(r.get("registro_anterior"))
            if not previous or previous.get("unidade")!=uid or previous.get("estado") not in {"desempenho_independente","transferencia_demonstrada","retencao_verificada"}:
                errors.append("Transferência/retenção exige registro anterior independente da mesma unidade")
            elif state=="transferencia_demonstrada" and (not r.get("contexto") or r.get("contexto")==previous.get("contexto")):
                errors.append("Transferência exige contexto diferente identificado")
            elif state=="retencao_verificada":
                try:before=date.fromisoformat(previous.get("data",""))
                except (ValueError,TypeError):before=None
                if not day or not before or day<=before:errors.append("Retenção exige retomada em data posterior")
        records[rid]=r
    return errors

def render_learning(root,subjects,courses,indices,skills,profiles,missions,pedagogy,table,write,export):
    sub={c["id"]:c for c in subjects};prof={p["id"]:p for p in profiles};by_sub=defaultdict(list);by_index=defaultdict(list)
    for u in skills:by_sub[u["disciplina"]].append(u);by_index[u["indice"]].append(u)
    itemmap={(ix["id"],i["id"]):i for ix in indices for i in ix["itens"]}
    def ul(u,p="../unidades/por-disciplina/"):return f'[{u["id"]}]({p}{u["disciplina"].lower()}.md#{u["id"].lower()})'
    author=sum(ix["tipo"]=="disciplina_autoral" for ix in indices)
    external=sum(ix["tipo"]=="curso_externo" for ix in indices)
    ready=sum(u["estado_editorial"]!="ROTEIRO" for u in skills)
    coverage="# Cobertura dos índices e estado editorial\n\n"
    coverage+=f"{author} índices autorais e {external} índices externos registrados, com {len(skills)} itens ligados a unidades. {ready} unidades possuem aula inicial; as demais são roteiros, não aulas completas nem competências já dominadas.\n\n"
    coverage+="Cobertura de todos os itens registrados é diferente de cobertura de todos os subitens de todos os cursos. O recorte dos índices externos está explícito abaixo; conteúdos internos e aulas não foram auditados integralmente.\n\n"
    coverage+=table(["Índice","Origem","Itens","Unidades","Recorte"],[(ix["id"],ix["tipo"],len(ix["itens"]),len(by_index[ix["id"]]),ix["escopo"]) for ix in indices])
    write("aprendizagem/cobertura.md",coverage)
    catalog="# Catálogo de habilidades práticas\n\nCada unidade corresponde a um item registrado de índice. Resultados e tarefas são propostas editoriais; não representam habilidades já adquiridas pelo usuário. Comece pela [trilha inicial](comecar.md).\n\n"
    catalog+=table(["Unidade","Disciplina","Resultado observável","Estado editorial"],[(ul(u),u["disciplina"],u["resultado_observavel"],u["estado_editorial"]) for u in skills])
    write("aprendizagem/habilidades.md",catalog)
    for c in subjects:
        s=f'# Unidades de habilidade — {c["id"]}: {c["nome"]}\n\n'
        s+="As unidades abaixo são organizadas por origem: tópicos autorais e itens de índices externos. Pré-requisitos e resultados são propostas. ROTEIRO requer seleção de exemplo, tarefa e avaliação específicos antes de ser tratado como aula pronta.\n\n"
        for u in by_sub[c["id"]]:
            p=prof[u["perfil"]];item=itemmap[(u["indice"],u["item"])]
            s+=f'## {u["id"]}\n\nOrigem: {u["indice"]}, item {item["numero_original"]}. Estado: **{u["estado_editorial"]}**. Revisão científica: {u["validacao_cientifica"]}.\n\n'
            s+="Resultado observável: "+u["resultado_observavel"]+"\n\n"
            s+="Pré-requisitos: "+(", ".join(ul(next(x for x in skills if x["id"]==uid),"") for uid in u["pre_requisitos"]) if u["pre_requisitos"] else "sem unidade anterior exigida; realizar diagnóstico")+".\n\n"
            if u["aula_local"]:s+=f'[Abrir aula inicial](../../{u["aula_local"]}) — inclui exemplo concreto e tentativa independente.\n\n'
            s+="Representação a construir: "+p["visualizacao"]["representacao"]+". "+p["visualizacao"]["alternativa_textual"]+"\n\n"
            s+=table(["Etapa","Instrução proposta"],[(x["etapa"],x["instrucao"]) for x in p["ciclo"]])+"\n"
            s+="Evidências esperadas:\n\n"+"\n".join("- "+e for e in p["evidencias_esperadas"])+"\n\n"
            s+="Feedback: "+p["feedback"]+"\n\nTransferência: "+p["transferencia"]+"\n\nJulgamento prático: "+p["julgamento_pratico"]+"\n\n"
        s+="[Ficha e fontes](../../disciplinas/"+c["id"].lower()+".md) · [Progresso](../../aprendizagem/progresso.md) · [Missões](../../missoes/README.md)\n"
        write("unidades/por-disciplina/"+c["id"].lower()+".md",s)
    for ix in indices:
        if ix["tipo"]!="curso_externo":continue
        s=f'# Índice externo — {ix["curso"]}\n\n[Origem consultada]({ix["fonte_url"]}). Versão: {ix["versao"]}. Consulta: {ix["consulta_em"]}. Estado da cobertura: {ix["status_indice"]}.\n\n'
        s+="Recorte: "+ix["escopo"]+". Título conferido não significa aula assistida ou domínio demonstrado. As habilidades associadas são propostas locais, não resultados oficiais transcritos do curso.\n\n"
        s+=table(["Número na fonte","Título no índice","Unidade proposta","Situação"],[(i["numero_original"],i["titulo"],ul(next(u for u in by_index[ix["id"]] if u["item"]==i["id"]),"../por-disciplina/"),i["situacao_no_cronograma"]) for i in ix["itens"]])
        s+="\nSubitens não registrados permanecem fora da cobertura declarada. Quando o índice mudar, conservar a versão anterior e revisar os vínculos, sem reutilizar silenciosamente um ID para outro conteúdo.\n"
        write("unidades/indices/"+ix["curso"].lower()+".md",s)
    intro="# Missões interdisciplinares\n\nIntegram habilidades para resolver um problema e justificar uma decisão. O contato inicial com outra disciplina não certifica seu domínio. Os pré-requisitos devem ser diagnosticados; as missões avançadas não são ponto de partida obrigatório para um iniciante.\n\n"
    intro+=table(["Missão","Problema","Fase","Disciplinas"],[(f'[{m["id"]}: {m["titulo"]}]({m["id"].lower()}.md)',m["problema"],m["fase"],", ".join(m["disciplinas"])) for m in missions])
    write("missoes/README.md",intro)
    for m in missions:
        s=f'# {m["id"]} — {m["titulo"]}\n\nProposta editorial. Fase: {m["fase"]}.\n\nProblema: {m["problema"]}\n\n'
        s+="## Habilidades requeridas\n\n"+"\n".join("- "+ul(next(u for u in skills if u["id"]==uid)) for uid in m["habilidades_requeridas"])+"\n\n"
        s+="## Como as disciplinas se conectam\n\n"+table(["Disciplina","Contribuição"],[(key,value) for key,value in m["contribuicoes"].items()])+"\n"
        if m["habilidades_introduzidas"]:s+="Habilidades apenas introduzidas neste contexto, sem certificação da disciplina inteira: "+", ".join(m["habilidades_introduzidas"])+".\n\n"
        s+="## Entregas\n\n"+"\n".join("- "+e for e in m["entregas"])+"\n\nTransferência: "+m["transferencia"]+"\n\nJulgamento prático: "+m["julgamento"]+"\n\nLimite: "+m["limite"]+"\n\n[Voltar às missões](README.md)\n"
        write("missoes/"+m["id"].lower()+".md",s)
    evidence="# Base pedagógica: evidências e limites\n\nPesquisa exploratória em 30/10/2026. Seleção: fontes primárias, editoras acadêmicas e guias institucionais pertinentes a aprendizagem ativa, multimídia, feedback e transferência. Não é revisão sistemática. A reorganização é proposta editorial e não teve eficácia medida com aprendizes.\n\n"
    for r in pedagogy:
        evidence+=f'## {r["id"]} — {r["titulo"]}\n\n{r["autoria"]}. Ano: {r["ano"] or "não identificado"}. Tipo: {r["tipo"]}. [Fonte original]({r["url"]}).'
        if r.get("doi"):evidence+=" DOI: "+r["doi"]+"."
        evidence+="\n\nLeitura: "+r["leitura"]+"\n\nSuporte delimitado: "+r["suporte"]+"\n\nAplicação proposta: "+r["aplicacao"]+"\n\nLimites: "+r["limites"]+"\n\nCorreções/retratações: NÃO VERIFICADO.\n\n"
    evidence+="As referências se referem principalmente à aprendizagem humana. O mesmo formato pode orientar tarefas de agentes, mas executar um arquivo não demonstra mudança dos pesos de um modelo, consciência ou sabedoria humana. Essa transposição é uma escolha de engenharia do projeto, não resultado estabelecido pelas fontes.\n"
    write("pedagogia/base-evidencias.md",evidence)
    export("data/habilidades.csv",["id","indice","item","disciplina","resultado_observavel","pre_requisitos","estado_editorial","validacao_cientifica","aula_local","perfil","curso"],skills)
    return {"habilidades":len(skills),"aulas_iniciais":ready,"indices":len(indices)}
