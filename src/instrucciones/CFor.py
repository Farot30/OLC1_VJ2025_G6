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
        # PRIMERO la inicialización, para que use el scope correcto
        res_init = self.inicializacion.interpretar(arbol, tabla)
        if isinstance(res_init, Errores):
            return res_init

        # Crear un scope único para este FOR
        scope_name = tabla.nuevoScope("For")

        try:
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

                # Crear un nuevo scope INTERNO para cada iteración
                # Esto es clave para los FOR anidados
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
                            return res
                        if res == "continue":
                            break
                        if res == "break":
                            return None

                    res_upd = self.actualizacion.interpretar(arbol, tabla)
                    if isinstance(res_upd, Errores):
                        return res_upd
                finally:
                    # Eliminar el scope de iteración
                    tabla.borrarScope()

        finally:
            # Eliminar el scope principal del FOR
            tabla.borrarScope()

        return None

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        nodoFor = grafo.agregar_nodo("For")
        nodoInicializacion = self.inicializacion.graficar(grafo, arbol, tabla)
        nodoCondicion = self.condicion.graficar(grafo, arbol, tabla)
        nodoActualizacion = self.actualizacion.graficar(grafo, arbol, tabla)
        nodoCuerpo = grafo.agregar_nodo("Cuerpo")

        grafo.agregar_arista(nodoFor, nodoInicializacion)
        grafo.agregar_arista(nodoFor, nodoCondicion)
        grafo.agregar_arista(nodoFor, nodoActualizacion)
        grafo.agregar_arista(nodoFor, nodoCuerpo)

        for instr in self.instrucciones:
            hijo = instr.graficar(grafo, arbol, tabla)
            if hijo is not None:  # <-- Solo agrega si el hijo existe
                grafo.agregar_arista(nodoCuerpo, hijo)

        return nodoFor
