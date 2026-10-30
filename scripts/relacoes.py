"""Renderização das relações editoriais e verificação de rastreabilidade."""
from collections import defaultdict
import json
STATES={"CONFIRMADO","PARCIAL","NÃO VERIFICADO"}
DECISIONS={"PROPOSTO","DECIDIDO","SUPERADO"}
LIMIT_TYPES={"acesso_leitura","relatada_na_fonte","proposta_para_estudo"}
ORIGINS={"assistente","pesquisador","fonte"}
def validate_relations(relations,subjects,refs,functions):
    """Devolve erros; não decide se o suporte textual é cientificamente suficiente."""
    errors=[];ids=set();pairs=set();suggestion_ids=set()
    sub={c["id"]:c for c in subjects};ref={r["id"]:r for r in refs};roles={r["id"] for r in functions}
    expected_pairs={(c["id"],r) for c in subjects for r in c["referencias_candidatas"]}
    for rel in relations:
        rid=rel.get("id","<sem ID>")
        def error(message):errors.append(rid+": "+message)
        if rid in ids:error("ID de relação duplicado")
        ids.add(rid)
        pair=(rel.get("disciplina"),rel.get("referencia"))
        if pair in pairs:error("par disciplina/referência duplicado")
        pairs.add(pair)
        if pair[0] not in sub:error("disciplina inexistente")
        if pair[1] not in ref:error("referência inexistente")
        roles_used=rel.get("funcoes_propostas",[])
        if not roles_used or not set(roles_used)<=roles:error("função acadêmica ausente ou inválida")
        if len(roles_used)!=len(set(roles_used)):error("função acadêmica duplicada")
        if not rel.get("justificativa"):error("justificativa ausente")
        if rel.get("status_decisao") not in DECISIONS:error("estado de decisão inválido")
        if rel.get("status_evidencia") not in STATES:error("estado de evidência inválido")
        if rel.get("status_evidencia")=="CONFIRMADO":
            if not rel.get("localizacao") or not rel.get("alegacao_sustentada"):
                error("suporte confirmado exige localização e alegação")
        if rel.get("uso_conteudo")!="somente_link_e_metadados":
            error("reprodução exige fluxo específico de direitos; não autorizada por esta relação")
        if not isinstance(rel.get("capitulos"),list):error("capítulos devem formar lista")
        limitations=rel.get("limitacoes",[])
        if not isinstance(limitations,list):error("limitações devem formar lista");limitations=[]
        for lim in limitations:
            kind=lim.get("tipo")
            if kind not in LIMIT_TYPES:error("tipo de limitação inválido")
            if not lim.get("descricao") or not lim.get("origem"):error("limitação sem descrição/origem")
            if lim.get("status_evidencia") not in STATES:error("estado de limitação inválido")
            if kind=="relatada_na_fonte":
                if lim.get("origem")!="fonte" or not lim.get("localizacao"):
                    error("limitação atribuída à fonte exige origem e localização")
            if kind=="proposta_para_estudo" and lim.get("origem") not in {"assistente","pesquisador"}:
                error("limitação proposta deve identificar quem a propõe")
        suggestions=rel.get("sugestoes_pesquisa",[])
        if not isinstance(suggestions,list):error("sugestões devem formar lista");suggestions=[]
        for sug in suggestions:
            sid=sug.get("id")
            if not sid or sid in suggestion_ids:error("ID de sugestão ausente ou duplicado")
            suggestion_ids.add(sid)
            if sug.get("origem") not in ORIGINS:error("sugestão sem origem válida")
            if sug.get("status_decisao") not in DECISIONS or sug.get("status_evidencia") not in STATES:
                error("estados de sugestão inválidos")
            if not sug.get("questao") or not sug.get("metodo_proposto") or not sug.get("justificativa"):
                error("sugestão exige questão, método e justificativa")
            if not isinstance(sug.get("limites_propostos"),list) or not sug.get("limites_propostos"):
                error("sugestão exige limites propostos")
            if sug.get("origem")=="fonte" and not sug.get("localizacao_na_fonte"):
                error("sugestão atribuída à fonte exige localização")
            if not isinstance(sug.get("lacuna_comprovada"),bool):error("indicar se lacuna foi comprovada")
            if sug.get("lacuna_comprovada") and (
                sug.get("status_evidencia")!="CONFIRMADO" or not sug.get("localizacao_na_fonte")
            ):error("lacuna comprovada exige evidência confirmada e localização")
    for pair in sorted(expected_pairs-pairs):errors.append("Relação candidata ausente: "+"/".join(pair))
    for pair in pairs-expected_pairs:errors.append("Relação fora das referências candidatas da disciplina: "+str(pair))
    return errors

def render_relations(subjects,refs,functions,relations,table,write,export):
    sub={c["id"]:c for c in subjects};ref={r["id"]:r for r in refs}
    roles={r["id"]:r for r in functions};by_sub=defaultdict(list);by_ref=defaultdict(list)
    for rel in relations:
        by_sub[rel["disciplina"]].append(rel);by_ref[rel["referencia"]].append(rel)
    def label(keys):return ", ".join(roles[k]["nome"] for k in keys)
    intro="Relações herdadas de referências candidatas, em estado PROPOSTO. Não comprovam que a fonte sustente uma alegação, uma lacuna ou a habilidade inteira. Assuntos e habilidades pertencem à ficha da disciplina; o escopo registrado da fonte é apresentado separadamente.\n\n"
    write("bibliografia/funcoes.md","# Funções das fontes no estudo e na pesquisa\n\nUma obra pode ter mais de uma função, desde que o suporte pertinente seja conferido. Não se atribuem automaticamente todas as funções a todas as obras.\n\n"+table(["ID","Função","Finalidade"],[(f["id"],f["nome"],f["finalidade"]) for f in functions])+"\nObjetivos, resumo, considerações finais e organização do sumário pertencem ao trabalho do pesquisador. Não há obrigação de inserir citação em cada um desses elementos. Livros ajudam na fundamentação; uma lacuna de pesquisa exige busca e evidências apropriadas, não apenas ausência de um tema em um livro.\n\n[Guia de uso](../docs/como-estudar-e-pesquisar.md)\n")
    rows=[]
    for rel in relations:
        c=sub[rel["disciplina"]];r=ref[rel["referencia"]]
        rows.append((f'[{rel["id"]}](relacoes/{c["id"].lower()}.md#{rel["id"].lower()})',c["nome"],r["titulo"],label(rel["funcoes_propostas"]),rel["status_decisao"],rel["status_evidencia"]))
    write("bibliografia/relacoes.md","# Relações entre disciplinas e fontes\n\n"+intro+table(["Relação","Disciplina","Fonte","Funções propostas","Decisão","Evidência"],rows)+"\nVer [funções](funcoes.md), [índice por fonte](por-fonte.md) e [limitações e pesquisa](limitacoes-e-pesquisa.md).\n")
    inverse="# Índice por fonte\n\n"+intro
    for r in refs:
        inverse+=f'## {r["id"]} — {r["titulo"]}\n\n[Origem da obra]({r["url"]}). Escopo: {r["escopo"]}. Acesso: {r["acesso"]}. Licença: {r["licenca"]}. Estado da leitura: {r["leitura"]}.\n\n'
        inverse+=table(["Disciplina relacionada","Funções propostas","Evidência"],[(f'[{sub[x["disciplina"]]["nome"]}](relacoes/{x["disciplina"].lower()}.md#{x["id"].lower()})',label(x["funcoes_propostas"]),x["status_evidencia"]) for x in by_ref[r["id"]]]) if by_ref[r["id"]] else "Sem relação por disciplina cadastrada. Isso não exclui possível uso após avaliação; a fonte não foi automaticamente associada a todas as disciplinas.\n"
        inverse+="\n"
    write("bibliografia/por-fonte.md",inverse)
    for c in subjects:
        page=f'# Fontes relacionadas — {c["id"]}: {c["nome"]}\n\n'+intro
        page+="**Assuntos da disciplina:** "+"; ".join(c["conhecimentos"])+".\n\n**Habilidade da disciplina:** "+c["habilidades"][0]+".\n\n"
        for rel in by_sub[c["id"]]:
            r=ref[rel["referencia"]]
            page+=f'## {rel["id"]}\n\n[{r["titulo"]}]({r["url"]}) — {r["autores"]}.\n\n'
            page+=f'**Escopo registrado da fonte:** {r["escopo"]}.\n\n**Funções propostas:** {label(rel["funcoes_propostas"])}.\n\n**Justificativa:** {rel["justificativa"]}\n\n'
            page+=f'**Decisão:** {rel["status_decisao"]}. **Evidência:** {rel["status_evidencia"]}. **Origem do vínculo:** {rel["origem"]}.\n\n'
            page+="**Capítulos selecionados:** "+("; ".join(rel["capitulos"]) if rel["capitulos"] else "a selecionar após leitura")+".\n\n"
            page+="**Localização de suporte:** "+(rel["localizacao"] or "não registrada")+". **Alegação sustentada:** "+(rel["alegacao_sustentada"] or "nenhuma alegação confirmada")+".\n\n"
            page+=f'**Acesso:** {r["acesso"]}. **Licença da obra:** {r["licenca"]}. Uso no repositório: apenas link e metadados, sem cópia do livro. A licença editorial do projeto não altera os direitos da obra.\n\n'
            page+="### Limitações registradas\n\n"
            page+=table(["Tipo","Descrição","Origem","Localização","Evidência"],[(l["tipo"],l["descricao"],l["origem"],l["localizacao"],l["status_evidencia"]) for l in rel["limitacoes"]]) if rel["limitacoes"] else "Nenhuma limitação cadastrada; isso não significa ausência de limitações.\n"
            page+="\n### Sugestões de pesquisa\n\n"
            if not rel["sugestoes_pesquisa"]:page+="Nenhuma sugestão cadastrada. Ausência de sugestão não comprova ausência de oportunidades de pesquisa.\n"
            for sug in rel["sugestoes_pesquisa"]:
                page+=f'**{sug["id"]} — origem: {sug["origem"]}; decisão: {sug["status_decisao"]}; evidência: {sug["status_evidencia"]}.**\n\n'
                page+=f'Pergunta: {sug["questao"]}\n\nJustificativa: {sug["justificativa"]}\n\n'
                page+="Hipótese: "+(sug["hipotese_proposta"] or "não definida; sua necessidade depende do desenho do estudo")+"\n\n"
                page+="Método proposto: "+sug["metodo_proposto"]+"\n\nLimites propostos:\n\n"+"\n".join("- "+l for l in sug["limites_propostos"])+"\n\n"
                page+="Lacuna comprovada: "+("sim, conferir suporte registrado" if sug["lacuna_comprovada"] else "não")+". Localização na fonte: "+(sug["localizacao_na_fonte"] or "não atribuída à obra")+".\n\n"
        page+="[Ficha da disciplina](../../disciplinas/"+c["id"].lower()+".md) · [Índice de relações](../relacoes.md) · [Como estudar e pesquisar](../../docs/como-estudar-e-pesquisar.md)\n"
        write("bibliografia/relacoes/"+c["id"].lower()+".md",page)
    overview="# Limitações e sugestões de pesquisa\n\nDistinguir três registros: **acesso/leitura**, **limitação relatada pela fonte** e **limitação proposta para um estudo**. Uma dificuldade de acesso ao livro não é uma limitação científica do trabalho descrito nele. Uma sugestão do assistente não é uma lacuna demonstrada nem uma decisão do usuário.\n\n"
    reported=[(x,l) for x in relations for l in x["limitacoes"] if l["tipo"]=="relatada_na_fonte"]
    overview+=f"Limitações atribuídas às fontes cadastradas: {len(reported)}. Na migração inicial, foram preservados limites de acesso/leitura; não foram inventadas limitações de resultados de obras não lidas integralmente.\n\n"
    if reported:overview+=table(["Relação","Limitação","Localização","Evidência"],[(x["id"],l["descricao"],l["localizacao"],l["status_evidencia"]) for x,l in reported])+"\n"
    overview+="## Exemplos de perguntas para investigação\n\nPropostas editoriais, não resultados ou projetos adotados pelo usuário. Cada estudo exige verificação de bibliografia, recursos, desenho e autorizações pertinentes antes da execução.\n\n"
    overview+=table(["Relação","Pergunta","Origem","Decisão","Evidência"],[(f'[{rel["id"]}](relacoes/{rel["disciplina"].lower()}.md#{rel["id"].lower()})',s["questao"],s["origem"],s["status_decisao"],s["status_evidencia"]) for rel in relations for s in rel["sugestoes_pesquisa"]])
    overview+="\n[Modelo de fichamento](../templates/fichamento.md) · [Modelo de sugestão](../templates/sugestao-pesquisa.md)\n"
    write("bibliografia/limitacoes-e-pesquisa.md",overview)
    flat=[]
    for rel in relations:
        c=sub[rel["disciplina"]];r=ref[rel["referencia"]]
        flat.append({**rel,"disciplina_nome":c["nome"],"assuntos_da_disciplina":c["conhecimentos"],"habilidades_da_disciplina":c["habilidades"],"fonte_titulo":r["titulo"],"fonte_url":r["url"],"fonte_escopo":r["escopo"],"acesso":r["acesso"],"licenca":r["licenca"],"limitacoes":json.dumps(rel["limitacoes"],ensure_ascii=False),"sugestoes_pesquisa":json.dumps(rel["sugestoes_pesquisa"],ensure_ascii=False)})
    export("data/relacoes-fontes.csv",["id","disciplina","disciplina_nome","assuntos_da_disciplina","habilidades_da_disciplina","referencia","fonte_titulo","fonte_url","fonte_escopo","funcoes_propostas","justificativa","capitulos","localizacao","alegacao_sustentada","status_decisao","status_evidencia","acesso","licenca","uso_conteudo","limitacoes","sugestoes_pesquisa"],flat)
