from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


class Println(Instruccion):
    def __init__(self, expresion, linea, col):
        super().__init__(None, linea, col)
        self.expresion = expresion
        self.valor_impreso = None  # <-- Nuevo atributo

    def interpretar(self, arbol, tabla):
        valor = self.expresion.interpretar(arbol, tabla)
        if isinstance(valor, Errores):
            print(valor)
            arbol.errores.append(valor)
            return None
        arbol.setConsola(arbol.getConsola() + str(valor) + "\n")
        self.valor_impreso = valor  # <-- Guarda el valor impreso
        return None

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        # Evaluar la expresión antes de graficar
        valor_evaluable = None
        try:
            if arbol is not None and tabla is not None:
                valor_evaluable = self.expresion.interpretar(arbol, tabla)
        except Exception:
            valor_evaluable = None

        # Si hay error semántico, NO graficar nada
        from src.excepciones.CErrores import Errores

        if isinstance(valor_evaluable, Errores):
            return None

        nodoPrintln = grafo.agregar_nodo("Println")
        if valor_evaluable is not None:
            nodoValor = grafo.agregar_nodo(str(valor_evaluable))
            grafo.agregar_arista(nodoPrintln, nodoValor)
        else:
            nodoExp = grafo.agregar_nodo(str(self.expresion))
            grafo.agregar_arista(nodoPrintln, nodoExp)
        return nodoPrintln
