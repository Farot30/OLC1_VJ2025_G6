
from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo
from src.simbolo.CArbol import Arbol
from src.simbolo.TablaSimbolo import tablaSimbolo


class Nativo(Instruccion):
    def __init__(self, tipo: Tipo, valor: any, linea: int, col: int):
        super().__init__(tipo, linea, col)
        self.valor = valor

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        return self.valor
