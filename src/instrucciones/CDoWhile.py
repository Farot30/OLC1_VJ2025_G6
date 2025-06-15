from src.abstracto.CInstruccion import Instruccion
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


class DoWhile(Instruccion):
    def __init__(self, instrucciones, condicion, linea, col):
        super().__init__(None, linea, col)
        self.instrucciones = instrucciones
        self.condicion = condicion

    def interpretar(self, arbol, tabla: tablaSimbolo):
        while True:
            tabla.nuevoScope("DoWhile")
            salto = False
            for instr in self.instrucciones:
                if "entorno" in instr.interpretar.__code__.co_varnames:
                    res = instr.interpretar(
                        arbol, tabla, en_ciclo=True, entorno="DoWhile"
                    )
                else:
                    res = (
                        instr.interpretar(arbol, tabla, en_ciclo=True)
                        if "en_ciclo" in instr.interpretar.__code__.co_varnames
                        else instr.interpretar(arbol, tabla)
                    )
                if isinstance(res, Errores):
                    arbol.errores.append(res)
                if res == "continue":
                    salto = True
                    break
                if res == "break":
                    tabla.borrarScope()
                    return  # Sale del ciclo do-while
            tabla.borrarScope()
            # evaluar condición
            valor_cond = self.condicion.interpretar(arbol, tabla)
            if isinstance(valor_cond, Errores):
                arbol.errores.append(valor_cond)
                break
            if not isinstance(valor_cond, bool):
                arbol.errores.append(
                    Errores(
                        "SEMANTICO",
                        f"Condición de DO-WHILE no booleana: {valor_cond}",
                        self.linea,
                        self.col,
                    )
                )
                break
            if not valor_cond:
                break
            if salto:
                continue

    def graficar(self, grafo: clasAST):
        nodoDoWhile = grafo.agregar_nodo("DoWhile")
        nodoCondicion = self.condicion.graficar(grafo)
        nodoCuerpo = grafo.agregar_nodo("Cuerpo")

        grafo.agregar_arista(nodoDoWhile, nodoCondicion)
        grafo.agregar_arista(nodoDoWhile, nodoCuerpo)

        for instr in self.instrucciones:
            nodoInstr = instr.graficar(grafo)
            grafo.agregar_arista(nodoCuerpo, nodoInstr)

        return nodoDoWhile
