from src.abstracto.CInstruccion import Instruccion
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


class While(Instruccion):
    def __init__(self, condicion, instrucciones, linea, col):
        super().__init__(None, linea, col)
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.en_error = False  # Bandera para saber si hay error en la condición

    def interpretar(self, arbol, tabla: tablaSimbolo):
        valor_cond = self.condicion.interpretar(arbol, tabla)
        if isinstance(valor_cond, Errores):
            self.en_error = True  # Marcar error para graficar
            arbol.errores.append(valor_cond)
            return valor_cond

        if not isinstance(valor_cond, bool):
            error = Errores(
                "SEMANTICO",
                f"Condición de WHILE no booleana: {valor_cond}",
                self.linea,
                self.col,
            )
            self.en_error = True  # Marcar error para graficar
            return error

        while valor_cond:
            tabla.nuevoScope("While")
            salto = False
            for instr in self.instrucciones:
                # Pasa el entorno "While" si la instrucción lo acepta
                if "entorno" in instr.interpretar.__code__.co_varnames:
                    if "en_ciclo" in instr.interpretar.__code__.co_varnames:
                        res = instr.interpretar(
                            arbol, tabla, en_ciclo=True, entorno="While"
                        )
                    else:
                        res = instr.interpretar(arbol, tabla, entorno="While")
                else:
                    if "en_ciclo" in instr.interpretar.__code__.co_varnames:
                        res = instr.interpretar(arbol, tabla, en_ciclo=True)
                    else:
                        res = instr.interpretar(arbol, tabla)

                if isinstance(res, Errores):
                    arbol.errores.append(res)
                elif res == "continue":
                    salto = True
                    break
                elif res == "break":
                    tabla.borrarScope()
                    return None  # Sale del ciclo while
            tabla.borrarScope()

            if salto:
                valor_cond = self.condicion.interpretar(arbol, tabla)
                continue

            valor_cond = self.condicion.interpretar(arbol, tabla)
            if isinstance(valor_cond, Errores):
                arbol.errores.append(valor_cond)
                break

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        # No graficar si hay error en la condición
        if getattr(self, "en_error", False):
            print("No se graficó WHILE por error en condición")
            return None

        nodoWhile = grafo.agregar_nodo("While")

        # Verificar que la condición sea válida para graficar
        if self.condicion is not None:
            nodoCondicion = self.condicion.graficar(grafo, arbol, tabla)
            if nodoCondicion is not None:  # Verificar que no sea None
                grafo.agregar_arista(nodoWhile, nodoCondicion)

        nodoCuerpo = grafo.agregar_nodo("Cuerpo")
        grafo.agregar_arista(nodoWhile, nodoCuerpo)

        for instr in self.instrucciones:
            if instr is not None:  # Verificar que la instrucción no sea None
                nodoInstr = instr.graficar(grafo, arbol, tabla)
                if (
                    nodoInstr is not None
                ):  # Verificar que el nodo resultante no sea None
                    grafo.agregar_arista(nodoCuerpo, nodoInstr)

        return nodoWhile
