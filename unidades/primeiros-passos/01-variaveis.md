# 1. Representar e atualizar valores

Unidade U-PRG01-01. Aula autoral inicial; revisão pedagógica pendente. Você pode começar com papel e lápis. Não é necessário já conhecer Python.

## Diagnóstico

Uma caixa possui 2 peças. Você coloca mais 3. Quantas peças existem? Explique o que mudou. Se a soma ainda for difícil, represente as peças com cinco marcas antes de avançar.

## Construir o modelo

Uma variável associa um nome a um valor no programa. Neste exemplo, o nome `pecas` nos ajuda a acompanhar uma quantidade que muda. O sinal `=` abaixo atribui um valor; não representa uma igualdade matemática a ser resolvida.

| Passo | Instrução | Valor associado a pecas |
|---|---|---|
| 1 | pecas = 2 | 2 |
| 2 | pecas = pecas + 3 | 5 |
| 3 | print(pecas) | continua 5; mostra 5 |

Descrição textual do visual: primeiro associamos 2 ao nome; depois lemos esse valor, somamos 3 e associamos 5 ao mesmo nome. Mostrar o valor não o altera.

## Exemplo guiado

```python
pecas = 2
pecas = pecas + 3
print(pecas)
```

Leia as instruções em ordem. Antes de executar, preveja o resultado. Você também pode ouvir sua própria leitura em voz alta; áudio não é requisito e não há gravação incluída.

## Prática com apoio

Troque o valor inicial por 4 e a quantidade adicionada por 2. Complete uma tabela como a anterior. Pista: calcule primeiro a expressão à direita da atribuição.

## Tentativa independente

Represente um estoque que começa com 10 peças, recebe 4 e perde 3. Entregue instruções ou pseudocódigo, tabela dos valores e explicação do resultado. Não copie o exemplo como evidência de solução independente.

## Transferência e julgamento

Use a mesma ideia para acompanhar carga restante de uma bateria simulada. O que seria diferente se um valor pudesse ficar negativo? Declare a regra que você escolheu e seu limite; o exemplo não modela uma bateria real.

## Conferência e retomada

Verifique as três operações, explique o significado de cada atribuição e localize o primeiro ponto de divergência. Registre se recebeu pista ou solução. Em outro momento combinado, refaça com valores diferentes sem consultar a tabela.

[Próxima aula: decisões](02-decisoes.md) · [Fonte candidata para aprofundar](https://greenteapress.com/wp/think-python-3rd-edition/) · [Como registrar progresso](../../aprendizagem/progresso.md)
