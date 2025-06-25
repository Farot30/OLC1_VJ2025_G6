from src.simbolo.CTipo import Tipo
from src.excepciones.CErrores import Errores


class Vector:
    def __init__(
        self,
        tipo: Tipo,
        id: str,
        dimensiones: list,
        valores: list,
        linea: int,
        col: int,
        scope: str = "global",
    ):
        self.tipo = tipo
        self.id = id.lower()
        self.dimensiones = dimensiones
        self.valores = valores
        self.linea = linea
        self.col = col
        self.scope = scope
        self.entidad = "vector"

    @property
    def valor(self):
        """Propiedad que retorna valores para compatibilidad con ImprimirTabla"""
        return self.valores

    @property
    def columna(self):
        """Propiedad que retorna col para compatibilidad con ImprimirTabla"""
        return self.col

    def getTipo(self) -> Tipo:
        return self.tipo

    def setTipo(self, tipo: Tipo):
        self.tipo = tipo

    def getId(self) -> str:
        return self.id

    def setId(self, id: str):
        self.id = id

    def getDimensiones(self) -> list:
        return self.dimensiones

    def setDimensiones(self, dimensiones: list):
        self.dimensiones = dimensiones

    def getValores(self) -> list:
        return self.valores

    def setValores(self, valores: list):
        # Añadir validación
        if not self._validar_dimensiones_valores(valores):
            raise ValueError(
                f"Los valores no coinciden con las dimensiones {self.dimensiones}"
            )
        self.valores = valores

    def _validar_dimensiones_valores(self, valores):
        """Verifica que los valores coincidan con las dimensiones declaradas"""

        def verificar_nivel(dims, vals, nivel=0):
            if nivel >= len(dims):
                return not isinstance(vals, list)
            if not isinstance(vals, list) or len(vals) != dims[nivel]:
                return False
            return all(verificar_nivel(dims, v, nivel + 1) for v in vals)

        return verificar_nivel(self.dimensiones, valores)

    def _es_tipo_compatible(self, valor):
        """Verifica si el valor es compatible con el tipo del vector"""
        from src.simbolo.CTipo import tipoDato

        if self.tipo.getTipo() == tipoDato.ENTERO:
            return isinstance(valor, int)
        elif self.tipo.getTipo() == tipoDato.DECIMAL:
            return isinstance(valor, (int, float))
        elif self.tipo.getTipo() == tipoDato.STRING:
            return isinstance(valor, str)
        elif self.tipo.getTipo() == tipoDato.BOOL:
            return isinstance(valor, bool)
        # Agregar otros tipos según sea necesario
        return False

    def asignar_valores(self, indices, valor, arbol, tabla):
        """Asigna un valor a una posición específica del vector"""
        # Validar que los índices sean correctos
        if len(indices) != len(self.dimensiones):
            return Errores(
                "SEMANTICO",
                f"Dimensiones incorrectas: se esperaban {len(self.dimensiones)}, se recibieron {len(indices)}",
                self.linea,
                self.col,
            )

        # Evaluar el valor a asignar
        valor_evaluado = valor.interpretar(arbol, tabla)
        if isinstance(valor_evaluado, Errores):
            return valor_evaluado

        # Verificar que el tipo sea compatible
        if not self._es_tipo_compatible(valor_evaluado):
            return Errores(
                "SEMANTICO",
                f"Tipo incompatible: no se puede asignar {type(valor_evaluado)} a un vector de tipo {self.tipo.tipo.name}",
                self.linea,
                self.col,
            )

        # Acceder a la posición correcta
        try:
            contenedor = self.valores
            for i in range(len(indices) - 1):
                contenedor = contenedor[indices[i]]

            # Asignar el valor
            contenedor[indices[-1]] = valor_evaluado
            print(
                f"Se asignó {valor_evaluado} a {self.id}[{']['.join(map(str, indices))}]"
            )
            return None
        except IndexError:
            return Errores("SEMANTICO", "Índice fuera de rango", self.linea, self.col)

    def getLinea(self) -> int:
        return self.linea

    def getColumna(self) -> int:
        return self.col

    def to_dict(self):
        return {
            "tipo": self.tipo,
            "id": self.id,
            "dimensiones": self.dimensiones,
            "valores": self.valores,
            "linea": self.linea,
            "columna": self.col,
        }

    def __str__(self):
        """Devuelve una representación en cadena del vector"""
        return (
            f"Vector {self.id} {self.dimensiones}: {self._formato_vector(self.valores)}"
        )

    def _formato_vector(self, valores):
        """Convierte recursivamente un vector en una cadena formateada"""
        if not isinstance(valores, list):
            return str(valores)

        elementos = [self._formato_vector(v) for v in valores]
        return f"[{', '.join(elementos)}]"
