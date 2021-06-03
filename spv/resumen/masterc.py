from spv.resumen.resumen import Resumen


class ResumenMasterCard(Resumen):
    def __init__(self):
        super().__init__(mark="master-card")
        self.identifiers = []
        self.operations = {}
        self.resumen = {
            'meta': {
                'version': '2021.1',
                'marca': 'visa',
                'segmento': ''
            }
        }
