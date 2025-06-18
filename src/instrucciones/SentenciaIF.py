from src.abstracto.CAST import clasAST
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
        #bandera si encuentra errores en la condicion
        self.enError = False
        #else
        if self.condicion is None:
            tabla.nuevoScope("IF")
            for instruccion in  self.instrucciones:
                res = instruccion.interpretar(arbol, tabla)
                if isinstance(res, Errores):
                    arbol.errores.append(res)
                elif res in ["continue", "break"]:
                    tabla.borrarScope()
                    return res
                tabla.borrarScope()
                #elif  isinstance(res, Break):
                 #   return res
            return
        cond = self.condicion.interpretar(arbol, tabla)

        if isinstance(cond, Errores):
            self.enError = True
            return cond

        if self.condicion.tipoDato.getTipo() != tipoDato.BOOL:
            self.enError = True
            return Errores('Semantico', 'La condición es errónea', self.linea, self.col)

        tabla.nuevoScope("If")
        if cond:
            # Si la condición es verdadera, se ejecuta
            for instruccion in self.instrucciones:
                resultado = instruccion.interpretar(arbol, tabla)
                if isinstance(resultado, Errores):
                    arbol.errores.append(resultado)
                elif resultado in ["continue", "break"]:
                    tabla.borrarScope()
                    return resultado
            tabla.borrarScope()
            return    

        tabla.borrarScope()

         # else IF
        if self.sig is not None:
            return self.sig.interpretar(arbol, tabla)
        return                

    def graficar(self, grafo: clasAST):
        if getattr(self, 'enError', False): #accede a el valor de enError en forma dinamica
            print("no se grafico")
            return None
        
        nodoIF = grafo.agregar_nodo("If")

        if self.condicion is not None:
            nodoCondicion = self.condicion.graficar(grafo)
            grafo.agregar_arista(nodoIF, nodoCondicion)

        nodoInstruccion = grafo.agregar_nodo("Instrucciones")
        grafo.agregar_arista(nodoIF, nodoInstruccion)

        for inst in self.instrucciones:
            hijo = inst.graficar(grafo)
            grafo.agregar_arista(nodoInstruccion, hijo)

        #else o elseif
        if self.sig is not None:
            if isinstance(self.sig, sentIF) and self.sig.condicion is not None:
                #elseif
                nodoElseIf = grafo.agregar_nodo("elseif")
                grafo.agregar_arista(nodoIF, nodoElseIf)
                hijoEI = self.sig.graficar(grafo)
                grafo.agregar_arista(nodoElseIf, hijoEI)
            
            else:  #else
                nodoElse = grafo.agregar_nodo("else")
                grafo.agregar_arista(nodoIF, nodoElse)

                # Puede ser un bloque de instrucciones o un solo nodo
                if hasattr(self.sig, 'graficar'):
                    hijoElse = self.sig.graficar(grafo)
                    grafo.agregar_arista(nodoElse, hijoElse)
                elif hasattr(self.sig, '__iter__'):
                    for instr in self.sig:
                        hijo = instr.graficar(grafo)
                        grafo.agregar_arista(nodoElse, hijo)

        return nodoIF