from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo, tipoDato
from src.simbolo.CArbol import Arbol
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.excepciones.CErrores import Errores


class Unario(Instruccion):
    def __init__(self, operador, expresion, linea, col):
        super().__init__(None, linea, col)
        self.operador = operador
        self.expresion = expresion

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        valor = self.expresion.interpretar(arbol, tabla)
        if isinstance(valor, Errores):
            return valor
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
