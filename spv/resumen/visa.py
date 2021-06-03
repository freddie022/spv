from spv.resumen.cabecera import Cabecera
from spv.resumen.detalle import Detalle
from spv.resumen.leyenda import Leyenda
from spv.resumen.movarios import MovimientoVarios
from spv.resumen.movimientos import Movimientos
from spv.resumen.resumen import Resumen


class ResumenVisa(Resumen):
    def __init__(self):
        super().__init__(mark="visa")
        self.identifiers = ['027501', '027502', '027503', '027505', '027506', '027507']
        self.operations = {
            '027501': MovimientoVarios,
            '027502': Movimientos,
            '027503': Movimientos,
            '027505': Movimientos,
            '027506': Detalle,
            '027507': Detalle,
            'default': Cabecera
        }

        self.movimientos_varios = {}
        self.movimientos = {}
        self.leyenda = []
        self.resumen = {
            'meta': {
                'version': '20211',
                'marca': 'visa',
                'segmento': ''
            },
            'detalle_cuenta': [],
            'movimientos_generales': [],
            'movimientos_totales': [],
            'descripcion_debito_automatico': [],
            'descripcion_leyenda': [],
            'cuotas_a_vencer': {'meses': [], 'valores': [], 'mensaje': ''},
            'aviso': ''
        }

    def postload(self, data):
        data['movimientos_generales'].append(self.movimientos_varios)
        data['movimientos_totales'].append(self.movimientos)
        data.update(Leyenda(self.mark).generar_leyenda(data["descripcion_leyenda"]))
        return data
