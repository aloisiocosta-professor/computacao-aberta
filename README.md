# Computação Aberta

**Aprender para conseguir fazer, explicar e decidir.** Um ambiente aberto de aprendizagem prática em Ciência da Computação e Engenharia de Computação, para pessoas e para tarefas verificáveis de agentes de IA.

O objetivo principal é transformar cada item registrado de índice em uma unidade de habilidade: diagnosticar, representar, tentar, receber feedback, aplicar em outro contexto e reconhecer limites. Ler, ver, ouvir e escrever são meios de construção do conhecimento; o progresso depende de evidências do que o aprendiz consegue fazer.

**Versão editorial 0.3.0 — proposta em revisão, 30/10/2026.** Curadoria e atividades produzidas com assistência do ChatGPT. Avaliação científica/pedagógica independente pendente. O projeto não emite diploma nem certifica sabedoria, consciência ou treinamento permanente de modelos.

## Comece pela prática

| Se você quer… | Abra |
|---|---|
| Começar sem formação prévia presumida | [Trilha inicial](aprendizagem/comecar.md) |
| Fazer a primeira atividade agora | [Representar e atualizar valores](unidades/primeiros-passos/01-variaveis.md) |
| Entender a estrutura do repositório | [Arquitetura e manutenção](docs/estrutura-repositorio.md) |
| Explorar relações visualmente | [Mapa pedagógico local](docs/mapa-aprendizagem.md) |
| Consultar conceitos e impacto de mudanças | [Ontologia curricular](ontologia/README.md) |
| Encontrar uma habilidade | [Catálogo de habilidades](aprendizagem/habilidades.md) |
| Integrar áreas em um problema | [Missões interdisciplinares](missoes/README.md) |
| Registrar o que consegue fazer | [Progresso por evidências](aprendizagem/progresso.md) |
| Usar um tutor humano ou agente | [Protocolo de tutoria e avaliação](agentes/PROTOCOLO.md) |

Você pode começar no navegador, com papel e lápis. Python e Git são opcionais para quem vai apenas estudar; a manutenção e os exemplos executáveis usam ferramentas já disponíveis, sem dependências Python externas ou chamadas pagas.

## Estrutura e cobertura real

| Camada | Conteúdo atual | Estado |
|---|---|---|
| Disciplinas | 108, em 16 eixos | Organização curricular proposta |
| Índices autorais | 359 tópicos das fichas | Numerados localmente; não são índices oficiais externos |
| Índices de cursos | 88 itens em sete recursos | Recorte de primeiro nível; subitens internos pendentes |
| Unidades de habilidade | 447 vínculos item → unidade | 4 aulas iniciais e 443 roteiros a desenvolver/revisar |
| Missões | 4 problemas integradores | Propostas com contribuições por disciplina |
| Fontes relacionadas | 232 relações e 14 funções acadêmicas | Candidatas; suporte científico não confirmado automaticamente |

Confira o [relatório de cobertura](aprendizagem/cobertura.md). Nenhuma aula foi declarada assistida e nenhum progresso pessoal foi preenchido. Conhecer os títulos de um índice não significa ter lido seu conteúdo. As aulas iniciais têm exemplos e tarefas; os roteiros exigem um exemplo concreto e revisão antes de serem anunciados como aulas completas.

## Como uma unidade funciona

Problema e previsão → modelo visual com descrição textual → exemplo guiado → prática com apoio decrescente → tarefa independente → evidência e feedback → transferência, decisão e retomada.

A pessoa ou o agente precisa justificar escolhas e reconhecer uma condição em que o modelo deixa de servir. Chamamos isso de julgamento prático, como objetivo operacional do projeto; não é medida validada de sabedoria.

Leia a [fundamentação pedagógica](pedagogia/fundamentos.md), a [base de evidências e limites de leitura](pedagogia/base-evidencias.md) e o [registro da pesquisa](pedagogia/buscas.md). A mesma estrutura de unidade pode orientar humanos e agentes, com critérios próprios de avaliação e atribuição do desempenho.

## Consultar disciplinas e fontes

- [Catálogo de disciplinas](curriculo/catalogo.md), [eixos](curriculo/eixos.md), [percurso CC](curriculo/percurso-cc.md) e [percurso EC](curriculo/percurso-ec.md).
- [Matrizes institucionais](matrizes/fontes-institucionais.md), [amostras rastreáveis](matrizes/amostras-rastreaveis.md) e [correspondências propostas CS2023](matrizes/correspondencias-cs2023.md).
- [Bibliografia](bibliografia/catalogo.md), [cursos](bibliografia/cursos.md), [fontes por função](bibliografia/funcoes.md), [relações](bibliografia/relacoes.md) e [índice por fonte](bibliografia/por-fonte.md).
- [Limitações e sugestões de pesquisa](bibliografia/limitacoes-e-pesquisa.md), [como estudar e pesquisar](docs/como-estudar-e-pesquisar.md) e [filtro de e-books](bibliografia/filtro-ebooks.md).

A [Universidade Livre](https://github.com/Universidade-Livre/ciencia-da-computacao) permanece a referência principal de orientação e descoberta. As matrizes, livros e cursos complementam a organização autoral. O [gist indicado pelo usuário](https://gist.github.com/baiwfg2/af827b8b75eebf8ab29f5531a0d265ce?permalink_comment_id=3896162) é usado para descoberta com verificação de origem e direitos por obra. Não hospedamos livros de terceiros. Ver [atribuições](NOTICE.md) e [curadoria](docs/curadoria.md).

## Para agentes e mantenedores

As instruções podem ser consultadas de forma estruturada:

```bash
python3 scripts/trilhar.py plano
python3 scripts/trilhar.py unidade U-PRG01-01
python3 scripts/trilhar.py verificar-progresso data/progresso.exemplo.json
```

Esses comandos não executam código do aprendiz nem certificam aquisição de habilidade. Leia [AGENTS.md](AGENTS.md) e o protocolo antes de tutorar ou avaliar. Artefatos de um agente não são evidência de desempenho independente do humano.

Para editar, altere primeiro os JSON em data/ e regenere as páginas. Índices, unidades e perfis ficam separados para preservar origem, cobertura e revisão. CSV e BibTeX são exportações de consulta.

```bash
python3 scripts/gerar.py
python3 scripts/validar.py
python3 -m unittest discover -s tests -v
```

Ver [validação](docs/validacao.md), [decisões](docs/decisoes.md), [pendências](docs/backlog.md) e [CONTRIBUTING](CONTRIBUTING.md). Fluxo: feature/*, PR ligado à issue, revisão, develop e main. Versões editoriais usam SemVer, sem criar tags ou releases automaticamente. A reorganização está ligada à issue #3 e continua as relações de fontes propostas no PR #2.

Código original: MIT. Documentação e organização editorial originais: CC BY 4.0. Obras vinculadas preservam seus próprios direitos. Ver [licenciamento](LICENSE).
