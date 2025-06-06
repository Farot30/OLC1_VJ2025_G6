from .CTipo import Tipo


class Simbolo:
    def __init__(self, tipo: Tipo, id: str, valor=None):
        self.tipo = tipo
        self.id = id.lower()
        self.valor = valor

    def getTipo(self) -> Tipo:
        return self.tipo

    def setTipo(self, tipo: Tipo):
        self.tipo = tipo

    def getId(self) -> str:
        return self.id

    def setId(self, id: str):
        self.id = id

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor
