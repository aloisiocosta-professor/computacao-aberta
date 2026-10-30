# 4. Dividir o problema e integrar a solução

Unidade U-PRG01-04. Aula autoral inicial; revisão pendente. Pré-requisitos: representar valores, decidir e repetir.

## Problema

Queremos receber uma lista de consumos simulados, calcular o total e decidir se o total atinge um limite. Antes do código, separe responsabilidades.

| Parte | Entrada | Responsabilidade | Saída |
|---|---|---|---|
| somar | lista de valores | acumular cada valor | número total |
| classificar | total e limite | comparar com o limite | alerta ou normal |
| integrar | lista e limite | chamar as duas partes | total e classificação |

Descrição textual: a classificação utiliza o resultado da soma. Podemos testar cada parte e depois sua integração.

## Exemplo guiado

```python
def somar(valores):
    total = 0
    for valor in valores:
        total = total + valor
    return total

def classificar(total, limite):
    if total >= limite:
        return "alerta"
    return "normal"

total = somar([3, 5, 2])
print(total, classificar(total, 12))
```

`def` define uma função e `return` devolve o resultado. Preveja primeiro o valor devolvido por cada chamada. Mostre no papel a entrada e a saída de cada parte.

## Tentativa independente

Implemente a integração para outra lista e outro limite. Cubra total abaixo, igual e acima do limite e lista vazia. Explique a regra para valores negativos; não aceite uma hipótese escondida como se fosse fato do domínio.

## Transferência interdisciplinar

Na [missão M01](../../missoes/m01.md), conecte representação de dados, condições, contagem, testes e comunicação de uma decisão. Depois compare com uma entrada em tabela: o armazenamento muda, mas a regra de classificação pode permanecer.

## Julgamento e avaliação

Quando a solução está correta para a tarefa, mas é insuficiente para uso real? Identifique pelo menos uma hipótese simplificadora. Entregue solução, testes, explicação e registro de apoio. A execução do código de referência não demonstra que você consegue resolver sozinho.

[Missões](../../missoes/README.md) · [Progresso](../../aprendizagem/progresso.md) · [Solução de referência, consultar após tentar](../../laboratorio/referencia.py)
