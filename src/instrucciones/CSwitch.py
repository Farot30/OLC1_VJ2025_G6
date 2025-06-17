from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


class Switch(Instruccion):
    def __init__(self, expresion, casos, defecto, linea, col):
        super().__init__(None, linea, col)
        self.expresion = expresion
        self.casos = casos
        self.defecto = defecto

    def interpretar(self, arbol, tabla):
        valor = self.expresion.interpretar(arbol, tabla)
        if isinstance(valor, Errores):
            return valor

        if not isinstance(valor, int):
            return Errores(
                "SEMANTICO",
                "La expresión del switch debe ser de tipo entero",
                self.linea,
                self.col,
            )

        tabla.nuevoScope("Switch")
        ejecutando = False
        for caso in self.casos:
            val_caso = caso.valor.interpretar(arbol, tabla)
            if isinstance(val_caso, Errores):
                tabla.borrarScope()
                return val_caso
            if ejecutando or val_caso == valor:
                ejecutando = True
                for instr in caso.instrucciones:
                    if "entorno" in instr.interpretar.__code__.co_varnames:
                        resultado = instr.interpretar(arbol, tabla, entorno="Switch")
                    else:
                        resultado = instr.interpretar(arbol, tabla)
                    if resultado == "break":
                        tabla.borrarScope()
                        return None
                    elif resultado == "continue":
                        tabla.borrarScope()
                        return "continue"

        if not ejecutando and self.defecto:
            for instr in self.defecto:
                if "entorno" in instr.interpretar.__code__.co_varnames:
                    resultado = instr.interpretar(arbol, tabla, entorno="Switch")
                else:
                    resultado = instr.interpretar(arbol, tabla)
                if resultado == "break":
                    tabla.borrarScope()
                    return None
                elif resultado == "continue":
                    tabla.borrarScope()
                    return "continue"

        tabla.borrarScope()
        return None

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        nodoSwitch = grafo.agregar_nodo("Switch")
        nodoExp = self.expresion.graficar(grafo, arbol, tabla)
        grafo.agregar_arista(nodoSwitch, nodoExp)

        nodoCasos = grafo.agregar_nodo("Casos")
        grafo.agregar_arista(nodoSwitch, nodoCasos)

        for caso in self.casos:
            nodoCase = grafo.agregar_nodo("Case")
            grafo.agregar_arista(nodoCasos, nodoCase)

            nodoValor = caso.valor.graficar(grafo, arbol, tabla)
            grafo.agregar_arista(nodoCase, nodoValor)

            nodoInstr = grafo.agregar_nodo("Instrucciones")
            grafo.agregar_arista(nodoCase, nodoInstr)
            for instr in caso.instrucciones:
                hijo = instr.graficar(grafo, arbol, tabla)
                if hijo is not None:  # <-- Solo agrega si el hijo existe
                    grafo.agregar_arista(nodoInstr, hijo)

        if self.defecto:
            nodoDefault = grafo.agregar_nodo("Default")
            grafo.agregar_arista(nodoSwitch, nodoDefault)

            nodoInstrDef = grafo.agregar_nodo("Instrucciones")
            grafo.agregar_arista(nodoDefault, nodoInstrDef)
            for instr in self.defecto:
                hijo = instr.graficar(grafo, arbol, tabla)
                if hijo is not None:  # <-- Solo agrega si el hijo existe
                    grafo.agregar_arista(nodoInstrDef, hijo)

        return nodoSwitch


class Case:
    def __init__(self, valor, instrucciones):
        self.valor = valor
        self.instrucciones = instrucciones
