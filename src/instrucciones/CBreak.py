from src.simbolo.CTipo import Tipo, tipoDato
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CArbol import Arbol
from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores


class Break(Instruccion):
    def __init__(self, linea: int, col: int):
        super().__init__(Tipo(tipoDato.VOID), linea, col)

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo, en_ciclo=False):
        if not en_ciclo:
            return Errores(
                "SEMANTICO",
                "La sentencia 'break' solo puede usarse dentro de un ciclo o switch.",
                self.linea,
                self.col,
            )
        return "break"
