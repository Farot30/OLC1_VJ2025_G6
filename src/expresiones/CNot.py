from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo, tipoDato
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


class Not(Instruccion):
    def __init__(self, expresion, linea, col):
        super().__init__(Tipo(tipoDato.BOOL), linea, col)
        self.expresion = expresion

    def interpretar(self, arbol, tabla):
        valor = self.expresion.interpretar(arbol, tabla)
        if isinstance(valor, Errores):
            return valor
        if isinstance(valor, bool):
            return not valor
        else:
            return Errores(
                "SEMANTICO",
                f"Error de tipo en NOT: se esperaba un booleano, pero se recibió {type(valor).__name__}",
                self.linea,
                self.col,
            )

    def graficar(self, grafo: clasAST):
        nodoNot = grafo.agregar_nodo("NOT")
        nodoExp = self.expresion.graficar(grafo)  # <-- Grafica la expresión

        grafo.agregar_arista(nodoNot, nodoExp)
        return nodoNot
