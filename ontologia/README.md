# Ontologia curricular com Open Ontologies

**Estado editorial: PROPOSTO. Validação estrutural: ATENDIDO nos casos executados. Certificado independente: CONFIRMADO no CI; execução local do checker indisponível.**

A ontologia torna explícito o significado das relações do currículo: uma disciplina pertence a um eixo, uma unidade tem pré-requisitos e uma referência pode ser apenas candidata. O [Open Ontologies](https://github.com/fabio-rovai/open-ontologies), versão fixada 2.1.0, consulta e valida essas relações. Não há afirmações de domínio por um estudante ou treinamento permanente de um agente.

## O que foi aplicado

| Camada | Arquivo | Finalidade |
|---|---|---|
| Vocabulário autoral | [Definições JSON](../data/ontologia.json) e [esquema RDF/OWL](esquema.ttl) | Classes, propriedades, nomes e limites |
| Dados | [Dados RDF](dados.ttl) e [currículo completo](curriculo.ttl) | Exportação dos JSON existentes, com arquivo e hash de origem |
| Restrições | [Formas SHACL](formas.ttl) | Cardinalidade, tipo dos alvos, estados e ciclos de pré-requisitos |
| Perguntas | [Contagem](consultas/contagem.rq), [pré-requisitos](consultas/pre-requisitos.rq), [missões](consultas/missoes.rq) e [fontes para metodologia](consultas/fontes-metodologia.rq) | Consultas SPARQL reproduzíveis |
| Proveniência | [Manifesto](manifesto.json) e [verificação local](verificacao.json) e [verificação no CI](verificacao-ci.json) | Contagens, hashes, resultados obtidos e limites |
| Evolução | [Verificador nativo](../scripts/verificar_ontologia.py) | Planejar, simular aplicação e reverter uma alteração em sandbox |

São 857 recursos: 16 eixos, 108 disciplinas, 447 unidades, 29 referências, sete cursos, quatro missões, 14 funções acadêmicas e 232 relações com fontes. O conjunto completo tem 10.884 triplas afirmadas. O vocabulário tem dez classes declaradas e 19 propriedades; contagens internas do motor podem incluir termos adicionais reconhecidos pelo seu critério de estatística.

`referenciaCandidata` preserva candidatura. `estadoDecisao` e `estadoEvidencia` são propriedades diferentes. Não usamos `owl:sameAs`, equivalência de cursos ou regras que convertam exposição em proficiência. As URNs são identificadores locais, não páginas publicadas ou endereços de serviços.

## Perguntas para estudar e manter

- O que preciso praticar antes de U-PRG01-04? A consulta retorna as três unidades anteriores; não declara que alguém as domina.
- Quais áreas cada missão integra? A consulta lista disciplinas, e a forma exige pelo menos duas.
- Que fontes estão propostas para metodologia? O resultado atual é vazio: nenhum vínculo dessa função foi preenchido. Isso não significa que as obras não discutam metodologia.
- Se eu retirar uma unidade, quais atividades dependem dela? A consulta local abaixo percorre dependências; o plano nativo avalia uma proposta RDF completa.

```bash
python3 scripts/ontologia.py --impacto U-PRG01-01
```

Esse comando não altera arquivos e não se apresenta como o cálculo semântico do motor. Diferentes relações respondem a perguntas diferentes: uma missão pode exigir uma habilidade ou apenas introduzi-la.

## Executar localmente

Para gerar RDF, basta Python já disponível:

```bash
python3 scripts/gerar.py
python3 scripts/ontologia.py
python3 scripts/validar.py
python3 -m unittest discover -s tests -v
```

Para executar o motor, obtenha o binário correspondente ao seu sistema na [release v2.1.0](https://github.com/fabio-rovai/open-ontologies/releases/tag/v2.1.0) e confira o SHA256 publicado. Os [metadados fixados](../ferramentas/open-ontologies.json) registram URL e hashes dos binários Linux x86_64 usados nesta execução. Não execute um binário Linux no Android ou Windows como se fosse compatível; a validação nativa automatizada deste projeto foi preparada para Linux x86_64.

Com os binários em um diretório externo ao repositório:

```bash
python3 scripts/verificar_ontologia.py --bin ../open-ontologies-bin/open-ontologies --checker ../open-ontologies-bin/oo-cert --saida ontologia/execucao.local/verificacao.json
```

O verificador usa `--no-connect`, diretório de estado temporário e comandos em batch para compartilhar o mesmo grafo. Valida contagens e consultas, executa SHACL, verifica dois erros intencionais, gera inferências RDFS e simula plan/apply/rollback. Não muda os JSON/TTL do currículo nem instala um servidor MCP nesta sessão. A release e seu checksum identificam o binário; ela não oferece `--version`, por isso o verificador usa `status`.

O [workflow dedicado](../.github/workflows/ontologia.yml) baixa apenas os dois binários fixados, verifica seus hashes e executa o mesmo roteiro. A aprovação estrutural do workflow é separada do resultado do checker, exibido no resumo. Nenhum serviço pago, chave de API, embedding, endpoint remoto ou publicação de progresso é necessário.

## Resultado observado e limites

O motor retornou zero ocorrências de lint no esquema, zero violações SHACL no currículo e as contagens esperadas por classe. O alvo inexistente produziu uma violação; o ciclo intencional, quatro. A remoção simulada de U-PRG01-01 foi classificada como risco alto, com 15 triplas afetadas. O estado alterado falhou em SHACL e o rollback restaurou a conformidade.

O plano não significa “todas as consequências conhecidas”: a conservatividade veio como `undecided_not_an_extension`, pois a proposta remove afirmações. A avaliação lógica não foi informada nesse retorno da release. O próprio relatório preserva esses limites. `apply` não é uma aprovação automática de um plano; aqui ele foi executado deliberadamente apenas na sandbox para testar a reversão.

A execução RDFS alcançou ponto fixo com 1.310 inferências e gerou um certificado temporário. O binário independente `oo-cert`, com SHA256 conferido, terminou com `uncaught exception: failed to locate application`. Essa execução local não verificou o certificado. No [CI remoto](https://github.com/aloisiocosta-professor/computacao-aberta/actions/runs/41224074176), o mesmo checker fixado retornou `ok: true`, confirmou 10.884 afirmações e 1.310 derivações e identificou `OOCert.certificate_sound`. Os dois resultados foram preservados separadamente. A aceitação é sobre as derivações a partir das premissas fornecidas, não sobre a verdade científica dessas premissas. O roteiro também testa a rejeição de uma conclusão adulterada quando o checker consegue executar. Os arquivos temporários são removidos ao terminar e podem ser regenerados pelo roteiro.

A conformidade mede estas restrições sobre estes dados; não estabelece verdade empírica, qualidade de uma referência ou aprendizagem. As obras vinculadas não foram lidas integralmente nesta integração. A revisão humana do vocabulário, das formas e dos vínculos científicos continua pendente.

## Relação com Understand Anything

O mapa visual existente e a ontologia têm funções complementares: o primeiro navega arquivos e habilidades; a segunda define tipos, relações e restrições consultáveis. Ambos derivam dos mesmos JSON autorais.

O snapshot estrutural do PR #8 foi preservado com seus hashes originais. Ele ainda não inclui a análise semântica dos novos scripts, formas e documentos desta integração; sua atualização está pendente e não foi simulada. A camada pedagógica continua sendo regenerada normalmente. Consultar o [guia de arquitetura](../docs/estrutura-repositorio.md) antes de reconstruir o snapshot com a skill.

## Fontes e escopo de consulta

Consulta exploratória em 31/10/2026: `github "Open Ontologies" "Rust" ontology`. Seleção do repositório oficial compatível com a imagem; leitura do README, SKILL.md, quickstart, lifecycle e trechos relevantes da CLI/batch. Documentação e nomes de ferramentas não equivalem a leitura integral do código, provas Lean ou artigos citados pelo projeto. Não usamos esses artigos como evidência científica aqui. Não foram verificadas correções/retratações acadêmicas: NÃO VERIFICADO.

Licença da ferramenta: MIT, preservada no projeto original. O vocabulário e a organização editorial seguem o licenciamento do Computação Aberta; obras e normas externas preservam seus próprios direitos.
