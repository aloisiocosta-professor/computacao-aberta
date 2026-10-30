# 3. Repetir uma operação e acompanhar o estado

Unidade U-PRG01-03. Aula autoral inicial; revisão pendente. Pré-requisito: decisões.

## Problema e previsão

Temos consumos simulados 3, 5 e 2. Como obter o total sem escrever uma soma diferente para cada tamanho de lista? Preveja o valor acumulado após cada elemento.

| Elemento visitado | Total antes | Operação | Total depois |
|---|---|---|---|
| 3 | 0 | 0 + 3 | 3 |
| 5 | 3 | 3 + 5 | 8 |
| 2 | 8 | 8 + 2 | 10 |

Descrição textual: o acumulador começa em zero; cada elemento é somado uma única vez ao total anterior.

## Exemplo guiado

```python
valores = [3, 5, 2]
total = 0
for valor in valores:
    total = total + valor
print(total)
```

`for` visita os elementos da lista. A linha recuada atualiza o total. Se a lista estiver vazia, nenhuma atualização ocorre e o total permanece zero.

## Práticas

Com apoio: faça a tabela para [1, 4]. Independente: conte quantos valores de [11, 12, 13, 7] atingem o limite 12. Defina um contador, uma repetição e uma decisão. Entregue a tabela do contador e testes para lista vazia e lista sem alertas.

## Transferência e julgamento

Use a contagem para avaliar resultados de testes ou observações simuladas. Uma repetição do programa não cria, por si só, novas observações independentes. Distingua processar uma lista de coletar novos dados.

Explique por que inicializar o acumulador fora da repetição. Registre pistas recebidas e refaça posteriormente com outra lista.

[Próxima aula: decomposição](04-decomposicao.md) · [Progresso](../../aprendizagem/progresso.md)
