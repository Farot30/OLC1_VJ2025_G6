from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import tipoDato
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST
from src.Vectores.Vector import Vector


class DeclaracionVector(Instruccion):
    def __init__(self, tipo, identificador, dimensiones, valores, linea, col):
        super().__init__(tipo, linea, col)
        self.tipo = tipo
        self.identificador = identificador
        self.dimensiones = dimensiones
        self.valores = valores
        self.en_error = False  # Agregar bandera para rastrear errores

    def __str__(self):
        return (
            super().__str__()
            + f"DIMENSIONES: {self.dimensiones}\nVALORES: {self.valores}"
        )

    def interpretar(self, arbol, tabla):
        # 1. Validar que las dimensiones coincidan con los valores proporcionados
        dimensiones_evaluadas = []
        for dim in self.dimensiones:
            if isinstance(dim, int):  # Si ya es un entero
                val = dim
            else:  # Si es un objeto con método interpretar
                val = dim.interpretar(arbol, tabla)
                if isinstance(val, Errores):
                    self.en_error = True
                    return val

            if not isinstance(val, int) or val <= 0:
                self.en_error = True
                return Errores(
                    "SEMANTICO",
                    f"La dimensión debe ser un entero positivo, no {val}",
                    self.linea,
                    self.col,
                )
            dimensiones_evaluadas.append(val)

        # 2. Evaluar valores y verificar tipos
        valores_evaluados = self._evaluar_valores(self.valores, arbol, tabla)
        if isinstance(valores_evaluados, Errores):
            return valores_evaluados

        # 3. Verificar que las dimensiones coincidan
        if not self._verificar_dimensiones(dimensiones_evaluadas, valores_evaluados):
            self.en_error = True
            return Errores(
                "SEMANTICO",
                "Las dimensiones declaradas no coinciden con los valores proporcionados",
                self.linea,
                self.col,
            )

        # 4. Crear vector (pero NO agregarlo a la tabla de símbolos)
        vector = Vector(
            tipo=self.tipo,
            id=self.identificador,
            dimensiones=dimensiones_evaluadas,
            valores=valores_evaluados,
            linea=self.linea,
            col=self.col,
            scope=tabla.current_scope,
        )

        # Almacenar el vector en otro lugar si es necesario
        # Por ejemplo, podrías almacenarlo en el árbol:
        if not hasattr(arbol, "vectores"):
            arbol.vectores = {}
        arbol.vectores[self.identificador] = vector

        tipo_str = self.tipo.tipo.name if hasattr(self.tipo, "tipo") else str(self.tipo)
        valores_str = self._obtener_representacion_valores(valores_evaluados)
        if len(valores_str) > 50:
            valores_str = valores_str[:47] + "..."

        print(
            f"Vector declarado: {self.identificador} [{tipo_str}] {dimensiones_evaluadas} = {valores_str}"
        )
        # Ya no llamamos a tabla.setVariable(vector)
        return None

    def _evaluar_valores(self, valores, arbol, tabla, nivel=0):
        """Evalúa recursivamente valores de vectores multidimensionales"""
        if not isinstance(valores, list):
            # Es un valor individual (expresión)
            valor = valores.interpretar(arbol, tabla)
            if isinstance(valor, Errores):
                return valor

            # Verificar tipo
            if not self._es_tipo_compatible(valor):
                return Errores(
                    "SEMANTICO",
                    f"El valor '{valor}' no es compatible con el tipo {self.tipo.tipo.name}",
                    self.linea,
                    self.col,
                )
            return valor

        # Es una lista de valores (vector/matriz)
        resultado = []
        for val in valores:
            evaluado = self._evaluar_valores(val, arbol, tabla, nivel + 1)
            if isinstance(evaluado, Errores):
                return evaluado
            resultado.append(evaluado)
        return resultado

    def _es_tipo_compatible(self, valor):
        """Verifica si el valor es compatible con el tipo del vector"""
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

    def _verificar_dimensiones(self, dims_declaradas, valores):
        """Verifica recursivamente que las dimensiones coincidan con la estructura"""

        def verificar_nivel(dims, valores_actuales, nivel=0):
            if nivel >= len(dims):
                # Ya no debería haber más niveles
                return not isinstance(valores_actuales, list)

            if not isinstance(valores_actuales, list):
                return False

            if len(valores_actuales) != dims[nivel]:
                return False

            # Verificar cada elemento del nivel actual
            for val in valores_actuales:
                if not verificar_nivel(dims, val, nivel + 1):
                    return False

            return True

        return verificar_nivel(dims_declaradas, valores)

    def _obtener_representacion_valores(self, valores):
        """Obtiene una representación legible de los valores para graficar"""
        if isinstance(valores, list):
            # Recursivamente procesar listas anidadas
            elementos = [self._obtener_representacion_valores(v) for v in valores]
            return f"[{', '.join(elementos)}]"
        else:
            # Para objetos de expresión
            if hasattr(valores, "valor"):
                return str(valores.valor)
            # Para valores primitivos
            return str(valores)

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        # Nodo principal para la declaración de vector
        if hasattr(self, "en_error") and self.en_error:
            return None
        nodoDeclaracionVector = grafo.agregar_nodo("Declaración Vector")

        # Nodo para el tipo
        tipo_str = self.tipo.tipo.name if hasattr(self.tipo, "tipo") else str(self.tipo)
        nodoTipo = grafo.agregar_nodo(f"Tipo: {tipo_str}")
        grafo.agregar_arista(nodoDeclaracionVector, nodoTipo)

        # Nodo para el identificador
        nodoId = grafo.agregar_nodo(f"ID: {self.identificador}")
        grafo.agregar_arista(nodoDeclaracionVector, nodoId)

        # Nodo para las dimensiones
        nodoDimensiones = grafo.agregar_nodo(f"Dimensiones: {self.dimensiones}")
        grafo.agregar_arista(nodoDeclaracionVector, nodoDimensiones)

        # Si hay valores, representarlos
        if self.valores:
            nodoValores = grafo.agregar_nodo("Valores")
            grafo.agregar_arista(nodoDeclaracionVector, nodoValores)

            # Usar el nuevo método para obtener una representación más legible
            representacion = self._obtener_representacion_valores(self.valores)
            # Truncar si es muy largo
            if len(representacion) > 30:
                representacion = representacion[:27] + "..."

            valorStr = grafo.agregar_nodo(representacion)
            grafo.agregar_arista(nodoValores, valorStr)

        return nodoDeclaracionVector
