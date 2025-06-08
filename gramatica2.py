from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo, tipoDato
from src.excepciones.CErrores import Errores
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CArbol import Arbol


class OperadoresRel:
    MENOR_IGUAL = 1
    MAYOR_IGUAL = 2
    MENOR_QUE = 3
    MAYOR_QUE = 4
    IGUAL_IGUAL = 5
    DIFERENTE = 6


class Relacional(Instruccion):
    def __init__(self, operador: int, linea: int, col: int, op1: Instruccion, op2: Instruccion):
        super().__init__(Tipo(tipoDato.BOOL), linea, col)
        self.operador = operador
        self.op1 = op1
        self.op2 = op2

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        val1 = self.op1.interpretar(arbol, tabla)
        val2 = self.op2.interpretar(arbol, tabla)

        if isinstance(val1, Errores):
            return val1
        if isinstance(val2, Errores):
            return val2

        try:
            if self.operador == OperadoresRel.MENOR_IGUAL:
                return val1 <= val2
            elif self.operador == OperadoresRel.MAYOR_IGUAL:
                return val1 >= val2
            elif self.operador == OperadoresRel.MENOR_QUE:
                return val1 < val2
            elif self.operador == OperadoresRel.MAYOR_QUE:
                return val1 > val2
            elif self.operador == OperadoresRel.IGUAL_IGUAL:
                return val1 == val2
            elif self.operador == OperadoresRel.DIFERENTE:
                return val1 != val2
            else:
                return Errores("SEMANTICO", "Operador relacional desconocido", self.linea, self.col)
        except Exception as e:
            return Errores("SEMANTICO", f"Error en comparación: {str(e)}", self.linea, self.col)
