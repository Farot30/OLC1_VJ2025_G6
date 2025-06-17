from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo, tipoDato
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


class Xor(Instruccion):
    def __init__(self, izq, der, linea, col):
        super().__init__(Tipo(tipoDato.BOOL), linea, col)
        self.izq = izq
        self.der = der

    def __str__(self):
        return f"XOR({self.izq}, {self.der})"

    def interpretar(self, arbol, tabla):
        val1 = self.izq.interpretar(arbol, tabla)
        if isinstance(val1, Errores):
            return val1
        val2 = self.der.interpretar(arbol, tabla)
        if isinstance(val2, Errores):
            return val2

        try:
            return bool(val1) ^ bool(val2)  # XOR lógico
        except Exception:
            return Errores(
                "SEMANTICO",
                f"Operador XOR no puede aplicarse a tipos {type(val1).__name__} y {type(val2).__name__}",
                self.linea,
                self.col,
            )

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        nodoXor = grafo.agregar_nodo("XOR")
        nodoIzq = self.izq.graficar(grafo, arbol, tabla)
        nodoDer = self.der.graficar(grafo, arbol, tabla)
        grafo.agregar_arista(nodoXor, nodoIzq)
        grafo.agregar_arista(nodoXor, nodoDer)
        return nodoXor
