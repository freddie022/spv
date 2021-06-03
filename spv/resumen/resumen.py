import json


class Resumen:
    def __init__(self, mark: str = 'visa'):
        self.mark = mark
        self.operations = {}
        self.identifiers = []
        self.resumen = {}

    def guia(self, line):
        start_line = str(line[0:6])
        if start_line not in self.identifiers:
            return 'default'
        return start_line

    def loads(self, data: str):
        try:
            brut = json.loads(data)
            for linea in brut['resumenCliente']:
                self.operations[self.guia(linea)](mark=self.mark).build(linea, parent=self)
            return json.dumps(self.postload(self.resumen), indent=2)
        except:
            raise Exception("Se ha occurido un error")

    def preload(self):
        pass

    def postload(self, data):
        return data
