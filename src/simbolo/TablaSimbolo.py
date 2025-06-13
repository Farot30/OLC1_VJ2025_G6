from typing import Dict, List
from src.simbolo.CSimbolo import Simbolo


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # las instancias las crea una sola vez, crea una sola tabla de simbolos
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class tablaSimbolo(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, "scopes"):
            self.scopes = ["global"]  # finje el funcionamiento de una pila
            # scopes las instancias
            self.tabla_actual = []
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

    def getTabla(self) -> []:  # type: ignore
        return self.tabla_actual

    def setTabla(self, tabla: []):  # type: ignore
        self.tabla_actual = tabla

    def getNombre(self) -> str:
        return self.nombre_dato

    def setNombre(self, nombre: str):
        self.nombre_dato = nombre

    def setVariable(self, simbolo: Simbolo) -> bool:
        key = simbolo.getId().lower()
        # Si estamos en global, solo debe fallar si ya existe en global
        if self.current_scope == "global":
            for var in self.tabla_actual:
                if var.id == key and var.scope == "global":
                    return False  # Ya existe en global
        else:
            # Si estamos en un entorno local, no debe existir en global ni en este entorno
            for var in self.tabla_actual:
                if var.id == key and (
                    var.scope == "global" or var.scope == self.current_scope
                ):
                    return False  # Ya existe en global o en este entorno
        self.tabla_actual.append(simbolo)
        return True

    def getVariable(self, id_, scope=None):
        key = id_.lower()
        scope = scope or self.current_scope
        # Busca primero en el scope actual
        for var in reversed(self.tabla_actual):
            if var.entidad == "variable" and var.id == key and var.scope == scope:
                return var
        # Si no está, busca en global
        if scope != "global":
            for var in reversed(self.tabla_actual):
                if (
                    var.entidad == "variable"
                    and var.id == key
                    and var.scope == "global"
                ):
                    return var
        raise KeyError(
            f"La variable '{id_}' no ha sido declarada en el entorno '{scope}' ni en global"
        )
        """if key in self.tabla_actual:
            return self.tabla_actual[key]
        elif self.padre is not None:
            return self.padre.getVariable(key)
        else:
            return None"""

    def agregarVariable(self, id, tipo, valor=None, linea=None, columna=None):
        sym = Simbolo(
            tipo=tipo,
            id=id,
            entidad="variable",
            valor=valor,
            scope=self.current_scope,
            linea=linea,
            columna=columna,
        )
        self.tabla_actual.append(sym)
        return sym

    def agregarFuncion(self, id, return_type, params=None, linea=None, columna=None):
        """Agregar una función al scope actual."""
        sym = Simbolo(
            tipo=return_type,
            id=id,
            entidad="function",
            valor={"params": params or []},
            scope=self.current_scope,
            linea=linea,
            columna=columna,
        )
        self.tabla_actual.append(sym)
        return sym

    def actualizarVariable(self, name, nevValor, scope=None):
        scope = scope or self.current_scope
        for sym in reversed(self.tabla_actual):
            if sym.entidad == "variable" and sym.id == name and sym.scope == scope:
                sym.valor = nevValor
                return sym
        raise KeyError(f"Variable '{name}' no declarada en scope '{scope}'")

    def ImprimirTabla(self):
        headers = [
            "id",
            "nombre",
            "entidad",
            "tipo",
            "valor",
            "entorno",
            "linea",
            "columna",
        ]
        print(" | ".join(headers))
        print("-" * (len(headers) * 15))
        for sym in self.tabla_actual:
            # Tipo como texto
            tipo_str = (
                sym.tipo.tipo.name
                if hasattr(sym.tipo, "tipo") and hasattr(sym.tipo.tipo, "name")
                else str(sym.tipo)
            )
            # Entorno: muestra el scope tal cual, solo cambia "global" por "Global"
            entorno_str = "Global" if sym.scope == "global" else str(sym.scope)
            # Valor como string
            valor_str = str(sym.valor)
            row = [
                str(
                    getattr(sym, "nID", "")
                ),  # Si tienes un atributo nID, si no, déjalo vacío
                sym.id,
                sym.entidad,
                tipo_str,
                valor_str,
                entorno_str,
                str(sym.linea),
                str(sym.columna),
            ]
            print(" |\t ".join(row))

    def tablaComoString(self):
        headers = [
            "id",
            "nombre",
            "entidad",
            "tipo",
            "valor",
            "entorno",
            "linea",
            "columna",
        ]
        output = " |\t ".join(headers) + "\n"
        output += "-" * (len(headers) * 15) + "\n"
        for sym in self.tabla_actual:
            tipo_str = (
                sym.tipo.tipo.name
                if hasattr(sym.tipo, "tipo") and hasattr(sym.tipo.tipo, "name")
                else str(sym.tipo)
            )
            entorno_str = "Global" if sym.scope == "global" else str(sym.scope)
            valor_str = str(sym.valor)
            row = [
                str(getattr(sym, "nID", "")),
                sym.id,
                sym.entidad,
                tipo_str,
                valor_str,
                entorno_str,
                str(sym.linea),
                str(sym.columna),
            ]
            output += " |\t ".join(row) + "\n"
        return output

    def existeVariable(self, id, scope) -> bool:
        for var in self.tabla_actual:
            if var.id == id.lower() and var.scope == scope:
                return True
        return False

    def limpiar(self):
        self.tabla_actual = []
        from src.simbolo.CSimbolo import Simbolo

        Simbolo._id_cc = 0  # Reinicia el contador de IDs
