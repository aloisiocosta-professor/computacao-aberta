# Registro de validação

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
