from abc import ABC

from src.abstracto.CAST import clasAST
from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CTipo import Tipo, tipoDato
from src.simbolo.CArbol import Arbol
from src.simbolo.CInstancia import tabla_S as aTab

class Operadores:
    SUMA = 0
    RESTA = 1
    NEG = 2
    MULTIPLICACION = 3
    DIVISION = 4
    POTENCIA = 5
    MODULO = 6


class Aritmeticas(Instruccion, ABC):
    def __init__(self, operacion: int, linea: int, col: int, op1: Instruccion, op2: Instruccion):
        super().__init__(Tipo(tipoDato.ENTERO), linea, col)
        self.operacion = operacion
        self.operando1 = op1
        self.operando2 = op2

    def interpretar(self, arbol: Arbol, tabla):
        op_izq = self.operando1.interpretar(arbol, tabla)
        if isinstance(op_izq, Errores):
            return op_izq

        op_der = self.operando2.interpretar(arbol, tabla)
        if isinstance(op_der, Errores):
            return op_der

        if self.operacion == Operadores.SUMA:
            return self.suma(op_izq, op_der)
        elif self.operacion == Operadores.RESTA:
            return self.resta(op_izq, op_der)
        elif self.operacion == Operadores.MULTIPLICACION:
            return self.multipliacion(op_izq, op_der)
        elif self.operacion == Operadores.DIVISION:
            return self.division(op_izq, op_der)
        elif self.operacion == Operadores.POTENCIA:
            return self.potencia(op_izq, op_der)
        elif self.operacion == Operadores.MODULO:
            return self.modulo(op_izq, op_der)
        else:
            return Errores("SEMANTICO", "Aritméticas erróneas", self.linea, self.col)

    def suma(self, op1, op2):
        tipo1 = self.operando1.tipoDato.getTipo()
        tipo2 = self.operando2.tipoDato.getTipo()

        if tipo1 == tipoDato.ENTERO:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.ENTERO)
                return int(op1) + int(op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) + float(op2)
            elif tipo2 == tipoDato.CHAR:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) + ord(op2)
            elif tipo2 == tipoDato.STRING:
                self.tipoDato.setTipo(tipoDato.STRING)
                return str(op1) + op2
            else:
                return Errores("SEMANTICO", "Suma entre tipos no valida", self.linea, self.col)

        elif tipo1 == tipoDato.DECIMAL:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) + float(op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) + float(op2)
            elif tipo2 == tipoDato.CHAR:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) + ord(op2)
            elif tipo2 == tipoDato.STRING:
                self.tipoDato.setTipo(tipoDato.STRING)
                return str(op1) + op2
            else:
                return Errores("SEMANTICO", "Suma entre tipos no iguales", self.linea, self.col)

        elif tipo1 == tipoDato.BOOL:
            if tipo2 == tipoDato.STRING:
                self.tipoDato.setTipo(tipoDato.STRING)
                return str(op1) + op2
            else:
                return Errores("SEMANTICO", "Suma entre tipos no iguales", self.linea, self.col)
            
        elif tipo1 == tipoDato.CHAR:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.ENTERO)
                return ord(op1) + int(op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return ord(op1) + float(op2)
            elif tipo2 == tipoDato.CHAR:
                self.tipoDato.setTipo(tipoDato.STRING)
                return ord(op1) + ord(op2)
            elif tipo2 == tipoDato.STRING:
                self.tipoDato.setTipo(tipoDato.STRING)
                return str(ord(op1)) + op2
            else:
                return Errores("SEMANTICO", "Suma entre tipos no iguales", self.linea, self.col)
        
        elif tipo1 == tipoDato.STRING:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.STRING)
                return op1 + str(op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.STRING)
                return op1 + str(op2)
            elif  tipo2 == tipoDato.BOOL:
                self.tipoDato.setTipo(tipoDato.STRING)
                return op1 + str(op2)
            elif tipo2 == tipoDato.CHAR:
                self.tipoDato.setTipo(tipoDato.STRING)
                return op1 + str(ord(op2))
            elif tipo2 == tipoDato.STRING:
                self.tipoDato.setTipo(tipoDato.STRING)
                return op1 + op2
            else:
                return Errores("SEMANTICO", "Suma entre tipos no permitidos", self.linea, self.col)
            
        return Errores("SEMANTICO", "Suma erronea", self.linea, self.col)
    
    def resta(self, op1, op2):
        tipo1 = self.operando1.tipoDato.getTipo()
        tipo2 = self.operando2.tipoDato.getTipo()

        if tipo1 == tipoDato.ENTERO:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.ENTERO)
                return int(op1) - int(op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) - float(op2)
            elif tipo2 == tipoDato.CHAR:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) - ord(op2)
            else:
                return Errores("SEMANTICO", "Resta entre tipos no valida", self.linea, self.col)

        elif tipo1 == tipoDato.DECIMAL:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) - float(op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) - float(op2)
            elif tipo2 == tipoDato.CHAR:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) - ord(op2)
            else:
                return Errores("SEMANTICO", "Resta entre tipos no valida", self.linea, self.col)

        elif tipo1 == tipoDato.CHAR:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.ENTERO)
                return int(op1) - int(op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) - float(op2)
            else:
                return Errores("SEMANTICO", "Resta entre tipos no valida", self.linea, self.col)
            
        return Errores("SEMANTICO", "Resta  entre tipos no valida", self.linea, self.col)

    def multipliacion(self, op1, op2):
        tipo1 = self.operando1.tipoDato.getTipo()
        tipo2 = self.operando2.tipoDato.getTipo()

        if tipo1 == tipoDato.ENTERO:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.ENTERO)
                return int(op1) * int(op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) * float(op2)
            elif tipo2 == tipoDato.CHAR:
                self.tipoDato.setTipo(tipoDato.ENTERO)
                return float(op1) * ord(op2)
            else:
                return Errores("SEMANTICO", "Multiplicación entre tipos no valida", self.linea, self.col)

        elif tipo1 == tipoDato.DECIMAL:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) * float(op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) * float(op2)
            elif tipo2 == tipoDato.CHAR:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) * ord(op2)
            else:
                return Errores("SEMANTICO", "Multiplicación entre tipos no valida", self.linea, self.col)

        elif tipo1 == tipoDato.CHAR:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.ENTERO)
                return ord(op1) * int(op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return ord(op1) * float(op2)
            else:
                return Errores("SEMANTICO", "Multiplicación entre tipos no valida", self.linea, self.col)
            
        return Errores("SEMANTICO", "Multiplicación entre tipos no iguales", self.linea, self.col)

    def division(self, op1, op2):
        tipo1 = self.operando1.tipoDato.getTipo()
        tipo2 = self.operando2.tipoDato.getTipo()

        if tipo1 == tipoDato.ENTERO:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return int(op1) / int(op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) / float(op2)
            elif tipo2 == tipoDato.CHAR:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) / ord(op2)
            else:
                return Errores("SEMANTICO", "División entre tipos no valida", self.linea, self.col)

        elif tipo1 == tipoDato.DECIMAL:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) / float(op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) / float(op2)
            elif tipo2 == tipoDato.CHAR:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) / ord(op2)
            else:
                return Errores("SEMANTICO", "División entre tipos no valida", self.linea, self.col)

        elif tipo1 == tipoDato.CHAR:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return ord(op1) / int(op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return ord(op1) / float(op2)
            else:
                return Errores("SEMANTICO", "División entre tipos no valida", self.linea, self.col)
            
        return Errores("SEMANTICO", "División entre tipos no valida", self.linea, self.col)

    def potencia(self, op1, op2):
        tipo1 = self.operando1.tipoDato.getTipo()
        tipo2 = self.operando2.tipoDato.getTipo()

        if tipo1 == tipoDato.ENTERO:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.ENTERO)
                return int(op1) ** int(op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) ** float(op2)
            else:
                return Errores("SEMANTICO", "Potencia entre tipos no valida", self.linea, self.col)

        elif tipo1 == tipoDato.DECIMAL:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return pow(op1,op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return pow(op1,op2)
            else:
                return Errores("SEMANTICO", "Potencia entre tipos no valida", self.linea, self.col)

        return Errores("SEMANTICO", "Potencia entre tipos no valida", self.linea, self.col)
    
    def modulo(self, op1, op2):
        tipo1 = self.operando1.tipoDato.getTipo()
        tipo2 = self.operando2.tipoDato.getTipo()

        if tipo1 == tipoDato.ENTERO:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) %  float(op2) 
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) % float(op2)
            else:
                return Errores("SEMANTICO", "Mosulo entre tipos no valida", self.linea, self.col)

        elif tipo1 == tipoDato.DECIMAL:
            if tipo2 == tipoDato.ENTERO:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) %  float(op2)
            elif tipo2 == tipoDato.DECIMAL:
                self.tipoDato.setTipo(tipoDato.DECIMAL)
                return float(op1) %  float(op2)
            else:
                return Errores("SEMANTICO", "Modulo entre tipos no valida", self.linea, self.col)

        return Errores("SEMANTICO", "Modulo entre tipos no valida", self.linea, self.col)
    

    def graficar(self, grafo: clasAST):
        #Nodo principal 
        tipOperacion = self.getNOpe()
        nodoPrincipal = grafo.agregar_nodo(f"Aritmética: {tipOperacion}", fillcolor="white")

        #operando 1
        nodoOp1 = self.operando1.graficar(grafo)
        grafo.agregar_arista(nodoPrincipal, nodoOp1)

         #operando 2
        nodoOp2 = self.operando2.graficar(grafo)
        grafo.agregar_arista(nodoPrincipal, nodoOp2)

        return nodoPrincipal
    
    def getNOpe(self):
        if self.operacion == Operadores.SUMA:
            return '+'
        elif self.operacion == Operadores.RESTA:
            return '-'
        elif self.operacion == Operadores.MULTIPLICACION:
            return '*'
        elif self.operacion == Operadores.DIVISION:
            return '/'
        elif self.operacion == Operadores.POTENCIA:
            return '**'
        elif self.operacion == Operadores.MODULO:
            return '%'
        else:
            return ' '