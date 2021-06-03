from spv.resumen.parser import ResumenParser
import re


class Leyenda(ResumenParser):
    def __init__(self, mark: str = 'visa'):
        super().__init__(mark)
        self.mark = mark
        self.operations = {
            'visa': self.generar_leyenda_visa
        }

    def generar_leyenda(self, data):
        return self.operations[self.mark](data)

    def generar_leyenda_visa(self, leyenda):
        i = 0
        leyendas = {
            "descripcion_leyenda": [],
            "cuotas_a_vencer": {
                "titulo": "",
                "meses": [],
                "valores": [],
                "mensaje": ""
            },
            "aviso": ""
        }
        leye = ""
        aviso = ""
        while i < len(leyenda):
            valor = leyenda[i].strip()
            if valor[-1] != ".":
                if valor[0:15] == "Cuotas a vencer":
                    leyendas["cuotas_a_vencer"]["titulo"] = valor
                    #
                    idx_meses = i + 1
                    idx_valores = i + 2
                    idx_mensaje = i + 3
                    #
                    linea_meses = leyenda[idx_meses]
                    linea_valores = leyenda[idx_valores]
                    linea_mensaje = leyenda[idx_mensaje]
                    #
                    meses = linea_meses.split(" ")
                    valores = linea_valores.split(" ")
                    #
                    meses = [var for var in meses if var]
                    valores = [var for var in valores if var]
                    #
                    leyendas["cuotas_a_vencer"] = {"meses": meses, "valores": valores, "mensaje": ''}
                    #
                    if linea_mensaje[0:8] == "A partir":
                        leyendas["cuotas_a_vencer"]["mensaje"] = re.sub(' +', ' ', linea_mensaje)
                        i = i + 3
                    else:
                        i = i + 2
                elif valor[0:17] == "SU BANCO LE AVISA":
                    for idx in range(i, i + 6):
                        desc = leyenda[idx].strip()
                        aviso = aviso + " " + desc
                    i = i + 16
                else:
                    leye = leye + " " + valor
            else:
                leye = leye + " " + valor
                leyendas["descripcion_leyenda"].append(leye)
                leye = ""
            leyendas["aviso"] = re.sub(' +', ' ', aviso)
            i = i + 1
        leyendas["descripcion_leyenda"].append(leye)
        return leyendas
