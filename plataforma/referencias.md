# Pesquisa de referências de interação

Consulta exploratória em 31/10/2026. Buscas: `site.codecombat.com learn coding game Python JavaScript`, `site:pythontutor.com visualize code execution`, `site:blockly.games programming games`, `site:codepip.com games flexbox froggy grid garden`. Selecionamos páginas dos próprios projetos para identificar recursos de interface e aprendizagem; não realizamos revisão sistemática nem avaliação comparativa de eficácia.

| Fonte primária consultada | Recurso observado na descrição oficial | Aplicação autoral |
|---|---|---|
| [CodeCombat: descrição](https://codecombat.zendesk.com/hc/en-us/articles/4410481859095-What-is-CodeCombat) e [jogo](https://codecombat.com/play) | Código digitado altera um cenário de jogo | Robô controlado por código; sem copiar níveis, engine ou personagens |
| [Blockly Games: apresentação](https://blockly.games/about?lang=pt-br) | Progressão de conceitos, laços/condições e transição a programação textual | Trilha curta por conceitos, desafios acessíveis e pistas |
| [Python Tutor: visualizador](https://pythontutor.com/visualize.html) | Navegação de estados de execução | Replay de estados das simulações e valores de variáveis; não replica stack/heap completo |
| [Codepip: catálogo](https://codepip.com/games/) | Tarefas visuais concretas ligadas a código | Objetivos visíveis, resultados e tentativa seguinte |

A apresentação do Blockly Games e as descrições oficiais foram consultadas. A tentativa de abrir o visualizador do Python Tutor retornou HTTP 403; a referência de recurso usa a descrição indexada da página, sem alegar teste prático. Não realizamos cursos, auditoria de acessibilidade nem assinatura dos produtos. Os exemplos são referências de interação, não suporte científico de que este protótipo ensina melhor.

## Skills pesquisadas

- **Modern Web Guidance:** aplicada para acessibilidade e interações em layouts complexos. Pesquisa pelo CLI oficial; guia de acessibilidade, semântica, foco, formulários, SVG, diálogos e fallback de desempenho consultados. Usamos HTML nativo e atualizações locais; não aplicamos content-visibility à área interativa por não ser necessário ao tamanho desta versão.
- **Sites:** consultada para fluxo de preparo e QA por preview gerenciado. A hospedagem escolhida pelo usuário é GitHub Pages; não criamos hospedagem alternativa no serviço Sites.
- **Game Development Studio:** consultada e considerada fora do escopo desta implementação, pois não houve produção/vendorização de assets, renderização offscreen de engine ou otimização de GPU. As cenas são SVG/CSS originais, apropriadas a um site estático.

Não instalamos um pacote de skills de origem desconhecida ou um serviço pago. O CLI de pesquisa Modern Web Guidance foi executado temporariamente pelo registro npm; o site publicado não depende dele. A skill local consultada anunciava versão de setembro; o CLI informou catálogo atualizado em outubro, e os guias retornados pelo CLI foram usados.

## Fontes de deployment

- [GitHub: workflows personalizados de Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).
- [GitHub: configurar a origem](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
- [Configure Pages: action.yml](https://github.com/actions/configure-pages/blob/v6.0.0/action.yml): habilitação inicial requer token com permissões adicionais ao GITHUB_TOKEN padrão; não criamos nem lemos credenciais.

Código, interface, desenho do robô, tabuleiros e atividades são autorais; links não implicam afiliação. Licenças originais dos projetos de referência não foram transferidas para este repositório. Avaliação científica, correções/retratações acadêmicas e aprovação humana desta implementação: NÃO VERIFICADO.
