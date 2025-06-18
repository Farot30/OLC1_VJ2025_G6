from src.excepciones.CErrores import Errores
from src.simbolo.CTipo import Tipo, tipoDato
from src.abstracto.CInstruccion import Instruccion
from src.abstracto.CAST import clasAST


class sentIF(Instruccion):
    def __init__(self, condicion, instrucciones, linea, col, sig=None):
        super().__init__(Tipo(tipoDato.VOID), linea, col)
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.sig = sig

    def interpretar(self, arbol, tabla, en_ciclo=False, entorno=None):
        # bandera si encuentra errores en la condicion
        self.enError = False
        # else
        if self.condicion is None:
            tabla.nuevoScope("IF")
            for instruccion in self.instrucciones:
                # Usa la función genérica para determinar parámetros correctos
                if hasattr(instruccion, "interpretar"):
                    if "en_ciclo" in instruccion.interpretar.__code__.co_varnames:
                        if "entorno" in instruccion.interpretar.__code__.co_varnames:
                            res = instruccion.interpretar(
                                arbol, tabla, en_ciclo=en_ciclo, entorno=entorno
                            )
                        else:
                            res = instruccion.interpretar(
                                arbol, tabla, en_ciclo=en_ciclo
                            )
                    else:
                        if "entorno" in instruccion.interpretar.__code__.co_varnames:
                            res = instruccion.interpretar(arbol, tabla, entorno=entorno)
                        else:
                            res = instruccion.interpretar(arbol, tabla)

                    if isinstance(res, Errores):
                        arbol.errores.append(res)
                    elif res in ["continue", "break"]:
                        tabla.borrarScope()
                        return res
            tabla.borrarScope()
            return

        cond = self.condicion.interpretar(arbol, tabla)

        if isinstance(cond, Errores):
            self.enError = True
            return cond

        if self.condicion.tipoDato.getTipo() != tipoDato.BOOL:
            self.enError = True
            return Errores("Semantico", "La condición es errónea", self.linea, self.col)

        tabla.nuevoScope("If")
        if cond:
            # Si la condición es verdadera, se ejecuta
            for instruccion in self.instrucciones:
                # Propagar parámetros correctamente
                if hasattr(instruccion, "interpretar"):
                    if "en_ciclo" in instruccion.interpretar.__code__.co_varnames:
                        if "entorno" in instruccion.interpretar.__code__.co_varnames:
                            resultado = instruccion.interpretar(
                                arbol, tabla, en_ciclo=en_ciclo, entorno=entorno
                            )
                        else:
                            resultado = instruccion.interpretar(
                                arbol, tabla, en_ciclo=en_ciclo
                            )
                    else:
                        if "entorno" in instruccion.interpretar.__code__.co_varnames:
                            resultado = instruccion.interpretar(
                                arbol, tabla, entorno=entorno
                            )
                        else:
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
            # Propagar parámetros al else/elseif
            if hasattr(self.sig, "interpretar"):
                if "en_ciclo" in self.sig.interpretar.__code__.co_varnames:
                    if "entorno" in self.sig.interpretar.__code__.co_varnames:
                        return self.sig.interpretar(
                            arbol, tabla, en_ciclo=en_ciclo, entorno=entorno
                        )
                    else:
                        return self.sig.interpretar(arbol, tabla, en_ciclo=en_ciclo)
                else:
                    return self.sig.interpretar(arbol, tabla)
        return

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        if getattr(self, "enError", False):
            print("no se grafico")
            return None

        nodoIF = grafo.agregar_nodo("If")
        if self.condicion is not None:
            nodoCondicion = self.condicion.graficar(grafo, arbol, tabla)
            if nodoCondicion is not None:
                grafo.agregar_arista(nodoIF, nodoCondicion)

        nodoInstruccion = grafo.agregar_nodo("Instrucciones")
        grafo.agregar_arista(nodoIF, nodoInstruccion)

        for inst in self.instrucciones:
            hijo = inst.graficar(grafo, arbol, tabla)
            if hijo is not None:
                grafo.agregar_arista(nodoInstruccion, hijo)

        # else o elseif
        if self.sig is not None:
            if isinstance(self.sig, sentIF) and self.sig.condicion is not None:
                # elseif
                nodoElseIf = grafo.agregar_nodo("elseif")
                grafo.agregar_arista(nodoIF, nodoElseIf)
                hijoEI = self.sig.graficar(grafo, arbol, tabla)
                if hijoEI is not None:
                    grafo.agregar_arista(nodoElseIf, hijoEI)
            else:  # else
                nodoElse = grafo.agregar_nodo("else")
                grafo.agregar_arista(nodoIF, nodoElse)
                # Puede ser un bloque de instrucciones o un solo nodo
                if hasattr(self.sig, "graficar"):
                    hijoElse = self.sig.graficar(grafo, arbol, tabla)
                    if hijoElse is not None:
                        grafo.agregar_arista(nodoElse, hijoElse)
                elif hasattr(self.sig, "__iter__"):
                    for instr in self.sig:
                        hijo = instr.graficar(grafo, arbol, tabla)
                        if hijo is not None:
                            grafo.agregar_arista(nodoElse, hijo)

        return nodoIF
