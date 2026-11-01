# Complemento de programação — índices de cursos externos

Data: 01/11/2026. Escopo: os 19 IDs recebidos em `programacao-pendente.json`, sem criação de títulos de índice novos. O complemento está em `conteudos-programacao-complemento.json` para integração pelo mantenedor. Não foi alterado `data/conteudos-programacao.json`.

## Produção e verificação

- 19 conceitos autorais específicos, entre 86 e 119 palavras, com exemplos fictícios e três passos verificáveis.
- 38 questões específicas, cada uma com quatro alternativas e feedback individual; a segunda preserva uma limitação do caso.
- 10 práticas numéricas com quatro casos cada, com ao menos duas saídas distintas por prática; todas as soluções executadas pelo interpretador limitado do projeto.
- 9 práticas de decisão, cada uma com duas rodadas; posições de respostas variam por unidade e rodada.
- Projetos pedem artefatos particulares do tópico, uma nova entrada e reconhecimento dos limites.
- `validateLesson` e `evaluatePractice`, em `plataforma/atividade.mjs`, executados sem erros. Comparação exata de conceitos, exemplos e conjuntos de questões com as 53 unidades existentes: sem duplicações.

O pequeno modelo JavaScript de uma atividade sobre C, Python ou Scratch reproduz somente a intenção algorítmica explicitada. Não oferece runtime dessas linguagens, execução dos projetos externos, tradução completa de Jack ou conformidade total de compilador.

## Fontes e acesso

Canal: abertura direta, via ferramenta de pesquisa web, das páginas oficiais abaixo. Não houve consulta bibliográfica por strings nesta subtarefa. Critérios: origem oficial e correspondência temática com os títulos pendentes. Leitura PARCIAL: páginas e trechos recuperados; não foram lidos integralmente os cursos, slides, livros ou todas as páginas dos tutoriais. Os exemplos são autorais, não cópias de exercícios dos cursos.

| Fonte | Parte identificada | Uso delimitado |
|---|---|---|
| [MIT OCW — 6.0001, Lecture Slides and Code](https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/pages/lecture-slides-code/) | Página oficial de recursos e tópicos | Delimitação do índice externo; não declarar que aulas foram assistidas |
| [Python — Data Structures](https://docs.python.org/3/tutorial/datastructures.html) | Estruturas de dados | Referência oficial para listas, mutabilidade e estruturas; não cobre todo o tutorial |
| [Python — Classes](https://docs.python.org/3/tutorial/classes.html) | Instâncias, métodos e herança | Recorte de orientação a objetos, sem afirmar análise de todos os mecanismos de Python |
| [Python — More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html) | Controle de fluxo | Delimitação de for/range; o laboratório é um modelo autoral limitado |
| [CS50 — Week 1](https://cs50.harvard.edu/x/notes/1/) | C | Conceitos introdutórios de tipos e divisão; sem compilação nativa nesta tarefa |
| [CS50 — Week 2](https://cs50.harvard.edu/x/notes/2/) | Arrays | Índices e limites; não representar todo o curso ou toda a linguagem C |
| [CS50 — Week 4](https://cs50.harvard.edu/x/notes/4/) | Memory | Referência para ponteiros e memória; exemplo de vida útil é conceitual |
| [Scratch — Ideas](https://scratch.mit.edu/ideas) | Página de ideias | URL identificada; recuperação mínima de três linhas, sem conteúdo interno dos tutoriais. Somente descoberta; não foi executado o editor de blocos |
| [Nand to Tetris — Project 9](https://www.nand2tetris.org/project09) | Project 9: High-Level Programming | Distinguir programa Jack e compilador; não afirmar execução do projeto oficial |

A descoberta de uma página oficial não valida integralmente cada alegação técnica. A aderência detalhada dos recursos e a eficácia das atividades exigem revisão especializada. Correções/retratações e erratas de cada material: NÃO VERIFICADO nesta subtarefa.

Estado editorial: PROPOSTA_AUTORAL. Validação pedagógica: NÃO VERIFICADO. Testes foram executados por agente e não representam aprendizagem do estudante ou revisão humana independente.
