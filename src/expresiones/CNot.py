from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo, tipoDato
from src.excepciones.CErrores import Errores


class Not(Instruccion):
    def __init__(self, expresion, linea, col):
        super().__init__(Tipo(tipoDato.BOOL), linea, col)
        self.expresion = expresion

    def interpretar(self, arbol, tabla):
        valor = self.expresion.interpretar(arbol, tabla)
        if isinstance(valor, bool):
            return not valor
        else:
            return Errores(
                "SEMANTICO",
                f"Error de tipo en NOT: se esperaba un booleano, pero se recibió {type(valor).__name__}",
                self.linea,
                self.col,
            )
