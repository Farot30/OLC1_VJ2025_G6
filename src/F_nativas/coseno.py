import math
from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.simbolo.CTipo import Tipo, tipoDato
from src.abstracto.CAST import clasAST


class Coseno(Instruccion):
    def __init__(self, expresion, linea, col):
        super().__init__(None, linea, col)
        self.expresion = expresion

    def interpretar(self, arbol, tabla):
        val = self.expresion.interpretar(arbol, tabla)
        if isinstance(val, Errores):
            return val

        # Rechazar booleanos explícitamente
        if isinstance(val, bool):
            return Errores(
                "SEMANTICO",
                f"Coseno requiere número (int/float), no bool",
                self.linea,
                self.col,
            )
        # Verificar si es un entero o flotante
        elif not isinstance(val, (int, float)):
            return Errores(
                "SEMANTICO",
                f"Coseno requiere número, no {type(val).__name__}",
                self.linea,
                self.col,
            )

        try:
            res = math.cos(val)
            self.tipoDato = Tipo(tipoDato.DECIMAL)
            return res
        except Exception as e:
            return Errores(
                "SEMANTICO", f"Error al calcular coseno: {e}", self.linea, self.col
            )

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        nodo = grafo.agregar_nodo("Coseno")
        hijo = self.expresion.graficar(grafo, arbol, tabla)
        grafo.agregar_arista(nodo, hijo)
        return nodo
