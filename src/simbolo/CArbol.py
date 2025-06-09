from __future__ import annotations 
from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.simbolo.TablaSimbolo import tablaSimbolo


class Arbol:
    def __init__(self, instrucciones: list[Instruccion]): 
        self.instrucciones = instrucciones
        self.consola = ""
        self.tabla_global = tablaSimbolo()
        self.errores = []

    def getConsola(self) -> str:
        return self.consola

    def setConsola(self, consola: str):
        self.consola = consola

    def getInstrucciones(self) -> list[Instruccion]: 
        return self.instrucciones

    def set_instrucciones(self, instrucciones: list[Instruccion]): 
        self.instrucciones = instrucciones

    def get_tabla_global(self) -> tablaSimbolo:
        return self.tabla_global

    def setTablaGlobal(self, tabla: tablaSimbolo):
        self.tabla_global = tabla

    def get_errores(self) -> list[Errores]:
        return self.errores
