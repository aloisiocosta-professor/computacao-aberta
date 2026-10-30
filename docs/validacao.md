# Registro de validação

Data: 30/10/2026. Escopo: pacote editorial inicial, antes de publicação remota.

| Verificação executada | Resultado | Limite |
|---|---|---|
| Validador estrutural offline | ATENDIDO: 3.107 verificações, sem erros | Não julga conteúdo científico |
| Links relativos | ATENDIDO: 885 links internos conferidos | URLs externas não auditadas em lote |
| IDs, referências, eixos e cursos | ATENDIDO | Existência de relação não comprova aderência científica |
| Grafo de pré-requisitos e ordem das etapas | ATENDIDO | Pré-requisitos ainda são proposta editorial |
| Detecção de ciclo deliberadamente injetado em cópia temporária | ATENDIDO | Nenhum dado do catálogo original foi alterado pelo teste |
| Geração determinística | ATENDIDO: hashes idênticos antes/depois | Não cobre disponibilidade futura de fontes |
| Sintaxe do workflow YAML | ATENDIDO: analisado com PyYAML já disponível | Execução do GitHub Actions não realizada |
| Correspondência temática das 17 siglas CS2023 | ATENDIDO estruturalmente | Cobertura de tópicos e competências NÃO VERIFICADA |
| Leitura integral de livros e aulas | NÃO ATENDIDO | Consulta em geral de apresentação, metadados e sumários |
| Revisão científica independente por eixo | NÃO VERIFICADO | Pareceres pendentes |
| Aprovação humana da proposta | NÃO VERIFICADO | Aceite do mantenedor pendente |
| Repositório remoto e CI remoto | NÃO ATENDIDO | A conexão GitHub não oferece criação de repositório |

O teste negativo verificou a capacidade do validador de rejeitar ciclos. Não prova que os pré-requisitos sejam pedagogicamente corretos. Nenhuma validação estrutural deve ser comunicada como aprovação científica.
