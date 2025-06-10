from src.abstracto.CInstruccion import Instruccion
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.excepciones.CErrores import Errores


class DoWhile(Instruccion):
    def __init__(self, instrucciones, condicion, linea, col):
        super().__init__(None, linea, col)
        self.instrucciones = instrucciones
        self.condicion = condicion

    def interpretar(self, arbol, tabla: tablaSimbolo):
        while True:
            nueva_tabla = tablaSimbolo(tabla)
            salto = False
            for instr in self.instrucciones:
                if "en_ciclo" in instr.interpretar.__code__.co_varnames:
                    res = instr.interpretar(arbol, nueva_tabla, en_ciclo=True)
                else:
                    res = instr.interpretar(arbol, nueva_tabla)
                if isinstance(res, Errores):
                    arbol.errores.append(res)
                if res == "continue":
                    salto = True
                    break
                if res == "break":
                    return  # Sale del ciclo do-while
            # evaluar condición
            valor_cond = self.condicion.interpretar(arbol, tabla)
            if isinstance(valor_cond, Errores):
                arbol.errores.append(valor_cond)
                break
            if not isinstance(valor_cond, bool):
                arbol.errores.append(
                    Errores(
                        "SEMANTICO",
                        f"Condición de DO-WHILE no booleana: {valor_cond}",
                        self.linea,
                        self.col,
                    )
                )
                break
            if not valor_cond:
                break
            if salto:
                continue
