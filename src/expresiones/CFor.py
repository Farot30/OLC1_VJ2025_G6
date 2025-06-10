from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo, tipoDato
from src.excepciones.CErrores import Errores


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
            # --- Validación de tipo booleano ---
            if isinstance(cond, Errores):
                return cond
            if not isinstance(cond, bool):
                return Errores(
                    "SEMANTICO",
                    "La condición del ciclo for debe ser booleana.",
                    self.linea,
                    self.col,
                )
            if not cond:
                break

            for instr in self.instrucciones:
                res = instr.interpretar(arbol, tabla)
                if isinstance(res, Errores):
                    return res

            res_upd = self.actualizacion.interpretar(arbol, tabla)
            if isinstance(res_upd, Errores):
                return res_upd
