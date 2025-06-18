from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST
from src.instrucciones.CBreak import Break
from src.simbolo.TablaSimbolo import tablaSimbolo 

class Switch(Instruccion):
    def __init__(self, expresion, casos, defecto, linea, col):
        super().__init__(None, linea, col)
        self.expresion = expresion
        self.casos = casos
        self.defecto = defecto

    def interpretar(self, arbol, tabla: tablaSimbolo):
        #Verificar que cada CASE tenga un BREAK al final
        for caso in self.casos:
            if not caso.tiene_break():
                error = Errores(
                    "SEMANTICO",
                    f"Falta un 'break' al final del CASE en la línea {caso.valor.linea}",
                    caso.valor.linea,
                    caso.valor.col,
                )
                arbol.errores.append(error)
                return error

        # Verificar que el default tenga break si existe
        if self.defecto and len(self.defecto) > 0:
            tiene_break_default = False
            # El default puede tener un break si es la última instrucción
            if len(self.defecto) > 0:
                tiene_break_default = isinstance(self.defecto[-1], Break)
            if not tiene_break_default:
                error = Errores(
                    "SEMANTICO",
                    f"Falta un 'break' al final del DEFAULT",
                    self.linea,
                    self.col,
                )
                arbol.errores.append(error)
                return error 
        valor_expresion_switch = self.expresion.interpretar(arbol, tabla)
        if isinstance(valor_expresion_switch, Errores):
            return valor_expresion_switch

        if not isinstance(valor_expresion_switch, int):
            error = Errores(
                "SEMANTICO",
                "La expresión del SWITCH debe ser de tipo entero",
                self.linea,
                self.col,
            )
            arbol.errores.append(error)
            return error # Retornar el error para detener la interpretación de este Switch
        
        tabla.nuevoScope("Switch")
        ejecutando_casos = False
        romper_switch = False

        for caso in self.casos:
            valor_caso_actual = caso.valor.interpretar(arbol, tabla)
            if isinstance(valor_caso_actual, Errores):
                tabla.borrarScope()
                return valor_caso_actual 


            if ejecutando_casos or valor_caso_actual == valor_expresion_switch:
                ejecutando_casos = True
                for instr in caso.instrucciones:
                    parametros_interpretar = instr.interpretar.__code__.co_varnames
                    if "entorno" in parametros_interpretar and "en_ciclo" in parametros_interpretar:
                        resultado_instr = instr.interpretar(arbol, tabla, entorno="Switch", en_ciclo=True)
                    elif "entorno" in parametros_interpretar:
                        resultado_instr = instr.interpretar(arbol, tabla, entorno="Switch")
                    elif "en_ciclo" in parametros_interpretar:
                        resultado_instr = instr.interpretar(arbol, tabla, en_ciclo=True)
                    else:
                        resultado_instr = instr.interpretar(arbol, tabla)

                    if isinstance(resultado_instr, Errores):
                        arbol.errores.append(resultado_instr)
                    elif resultado_instr == "break":
                        romper_switch = True
                        break 
                    elif resultado_instr == "continue":
                        tabla.borrarScope()
                        return "continue"
            if romper_switch:
                break

        if not ejecutando_casos and self.defecto:
            for instr in self.defecto:
                parametros_interpretar = instr.interpretar.__code__.co_varnames
                if "entorno" in parametros_interpretar and "en_ciclo" in parametros_interpretar:
                    resultado_instr = instr.interpretar(arbol, tabla, entorno="Switch", en_ciclo=True)
                elif "entorno" in parametros_interpretar:
                    resultado_instr = instr.interpretar(arbol, tabla, entorno="Switch")
                elif "en_ciclo" in parametros_interpretar:
                    resultado_instr = instr.interpretar(arbol, tabla, en_ciclo=True)
                else:
                    resultado_instr = instr.interpretar(arbol, tabla)

                if isinstance(resultado_instr, Errores):
                    arbol.errores.append(resultado_instr)
                elif resultado_instr == "break":
                    break
                elif resultado_instr == "continue":
                    tabla.borrarScope()
                    return "continue"

        tabla.borrarScope()
        return None 

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        valor_expresion_para_graficar = None
        try:
            if arbol is not None and tabla is not None:
                valor_expresion_para_graficar = self.expresion.interpretar(arbol, tabla)
        except Exception:
            valor_expresion_para_graficar = None 

     
        if isinstance(valor_expresion_para_graficar, Errores) or not isinstance(valor_expresion_para_graficar, int):
         return None

        for caso in self.casos:
            if not caso.tiene_break():
                return None
        if self.defecto and len(self.defecto) > 0 and not isinstance(self.defecto[-1], Break):
            return None
        
        # Graficar el Switch
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
                if hijo is not None:
                    grafo.agregar_arista(nodoInstr, hijo)

        if self.defecto:
            nodoDefault = grafo.agregar_nodo("Default")
            grafo.agregar_arista(nodoSwitch, nodoDefault)

            nodoInstrDef = grafo.agregar_nodo("Instrucciones")
            grafo.agregar_arista(nodoDefault, nodoInstrDef)
            for instr in self.defecto:
                hijo = instr.graficar(grafo, arbol, tabla)
                if hijo is not None:
                    grafo.agregar_arista(nodoInstrDef, hijo)

        return nodoSwitch


class Case:
    def __init__(self, valor, instrucciones):
        self.valor = valor
        self.instrucciones = instrucciones

    def tiene_break(self):
        """Verifica si el caso termina con un break"""
        if not self.instrucciones:
            return False
        # Verificar si la última instrucción es un Break
        return isinstance(self.instrucciones[-1], Break)