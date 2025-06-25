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
            self.scopes = ["global"]
            self.tabla_actual = []
            self.nombre_dato: str = ""
            self.entorno_contadores = {}  # <-- Agrega esto.
            self.procActual = None
            self.tabla_Procedimientos = {}

    @property
    def current_scope(self):
        return self.scopes[-1]

    def nuevoScope(self, tipo_entorno="scope"):
        # Usa un contador para cada tipo de entorno
        contador = self.entorno_contadores.get(tipo_entorno, 0) + 1
        self.entorno_contadores[tipo_entorno] = contador
        nombre_scope = f"{tipo_entorno}_{contador}"
        self.scopes.append(nombre_scope)
        return nombre_scope

    def borrarScope(self):
        if len(self.scopes) > 1:
            scope_to_remove = self.scopes.pop()

            # Solo elimina variables si es un scope temporal
            if scope_to_remove.startswith("temp"):
                self.tabla_actual = [
                    var for var in self.tabla_actual if var.scope != scope_to_remove
                ]

            return scope_to_remove
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

        # Primero buscar en el scope actual y todos los scopes ancestros
        idx = len(self.scopes) - 1
        while idx >= 0:
            current_scope = self.scopes[idx]
            # Buscar directo en current_scope
            for var in self.tabla_actual:
                if (
                    var.entidad == "variable"
                    and var.id == key
                    and var.scope == current_scope
                ):
                    return var
            idx -= 1

        # Si no se encontró, buscar en global explícitamente
        for var in self.tabla_actual:
            if var.entidad == "variable" and var.id == key and var.scope == "global":
                return var

        # No se encontró la variable
        raise KeyError(
            f"La variable '{id_}' no ha sido declarada en el entorno '{scope}' ni en global"
        )

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

    def actualizarVariable(
        self, name, nevValor, nevTipo=None, linea=None, columna=None, scope=None
    ):
        name = name.lower()  # Normalizar el identificador
        scope = scope or self.current_scope

        for sym in reversed(self.tabla_actual):
            if sym.entidad == "variable" and sym.id == name and sym.scope == scope:
                # Actualizar todos los campos proporcionados
                sym.valor = nevValor
                if nevTipo is not None:
                    sym.tipo = nevTipo
                if linea is not None:
                    sym.linea = linea
                if columna is not None:
                    sym.columna = columna
                return sym

        # Si llegamos aquí, no se encontró la variable
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
        self.scopes = ["global"]  # <-- Reinicia los scopes también
        self.entorno_contadores = {}  # <-- Reinicia los contadores de scopes

        Simbolo._id_cc = 0  # Reinicia el contador de IDs

    def setProc(self, nom):
        self.procActual = nom

    def getProc(self):
        return self.procActual
