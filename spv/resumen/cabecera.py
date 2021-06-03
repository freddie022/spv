from spv.resumen.parser import ResumenParser
from spv.utils.utils import conversion_saldos, conversion_tasas, parse_fecha_cierre_vto, conversion_valor


class Cabecera(ResumenParser):
    def __init__(self, mark: str = 'visa'):
        super().__init__(mark)
        self.current_key = 'detalle_cuenta'
        self.actions = {
            "visa": {
                '027T': self.cabecera_h,
                '027H': self.cabecera_h,
                '027B': self.cabecera_b,
                '0271': self.cabecera_uno,
                '0272': self.cabecera_dos,
                '027D': self.cabecera_d
            },
        }

    def build(self, linea, parent):
        try:
            out = self.actions[self.mark][linea[:4]](linea)
            if self.current_key in parent.resumen:
                if out:
                    parent.resumen[self.current_key].append(out)
        except:
            pass

    def cabecera_h(self, linea):
        pass

    def cabecera_b(self, linea):
        out = {'pago': {}}
        out['pago']["codigo_de_barras_cabecera"] = linea[4:29]
        out['pago']["codigo_de_barra_pie"] = linea[29:54]
        out['pago']["marca_cuadro_de_plan_v"] = linea[54:55]
        out['pago']["marca_talon"] = linea[55:56]
        out['pago']["producto_de_la_cuenta"] = linea[56:62]
        return out

    def cabecera_uno(self, linea):
        out = {"datos_cuenta": {}, "tasas": {}, "fechas_cierres_vencimientos": {}}
        out['datos_cuenta']['sucursal'] = linea[7:10]
        out['datos_cuenta']['numero_cuenta'] = linea[10:20]
        out['datos_cuenta']['limite_de_compra'] = conversion_saldos(linea[20:33])
        out['datos_cuenta']['limite_de_financiacion'] = conversion_saldos(linea[34:47])
        out['tasas']['tna_pesos'] = conversion_tasas(linea[47:54])
        out['tasas']['tem_pesos'] = conversion_tasas(linea[54:61])
        out['fechas_cierres_vencimientos']['fecha_cierre_anterior'] = parse_fecha_cierre_vto(linea[61:67])
        out['fechas_cierres_vencimientos']['fecha_vencimiento_anterior'] = parse_fecha_cierre_vto(linea[67:73])
        out['fechas_cierres_vencimientos']['fecha_cierre_actual'] = parse_fecha_cierre_vto(linea[73:79])
        out['fechas_cierres_vencimientos']['fecha_vencimiento_actual'] = parse_fecha_cierre_vto(linea[79:85])
        out['fechas_cierres_vencimientos']['fecha_proximo_vencimiento'] = parse_fecha_cierre_vto(linea[85:91])
        out['fechas_cierres_vencimientos']['fecha_cierre_proximo'] = parse_fecha_cierre_vto(linea[91:97])
        out['datos_cuenta']['compra_en_cuotas'] = conversion_saldos(linea[97:110])
        out['tasas']['tna_dolares'] = conversion_tasas(linea[110:117])
        out['tasas']['tem_dolares'] = conversion_tasas(linea[117:124])
        out['datos_cuenta']['grupo_afinidad'] = linea[126:130]
        out['datos_cuenta']['tipo_tarjeta_titular'] = linea[130:131]
        out['datos_cuenta']['cartera'] = linea[131:132]
        out['datos_cuenta']['modelo_de_liquidacion'] = linea[132:135]
        out['datos_cuenta']['codigo_mensaje'] = linea[135:137]
        out['datos_cuenta']['tipo_documento'] = linea[137:140]
        out['datos_cuenta']['numero_documento'] = linea[140:150]
        out['datos_cuenta']['forma_de_pago'] = linea[150:152]
        return out

    def cabecera_dos(self, linea):
        out = {"saldos": {}, "datos_cuenta": {}}
        out['saldos']['saldo_anterior_pesos'] = conversion_valor(linea[4:17], linea[17:18])
        out['saldos']['saldo_anterior_dolares'] = conversion_valor(linea[18:31], linea[31:32])
        out['saldos']['pago_minimo_pesos'] = conversion_valor(linea[32:45], linea[45:46])
        out['saldos']['pago_minimo_dolares'] = conversion_valor(linea[46:59], linea[59:60])
        out['saldos']['saldo_actual_pesos'] = conversion_valor(linea[60:73], linea[73:74])
        out['saldos']['saldo_actual_dolares'] = conversion_valor(linea[74:87], linea[87:88])
        out['saldos']['franquicia_proximo_periodo'] = conversion_saldos(linea[88:101])
        out['datos_cuenta']['numero_cuit'] = linea[102:115]
        out['datos_cuenta']['numero_liquidacion'] = linea[115:124]
        out['datos_cuenta']['titular_de_cuenta'] = linea[124:150]
        out['datos_cuenta']['marca_resumen_virtual'] = linea[150:151]
        return out

    def cabecera_d(self, linea):
        out = {"domicilio": {}, "datos_cuenta": {}}
        out['domicilio']['denominacion_sucursal'] = linea[4:24]
        out['domicilio']['denominacion_gaff'] = linea[24:44]
        out['domicilio']['localidad'] = linea[44:64]
        out['domicilio']['calle'] = linea[64:84]
        out['domicilio']['puerta'] = linea[84:89]
        out['domicilio']['piso'] = linea[89:91]
        out['domicilio']['lod'] = linea[91:94]
        out['domicilio']['cod_postal_cpa'] = linea[94:102]
        out['domicilio']['numero_de_lod'] = linea[94:98]
        out['domicilio']['codigo_postal'] = linea[98:102]
        out['domicilio']['codigo_geografico'] = linea[102:107]
        out['domicilio']['codigo_provincia'] = linea[102:103]
        out['domicilio']['codigo_localidad'] = linea[103:107]
        if any(chr.isdigit() for chr in linea[107:119]):
            out['datos_cuenta']['adelanto_efectivo'] = conversion_saldos(linea[107:119])
        else:
            out['domicilio']['aT'] = linea[107:119]
        out['datos_cuenta']['pago_minimo_anterior'] = conversion_saldos(linea[122:131])
        return out
