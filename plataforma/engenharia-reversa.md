# Análise funcional e jornada gamificada

Data: 31/10/2026. Fase: implementação da plataforma 0.2.0, vinculada à issue #13. Objetivo: transformar o currículo inteiro em missões acessíveis, preservando os limites entre atividade disponível, conteúdo especializado e evidência de aprendizagem.

## Método e limites da análise

Foi consultada a skill oficial [Reverse Engineer Anything, versão declarada 59](https://github.com/morluto/rea/blob/main/.agents/skills/reverse-engineer-anything/SKILL.md), do projeto morluto/rea. Aplicamos a parte de decomposição de perguntas e registro de observações, inferências e desconhecidos. Seu servidor MCP não está conectado nesta sessão: não houve execução do motor REA, descompilação, instalação de engine ou inspeção do backend do Khan Academy. A análise do repositório próprio usou os arquivos-fonte, como a própria skill recomenda para código disponível. A inspeção da experiência pública usou um navegador sem login.

A skill Modern Web Guidance foi aplicada às decisões de interface: guias `progress` e `forms`, obtidos pelo CLI. A skill Sites foi aplicada somente ao preview gerenciado para QA; o destino de publicação continua GitHub Pages, conforme a escolha do mantenedor. Nenhum serviço pago ou credencial foi utilizado.

## Registro de busca exploratória

Base/canal: busca web e páginas oficiais; data 31/10/2026. Consultas literais: `site.khanacademy.org mastery learning course unit mastery practice skills`; `"reverse engineer anything" skill github`; `site.support.khanacademy.org "What are Mastery levels?"`; `site.khanacademy.org/computing/computer-programming`. Critério de seleção: origem oficial e correspondência com organização de cursos, unidades e atividades. Não é uma revisão sistemática nem avaliação de eficácia pedagógica. Algumas páginas de suporte não foram recuperadas integralmente; seu conteúdo não foi usado para reconstruir um algoritmo de domínio.

Página principal consultada e inspecionada: [Computer programming — JavaScript and the web](https://www.khanacademy.org/computing/computer-programming?editor=no). Leitura: estrutura pública do curso, navegação e tipos de atividades; aulas e vídeos individuais não foram integralmente consumidos. Correções/retratações de estudos científicos: NÃO VERIFICADO, pois esta etapa é análise de produto, não síntese de evidências científicas.

## Evidências e decisões

| Pergunta | Observação ou limite | Implementação própria | Estado |
|---|---|---|---|
| Como o aluno encontra o conteúdo? | Navegação lateral por unidades e hierarquia de tópicos observadas no curso público | 16 eixos, 108 disciplinas, busca e filtros CC/EC | ATENDIDO estruturalmente |
| Como estudo e prática se relacionam? | A listagem pública distingue artigos, vídeos, exercícios, desafios e projetos | Cinco etapas: estudar, prever, programar, construir e retomar | ATENDIDO como fluxo |
| Como retomar o percurso? | O comportamento de uma conta autenticada não foi inspecionado | Última unidade e evidências guardadas localmente | DECIDIDO, implementação autoral |
| Como avaliar domínio? | Algoritmo interno e inferências de domínio do Khan não foram observados | Sem estado automático “dominado”; casos de modelo e autoavaliação separados | DECIDIDO |
| Como motivar sem competição? | Escolha de produto própria; eficácia não medida | XP por etapa uma única vez, conquistas locais e ausência de vidas/punição | DECIDIDO; eficácia NÃO VERIFICADA |
| Como transformar todos os itens em missões? | 447 IDs existentes nos dados canônicos | Exportação rastreável por item, objetivo, fontes, critérios, prática e projeto | ATENDIDO estruturalmente |
| Há 447 simuladores específicos diferentes? | Não: há 16 modelos introdutórios de eixo e sete jogos anteriores | Reutilização explícita, cenário/registro por unidade e tarefa do tópico | PARCIAL quanto à especialização temática |

Não copiamos marca, textos didáticos, exercícios, projetos, ilustrações ou código do Khan Academy. A semelhança buscada está na experiência de navegar e aprender por habilidades. Não existe vínculo institucional.

## Contrato da progressão

Cada unidade tem cinco etapas, com no máximo 50 XP: estudo declarado pelo aprendiz (5), previsão correta no modelo (10), programa aprovado nos casos (20), evidência textual autoavaliada (5) e retomada correta após prática aprovada (10). Repetir uma etapa não multiplica pontos. Erros não apagam pontos. Os estados descrevem etapas realizadas, e não competência certificada. Explicações, autoria e correção do projeto aguardam revisão humana.

A fila sugere retomada imediata quando ainda não houve revisão e nova retomada sete dias após uma revisão correta. A primeira data sugerida é calculada três dias após a prática, sem bloquear a revisão antecipada. Esses intervalos são escolhas editoriais, não um protocolo validado. A sessão mista avalia apenas os modelos selecionados, sem representar prova integral da disciplina.

O armazenamento é separado do registro v1 dos sete jogos. Não migramos aprovações entre atividades diferentes. Não há conta, sincronização entre dispositivos ou envio de evidências para terceiros. O aluno pode exportar o JSON local e apagar o registro com confirmação. Alterar localStorage pode alterar os registros; eles não são credenciais ou certificados.

## Cobertura e próximos critérios

ATENDIDO: todos os 447 itens possuem uma missão com objetivo e tarefa do tópico, recursos candidatos, previsão, prática codificável, evidência e retomada. A geração preserva estados editoriais, IDs, pré-requisitos e limites de leitura. O modelo é apresentado como ponte introdutória do eixo, sem substituir o conteúdo específico.

PARCIAL: aulas especializadas, variedade de simuladores por subtema e avaliação automática do projeto. Uma missão de criptografia, por exemplo, não recebe validação de criptografia por passar um modelo de teste de fronteiras. Aderência entre o modelo e cada tópico precisa de revisão especializada; a interface permite registrar quando a ponte não serve ao caso.

NÃO VERIFICADO: eficácia com estudantes, retenção de longo prazo, acessibilidade com leitores de tela e avaliação independente dos percursos. A cobertura estrutural automatizada não demonstra estes resultados.

Próximo resultado: substituir progressivamente as pontes por atividades específicas revisadas, começando pelas disciplinas iniciais, com exemplos, casos-limite, feedback e tarefa de transferência próprios. Manter cada unidade como proposta até revisão da área, sem renomear centenas de roteiros para aulas revisadas.

O snapshot estrutural anterior Understand Anything permanece preservado e defasado em relação aos novos arquivos da plataforma. Não foi anunciada sua atualização nesta entrega. A ontologia curricular continua gerada pelo fluxo existente.

## Verificações executadas nesta versão

- 52 testes Node aprovados: interpretador/jogos anteriores, 16 modelos novos, cobertura dos 447 IDs, respostas e cenários, limites de execução, registro corrompido, fila de retomada e XP idempotente.
- 51 testes Python aprovados: currículo, mapas, ontologia e empacotamento explícito dos arquivos públicos.
- Navegador: missão de programação percorrida pelas cinco etapas; retomada correta, persistência e 50 XP sem multiplicação por repetição; busca por redes e abertura de seu mapa; início de sessão mista; missão de eletrônica executada em iframe de 390 px. Largura útil e largura de rolagem foram ambas 375 px nessa missão móvel.
- Estes registros de QA são desempenho do agente em testes, sem preenchimento do progresso de Aloisio. Não foi realizado teste em aparelho físico nem auditoria completa de acessibilidade.
