from src.simbolo.CTipo import Tipo, tipoDato
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CArbol import Arbol
from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


class Break(Instruccion):
    def __init__(self, linea: int, col: int):
        super().__init__(Tipo(tipoDato.VOID), linea, col)
        self.error = False  # <-- Agrega esta bandera

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo, en_ciclo=False):
        if not en_ciclo:
            self.error = True  # <-- Marca error
            return Errores(
                "SEMANTICO",
                "La sentencia 'break' solo puede usarse dentro de un ciclo o switch.",
                self.linea,
                self.col,
            )
        self.error = False
        return "break"

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        if getattr(self, "error", False):
            return None  # <-- No grafica si hubo error
        nodo_id = grafo.agregar_nodo("Break")
        return nodo_id
