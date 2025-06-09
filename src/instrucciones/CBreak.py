from src.simbolo.CTipo import Tipo, tipoDato
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CArbol import Arbol
from src.abstracto.CInstruccion import Instruccion


class Break(Instruccion):
    def __init__(self, linea: int, col: int):
        super().__init__(Tipo(tipoDato.VOID), linea, col)

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        return
