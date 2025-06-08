from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo, tipoDato


class Or(Instruccion):
    def __init__(self, izq, der, linea, col):
        super().__init__(Tipo(tipoDato.BOOL), linea, col)
        self.izq = izq
        self.der = der

    def interpretar(self, arbol, tabla):
        val1 = self.izq.interpretar(arbol, tabla)
        val2 = self.der.interpretar(arbol, tabla)
        return bool(val1) or bool(val2)
