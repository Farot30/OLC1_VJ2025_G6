from enum import Enum, auto


class tipoDato(Enum):
    ENTERO = auto()
    DECIMAL = auto()
    BOOL = auto()
    CHAR = auto()
    STRING = auto()
    VOID = auto()
    VECTOR = auto()


class Tipo:
    def __init__(self, tipo: tipoDato):
        self.tipo = tipo

    def setTipo(self, tipo: tipoDato):
        self.tipo = tipo

    def getTipo(self) -> tipoDato:
        return self.tipo
