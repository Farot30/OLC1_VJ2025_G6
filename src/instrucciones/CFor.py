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

        tabla.nuevoScope("For")  # Scope solo para el cuerpo del for
        while True:
            cond = self.condicion.interpretar(arbol, tabla)
            if isinstance(cond, Errores):
                tabla.borrarScope()
                return cond
            if not isinstance(cond, bool):
                tabla.borrarScope()
                return Errores(
                    "SEMANTICO",
                    "La condición del ciclo for debe ser booleana.",
                    self.linea,
                    self.col,
                )
            if not cond:
                break

            for instr in self.instrucciones:
                if "entorno" in instr.interpretar.__code__.co_varnames:
                    if "en_ciclo" in instr.interpretar.__code__.co_varnames:
                        res = instr.interpretar(
                            arbol, tabla, en_ciclo=True, entorno="For"
                        )
                    else:
                        res = instr.interpretar(arbol, tabla, entorno="For")
                else:
                    if "en_ciclo" in instr.interpretar.__code__.co_varnames:
                        res = instr.interpretar(arbol, tabla, en_ciclo=True)
                    else:
                        res = instr.interpretar(arbol, tabla)
                if isinstance(res, Errores):
                    tabla.borrarScope()
                    return res
                if res == "continue":
                    break
                if res == "break":
                    tabla.borrarScope()
                    return None

            res_upd = self.actualizacion.interpretar(arbol, tabla)
            if isinstance(res_upd, Errores):
                tabla.borrarScope()
                return res_upd
        tabla.borrarScope()
        return None

    def graficar(self, grafo: clasAST):
        nodoFor = grafo.agregar_nodo("For")
        nodoInicializacion = self.inicializacion.graficar(grafo)
        nodoCondicion = self.condicion.graficar(grafo)
        nodoActualizacion = self.actualizacion.graficar(grafo)
        nodoCuerpo = grafo.agregar_nodo("Cuerpo")

        grafo.agregar_arista(nodoFor, nodoInicializacion)
        grafo.agregar_arista(nodoFor, nodoCondicion)
        grafo.agregar_arista(nodoFor, nodoActualizacion)
        grafo.agregar_arista(nodoFor, nodoCuerpo)

        for instr in self.instrucciones:
            hijo = instr.graficar(grafo)
            grafo.agregar_arista(nodoCuerpo, hijo)

        return nodoFor
