from src.instrucciones.CBreak import Break
from src.excepciones.CErrores import Errores
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CTipo import Tipo, tipoDato
from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CInstancia import tabla_S as aTab


class sentIF(Instruccion):
    def __init__(self, condicion, instrucciones, linea, col, sig = None):
        super().__init__(Tipo(tipoDato.VOID), linea, col)
        self.condicion = condicion # puede venir o no 
        self.instrucciones = instrucciones
        self.sig = sig #otro IF

    def interpretar(self, arbol, tabla):
        #else
        if self.condicion is None:
            nueTabla = aTab.nuevoScope()
            for instruccion in  self.instrucciones:
                res = instruccion.interpretar(arbol, nueTabla)
                if isinstance(res, Errores):
                    arbol.addErrores(res)
                elif  isinstance(res, Break):
                    return res
            return
        cond = self.condicion.interpretar(arbol, tabla)

        if isinstance(cond, Errores):
            return cond

        if self.condicion.tipoDato.getTipo() != tipoDato.BOOL:
            return Errores('Semantico', 'La condición es errónea', self.linea, self.col)

        nueva_tabla = aTab.nuevoScope()
        if cond:
            # Si la condición es verdadera, se ejecuta
            for instruccion in self.instrucciones:
                resultado = instruccion.interpretar(arbol, nueva_tabla)
                if isinstance(resultado, Errores):
                    arbol.addErrores(resultado)
            return    

         # else IF
        if self.sig is not None:
            return self.sig.interpretar(arbol, tabla)
        return                

