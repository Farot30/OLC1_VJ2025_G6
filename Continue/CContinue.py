from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo, tipoDato
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CArbol import Arbol

class Continue(Instruccion):
    def __init__(self, linea, col):
        super().__init__(Tipo(tipoDato.VOID), linea, col)

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        return "continue"
