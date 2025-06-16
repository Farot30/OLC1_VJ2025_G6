from src.abstracto.CInstruccion import Instruccion
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


class While(Instruccion):
    def __init__(self, condicion, instrucciones, linea, col):
        super().__init__(None, linea, col)
        self.condicion = condicion
        self.instrucciones = instrucciones

    def interpretar(self, arbol, tabla: tablaSimbolo):
        valor_cond = self.condicion.interpretar(arbol, tabla)
        if isinstance(valor_cond, Errores):
            arbol.errores.append(valor_cond)
            return
        if not isinstance(valor_cond, bool):
            arbol.errores.append(
                Errores(
                    "SEMANTICO",
                    f"Condición de WHILE no booleana: {valor_cond}",
                    self.linea,
                    self.col,
                )
            )
            return
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
                if res == "continue":
                    salto = True
                    break
                if res == "break":
                    tabla.borrarScope()
                    return  # Sale del ciclo while
            tabla.borrarScope()
            if salto:
                valor_cond = self.condicion.interpretar(arbol, tabla)
                continue
            valor_cond = self.condicion.interpretar(arbol, tabla)
            if isinstance(valor_cond, Errores):
                arbol.errores.append(valor_cond)
                break

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        nodoWhile = grafo.agregar_nodo("While")
        nodoCondicion = self.condicion.graficar(grafo, arbol, tabla)
        nodoCuerpo = grafo.agregar_nodo("Cuerpo")

        grafo.agregar_arista(nodoWhile, nodoCondicion)
        grafo.agregar_arista(nodoWhile, nodoCuerpo)

        for instr in self.instrucciones:
            nodoInstr = instr.graficar(grafo, arbol, tabla)
            grafo.agregar_arista(nodoCuerpo, nodoInstr)

        return nodoWhile
