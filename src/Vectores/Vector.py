from src.simbolo.CTipo import Tipo
from src.excepciones.CErrores import Errores
from src.simbolo.CTipo import tipoDato


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

    def asignar_valores(
        self, dimensiones, valor_nuevo, arbol, tabla, linea=None, col=None
    ):
        """
        Asigna un valor a una posición específica del vector
        """

        linea = linea if linea is not None else self.linea
        col = col if col is not None else self.col

        # 1. Evaluar el valor a asignar
        valor_evaluado = valor_nuevo.interpretar(arbol, tabla)
        if isinstance(valor_evaluado, Errores):
            return valor_evaluado

        # 2. VALIDACIÓN DE TIPOS: Verificar que el tipo del valor coincida con el tipo del vector
        if not self._es_tipo_compatible(valor_evaluado):
            return Errores(
                "SEMANTICO",
                f"No se puede asignar un valor de tipo {type(valor_evaluado).__name__} a un vector de tipo {self.tipo.tipo.name}",
                linea,
                col,
            )

        # 3. Evaluar todos los índices
        indices_evaluados = []
        for dim in dimensiones:
            valor_indice = dim.interpretar(arbol, tabla)
            if isinstance(valor_indice, Errores):
                return valor_indice
            if not isinstance(valor_indice, int):
                return Errores(
                    "SEMANTICO",
                    f"Los índices deben ser enteros, no {type(valor_indice).__name__}",
                    self.linea,
                    self.col,
                )
            indices_evaluados.append(valor_indice)

        # 4. Verificar si estamos asignando a un vector 2D (matriz)
        if len(self.dimensiones) == 2 and len(indices_evaluados) == 2:
            # Vector 2D (matriz)
            columnas, filas = self.dimensiones
            columna, fila = indices_evaluados

            # Validar límites
            if columna < 0 or columna >= columnas:
                return Errores(
                    "SEMANTICO",
                    f"Índice de columna fuera de rango (0-{columnas-1}): {columna}",
                    self.linea,
                    self.col,
                )
            if fila < 0 or fila >= filas:
                return Errores(
                    "SEMANTICO",
                    f"Índice de fila fuera de rango (0-{filas-1}): {fila}",
                    self.linea,
                    self.col,
                )

            # Asignar valor
            try:
                self.valores[fila][columna] = valor_evaluado
                return None
            except Exception as e:
                return Errores(
                    "SEMANTICO",
                    f"Error al asignar valor: {str(e)}",
                    self.linea,
                    self.col,
                )
        else:
            # Vector 1D u otras dimensiones
            try:
                # Navegar a la posición correcta
                container = self.valores
                for i in range(len(indices_evaluados) - 1):
                    idx = indices_evaluados[i]
                    # Validar límites en cada nivel
                    if idx < 0 or idx >= len(container):
                        return Errores(
                            "SEMANTICO",
                            f"Índice fuera de rango: {idx}",
                            self.linea,
                            self.col,
                        )
                    container = container[idx]

                # Asignar en el último nivel
                ultimo_indice = indices_evaluados[-1]
                if ultimo_indice < 0 or ultimo_indice >= len(container):
                    return Errores(
                        "SEMANTICO",
                        f"Índice fuera de rango: {ultimo_indice}",
                        self.linea,
                        self.col,
                    )

                container[ultimo_indice] = valor_evaluado
                return None
            except Exception as e:
                return Errores(
                    "SEMANTICO",
                    f"Error al asignar valor: {str(e)}",
                    self.linea,
                    self.col,
                )

    def _es_tipo_compatible(self, valor):
        """Verifica si un valor es compatible con el tipo del vector"""
        if self.tipo.getTipo() == tipoDato.ENTERO:
            return isinstance(valor, int)
        elif self.tipo.getTipo() == tipoDato.DECIMAL:
            return isinstance(valor, (int, float))  # Permitimos enteros en decimales
        elif self.tipo.getTipo() == tipoDato.STRING:
            return isinstance(valor, str)
        elif self.tipo.getTipo() == tipoDato.BOOL:
            return isinstance(valor, bool)
        elif self.tipo.getTipo() == tipoDato.CHAR:
            return isinstance(valor, str) and len(valor) == 1
        # Si llegamos aquí, el tipo no está soportado
        return False

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
        return f"{self._formato_vector(self.valores)}"

    def _formato_vector(self, valores):
        """Convierte recursivamente un vector en una cadena formateada"""
        if not isinstance(valores, list):
            return str(valores)

        elementos = [self._formato_vector(v) for v in valores]
        return f"[{', '.join(elementos)}]"
