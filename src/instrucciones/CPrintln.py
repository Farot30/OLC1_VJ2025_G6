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
            self.valor_impreso = valor  # Guardar el error también
            return None
        arbol.setConsola(arbol.getConsola() + str(valor) + "\n")
        self.valor_impreso = valor
        return None

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        # No graficar si hay un error semántico
        if hasattr(self, "valor_impreso") and isinstance(self.valor_impreso, Errores):
            return None

        # Si estamos en modo verificación (cuando no se ha ejecutado aún)
        if (
            arbol is not None
            and tabla is not None
            and not hasattr(self, "valor_impreso")
        ):
            # Verificar si habría un error al evaluar la expresión
            valor_temp = self.expresion.interpretar(arbol, tabla)
            if isinstance(valor_temp, Errores):
                return None  # No graficar si detectamos un error

        # Continuar con la graficación normal
        nodoPrintln = grafo.agregar_nodo("Println")

        if hasattr(self, "valor_impreso") and self.valor_impreso is not None:
            nodo_valor = grafo.agregar_nodo(f"{self.valor_impreso}")
            grafo.agregar_arista(nodoPrintln, nodo_valor)
        else:
            nodoExp = self.expresion.graficar(grafo, arbol, tabla)
            if nodoExp is not None:
                grafo.agregar_arista(nodoPrintln, nodoExp)
            else:
                nodo_fallback = grafo.agregar_nodo(f"Expr: {str(self.expresion)}")
                grafo.agregar_arista(nodoPrintln, nodo_fallback)

        return nodoPrintln
