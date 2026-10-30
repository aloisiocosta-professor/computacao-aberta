# Computação Aberta

Currículo aberto e independente para estudar **Ciência da Computação e Engenharia de Computação**, em português, com fontes rastreáveis e materiais complementares.

**Versão editorial 0.1.0 — proposta inicial, 30/10/2026.** Curadoria produzida com assistência do ChatGPT; avaliação científica e aceite humano pendentes. O projeto não emite diploma, não concede equivalência acadêmica e não representa instituições consultadas.

## Comece aqui

- [Catálogo: 108 disciplinas](curriculo/catalogo.md), em [16 eixos](curriculo/eixos.md).
- [Percurso de Ciência da Computação](curriculo/percurso-cc.md) e [Engenharia de Computação](curriculo/percurso-ec.md).
- [Fontes curriculares e matrizes institucionais](matrizes/fontes-institucionais.md); [amostras rastreáveis](matrizes/amostras-rastreaveis.md).
- [Correspondências propostas com CS2023](matrizes/correspondencias-cs2023.md).
- [29 referências bibliográficas](bibliografia/catalogo.md), [sete cursos/conjuntos de aulas](bibliografia/cursos.md) e [filtro de e-books](bibliografia/filtro-ebooks.md).
- [Metodologia](docs/metodologia.md), [curadoria](docs/curadoria.md), [buscas](docs/buscas.md), [decisões](docs/decisoes.md) e [pendências](docs/backlog.md).

## O que cada disciplina registra

Tema/eixo → conhecimentos → habilidade observável → pré-requisitos → metodologia → atividade e avaliação → cursos → referências candidatas → limites de verificação.

As 108 disciplinas compõem um catálogo extensível, não a soma exaustiva de todas as disciplinas de todas as universidades. Os percursos iniciais selecionam 57 disciplinas para CC e 67 para EC, com 32 aprofundamentos opcionais no catálogo; há sobreposição entre os percursos. Etapas são camadas lógicas, não semestres. Não foram atribuídas cargas horárias fictícias.

## Fontes e autoria

A [Universidade Livre](https://github.com/Universidade-Livre/ciencia-da-computacao) é a referência principal de orientação e descoberta. CS2023, CE2016, SBC e matrizes institucionais ampliam a comparação. A taxonomia, fichas e habilidades deste projeto são propostas autorais, não currículos oficiais transcritos. Ver [atribuições](NOTICE.md).

O [gist indicado](https://gist.github.com/baiwfg2/af827b8b75eebf8ab29f5531a0d265ce?permalink_comment_id=3896162) é uma lista de descoberta; os destinos são filtrados por origem e condições de acesso. Não hospedamos livros de terceiros. Leitura gratuita não implica licença para redistribuir.

## Editar e verificar

Requer Python 3 e Git já disponíveis. Não há dependências Python externas, instalação automática ou chamada paga.

```bash
python3 scripts/gerar.py
python3 scripts/validar.py
```

Edite primeiro os JSON em `data/` e regenere os documentos. CSV e BibTeX são exportações de consulta; os registros bibliográficos ainda requerem revisão antes de uso em artigo.

## Participar e versionar

Leia [CONTRIBUTING](CONTRIBUTING.md). Fluxo: branches `main`, `develop` e `feature/*`; Conventional Commits; SemVer para versões editoriais. Alterações devem apontar uma issue e critérios de aceite. A versão 0.1.0 não implica tag ou release publicada.

## Estado atual

- Estrutura e dados iniciais: implementados.
- Validação automatizada estrutural: ver [relatório](docs/validacao.md).
- Leitura integral das obras e auditoria de todas as aulas: pendentes.
- Cobertura integral de competências SBC/CE2016/CS2023: não verificada.
- Publicação no GitHub e execução remota do CI: pendentes.

Código original: MIT. Documentação e organização editorial originais: CC BY 4.0. Obras externas conservam suas próprias condições. Ver [licenciamento](LICENSE).
