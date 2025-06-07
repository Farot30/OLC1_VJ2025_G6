from src.abstracto.CInstruccion import Instruccion


class Print(Instruccion):
    def __init__(self, expresion, linea, col):
        super().__init__(None, linea, col)
        self.expresion = expresion

    def interpretar(self, arbol, tabla):
        valor = self.expresion.interpretar(arbol, tabla)
        arbol.setConsola(arbol.getConsola() + str(valor))
        return None
