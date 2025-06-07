from abc import ABC
from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo, tipoDato


class OperadoresRel:
    MENOR_IGUAL = 1
    MAYOR_QUE = 2
    MAYOR_IGUAL = 3


class Relacional(Instruccion, ABC):
    def __init__(self, operador, linea, col, op1, op2):
        super().__init__(Tipo(tipoDato.BOOL), linea, col)
        self.operador = operador
        self.op1 = op1
        self.op2 = op2

    def interpretar(self, arbol, tabla):
        val1 = self.op1.interpretar(arbol, tabla)
        val2 = self.op2.interpretar(arbol, tabla)
        if self.operador == OperadoresRel.MENOR_IGUAL:
            return val1 <= val2
        elif self.operador == OperadoresRel.MAYOR_QUE:
            return val1 > val2
        elif self.operador == OperadoresRel.MAYOR_IGUAL:
            return val1 >= val2
