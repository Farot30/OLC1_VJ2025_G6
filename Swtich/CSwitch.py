from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.simbolo.CTipo import tipoDato

class Switch(Instruccion):
    def __init__(self, expresion, casos, defecto, linea, col):
        super().__init__(None, linea, col)
        self.expresion = expresion
        self.casos = casos  
        self.defecto = defecto 

    def interpretar(self, arbol, tabla):
        valor = self.expresion.interpretar(arbol, tabla)
        if isinstance(valor, Errores):
            return valor

        if not isinstance(valor, int):
            return Errores("SEMANTICO", "La expresión del switch debe ser de tipo entero", self.linea, self.col)

        ejecutando = False
        for caso in self.casos:
            val_caso = caso.valor.interpretar(arbol, tabla)
            if isinstance(val_caso, Errores):
                return val_caso
            if ejecutando or val_caso == valor:
                ejecutando = True
                for instr in caso.instrucciones:
                    resultado = instr.interpretar(arbol, tabla)
                    if resultado == "break":
                        return None

        if not ejecutando and self.defecto:
            for instr in self.defecto:
                resultado = instr.interpretar(arbol, tabla)
                if resultado == "break":
                    return None

        return None


class Case:
    def __init__(self, valor, instrucciones):
        self.valor = valor
        self.instrucciones = instrucciones
