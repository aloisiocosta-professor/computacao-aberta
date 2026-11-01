# Validação técnica 0.3.0

- Auditoria:447/447 unidades,894 questões,211 práticas numéricas e236 práticas de decisão; sem IDs, conceitos, exemplos ou conjuntos de questões exatamente duplicados.
- Node:715 testes passaram; interpretador, soluções de referência, rejeição de APIs/loops, progresso e todas as combinações alcançáveis de estado/evento do computador.
- Python:53 testes passaram; gerador, relações e barreira explícita de arquivos públicos, inclusive subpastas. Validador estrutural:9287 verificações e3840 links locais.
- TLC1.7.4 executado também pelos scripts vendorizados do repositório:7 estados,13 transições; quatro invariantes e ausência de deadlock. Relatório e grafo em statecharts/. Não prova equivalência completa do runtime com TLA+ nem comportamento de hardware.
- Navegador: estudo→duas questões→duas decisões→evidência demonstrativa→duas questões de retomada atingiu50/50 XP em abstração; programa resolver(a,b)=a+b aprovou quatro casos de variáveis e mostrou traço. Testadas ordem inválida e sequência +2,×3,STORE da figura, vista fechada/interna/traseira, rótulos e largura390px. Não foi feito estudo com alunos ou auditoria completa de acessibilidade.
- QA usa registros demonstrativos no navegador de teste, não evidência de aprendizagem real. A publicação deve ser confirmada pelo release.json e pelo workflow nativo Pages.
