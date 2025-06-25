from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo, tipoDato
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


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
        scope_name = tabla.nuevoScope("For")

        try:
            res_init = self.inicializacion.interpretar(arbol, tabla)
            if isinstance(res_init, Errores):
                return res_init

            while True:
                cond = self.condicion.interpretar(arbol, tabla)
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

                tabla.nuevoScope(f"{scope_name}_iter")

                try:
                    for instr in self.instrucciones:

                        if "entorno" in instr.interpretar.__code__.co_varnames:
                            if "en_ciclo" in instr.interpretar.__code__.co_varnames:
                                res = instr.interpretar(
                                    arbol, tabla, en_ciclo=True, entorno=scope_name
                                )
                            else:
                                res = instr.interpretar(
                                    arbol, tabla, entorno=scope_name
                                )
                        else:
                            if "en_ciclo" in instr.interpretar.__code__.co_varnames:
                                res = instr.interpretar(arbol, tabla, en_ciclo=True)
                            else:
                                res = instr.interpretar(arbol, tabla)

                        if isinstance(res, Errores):
                            arbol.errores.append(res)
                            continue

                        # Mantener el comportamiento para break/continue
                        if res == "continue":
                            break
                        if res == "break":
                            return None

                    res_upd = self.actualizacion.interpretar(arbol, tabla)
                    if isinstance(res_upd, Errores):
                        return res_upd
                finally:
                    tabla.borrarScope()

        finally:
            tabla.borrarScope()

        return None

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        if arbol and tabla:
            tabla_temp = tabla
            tabla_temp.nuevoScope("temp")
            try:
                res_init = self.inicializacion.interpretar(arbol, tabla_temp)
                # print("FOR INIT:", res_init)
                if isinstance(res_init, Errores):
                    # print("NO GRAFICA FOR POR INIT")
                    return None

                cond = self.condicion.interpretar(arbol, tabla)
                # print("FOR COND:", cond)
                if isinstance(cond, Errores) or not isinstance(cond, bool):
                    # print("NO GRAFICA FOR POR COND")
                    return None

                res_upd = self.actualizacion.interpretar(arbol, tabla)
                # print("FOR UPD:", res_upd)
                if isinstance(res_upd, Errores):
                    # print("NO GRAFICA FOR POR UPD")
                    return None

            finally:
                tabla_temp.borrarScope()

        # Si no hay errores, crear el nodo FOR normal
        nodoFor = grafo.agregar_nodo("For")
        nodoInicializacion = self.inicializacion.graficar(grafo, arbol, tabla)
        nodoCondicion = self.condicion.graficar(grafo, arbol, tabla)
        nodoActualizacion = self.actualizacion.graficar(grafo, arbol, tabla)
        nodoCuerpo = grafo.agregar_nodo("Cuerpo")

        # Verificar si los nodos son None antes de agregarlos
        if nodoInicializacion is not None:
            grafo.agregar_arista(nodoFor, nodoInicializacion)
        if nodoCondicion is not None:
            grafo.agregar_arista(nodoFor, nodoCondicion)
        if nodoActualizacion is not None:
            grafo.agregar_arista(nodoFor, nodoActualizacion)

        grafo.agregar_arista(nodoFor, nodoCuerpo)

        # El resto sigue igual...
        for instr in self.instrucciones:
            hijo = instr.graficar(grafo, arbol, tabla)
            if hijo is not None:
                grafo.agregar_arista(nodoCuerpo, hijo)

        return nodoFor
