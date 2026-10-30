# Como estudar e relacionar fontes à pesquisa

Estado: protocolo editorial proposto. A implementação organiza registros; não substitui leitura, revisão científica ou aprovação do pesquisador.

## Para aprender uma disciplina

1. Escolha o [percurso CC](../curriculo/percurso-cc.md) ou [EC](../curriculo/percurso-ec.md) e confira os pré-requisitos.
2. Abra a ficha e identifique o assunto e a habilidade que deseja demonstrar.
3. Abra o link “relações detalhadas desta disciplina”. Compare o escopo registrado da obra com o assunto da ficha; a relação inicial ainda é uma candidata.
4. Acesse a página original da obra. Confira edição, disponibilidade e idioma. O catálogo registra links e metadados; não hospeda o livro.
5. Selecione e leia o capítulo pertinente. Registre localização, síntese própria, limites e estado de leitura no [fichamento](../templates/fichamento.md).
6. Faça a atividade da ficha e explique o resultado. Uma lista de leituras não demonstra, por si só, domínio da habilidade.

Não é necessário instalar Git ou Python para navegar e ler. Os scripts são destinados à manutenção dos dados e páginas.

## Para organizar a pesquisa

Use as [14 funções das fontes](../bibliografia/funcoes.md). A mesma obra pode contribuir para mais de uma função, mas cada contribuição exige justificativa. Há um [índice por fonte](../bibliografia/por-fonte.md) e um [índice por relação](../bibliografia/relacoes.md).

A classificação por tema, conteúdo, habilidade e revisão foi herdada das referências candidatas. Introdução, problema, hipótese, objetivos, metodologia, considerações finais, resumo e sumário/índice estão disponíveis na taxonomia; não foram atribuídos automaticamente a cada obra. A função deve ser selecionada para um projeto concreto depois de examinar o suporte pertinente.

Objetivos pertencem ao projeto do pesquisador; resumo e considerações finais dependem do trabalho realizado. Não se inserem citações apenas para preencher essas partes. O sumário organiza o documento; pode-se indicar o sumário oficial de um livro para localizar capítulos.

## Três tipos de limitações

| Tipo | O que registrar | Exemplo de interpretação |
|---|---|---|
| acesso_leitura | O que foi ou não acessado/lido, com origem no registro de curadoria | Apenas apresentação consultada; texto integral pendente |
| relatada_na_fonte | Limitação efetivamente relatada pelo autor, com localização e atribuição | Só preencher depois de conferir o trecho; não inferir pelo título |
| proposta_para_estudo | Limite antecipado do estudo que se pretende fazer, com autoria da proposta | Possível restrição de generalização de um experimento pequeno |

As três categorias não são intercambiáveis. Um livro inacessível não demonstra fragilidade de seus resultados. Uma limitação de um único estudo não comprova automaticamente uma lacuna de toda a área.

## Sugestões de pesquisa

Uma sugestão deve registrar pergunta respondível, justificativa, autoria/origem, hipótese quando cabível, método, limites e estado de decisão. Diferencie recomendação do autor, ideia do pesquisador e proposta do assistente. Uma ideia só é adotada pelo usuário após decisão explícita; nenhuma das três sugestões iniciais representa essa adoção.

Os [exemplos cadastrados](../bibliografia/limitacoes-e-pesquisa.md) tratam de geração de testes, compreensão de programação e análise de sensibilidade bayesiana. São pontos de partida editoriais; não derivam de leitura integral nem são lacunas demonstradas. Hipóteses são previsões a testar, nunca resultados antecipadamente obtidos.

Antes de executar um estudo, delimitar objetivo → dados → coleta → análise → inferência → limites; conferir recursos, independência das unidades e autorizações pertinentes. Em pesquisa com participantes, verificar as exigências éticas antes da coleta.

## Manutenção dos registros

- Referências bibliográficas: data/referencias.json.
- Vínculos por disciplina e fonte: data/relacoes-fontes.json.
- Vocabulário das funções: data/funcoes-fontes.json.
- Modelo de relacionamento: [template](../templates/relacao-fonte.md).
- Modelo de pergunta de pesquisa: [template](../templates/sugestao-pesquisa.md).

CONFIRMADO se aplica ao elemento realmente conferido. Para marcar uma relação como suporte confirmado, registrar alegação e localização; o validador exige esses campos, mas não julga a suficiência científica do texto. A leitura pode ser parcial e o trecho estar localizado: não é necessário alegar leitura integral para registrar esse trecho. O protocolo do projeto de pesquisa pode exigir leitura integral de suas fontes centrais.

Ao atribuir uma limitação ou sugestão ao autor da fonte, registrar sua localização. Para declarar uma lacuna comprovada, registrar evidência confirmada e localização; essa condição estrutural é necessária, mas não suficiente para a avaliação científica de uma lacuna.

Após editar os dados, executar:

```bash
python3 scripts/gerar.py
python3 scripts/validar.py
python3 -m unittest discover -s tests -v
```

Não edite as páginas geradas como fonte principal: a geração seguinte as substitui. O CSV de relações é uma exportação dos JSON, adequada a consulta e filtragem.
