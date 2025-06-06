from abc import ABC

from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CTipo import Tipo, tipoDato
from src.simbolo.CArbol import Arbol


class Operadores:
    SUMA = 0
    RESTA = 1
    MULTIPLICACION = 2
    DIVISION = 3
    POTENCIA = 4
    MODULO = 5
    NEG = 6


class Aritmeticas(Instruccion, ABC):
    def __init__(
        self, operacion: int, linea: int, col: int, op1: Instruccion, op2: Instruccion
    ):
        super().__init__(Tipo(tipoDato.ENTERO), linea, col)
        self.operacion = operacion
        self.operando1 = op1
        self.operando2 = op2

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        op_izq = self.operando1.interpretar(arbol, tabla)
        if isinstance(op_izq, Errores):
            return op_izq

        op_der = self.operando2.interpretar(arbol, tabla)
        if isinstance(op_der, Errores):
            return op_der

        if self.operacion == Operadores.SUMA:
            return self.suma(op_izq, op_der)
        else:
            return Errores("SEMANTICO", "Aritméticas erróneas", self.linea, self.col)

    def suma(self, op1, op2):
        tipo1 = self.operando1.tipoDato.getTipo()
        tipo2 = self.operando2.tipoDato.getTipo()

        if tipo1 == tipoDato.ENTERO:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.ENTERO)
                return int(op1) + int(op2)
            else:
                return Errores(
                    "SEMANTICO", "Suma entre tipos no iguales", self.linea, self.col
                )

        elif tipo1 == tipoDato.DECIMAL:
            if tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) + float(op2)
            else:
                return Errores(
                    "SEMANTICO", "Suma entre tipos no iguales", self.linea, self.col
                )

        return Errores("SEMANTICO", "Suma entre tipos no iguales", self.linea, self.col)
