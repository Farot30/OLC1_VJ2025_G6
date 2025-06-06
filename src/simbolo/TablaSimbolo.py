from typing import Dict
from src.simbolo.CSimbolo import Simbolo

class tablaSimbolo:
    def __init__(self):
        self.tabla_actual: Dict[str, Simbolo] = {}
        self.nombre_dato: str = ""

    def getTabla(self) -> Dict[str, Simbolo]:
        return self.tabla_actual

    def setTabla(self, tabla: Dict[str, Simbolo]):
        self.tabla_actual = tabla

    def getNombre(self) -> str:
        return self.nombre_dato

    def setNombre(self, nombre: str):
        self.nombre_dato = nombre

    def setVariable(self, simbolo: Simbolo) -> bool:
        key = simbolo.getId().lower()
        if key not in self.tabla_actual:
            self.tabla_actual[key] = simbolo
            return True
        return False

    def getVariable(self, id_: str):
        return self.tabla_actual.get(id_.lower())
