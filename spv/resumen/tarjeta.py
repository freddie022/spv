from spv.resumen.parser import ResumenParser


class Tarjeta(ResumenParser):
    def __init__(self, mark: str):
        super().__init__(mark)
