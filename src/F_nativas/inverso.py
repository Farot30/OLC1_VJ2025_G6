from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.simbolo.CTipo import Tipo, tipoDato
from src.abstracto.CAST import clasAST


class Inverso(Instruccion):
    def __init__(self, expresion, linea, col):
        super().__init__(None, linea, col)
        self.expresion = expresion

    def interpretar(self, arbol, tabla):
        val = self.expresion.interpretar(arbol, tabla)
        if isinstance(val, Errores):
            return val
        if not isinstance(val, int):
            return Errores(
                "SEMANTICO",
                f"Inv requiere entero, no {type(val).__name__}",
                self.linea,
                self.col,
            )
        try:
            sign = -1 if val < 0 else 1
            s = str(abs(val))[::-1]
            res = sign * int(s)
            self.tipoDato = Tipo(tipoDato.ENTERO)
            return res
        except Exception as e:
            return Errores(
                "SEMANTICO", f"Error al invertir dígitos: {e}", self.linea, self.col
            )

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        nodo = grafo.agregar_nodo("Inv")
        hijo = self.expresion.graficar(grafo, arbol, tabla)
        grafo.agregar_arista(nodo, hijo)
        return nodo
