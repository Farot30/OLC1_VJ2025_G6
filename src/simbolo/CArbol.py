from __future__ import annotations 
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

    def getConsola(self) -> str:
        return self.consola

    def setConsola(self, consola: str):
        self.consola = consola

    def getInstrucciones(self) -> list[Instruccion]: 
        return self.instrucciones

    def set_instrucciones(self, instrucciones: list[Instruccion]): 
        self.instrucciones = instrucciones

    def get_tabla_global(self) -> aTab:
        return self.tabla_global

    def setTablaGlobal(self, tabla: aTab):
        self.tabla_global = tabla

    def get_errores(self) -> list[Errores]:
        return self.errores

    def graficar(self, grafo:clasAST):
        nodoRaiz = grafo.agregar_nodo("REPORTE")
        for instru in self.instrucciones:
            nodoHijo = instru.graficar(grafo)
            grafo.agregar_arista(nodoRaiz, nodoHijo)
        return nodoRaiz