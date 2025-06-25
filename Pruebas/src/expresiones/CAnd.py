from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo, tipoDato
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


class And(Instruccion):
    def __init__(self, izq, der, linea, col):
        super().__init__(Tipo(tipoDato.BOOL), linea, col)
        self.izq = izq
        self.der = der

    def __str__(self):
        return f"({self.izq} AND {self.der})"

    def interpretar(self, arbol, tabla):
        val1 = self.izq.interpretar(arbol, tabla)
        if isinstance(val1, Errores):
            return val1
        val2 = self.der.interpretar(arbol, tabla)
        if isinstance(val2, Errores):
            return val2
        # print("DEBUG AND:", val1, type(val1), val2, type(val2))

        # Ambos operandos deben ser booleanos
        if type(val1) is not bool or type(val2) is not bool:
            return Errores(
                "SEMANTICO",
                f"Operador AND solo puede aplicarse a booleanos, no a {type(val1).__name__} y {type(val2).__name__}",
                self.linea,
                self.col,
            )
        return val1 and val2

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        nodoAND = grafo.agregar_nodo("AND")
        nodoIzq = self.izq.graficar(grafo, arbol, tabla)
        nodoDer = self.der.graficar(grafo, arbol, tabla)
        if nodoIzq is not None:
            grafo.agregar_arista(nodoAND, nodoIzq)
        if nodoDer is not None:
            grafo.agregar_arista(nodoAND, nodoDer)
        return nodoAND
