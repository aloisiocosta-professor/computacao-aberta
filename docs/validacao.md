# Registro de validação

## Proposta editorial 0.3.0 — aprendizagem por habilidades

Verificação local em 30/10/2026: ATENDIDO. Há 447 unidades para 359 tópicos autorais e 88 itens de índices externos, com vínculo um a um para todos os itens registrados. O escopo externo é parcial e explícito: a cobertura não inclui todos os subitens de todas as aulas.

Passaram 34 testes: 12 das relações de fontes, 17 de cobertura/progresso e cinco dos exemplos executáveis. Os testes rejeitam índice sem origem, item inexistente, cobertura incompleta, ciclos, visual sem descrição textual, independência com solução e retenção sem data posterior. Não demonstram aprendizagem de uma pessoa ou de um agente.

A geração foi novamente comparada por hashes e permaneceu determinística. O modelo de progresso começa vazio; o validador não inseriu desempenho em nome do usuário. Quatro aulas iniciais possuem exemplos e tarefas; 443 unidades ainda são roteiros. A avaliação de eficácia e a revisão científica/pedagógica permanecem NÃO VERIFICADAS. O resultado remoto específico será ligado ao PR da issue #3.

## Proposta editorial 0.2.0 — relações entre fontes e pesquisa

Validação local em 30/10/2026: ATENDIDO. Foram verificadas 232 relações entre disciplinas e referências e 14 funções acadêmicas. Os 12 testes de regressão passaram, incluindo rejeição de suporte confirmado sem localização, atribuição à fonte sem suporte localizado, relações ausentes/duplicadas e lacuna comprovada sem evidência confirmada.

Os índices, páginas por disciplina e CSV são gerados dos mesmos JSON. A geração foi comparada por hashes antes/depois de nova execução e permaneceu determinística. As relações herdadas continuam PROPOSTAS, com evidência NÃO VERIFICADA. As três sugestões iniciais são exemplos do assistente, não projetos adotados pelo usuário nem recomendações extraídas das obras.

O validador estrutural não certifica a veracidade de uma alegação, a suficiência de uma lacuna, a validade de um estudo ou os direitos de reprodução de um livro. A revisão científica e a leitura das fontes permanecem pendentes. A execução remota específica desta versão será registrada no PR relacionado à issue #1.

## Linha de base 0.1.0

Data: 30/10/2026. Escopo: pacote editorial inicial e primeira publicação remota.

| Verificação executada | Resultado | Limite |
|---|---|---|
| Validador estrutural offline | ATENDIDO: 3.107 verificações, sem erros | Não julga conteúdo científico |
| Links relativos | ATENDIDO: 885 links internos conferidos | URLs externas não auditadas em lote |
| IDs, referências, eixos e cursos | ATENDIDO | Existência de relação não comprova aderência científica |
| Grafo de pré-requisitos e ordem das etapas | ATENDIDO | Pré-requisitos ainda são proposta editorial |
| Detecção de ciclo deliberadamente injetado em cópia temporária | ATENDIDO | Nenhum dado do catálogo original foi alterado pelo teste |
| Geração determinística | ATENDIDO: hashes idênticos antes/depois | Não cobre disponibilidade futura de fontes |
| Sintaxe e execução do workflow | ATENDIDO: análise local e execução remota aprovada | Não valida cientificamente o currículo |
| Correspondência temática das 17 siglas CS2023 | ATENDIDO estruturalmente | Cobertura de tópicos e competências NÃO VERIFICADA |
| Leitura integral de livros e aulas | NÃO ATENDIDO | Consulta em geral de apresentação, metadados e sumários |
| Revisão científica independente por eixo | NÃO VERIFICADO | Pareceres pendentes |
| Aprovação humana da proposta | NÃO VERIFICADO | Aceite do mantenedor pendente |
| Repositório remoto e CI remoto | ATENDIDO | Branches main/develop publicadas; execução 41068161809 aprovada |

Evidência remota: [execução 41068161809](https://github.com/aloisiocosta-professor/computacao-aberta/actions/runs/41068161809), commit def41c5bb4a3e473a2eced2ddfa61b0a3b285309. A árvore inicial publicada foi comparada pelo identificador Git e coincide com os 150 arquivos do pacote original. Os números de verificações e links acima correspondem a essa linha de base.

O teste negativo verificou a capacidade do validador de rejeitar ciclos. Não prova que os pré-requisitos sejam pedagogicamente corretos. Nenhuma validação estrutural deve ser comunicada como aprovação científica.
