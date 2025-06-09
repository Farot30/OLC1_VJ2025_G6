from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo, tipoDato
from src.excepciones.CErrores import Errores
from src.simbolo.TablaSimbolo import tablaSimbolo


class For(Instruccion):
    def __init__(
        self,
        inicializacion,
        condicion,
        actualizacion,
        instrucciones,
        linea,
        col,
    ):
        super().__init__(Tipo(tipoDato.VOID), linea, col)
        self.inicializacion = inicializacion
        self.condicion = condicion
        self.actualizacion = actualizacion
        self.instrucciones = instrucciones

    def interpretar(self, arbol, tabla):
        # Ejecuta la inicialización
        res_init = self.inicializacion.interpretar(arbol, tabla)
        if isinstance(res_init, Errores):
            return res_init

        while True:
            cond = self.condicion.interpretar(arbol, tabla)
            x_val = (
                tabla.getVariable("x").getValor() if tabla.getVariable("x") else None
            )
            if isinstance(cond, Errores):
                return cond
            if not cond:
                break

            for instr in self.instrucciones:
                res = instr.interpretar(arbol, tabla)
                if isinstance(res, Errores):
                    return res

            res_upd = self.actualizacion.interpretar(arbol, tabla)
            if isinstance(res_upd, Errores):
                return res_upd
