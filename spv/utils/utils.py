def hashmap(keys, obj) -> dict:
    mapped = {}
    for index in obj:
        if index in keys:
            mapped[index] = obj[index]
    return mapped


def conversion_valor(x, y):
    if y == "-":
        valor = -(float(x) / 100)
    else:
        valor = float(x) / 100
    valor_formato = f"{valor:,.2f}".format(valor).replace(",", "@").replace(".", ",").replace("@", ".")
    return valor_formato


def conversion_tasas(x):
    valor = float(x) / 1000
    valor_formato = f"{valor:,.3f}".format(valor).replace(",", "@").replace(".", ",").replace("@", ".")
    return valor_formato


def conversion_saldos(x):
    valor = float(x) / 100
    valor_formato = f"{valor:,.2f}".format(valor).replace(",", "@").replace(".", ",").replace("@", ".")
    return valor_formato


def parse_fecha_cierre_vto(fecha):
    return "{}/{}/{}".format(fecha[4:6], fecha[2:4], fecha[0:2])


def parse_fecha_movimientos(fecha):
    return "{}/{}/{}".format(fecha[0:2], fecha[2:4], fecha[4:6])
