from __future__ import annotations 
from src.instrucciones.CProcedimientos import Procedimientos
from src.abstracto.CAST import clasAST
from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CInstancia import tabla_S as aTab


class Arbol:
    def __init__(self, instrucciones: list[Instruccion]): 
        self.instrucciones = instrucciones
        self.consola = ""
        self.tabla_global = aTab
        self.errores = []
        self.procedimientos = []
        self.procActual = None
        
    def getConsola(self) -> str:
        return self.consola

    def setConsola(self, consola: str):
        self.consola = consola

    def getInstrucciones(self) -> list[Instruccion]: 
        return self.instrucciones

    def set_instrucciones(self, instrucciones: list[Instruccion]): 
        self.instrucciones = instrucciones

    def get_tabla_global(self) -> aTab: # type: ignore
        return self.tabla_global

    def setTablaGlobal(self, tabla: aTab): # type: ignore
        self.tabla_global = tabla

    def get_errores(self) -> list[Errores]:
        return self.errores

    def graficar(self, grafo:clasAST):
        nodoRaiz = grafo.agregar_nodo("REPORTE")
        for instru in self.instrucciones:
            nodoHijo = instru.graficar(grafo)
            grafo.agregar_arista(nodoRaiz, nodoHijo)
        return nodoRaiz
    
    def setProc(self, nom):
        self.procActual = nom

    def getProc(self):
        return self.procActual
    
    def setFuncion(self, prodec):
        self.procedimientos.append(prodec)

    def getFunciones(self):
        return self.procedimientos
    
    def getFuncion(self, id):
        for i in self.getFunciones():
            if isinstance(i, Procedimientos):
                if i.id.lower() == id.lower():
                    return i
        return None
            
        