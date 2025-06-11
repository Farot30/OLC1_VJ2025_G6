from abc import ABC
from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo, tipoDato
from src.excepciones.CErrores import Errores
from src.simbolo.CInstancia import tabla_S as aTab


class OperadoresRel:
    MENOR_IGUAL = 1
    MAYOR_QUE = 2
    MAYOR_IGUAL = 3
    IGUAL_IGUAL = 4
    DIFERENTE = 5
    MENOR_QUE = 6


class Relacional(Instruccion, ABC):
    def __init__(self, operador, linea, col, op1, op2):
        super().__init__(Tipo(tipoDato.BOOL), linea, col)
        self.operador = operador
        self.op1 = op1
        self.op2 = op2

    def interpretar(self, arbol, tabla):
        val1 = self.op1.interpretar(arbol, tabla)
        val2 = self.op2.interpretar(arbol, tabla)

        tipos_validos = (int, float, str, bool)
        if not isinstance(val1, tipos_validos) or not isinstance(val2, tipos_validos):
            return Errores(
                "SEMANTICO",
                f"No se puede comparar valores de tipo {type(val1).__name__} y {type(val2).__name__}",
                self.linea,
                self.col,
            )

        # Comparación entre booleanos (solo con booleanos)
        if isinstance(val1, bool) or isinstance(val2, bool):
            if isinstance(val1, bool) and isinstance(val2, bool):
                pass  # permitido
            else:
                return Errores(
                    "SEMANTICO",
                    f"No se puede comparar valores de tipo {type(val1).__name__} y {type(val2).__name__}",
                    self.linea,
                    self.col,
                )
        # Comparación entre int, float, char (char como int)
        elif (
            isinstance(val1, (int, float)) or (isinstance(val1, str) and len(val1) == 1)
        ) and (
            isinstance(val2, (int, float)) or (isinstance(val2, str) and len(val2) == 1)
        ):
            if isinstance(val1, str) and len(val1) == 1:
                val1 = ord(val1)
            if isinstance(val2, str) and len(val2) == 1:
                val2 = ord(val2)
        # Comparación entre cadenas completas
        elif isinstance(val1, str) and isinstance(val2, str):
            pass  # permitido
        else:
            return Errores(
                "SEMANTICO",
                f"No se puede comparar valores de tipo {type(val1).__name__} y {type(val2).__name__}",
                self.linea,
                self.col,
            )

        if self.operador == OperadoresRel.MENOR_IGUAL:
            return val1 <= val2
        elif self.operador == OperadoresRel.MAYOR_QUE:
            return val1 > val2
        elif self.operador == OperadoresRel.MAYOR_IGUAL:
            return val1 >= val2
        elif self.operador == OperadoresRel.IGUAL_IGUAL:
            return val1 == val2
        elif self.operador == OperadoresRel.DIFERENTE:
            return val1 != val2
        elif self.operador == OperadoresRel.MENOR_QUE:
            return val1 < val2
        else:
            return Errores(
                "SEMANTICO",
                f"Operador relacional desconocido: {self.operador}",
                self.linea,
                self.col,
            )