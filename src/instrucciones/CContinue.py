from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo, tipoDato
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


class Continue(Instruccion):
    def __init__(self, linea, col):
        super().__init__(Tipo(tipoDato.VOID), linea, col)

    def interpretar(self, arbol, tabla, en_ciclo=False):
        if not en_ciclo:
            return Errores(
                "SEMANTICO",
                "La sentencia 'continue' solo puede usarse dentro de un ciclo.",
                self.linea,
                self.col,
            )
        return "continue"

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        nodo_id = grafo.agregar_nodo("Continue")
        return nodo_id
