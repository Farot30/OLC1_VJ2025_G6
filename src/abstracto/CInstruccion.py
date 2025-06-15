from abc import ABC, abstractmethod

# from src.simbolo.CArbol import Arbol
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CTipo import Tipo


class Instruccion(ABC):
    def __init__(self, tipo: Tipo, linea: int, col: int):
        self.tipoDato = tipo
        self.linea = linea
        self.col = col

    @abstractmethod
    def interpretar(self, arbol, tabla: tablaSimbolo):
        pass
