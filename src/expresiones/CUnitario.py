from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CArbol import Arbol
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


class Unario(Instruccion):
    def __init__(self, operador, expresion, linea, col):
        super().__init__(None, linea, col)
        self.operador = operador
        self.expresion = expresion

    def __str__(self):
        return f"{self.operador}{self.expresion}"

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        valor = self.expresion.interpretar(arbol, tabla)
        if isinstance(valor, Errores):
            return valor

        # Copia el tipo de la expresión interna
        self.tipoDato = self.expresion.tipoDato
        if self.operador == "-":
            if isinstance(valor, (int, float)):
                return -valor
            return Errores(
                "SEMANTICO",
                "No se puede aplicar signo negativo a un valor no numérico",
                self.linea,
                self.col,
            )
        return Errores(
            "SEMANTICO",
            f"Operador unario desconocido: {self.operador}",
            self.linea,
            self.col,
        )

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        unario = grafo.agregar_nodo("Unario")
        nodoOperador = grafo.agregar_nodo(self.operador)
        nodoExp = self.expresion.graficar(grafo, arbol, tabla)
        grafo.agregar_arista(unario, nodoOperador)
        if nodoExp is not None:
            grafo.agregar_arista(unario, nodoExp)
        return unario
