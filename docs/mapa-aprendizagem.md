# Mapa pedagógico com Understand Anything

Integração proposta em 31/10/2026, apoiada no [projeto oficial](https://github.com/Egonex-AI/Understand-Anything). Versão do plugin 2.9.8, código fixado em `4e6d3299017a7432da15957874992837a315c5b4`, licença MIT. A instalação foi executada no ambiente de trabalho desta sessão; não instala no computador pessoal de quem acessa o GitHub.

## Aprender com o mapa

1. Para estudar, comece pela [trilha inicial](../aprendizagem/comecar.md): variáveis, decisões, repetição, decomposição e missão M01. O tour do mapa completo apresenta a arquitetura; a exportação pedagógica preserva seu percurso de prática próprio.
2. Selecione uma habilidade e abra seu arquivo. Faça a previsão e a tentativa antes de consultar a solução.
3. Explore `depends_on`: a seta vai da habilidade para o pré-requisito. Diagnostique o que falta; a relação é uma proposta editorial.
4. Compare missões e disciplinas para explicar como duas áreas contribuem para a mesma decisão.
5. Consulte uma fonte candidata e verifique capítulos e direitos. Uma aresta `related` não confirma que a fonte sustenta uma afirmação.
6. Registre evidência conforme o [protocolo de progresso](../aprendizagem/progresso.md). Abrir nós, ler resumos e concluir um tour não comprova domínio.

A camada pedagógica contém os 16 eixos, 108 disciplinas, 447 habilidades, 29 referências, sete cursos e quatro missões: 611 nós. O mapa completo também contém a estrutura de arquivos e símbolos; consulte a [arquitetura do repositório](estrutura-repositorio.md). As camadas representam eixos e recursos; o peso das arestas é apenas visual, nunca nível de evidência ou proficiência. Os rótulos ROTEIRO/AULA_INICIAL continuam explícitos. Para navegação textual acessível, use o [catálogo de habilidades](../aprendizagem/habilidades.md) e os [pré-requisitos por disciplina](../curriculo/catalogo.md).

## Instalação local reproduzível

Requer Git, Node.js >=22 e pnpm >=10 já instalados. Estes comandos instalam dependências e compilam o visualizador oficial; não exigem chave de API. Escolha um diretório externo ao Computação Aberta para o código da ferramenta:

```bash
git clone https://github.com/Egonex-AI/Understand-Anything.git ../understand-anything
git -C ../understand-anything checkout 4e6d3299017a7432da15957874992837a315c5b4
cd ../understand-anything
pnpm install --frozen-lockfile
pnpm --filter understand-anything-viewer build
cd ../computacao-aberta
python3 scripts/mapa.py
node ../understand-anything/understand-anything-plugin/packages/viewer/bin/viewer.mjs . --no-open
```

Abra a URL completa com `?token=` impressa pelo servidor. Ele escuta somente em `127.0.0.1`; a URL desta sessão não corresponde ao localhost do seu computador. Encerre com Ctrl+C. O visualizador exibe dados locais sem chamar um modelo. O download do pacote pronto para v2.9.8 retornou HTTP 404 na pesquisa; por isso usamos a compilação do código fixado.

As skills de Codex são opcionais. O instalador oficial revisado `install.sh codex` cria links em `~/.agents/skills` e um link para a raiz do plugin. Ele atualiza o checkout e pode substituir links de mesmo nome; examine o script e conflitos antes de executar no seu computador. Reinicie a CLI/IDE para descoberta automática. Codex usa `$understand-dashboard`. A desinstalação é `bash install.sh --uninstall codex`; o checkout permanece.

## O que foi aplicado e seus limites

A camada pedagógica é um **adaptador determinístico**; a camada estrutural é produzida pela pipeline da skill `/understand`, com extração oficial, análise assistida, revisão de montagem, camadas e tour. Os JSON seguem o esquema oficial. O exportador pedagógico lê apenas os nove conjuntos de dados listados em `scripts/mapa.py`; a pipeline estrutural lê o inventário local autorizado. Não incluem progresso privado, credenciais, PDFs ou livros externos. A análise de arquivos não infere suporte científico para as referências candidatas.

`python3 scripts/gerar.py` regenera a camada pedagógica e a compõe com o snapshot estrutural, preservado em `.ua/structural-graph.json`. O SHA256 dos dados fica na descrição da exportação pedagógica; o snapshot estrutural registra a base Git e os hashes dos arquivos observados em `.ua/analysis.json`. A pipeline oficial também gera fingerprints e metadados. O gerador Python não substitui uma nova análise semântica quando os arquivos mudam. Atualização automática e hooks estão desativados. Siga o procedimento de preservação e recomposição no guia de arquitetura ao executar a skill novamente; a análise pode consumir tokens.

Recursos de busca semântica, chat e descoberta por agentes não foram ativados nem validados nesta integração. O painel e o tour apoiam exploração; sua eficácia pedagógica ainda precisa de avaliação com estudantes. O idioma dos dados é português; traduções completas da interface não são garantidas.

Os testes verificam cobertura, direção de pré-requisitos, caminhos, referências e determinismo. Conferir também o esquema oficial e os endpoints do visualizador após atualizar a versão. Dependências da ferramenta ficam fora deste repositório; o CI curricular continua somente com biblioteca padrão Python.

## Verificação da integração inicial (anterior à análise completa)

Em 31/10/2026: 42 testes Python passaram; validador registrou 8.350 verificações e 3.379 links locais, sem erros. `KnowledgeGraphSchema.safeParse` do código oficial aceitou o grafo. A instalação com lockfile e o build oficial do visualizador terminaram com sucesso. Teste HTTP local verificou HTML, grafo com 611 nós, prévia da primeira aula, 403 sem token e 404 para arquivo fora do mapa. O servidor de verificação foi encerrado. A interface não passou por inspeção visual automatizada nesta sessão; chat e busca semântica não foram testados.

Implementação acompanhada na [issue #5](https://github.com/aloisiocosta-professor/computacao-aberta/issues/5), sobre a reorganização do PR #4. A compilação oficial emitiu aviso de tamanho de bundle, sem impedir o build.
