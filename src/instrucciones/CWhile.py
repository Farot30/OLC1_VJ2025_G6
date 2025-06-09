from src.abstracto.CInstruccion import Instruccion
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.excepciones.CErrores import Errores


class While(Instruccion):
    def __init__(self, condicion, instrucciones, linea, col):
        super().__init__(None, linea, col)
        self.condicion = condicion
        self.instrucciones = instrucciones

    def interpretar(self, arbol, tabla: tablaSimbolo):
        # evaluar condición inicial
        valor_cond = self.condicion.interpretar(arbol, tabla)
        if isinstance(valor_cond, Errores):
            arbol.errores.append(valor_cond)
            return
        # verificar booleano
        if not isinstance(valor_cond, bool):
            arbol.errores.append(
                Errores(
                    "SEMANTICO",
                    f"Condición de WHILE no booleana: {valor_cond}",
                    self.linea,
                    self.col,
                )
            )
            return
        # ejecución del ciclo
        while valor_cond:
            nueva_tabla = tablaSimbolo(tabla)
            for instr in self.instrucciones:
                res = instr.interpretar(arbol, nueva_tabla)
                if isinstance(res, Errores):
                    arbol.errores.append(res)
            valor_cond = self.condicion.interpretar(arbol, tabla)
            if isinstance(valor_cond, Errores):
                arbol.errores.append(valor_cond)
                break
