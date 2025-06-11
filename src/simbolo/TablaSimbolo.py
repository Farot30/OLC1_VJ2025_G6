from typing import Dict, List
from src.simbolo.CSimbolo import Simbolo

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            #las instancias las crea una sola vez, crea una sola tabla de simbolos
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class tablaSimbolo(metaclass = SingletonMeta):
    def __init__(self):
        if not hasattr(self, 'scopes'):
            self.scopes = ['global']  #finje el funcionamiento de una pila
            #scopes las instancias 
            self.tabla_actual= []
            self.nombre_dato: str = ""
          #  self.padre = padre  # <-- Nuevo

    @property
    def current_scope(self):
        return self.scopes[-1]
    
    def nuevoScope(self, id=None):
        id = id or f"scope_{len(self.scopes)}"
        self.scopes.append(id)
        return id
    
    def borrarScope(self):
        if len(self.scopes) > 1:
            return self.scopes.pop()
        raise RuntimeError("No se puede eliminar el scope global")
    
    def getTabla(self) -> []: # type: ignore
        return self.tabla_actual

    def setTabla(self, tabla: []): # type: ignore
        self.tabla_actual = tabla

    def getNombre(self) -> str:
        return self.nombre_dato

    def setNombre(self, nombre: str):
        self.nombre_dato = nombre

    def setVariable(self, simbolo: Simbolo) -> bool:
        key = simbolo.getId().lower()
        for var in self.tabla_actual:
            if var.id == key and var.scope == self.current_scope:
                return False  # Ya existe
        self.tabla_actual.append(simbolo)
        return True

    def getVariable(self, id_, scope=None):
        key = id_.lower()
        scope = scope or self.current_scope

        for var in reversed(self.tabla_actual):
            if var.entidad == 'variable' and var.id == key and var.scope == scope:
                return var.valor

        varE = self.scopes.index(scope)
        for enc in reversed(self.scopes[:varE]):
            for var in reversed(self.tabla_actual):
                if var.entidad == 'variable' and var.id == key and var.scope == enc:
                    return var.valor
        raise KeyError(f"La variable '{id_}' no ha sido declarada")
        '''if key in self.tabla_actual:
            return self.tabla_actual[key]
        elif self.padre is not None:
            return self.padre.getVariable(key)
        else:
            return None'''
        
    def agregarVariable(self, id, tipo, valor=None, linea=None, columna=None):
        sym = Simbolo(tipo=tipo, id=id, entidad='variable', 
                     valor=valor, scope=self.current_scope,
                     linea=linea, columna=columna)
        self.tabla_actual.append(sym)
        return sym
    
    def agregarFuncion(self, id, return_type, params=None, linea=None, columna=None):
        """Agregar una función al scope actual."""
        sym = Simbolo(tipo=return_type, id=id, entidad='function', 
                     valor={'params': params or []}, scope=self.current_scope,
                     linea=linea, columna=columna)
        self.tabla_actual.append(sym)
        return sym

    def actualizarVariable(self, name, nevValor, scope=None):
        scope = scope or self.current_scope
        for sym in reversed(self.tabla_actual):
            if sym.entidad == 'variable' and sym.id == name and sym.scope == scope:
                sym.valor = nevValor
                return sym
        raise KeyError(f"Variable '{name}' no declarada en scope '{scope}'")

    def ImprimirTabla(self):
        headers = ['id', 'nombre', 'entidad', 'tipo', 'valor', 'scope', 'linea', 'columna']
        print(" | ".join(headers))
        print("-" * (len(headers) * 15))
        for sym in self.tabla_actual:
            d = sym.to_dict()
            row = [str(d[h]) for h in headers]
            print(" | ".join(row))

    def existeVariable(self, id, scope) -> bool:
        for var in self.tabla_actual:
            if var.id == id.lower() and var.scope == scope:
                return True
        return False
