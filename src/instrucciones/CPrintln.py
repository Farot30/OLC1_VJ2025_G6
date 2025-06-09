from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores


class Println(Instruccion):
    def __init__(self, expresion, linea, col):
        super().__init__(None, linea, col)
        self.expresion = expresion

    def interpretar(self, arbol, tabla):
        valor = self.expresion.interpretar(arbol, tabla)
        if isinstance(valor, Errores):
            print(valor)
            arbol.errores.append(valor)  # <-- Agrega el error a la lista
            return None
        arbol.setConsola(arbol.getConsola() + str(valor) + "\n")
        return None