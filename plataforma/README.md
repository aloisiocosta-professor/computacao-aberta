## Versão0.3.0

447 unidades com conteúdo temático próprio, carregado sob demanda dos seis arquivos conteudos-*.json. Fluxo em cinco etapas com feedback, prática numérica/decisória e autoavaliação de projeto. Registro v3 separado de v2. Laboratório em computador-3d.html usa Colorfigures MIT vendorizado e máquina finita própria. Consulte ../docs/cobertura-tematica.md e ../docs/skills-instaladas.md.

# Plataforma de aprendizagem — versão 0.2.0

Jornada gamificada para todos os 447 itens do currículo, organizada em 108 disciplinas e 16 eixos. A página inicial apresenta caminhos, busca, filtros, progresso, retomadas e conquistas. Cada missão inclui objetivo do tópico, fontes, estudo, previsão com feedback, código testável, evidência e revisão. Os sete jogos da versão anterior permanecem em `laboratorio.html`.

A jornada reutiliza 16 modelos introdutórios, um por eixo, com casos e registros por unidade. O projeto é vinculado ao objetivo específico do item. Isso amplia a cobertura de missões, mas não equivale a criar 447 simuladores especializados ou aulas integrais. Os estados editoriais dos roteiros não foram alterados. Leia [análise funcional, cobertura e limites](engenharia-reversa.md).

O código é interpretado no navegador, sem servidor, conta ou chamadas de IA. XP mede etapas: estudo declarado (5), previsão correta (10), casos de código aprovados (20), evidência autoavaliada (5) e retomada correta (10), sem multiplicação por repetição. Não certifica domínio. O registro da jornada v2 preserva separadamente o v1 dos laboratórios.

## Aprender praticando

1. Leia a missão e faça uma previsão.
2. Edite o código no subconjunto de JavaScript descrito no guia.
3. Execute e observe o resultado. Pause, volte ou avance pelos passos visíveis da simulação e examine as variáveis.
4. Use uma pista se necessário. O registro conserva a indicação de apoio.
5. Troque o cenário quando disponível e explique como sua solução se transfere a outra situação.

O registro local indica casos executados e aprovados, sem certificar domínio ou autoria independente. As explicações são escritas pelo aprendiz, sem nota automática. O JSON exportado é um registro de simulador próprio; não equivale ao esquema de avaliações do currículo.

## Cobertura executável

| Desafio | Simulação | Unidade relacionada | Critério |
|---|---|---|---|
| Variáveis | Robô em grade | U-PRG01-01 | Usar valor de variável e alcançar a estação |
| Laços | Robô em grade | U-PRG01-03 | Executar repetição e alcançar a estação |
| Condições | Robô com curva e sensor | U-PRG01-02 | Decidir com condição e alcançar a estação |
| Funções | Robô com dois trechos | U-PRG01-04 | Reutilizar função no percurso |
| Ordenação | Barras e trocas | U-ALG01-01 | Ordenar duas listas, incluindo valores repetidos |
| Lógica digital | Circuito e tabela-verdade | U-MAT02-01 | Passar as quatro combinações de entradas |
| Consumo | Amostras, total e alerta | M01 / U-PRG01-04 | Testar abaixo, igual e acima do limite e lista vazia |

Essas correspondências são propostas editoriais. A atividade de ordenação complementa o estudo de vetores, sem representar a disciplina inteira. Tempos exibidos são estimativas de exploração do protótipo, não medidas validadas de aprendizagem. As 108 disciplinas e 447 unidades permanecem no catálogo; sete desafios não significam 447 aulas interativas completas.

## Linguagem e limites

O interpretador implementa um subconjunto de sintaxe JavaScript: números e booleanos, let/const, operações aritméticas e lógicas, if/else, for/while, funções com parâmetros e return, além das APIs específicas de cada simulação. Não implementa JavaScript integral, objetos, arrays de usuário, DOM, rede, imports, bibliotecas, Python ou execução nativa de programas. Não usa eval ou Function.

Há limites de 6.000 caracteres, 2.000 tokens, profundidade de análise, operações interpretadas, chamadas e ações. O interpretador é original e tem testes para interrupção de laços/recursão e rejeição de construções não oferecidas. Isso não é uma auditoria de segurança formal nem um ambiente para código arbitrário irrestrito.

A execução produz uma sequência limitada de estados associada a ações da simulação. O controle de passos navega por esses estados, não por todas as operações internas de uma implementação JavaScript real. Limites e erros aparecem no feedback, preservando as ações anteriores quando possível.

## Manter e publicar

Edite [os modelos de eixo](../data/gamificacao.json), [os desafios JSON](../data/desafios-plataforma.json) e os dados curriculares antes de regenerar os módulos e o catálogo. Código da interface fica aqui; [o empacotador](../scripts/construir_plataforma.py) publica somente uma lista explícita de arquivos. Não copia dados privados, dependências, relatórios ou o repositório inteiro para o site.

```bash
python3 scripts/gerar.py
node --test tests/web/*.test.mjs
python3 -m unittest discover -s tests -q
python3 scripts/construir_plataforma.py
```

O [workflow de preparo](../.github/workflows/pages.yml) verifica testes, gera `dist/` e guarda o artefato em pushes e PRs. A publicação usa a branch `gh-pages`, já permitida pela configuração do ambiente, e o workflow nativo “pages build and deployment” do GitHub. Para atualizar o site, o mantenedor publica os quinze arquivos públicos gerados nessa branch depois de validar a fonte; não há promessa de publicação automática de toda edição da branch de desenvolvimento. O deployment direto de feature/plataforma-visual foi recusado pela regra do ambiente e o fluxo foi corrigido para respeitar a origem permitida. As proteções foram preservadas. O site inclui `release.json` com versão e commit fonte. Não são criadas tags ou releases automaticamente.

Versão 0.1.0 publicada em [Computação Aberta](https://aloisiocosta-professor.github.io/computacao-aberta/). O [primeiro deployment verificado](https://github.com/aloisiocosta-professor/computacao-aberta/actions/runs/41226971693) publicou os arquivos gerados do commit 87aa2d1a970fdc7467b747923304690a8c8d0fe0.

O runtime não depende de pacotes externos, scripts remotos ou analytics. Progresso, rascunhos e explicações ficam em localStorage. A exportação é iniciada pelo usuário; o botão de apagar solicita confirmação. O recurso opcional de voz depende do navegador e pode usar o serviço de voz configurado nele; o texto está sempre disponível.

O layout tem alternativas textuais para as cenas, controles nativos, foco visível, diálogos com Escape, navegação por teclado e redução de movimento. Verificação em navegador não substitui avaliação com pessoas com deficiência ou testes em leitores de tela. Não alegamos conformidade integral com WCAG.

Leia a [pesquisa de referências](referencias.md). Os snapshots anteriores de Understand Anything e seus hashes foram preservados; sua reanálise para incluir os novos arquivos e a interface permanece pendente. A ontologia curricular continua sendo regenerada separadamente. A eficácia pedagógica desta versão ainda precisa de avaliação com estudantes.
