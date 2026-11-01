# Conteúdos específicos — sinais, redes e engenharia de software

Data da elaboração: 01/11/2026. Escopo: 83 unidades dos eixos SIN, NET e SWE, inclusive os itens associados de MIT 6.0001, CS50, Missing Semester e Modern Robotics. Arquivo autoral: `data/conteudos-engenharia.json`.

## Estado e método

As unidades são propostas autorais introdutórias, com exemplos fictícios pequenos. Cada título tem conceito e exemplo distintos, duas questões com feedback, prática contextualizada e projeto de transferência. Não são transcrições de livros ou cursos. Os títulos/IDs vieram de `data/habilidades.json` e dos índices canônicos existentes; nenhum subitem externo foi acrescentado.

O material foi escrito com assistência de IA. Validação pedagógica e revisão humana especializada: **NÃO VERIFICADO**. Os exemplos não representam resultados empíricos. As fontes abaixo são referências de aprofundamento com consulta parcial; sua listagem não significa que sustentem integralmente todas as afirmações da unidade. Não houve leitura integral dos cursos, dos livros ou das RFCs, nem visualização integral de vídeos.

## Busca exploratória rastreável

Canal: busca web e abertura de páginas oficiais. Data: 01/11/2026. Não é revisão sistemática. Critérios: autoria institucional/projeto oficial, relação direta com tópico e disponibilidade de página pública. Foram excluídas páginas de terceiros quando havia fonte institucional equivalente.

Consultas literais:

- `site.modernrobotics.northwestern.edu chapters configuration space forward kinematics`
- `site.rfc-editor.org RFC 9110 HTTP semantics`
- `site.docs.pytest.org assertions fixtures parametrize`
- `site.owasp.org cheat sheet authentication secrets management`
- `site.ocw.mit.edu signals systems convolution sampling feedback linearity`
- `site.swebokwiki.org software requirements testing configuration management`
- `site.flask.palletsprojects.com quickstart route request`
- `site.missing.csail.mit.edu debugging profiling packaging shipping code`

## Fontes e limites de acesso

| Fonte primária | URL | Consulta efetiva e limite |
|---|---|---|
| MIT OCW — Signals and Systems | https://ocw.mit.edu/courses/res-6-007-signals-and-systems-spring-2011/pages/lecture-notes/ | Índice de notas e descrição dos temas consultados; PDFs e vídeos não lidos/assistidos integralmente. |
| Northwestern — Modern Robotics | https://modernrobotics.northwestern.edu/chapters/chapter2/ | Página de Configuration Space e índice de capítulos consultados. Livro e vídeos integrais não consumidos. |
| IETF/RFC Editor — HTTP Semantics | https://www.rfc-editor.org/rfc/rfc9110.html | Abstract e organização do documento consultados parcialmente; leitura integral e consulta a todas as erratas NÃO VERIFICADAS. |
| SWEBOK — Software Requirements | https://swebokwiki.org/Chapter_1%3A_Software_Requirements | Página/descrição do escopo consultadas; não corresponde à leitura integral do guia ou de todos os capítulos relacionados. |
| OWASP — Authentication Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | Consulta parcial da página oficial e descrição do escopo. Não é auditoria de conformidade ou segurança. |
| OWASP — Secrets Management | https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html | Consulta parcial da página oficial e descrição do ciclo de vida de segredos. |
| pytest — parametrização | https://docs.pytest.org/en/stable/how-to/parametrize.html | Consulta parcial da documentação oficial para aprofundamento de testes por exemplos. |
| Flask — Quickstart | https://flask.palletsprojects.com/en/stable/quickstart/ | Consulta parcial do recurso oficial sobre rotas/requisições. Não foi reproduzida uma implantação Flask. |
| MIT — Missing Semester 2026 | https://missing.csail.mit.edu/2026/ | Índice de aulas e descrições de ferramentas consultados; curso não assistido integralmente. |

Correções/retratações científicas: **NÃO VERIFICADO**. Estas fontes são documentação técnica e materiais didáticos; não foram selecionadas como estudos empíricos de eficácia pedagógica. Atualizações e erratas técnicas não foram auditadas exaustivamente.

## Verificações executadas

- Cobertura exata de 83 IDs do escopo, sem duplicação e com títulos obtidos dos índices canônicos.
- 83 conceitos distintos, com 70 a 95 palavras cada, e 83 enunciados de exemplos distintos.
- `validateLesson` de `plataforma/atividade.mjs`: zero erros nas 83 unidades.
- 24 práticas numéricas executadas com `evaluatePractice`; todas as soluções de referência passam os quatro casos definidos. A solução constante `return 0` não passa integralmente nenhuma dessas práticas.
- 59 jogos de decisão com duas rodadas e feedback por alternativa, incluindo cenários de limite. Gabaritos são decisões delimitadas ao cenário; não representam verdades universais de projeto.

Estas verificações avaliam estrutura e execução dos exemplos. Não demonstram aquisição de habilidade pelo estudante, correção científica integral ou aprovação humana.

## Pendências e uso

Revisão especializada das explicações, dificuldade, distrações e cenários de transferência; testes com estudantes; avaliação de acessibilidade no produto integrado; expansão dos exemplos pequenos para práticas completas de laboratório. O projeto da unidade exige artefato e justificativa próprios, preservando o registro do apoio recebido. Nenhum progresso pessoal foi preenchido.

## Complementação de aderência temática

Consultas adicionais em 01/11/2026: `site.gov.br/anpd dados pessoais pessoa identificada identificavel`; `site.sigsoft.org empirical standards experiments replication`; `site.docs.python.org socket HOWTO partial recv`. Fontes primárias selecionadas: [ANPD — Perguntas Frequentes](https://www.gov.br/anpd/pt-br/acesso-a-informacao/perguntas-frequentes), conceito de dado pessoal; [ACM SIGSOFT — Empirical Standards](https://www2.sigsoft.org/EmpiricalStandards/), apresentação e organização dos métodos; [Python — Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html), comunicação por sockets. Consulta parcial de apresentação, trechos ou descrições; nenhum documento integral foi declarado lido, nenhuma revisão jurídica ou aplicação integral dos padrões foi realizada.

Consultas de aderência em redes: `site.computer-networking.info "Computer Networking" "Wireless"`; `site.rfc-editor.org/rfc/rfc1812 "longest match"`; `site.rfc-editor.org/rfc/rfc1122 "layers"`. Foram selecionadas a [página autoral do livro aberto CNP3](https://www.computer-networking.info/) como referência de aprofundamento e a [RFC 1812](https://www.rfc-editor.org/info/rfc1812/) para a regra de prefixo mais específico. Apresentação, índice e trecho pertinente consultados, sem alegar leitura integral dos livros ou RFCs. As unidades de projeto, manutenção, configuração e qualidade ligam também ao [índice SWEBOK](https://swebokwiki.org/Main_Page), sem atribuir ao capítulo de requisitos a validação integral de outros temas.
