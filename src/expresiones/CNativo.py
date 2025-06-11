
from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo
from src.simbolo.CArbol import Arbol
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CInstancia import tabla_S as aTab


class Nativo(Instruccion):
    def __init__(self, tipo: Tipo, valor: any, linea: int, col: int):
        super().__init__(tipo, linea, col)
        self.valor = valor

    def interpretar(self, arbol: Arbol, tabla: aTab):
        return self.valor
