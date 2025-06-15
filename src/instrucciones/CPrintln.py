from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


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

    def graficar(self, grafo: clasAST):
        nodoPrintln = grafo.agregar_nodo("Println")
        nodoExp = self.expresion.graficar(grafo)
        grafo.agregar_arista(nodoPrintln, nodoExp)
        return nodoPrintln
