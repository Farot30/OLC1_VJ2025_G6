from src.simbolo.CTipo import Tipo


class Simbolo:
    def __init__(self, tipo: Tipo, id: str, valor=None, linea=0, columna=0):
        self.tipo = tipo
        self.id = id.lower()
        self.valor = valor
        self.linea = linea
        self.columna = columna

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

    def getLinea(self):
        return self.linea

    def getColumna(self):
        return self.columna
