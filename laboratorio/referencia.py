"""Soluções autorais de referência: consultar depois da própria tentativa."""
def somar(valores):
    total = 0
    for valor in valores:
        total = total + valor
    return total

def classificar(total, limite):
    return "alerta" if total >= limite else "normal"

def contar_alertas(valores, limite):
    quantidade = 0
    for valor in valores:
        if valor >= limite:
            quantidade += 1
    return quantidade

def resumir(valores, limite):
    total = somar(valores)
    return {"total": total, "estado": classificar(total, limite)}
