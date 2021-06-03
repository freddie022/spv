from spv.resumen.parser import ResumenParser
from spv.utils.utils import conversion_valor, parse_fecha_movimientos


class Movimientos(ResumenParser):
    def __init__(self, mark: str = 'visa'):
        super().__init__(mark)
        self.tarjeta = ''
        self.actions = {
            "visa": {
                '027502': self.detalle_cinco_dos,
                '027503': self.detalle_cinco_tres,
                '027505': self.detalle_cinco_cinco
            }
        }

    def build(self, linea, parent):
        try:
            out = self.actions[self.mark][linea[:6]](linea)
            parent.movimientos['tarjeta_numero'] = self.tarjeta
            if self.current_key not in parent.movimientos:
                parent.movimientos.update({self.current_key: []})
            parent.movimientos[self.current_key].append(out)
        except:
            pass

    def detalle_cinco_dos(self, linea):
        consumos = {}
        consumos['fecha_origen'] = parse_fecha_movimientos(linea[6:12])
        consumos['numero_tc'] = linea[24:28]
        consumos['detalle_de_transaccion'] = linea[28:71]
        consumos['importe_en_pesos'] = conversion_valor(
            linea[78:91], linea[91:92])
        consumos['importe_en_dolares'] = conversion_valor(
            linea[92:105], linea[105:106])
        consumos['comprobante'] = linea[71:77]
        consumos['codigo_operacion'] = linea[139:143]
        self.current_key = 'pesos'
        self.tarjeta = consumos['numero_tc']
        return consumos

    def detalle_cinco_tres(self, linea):
        sub_totales = {}
        sub_totales['numero_tc'] = linea[24:28]
        sub_totales['descripcion_subtotal_tc'] = linea[28:78]
        sub_totales['subtotal_importe_en_pesos'] = conversion_valor(
            linea[78:91], linea[91:92])
        sub_totales['subtotal_importe_dolares'] = conversion_valor(
            linea[92:105], linea[105:106])
        self.current_key = 'subtotales'
        self.tarjeta = sub_totales['numero_tc']
        return sub_totales

    def detalle_cinco_cinco(self, linea):
        consumos = {}
        consumos['fecha_origen'] = parse_fecha_movimientos(linea[6:12])
        consumos['numero_tc'] = linea[24:28]
        consumos['detalle_de_transaccion'] = linea[28:78]
        consumos['importe_en_pesos'] = conversion_valor(
            linea[78:91], linea[91:92])
        consumos['importe_en_dolares'] = conversion_valor(
            linea[92:105], linea[105:106])
        consumos['comprobante'] = linea[71:77]
        consumos['codigo_operacion'] = linea[139:143]
        self.current_key = 'moneda_extranjera'
        self.tarjeta = consumos['numero_tc']
        return consumos
