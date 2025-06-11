from .CTipo import Tipo


class Simbolo:
    _id_cc = 0 #atreibuto de clase 

    def __init__(self, tipo: Tipo, id: str, entidad, valor, scope, linea, columna):
        Simbolo._id_cc += 1 
        self.nID = Simbolo._id_cc
        self.tipo = tipo
        self.id = id.lower()
        self.entidad = entidad
        self.valor = valor
        self.scope = scope
        self.linea = linea
        self.columna = columna

    def getTipo(self) -> Tipo:
        return self.tipo

    def setTipo(self, tipo: Tipo):
        self.tipo = tipo

    def getId(self) -> str:
        return self.id

    def setId(self, id: str):
        self.id = id

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor
        
    def getLinea(self):
        return self.linea

    def getColumna(self):
        return self.columna

    def to_dict(self):
        return {
            'id': self.nID,
            'nombre': self.id,
            'entidad': self.entidad,
            'tipo': self.tipo,
            'valor': self.valor,
            'scope': self.scope,
            'linea': self.linea,
            'columna': self.columna
        }
