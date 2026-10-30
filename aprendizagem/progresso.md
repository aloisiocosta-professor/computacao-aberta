# Progresso por evidências

Não há perfil de desempenho preenchido para o usuário. O arquivo data/progresso.exemplo.json começa com registros vazios. Faça uma cópia local chamada progresso.local.json; esse nome é ignorado pelo Git para reduzir publicação acidental. Você decide quais artefatos quer compartilhar.

| Estado | Significado no projeto | Evidência necessária |
|---|---|---|
| nao_iniciado | Ainda não houve atividade registrada | Nenhuma |
| exposicao | Houve leitura, vídeo, áudio ou contato inicial | Não implica habilidade adquirida |
| pratica_assistida | Houve tentativa com suporte declarado | Artefato, apoio, avaliador e justificativa |
| desempenho_independente | Caso resolvido sem pistas ou cópia | Artefato e critérios registrados, apoio nenhum |
| transferencia_demonstrada | Aplicação em outro contexto | Registro independente anterior e novo contexto identificado |
| retencao_verificada | Retomada em outro momento | Registro independente anterior e data posterior |

Critérios mínimos para registrar os três últimos estados: correção, explicação, representação e limites. São critérios editoriais do projeto; seu preenchimento não autentica artefatos nem substitui avaliação. Autoavaliação, ferramenta e revisão humana devem ter seu tipo identificado no campo avaliador. Nunca registrar o trabalho de um agente como desempenho independente do humano.

## Formato de um registro

Campos: id, unidade, estado, data em formato AAAA-MM-DD, apoio (nenhum/pista/exemplo/solucao/nao_informado), artefatos (lista de caminhos ou URLs), avaliador, justificativa, criterios_atendidos (correcao/explicacao/representacao/limites), contexto e registro_anterior quando aplicável.

O campo avaliador deve identificar o tipo e a pessoa/ferramenta responsável, em texto ou objeto descritivo. Uma transição avançada não é feita pelo fato de os testes do repositório passarem; o registro pertence ao desempenho do aprendiz numa tarefa concreta.

Para transferência, use registro_anterior com ID de uma evidência independente da mesma unidade e descreva um contexto diferente. Para retenção, a retomada deve ter data posterior à evidência anterior. Não foi adotado um intervalo universal de revisão nem uma promessa de retenção permanente.

```bash
python3 scripts/trilhar.py plano
python3 scripts/trilhar.py plano --disciplina PRG01
python3 scripts/trilhar.py unidade U-PRG01-01
python3 scripts/trilhar.py verificar-progresso progresso.local.json
```

A ferramenta consulta dados e verifica a estrutura do registro; não executa código do aprendiz nem certifica aquisição de conhecimento. A autenticidade, a independência e a qualidade das evidências requerem verificação apropriada ao contexto.
