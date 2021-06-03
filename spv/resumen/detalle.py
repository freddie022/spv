from spv.resumen.parser import ResumenParser
from spv.utils.utils import conversion_saldos, conversion_tasas, parse_fecha_cierre_vto, conversion_valor, \
    parse_fecha_movimientos


class Detalle(ResumenParser):
    def __init__(self, mark: str = 'visa'):
        super().__init__(mark)
        self.actions = {
            "visa": {
                '027506': self.detalle_cinco_seis,
                '027507': self.detalle_cinco_siete
            }
        }

    def build(self, linea, parent):
        try:
            out = self.actions[self.mark][linea[:6]](linea)
            if self.current_key in parent.resumen:
                if out:
                    parent.resumen[self.current_key].append(out)
        except:
            pass

    def detalle_cinco_seis(self, linea):
        self.current_key = 'descripcion_leyenda'
        out = linea[6:88]
        return out

    def detalle_cinco_siete(self, linea):
        self.current_key = 'descripcion_debito_automatico'
        out = linea[6:88]
        return out
