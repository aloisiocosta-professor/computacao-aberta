# Conteúdos específicos — teoria, hardware e sistemas

Consulta exploratória em 01/11/2026. Escopo: 79 unidades existentes dos eixos TEO, HWD e SYS, incluindo itens de Nand to Tetris e três itens de Berkeley sobre transações distribuídas. Não foram criados subitens de índices externos. Arquivo: `data/conteudos-sistemas.json`.

O material contém explicações introdutórias autorais de 92 a 137 palavras, exemplos fictícios com três passos, tabelas de raciocínio, duas questões com feedback por alternativa, prática temática e projeto. Há 31 práticas numéricas com quatro casos de teste e 48 jogos de decisão com duas rodadas. A função fornecida é uma solução de referência de um pequeno exercício, não uma implementação integral do tópico ou do curso.

## Estratégia de busca

Canal: busca web e abertura de fontes primárias oficiais. Consultas literais:

- `site.ocw.mit.edu 6.045 automata computability complexity lecture notes`
- `site.nand2tetris.org project 1 2 3 4 5 6 7 8 10 11 12`
- `site.pages.cs.wisc.edu remzi OSTEP processes virtualization persistence concurrency`
- `site.sre.google workbook implementing slos monitoring distributed systems`
- `site.freertos.org Documentation task fundamentals priority scheduling interrupt timers`
- `site.kernel.org documentation control groups namespaces containers`

Critérios: origem institucional/autoral, aderência temática explícita e acesso público. Trata-se de pesquisa exploratória de fontes para atividades introdutórias; não é revisão sistemática. Não se aplica filtro temporal de artigo científico a esses manuais técnicos. Correções e retratações: NÃO VERIFICADO; não foi executada uma consulta específica de erratas de cada obra.

## Acesso efetivamente obtido

| Fonte primária | Canal e resultado | Limite de uso |
|---|---|---|
| [MIT OCW — 6.045J, Lecture Notes](https://ocw.mit.edu/courses/6-045j-automata-computability-and-complexity-spring-2011/pages/lecture-notes/) | Página de índice e tópicos recuperada; identificação de autômatos, decidibilidade, reduções e complexidade | Não declarar leitura integral das notas PDF; fonte de delimitação e aprofundamento candidato |
| [Nand to Tetris — Projects](https://www.nand2tetris.org/course) | Índice oficial recuperado com a sequência dos doze projetos | Não declarar execução dos projetos oficiais, capítulos completos lidos ou conformidade ao hardware Hack completo |
| [OSTEP — página dos autores](https://pages.cs.wisc.edu/~remzi/OSTEP/) | Apresentação e organização em virtualização, concorrência e persistência recuperadas | Capítulos não foram todos lidos integralmente; exemplos e contas são autorais |
| [Software Foundations — Hoare Logic](https://softwarefoundations.cis.upenn.edu/plf-current/Hoare.html) | Página oficial recuperada parcialmente, com introdução a estados e correção | Não alegar prova formal mecanizada dos exercícios ou verificação completa de um programa real |
| [Yosys — Introduction](https://yosyshq.readthedocs.io/projects/yosys/en/latest/introduction.html) | Introdução oficial recuperada parcialmente | Não foi executada síntese, análise física ou fabricação; CMOS exige aprofundamento específico adicional |
| [FreeRTOS — RTOS Fundamentals](https://developer.freertos.org/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/01-RTOS-fundamentals) | Resultado primário com trechos de estados, multitarefa e escalonamento; URL inicial www.freertos.org falhou e foi substituída pela fonte oficial recuperada | Não foi executado RTOS nem ensaio de pior caso; cálculos temporais são modelos explicitamente idealizados |
| [Lamport — Paxos Made Simple](https://lamport.azurewebsites.net/pubs/paxos-simple.pdf) | PDF primário recuperado parcialmente, 14 páginas identificadas | Não declarar leitura integral ou prova de uma implementação; não usar esse texto como suporte integral do módulo de 2PC |
| [Google SRE — Implementing SLOs](https://sre.google/workbook/implementing-slos/) e [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) | Páginas oficiais recuperadas parcialmente | Cenários numéricos não são dados do Google; operação e observabilidade requerem validação em contexto |
| [Linux Kernel — Control Group v2](https://docs.kernel.org/admin-guide/cgroup-v2.html) | Documentação oficial recuperada parcialmente | Não cobre sozinha imagens, readiness, deploys ou segurança completa de containers; esses temas precisam de referências específicas complementares |

Fontes em cada unidade estão marcadas PARCIAL com seu uso efetivo. As explicações são propostas autorais; o vínculo bibliográfico é de descoberta/delimitação e não uma afirmação de suporte científico integral. Não há transcrição de capítulos ou instalação dos ambientes descritos.

## Verificações executadas

- 79 IDs exatos, sem duplicação, confrontados com `data/habilidades.json` e seus títulos de índice.
- Validação com `validateLesson` do módulo `plataforma/atividade.mjs`: nenhum erro estrutural.
- 31 soluções de referência executadas com `evaluatePractice`: todos os quatro casos por exercício aprovados.
- Programa constante `return 0` não aprova integralmente nenhuma das 31 atividades numéricas.
- Conceitos, exemplos e conjuntos de questões conferidos contra duplicações exatas no grupo; enunciados das questões de limitação incluem o caso concreto.

Essas verificações foram executadas pelo agente. Não são desempenho de estudante, revisão humana independente ou demonstração de eficácia pedagógica. Estado editorial: PROPOSTA_AUTORAL. Validação pedagógica: NÃO VERIFICADO. A cobertura de atividades específicas não equivale ao tratamento integral de disciplinas, cursos ou bibliografia.
