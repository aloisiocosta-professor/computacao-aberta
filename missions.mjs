// Gerado de data/desafios-plataforma.json.
export const missions=[
  {
    "id": "variaveis",
    "title": "Uma distância, uma variável",
    "topic": "Variáveis",
    "kind": "rover",
    "unit": "U-PRG01-01",
    "discipline": "PRG01",
    "minutes": "5–10 min",
    "goal": "Leve o robô até a estação verde. A variável passos controla quantas casas ele anda.",
    "predict": "Antes de executar: com passos igual a 2, em qual coluna o robô vai parar?",
    "starter": "// Ajuste a distância até a estação.\nlet passos = 2;\nmover(passos);",
    "hint": "O robô começa na coluna 1 e a estação está na coluna 4. Quantas casas separam os dois?",
    "concept": "Uma variável dá um nome a um valor. Mudar esse valor altera o comportamento do programa.",
    "transfer": "Mova a estação uma casa para a direita usando “Outro cenário”. Qual valor precisa mudar?",
    "grid": [
      "######",
      "######",
      "######",
      "#....#",
      "######"
    ],
    "start": [
      1,
      3,
      1
    ],
    "goalAt": [
      4,
      3
    ],
    "variantGoal": [
      3,
      3
    ],
    "require": "variableReads",
    "estado_editorial": "PROTOTIPO_INTERATIVO",
    "avaliacao_pedagogica": "NÃO VERIFICADO"
  },
  {
    "id": "repeticao",
    "title": "Repita a ideia, não as linhas",
    "topic": "Laços",
    "kind": "rover",
    "unit": "U-PRG01-03",
    "discipline": "PRG01",
    "minutes": "8–12 min",
    "goal": "Alcance a estação com um laço for. Observe o contador i mudar a cada repetição.",
    "predict": "Quantas vezes o corpo do laço será executado quando i < 2?",
    "starter": "for (let i = 0; i < 2; i++) {\n  mover();\n}",
    "hint": "O contador começa em 0. Para andar quatro casas, ele deve assumir os valores 0, 1, 2 e 3.",
    "concept": "Um laço combina estado inicial, condição e atualização. A condição é conferida antes de cada repetição.",
    "transfer": "Troque o cenário. Ajuste a condição e explique por que i começa em zero.",
    "grid": [
      "#######",
      "#######",
      "#######",
      "#.....#",
      "#######"
    ],
    "start": [
      1,
      3,
      1
    ],
    "goalAt": [
      5,
      3
    ],
    "variantGoal": [
      4,
      3
    ],
    "require": "loops",
    "estado_editorial": "PROTOTIPO_INTERATIVO",
    "avaliacao_pedagogica": "NÃO VERIFICADO"
  },
  {
    "id": "decisoes",
    "title": "Observe antes de avançar",
    "topic": "Condições",
    "kind": "rover",
    "unit": "U-PRG01-02",
    "discipline": "PRG01",
    "minutes": "10–15 min",
    "goal": "Contorne a curva até a estação. Use livre() para decidir entre andar e virar.",
    "predict": "O que acontece quando livre() retorna false e não existe um else?",
    "starter": "for (let i = 0; i < 7; i++) {\n  if (livre()) {\n    mover();\n  }\n  // E quando o caminho estiver bloqueado?\n}",
    "hint": "Se houver caminho, ande. Caso contrário, vire à direita. A condição precisa de uma alternativa.",
    "concept": "Uma condição escolhe um caminho de execução a partir de um valor verdadeiro ou falso.",
    "transfer": "Explique uma situação em que virar sempre à direita não resolve um labirinto.",
    "grid": [
      "######",
      "#....#",
      "#.####",
      "#.####",
      "#.####",
      "######"
    ],
    "start": [
      1,
      4,
      0
    ],
    "goalAt": [
      4,
      1
    ],
    "require": "conditions",
    "estado_editorial": "PROTOTIPO_INTERATIVO",
    "avaliacao_pedagogica": "NÃO VERIFICADO"
  },
  {
    "id": "funcoes",
    "title": "Um caminho em pequenas funções",
    "topic": "Funções",
    "kind": "rover",
    "unit": "U-PRG01-04",
    "discipline": "PRG01",
    "minutes": "10–15 min",
    "goal": "Reutilize avancar para percorrer os dois trechos do caminho.",
    "predict": "Qual chamada controla o trecho depois da curva?",
    "starter": "function avancar(passos) {\n  for (let i = 0; i < passos; i++) {\n    mover();\n  }\n}\navancar(3);\nvirarDireita();\navancar(2);",
    "hint": "A primeira chamada percorre três casas para cima. Depois da curva também faltam três casas.",
    "concept": "Uma função reúne um procedimento e recebe parâmetros para reutilizá-lo em situações diferentes.",
    "transfer": "O que você mudaria para usar a mesma função em um caminho com trechos de tamanhos diferentes?",
    "grid": [
      "######",
      "#....#",
      "#.####",
      "#.####",
      "#.####",
      "######"
    ],
    "start": [
      1,
      4,
      0
    ],
    "goalAt": [
      4,
      1
    ],
    "require": "functionCalls",
    "estado_editorial": "PROTOTIPO_INTERATIVO",
    "avaliacao_pedagogica": "NÃO VERIFICADO"
  },
  {
    "id": "ordenacao",
    "title": "Organize o que está fora de ordem",
    "topic": "Algoritmos",
    "kind": "sort",
    "unit": "U-ALG01-01",
    "discipline": "ALG01",
    "minutes": "12–20 min",
    "goal": "Ordene os valores do menor para o maior. Compare vizinhos e visualize cada troca.",
    "predict": "Uma única passagem pelas barras sempre é suficiente para ordenar tudo?",
    "starter": "for (let i = 0; i < tamanho() - 1; i++) {\n  if (valor(i) > valor(i + 1)) {\n    trocar(i, i + 1);\n  }\n}",
    "hint": "Uma passagem leva o maior valor ao final. Use outro laço por fora para repetir as passagens.",
    "concept": "Um algoritmo precisa funcionar em mais de uma entrada. Aqui avaliamos duas listas, incluindo valores repetidos.",
    "transfer": "Por que comparar com > evita trocas desnecessárias entre valores iguais?",
    "values": [
      5,
      2,
      8,
      1
    ],
    "alternative": [
      4,
      3,
      3,
      1
    ],
    "require": "loops",
    "estado_editorial": "PROTOTIPO_INTERATIVO",
    "avaliacao_pedagogica": "NÃO VERIFICADO"
  },
  {
    "id": "circuito",
    "title": "Duas entradas, uma decisão",
    "topic": "Lógica digital",
    "kind": "logic",
    "unit": "U-MAT02-01",
    "discipline": "MAT02",
    "minutes": "8–12 min",
    "goal": "Acenda a saída se ao menos uma entrada estiver ligada. Seu programa será testado nas quatro combinações.",
    "predict": "Com A ligada e B desligada, a expressão A && B é verdadeira?",
    "starter": "let a = entradaA();\nlet b = entradaB();\nsaida(a && b);",
    "hint": "&& exige as duas entradas verdadeiras. O operador || representa “ao menos uma”.",
    "concept": "Uma tabela-verdade explicita o resultado de uma expressão para cada combinação de entradas.",
    "transfer": "Agora pense em um alarme que só dispara quando as duas condições ocorrem. Qual operador você usaria?",
    "estado_editorial": "PROTOTIPO_INTERATIVO",
    "avaliacao_pedagogica": "NÃO VERIFICADO"
  },
  {
    "id": "consumo",
    "title": "Da amostra à decisão",
    "topic": "Missão integradora",
    "kind": "energy",
    "unit": "U-PRG01-04",
    "discipline": "PRG01",
    "mission": "M01",
    "minutes": "12–20 min",
    "goal": "Some as amostras e emita um alerta quando o total atingir ou ultrapassar o limite. Teste também a fronteira.",
    "predict": "Se total for exatamente igual ao limite, o operador > aciona o alerta?",
    "starter": "let total = 0;\nfor (let i = 0; i < amostras(); i++) {\n  total += consumo(i);\n}\nregistrar(total);\nalertar(total > limite());",
    "hint": "“Atingir ou ultrapassar” inclui igualdade. Confira a diferença entre > e >=.",
    "concept": "Uma decisão precisa de testes abaixo, igual e acima da fronteira. Os consumos são dados fictícios para estudo.",
    "transfer": "Que entradas você rejeitaria em um sistema real? Explique o efeito de valores negativos ou amostras ausentes.",
    "samples": [
      3,
      5,
      2
    ],
    "limit": 10,
    "estado_editorial": "PROTOTIPO_INTERATIVO",
    "avaliacao_pedagogica": "NÃO VERIFICADO"
  }
];
export const byId=id=>missions.find(m=>m.id===id)||missions[0];
