import math
from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.simbolo.CTipo import Tipo, tipoDato
from src.abstracto.CAST import clasAST


class Seno(Instruccion):
    def __init__(self, expresion, linea, col):
        super().__init__(None, linea, col)
        self.expresion = expresion

    def interpretar(self, arbol, tabla):
        val = self.expresion.interpretar(arbol, tabla)
        if isinstance(val, Errores):
            return val
        if not isinstance(val, (int, float)):
            return Errores(
                "SEMANTICO",
                f"Seno requiere número, no {type(val).__name__}",
                self.linea,
                self.col,
            )
        try:
            res = math.sin(val)
            # Registrar el tipo de este nodo como decimal
            self.tipoDato = Tipo(tipoDato.DECIMAL)
            return res
        except Exception as e:
            return Errores(
                "SEMANTICO", f"Error al calcular seno: {e}", self.linea, self.col
            )

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        nodo = grafo.agregar_nodo("Seno")
        hijo = self.expresion.graficar(grafo, arbol, tabla)
        grafo.agregar_arista(nodo, hijo)
        return nodo
