from spv.resumen.parser import ResumenParser
from spv.utils.utils import parse_fecha_movimientos, conversion_valor


class MovimientoVarios(ResumenParser):
    def __init__(self, mark: str = 'visa'):
        super().__init__(mark)
        self.actions = {
            "visa": {
                '027501': self.detalle_cinco_uno
            }
        }
        self.keys = {
            '9999999999999999': 'detalles_movimientos_fin',
            '0000000000000000': 'detalles_movimientos_inicio'
        }

    def build(self, linea, parent):
        try:
            out = self.actions[self.mark][linea[:6]](linea)
            if self.current_key not in parent.movimientos_varios:
                parent.movimientos_varios.update({self.current_key: []})
            parent.movimientos_varios[self.current_key].append(out)
        except:
            pass

    def detalle_cinco_uno(self, linea):
        mov_varios = {}
        mov_varios['fecha_origen'] = parse_fecha_movimientos(linea[6:12])
        mov_varios['dato_validacion'] = linea[12:28]
        mov_varios['descripcion'] = linea[28:78]
        mov_varios['importe_en_pesos'] = conversion_valor(linea[78:91], linea[91:92])
        mov_varios['importe_en_dolares'] = conversion_valor(linea[92:105], linea[105:106])
        mov_varios['codigo_operacion'] = linea[139:143]
        self.current_key = self.keys[mov_varios['dato_validacion']]
        return mov_varios
