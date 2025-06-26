from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import tipoDato
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST
from src.Vectores.Vector import Vector


def _es_anidada(valores, dimensiones):
    """
    Verifica si una estructura anidada coincide con las dimensiones.
    Para 2D, dimensiones[0] = columnas, dimensiones[1] = filas
    """
    if len(dimensiones) == 0:
        return not isinstance(valores, list)

    # Caso especial para 2D
    if len(dimensiones) == 2:
        columnas, filas = dimensiones
        # Verificar número de filas
        if not isinstance(valores, list) or len(valores) != filas:
            return False
        # Verificar número de columnas en cada fila
        for fila in valores:
            if not isinstance(fila, list) or len(fila) != columnas:
                return False
        return True

    # Para otras dimensiones
    if not isinstance(valores, list) or len(valores) != dimensiones[0]:
        return False
    for v in valores:
        if not _es_anidada(v, dimensiones[1:]):
            return False
    return True


def _reconstruir_anidado(lista, dimensiones):
    """
    Reconstruye una lista plana en una estructura anidada según dimensiones.
    Para 2D, dimensiones[0] = columnas, dimensiones[1] = filas
    Para 3D, dimensiones[0] = columnas, dimensiones[1] = filas, dimensiones[2] = capas
    """
    # Caso base: si solo queda una dimensión, devuelve un segmento de la lista
    if len(dimensiones) == 1:
        return lista

    # Para vectores 2D
    if len(dimensiones) == 2:
        columnas, filas = dimensiones  # Primera dimensión = columnas, segunda = filas
        if len(lista) != filas * columnas:
            return lista
        anidado = []
        idx = 0
        for f in range(filas):
            fila = []
            for c in range(columnas):
                fila.append(lista[idx])
                idx += 1
            anidado.append(fila)
        return anidado

    # NUEVO: Caso especial para vectores 3D
    if len(dimensiones) == 3:
        columnas, filas, capas = dimensiones  # [columnas, filas, capas]
        if len(lista) != capas * filas * columnas:
            return lista

        resultado = []
        for capa in range(capas):
            matriz_capa = []
            for fila in range(filas):
                fila_actual = []
                for col in range(columnas):
                    # Calcular índice lineal basado en convención [columnas, filas, capas]
                    idx = capa * (filas * columnas) + fila * columnas + col
                    fila_actual.append(lista[idx])
                matriz_capa.append(fila_actual)
            resultado.append(matriz_capa)
        return resultado

    # Para 4D o más, usamos recursión general
    tamanio_restante = 1
    for dim in dimensiones[1:]:
        tamanio_restante *= dim

    resultado = []
    for i in range(dimensiones[0]):
        inicio = i * tamanio_restante
        fin = inicio + tamanio_restante
        subvector = _reconstruir_anidado(lista[inicio:fin], dimensiones[1:])
        resultado.append(subvector)

    return resultado


class DeclaracionVector(Instruccion):
    def __init__(self, tipo, identificador, dimensiones, valores, linea, col):
        super().__init__(tipo, linea, col)
        self.tipo = tipo
        self.identificador = identificador.lower()
        self.dimensiones = dimensiones
        self.valores = valores
        self.en_error = False  # Agregar bandera para rastrear errores

    def __str__(self):
        return (
            super().__str__()
            + f"DIMENSIONES: {self.dimensiones}\nVALORES: {self.valores}"
        )

    def interpretar(self, arbol, tabla):
        # 1. Evaluar dimensiones declaradas (columnas, filas)
        dimensiones_evaluadas = []
        for dim in self.dimensiones:
            if isinstance(dim, int):
                val = dim
            else:
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

        # Preparar variables para valores finales
        vals = None
        dims_res = None

        # 2. Si hay RHS (valores proporcionados)
        if self.valores is not None:
            # Caso 2a: self.valores es lista literal de ASTs/nested lists
            if isinstance(self.valores, list):
                # Evaluar recursivamente lista de expresiones
                valores_evaluados = self._evaluar_valores(self.valores, arbol, tabla)
                if isinstance(valores_evaluados, Errores):
                    self.en_error = True
                    return valores_evaluados
                vals = valores_evaluados

                # VALIDACIÓN NUEVA: Verificar estructura antes de continuar
                if not self._verificar_dimensiones(dimensiones_evaluadas, vals):
                    self.en_error = True
                    return Errores(
                        "SEMANTICO",
                        f"La estructura de los datos proporcionados no coincide con las dimensiones declaradas {dimensiones_evaluadas}. En una matriz, el primer valor es COLUMNAS y el segundo es FILAS.",
                        self.linea,
                        self.col,
                    )

                dims_res = dimensiones_evaluadas
            else:
                # Caso 2b: self.valores es un nodo AST (Nativo, Shuffle, etc.)
                res = self.valores.interpretar(arbol, tabla)
                if isinstance(res, Errores):
                    self.en_error = True
                    return res

                # VALIDACIÓN DE TIPOS PARA VECTORES
                if isinstance(res, Vector):
                    # Verificar compatibilidad de tipos entre vectores
                    if not self._son_tipos_compatibles(
                        self.tipo.getTipo(), res.tipo.getTipo()
                    ):
                        self.en_error = True
                        return Errores(
                            "SEMANTICO",
                            f"No se puede asignar un vector de tipo {res.tipo.tipo.name} a un vector de tipo {self.tipo.tipo.name}",
                            self.linea,
                            self.col,
                        )

                    # Si es compatible, podemos intentar convertir los valores
                    try:
                        vals = self._convertir_valores_si_necesario(
                            res.valores, res.tipo.getTipo()
                        )
                    except Exception as e:
                        self.en_error = True
                        return Errores(
                            "SEMANTICO",
                            f"Error al convertir valores: {str(e)}",
                            self.linea,
                            self.col,
                        )

                    dims_res = res.dimensiones

                elif isinstance(res, list):
                    # Lista resultante de interpretar alguna llamada
                    # Verificar compatibilidad de tipos para cada elemento de la lista
                    try:
                        # Primero aplanamos la lista para verificar cada elemento
                        lista_plana = self._aplanar_lista(res)
                        for valor in lista_plana:
                            if not self._es_tipo_compatible(valor):
                                self.en_error = True
                                return Errores(
                                    "SEMANTICO",
                                    f"El valor '{valor}' de tipo {type(valor).__name__} no es compatible con el tipo {self.tipo.tipo.name}",
                                    self.linea,
                                    self.col,
                                )

                        vals = res
                    except Exception as e:
                        self.en_error = True
                        return Errores(
                            "SEMANTICO",
                            f"Error al verificar tipos: {str(e)}",
                            self.linea,
                            self.col,
                        )

                    if _es_anidada(vals, dimensiones_evaluadas):
                        dims_res = dimensiones_evaluadas
                    else:
                        dims_res = dimensiones_evaluadas
                else:
                    self.en_error = True
                    return Errores(
                        "SEMANTICO",
                        "RHS no es vector válido ni lista literal",
                        self.linea,
                        self.col,
                    )

            # 3. Verificar coincidencia de dimensiones (mantener esta verificación)
            if dims_res != dimensiones_evaluadas:
                self.en_error = True
                return Errores(
                    "SEMANTICO",
                    f"Las dimensiones declaradas {dimensiones_evaluadas} no coinciden con las dimensiones de los datos {dims_res}",
                    self.linea,
                    self.col,
                )
            # 4. Reconstruir anidado si lista plana
            if isinstance(vals, list) and not _es_anidada(vals, dimensiones_evaluadas):
                vals = _reconstruir_anidado(vals, dimensiones_evaluadas)
            # 5. Crear Vector y guardar
            try:
                vector = Vector(
                    tipo=self.tipo,
                    id=self.identificador,
                    dimensiones=dimensiones_evaluadas,
                    valores=vals,
                    linea=self.linea,
                    col=self.col,
                    scope=tabla.current_scope,
                )
            except Exception as e:
                self.en_error = True
                return Errores(
                    "SEMANTICO",
                    f"No se pudo crear vector: {e}",
                    self.linea,
                    self.col,
                )
            if not hasattr(arbol, "vectores"):
                arbol.vectores = {}
            arbol.vectores[self.identificador] = vector

            tabla.agregarVector(
                self.identificador,
                self.tipo,
                dimensiones_evaluadas,
                self.linea,
                self.col,
            )
            return None

        # 6. Caso sin RHS: inicializar con valores por defecto según tipo
        prod = 1
        for d in dimensiones_evaluadas:
            prod *= d

        # Valores por defecto según tipo
        if self.tipo.getTipo() == tipoDato.ENTERO:
            default = 0
        elif self.tipo.getTipo() == tipoDato.DECIMAL:
            default = 0.0
        elif self.tipo.getTipo() == tipoDato.STRING:
            default = ""
        elif self.tipo.getTipo() == tipoDato.BOOL:
            default = True
        elif self.tipo.getTipo() == tipoDato.CHAR:
            default = "\u0000"  # Carácter nulo en lugar de cadena vacía
        else:
            default = None

        vals = [default] * prod
        if not _es_anidada(vals, dimensiones_evaluadas):
            vals = _reconstruir_anidado(vals, dimensiones_evaluadas)

        try:
            vector = Vector(
                tipo=self.tipo,
                id=self.identificador,
                dimensiones=dimensiones_evaluadas,
                valores=vals,
                linea=self.linea,
                col=self.col,
                scope=tabla.current_scope,
            )
        except Exception as e:
            self.en_error = True
            return Errores(
                "SEMANTICO",
                f"No se pudo crear vector por defecto: {e}",
                self.linea,
                self.col,
            )
        if not hasattr(arbol, "vectores"):
            arbol.vectores = {}
        arbol.vectores[self.identificador] = vector
        return None

    # Método para convertir valores según el tipo destino
    def _convertir_valores_si_necesario(self, valores, tipo_origen):
        """Convierte los valores al tipo destino si es necesario"""
        # Si son listas anidadas, aplicar recursivamente
        if isinstance(valores, list):
            return [
                self._convertir_valores_si_necesario(v, tipo_origen) for v in valores
            ]

        # Conversión basada en el tipo destino
        tipo_destino = self.tipo.getTipo()

        # Si el tipo origen y destino son iguales, no necesitamos convertir
        if tipo_destino == tipo_origen:
            return valores

        # Convertir enteros a decimales
        if tipo_destino == tipoDato.DECIMAL and tipo_origen == tipoDato.ENTERO:
            return float(valores)

        # Convertir cualquier cosa a string
        if tipo_destino == tipoDato.STRING:
            return str(valores)

        # Si llegamos aquí, no podemos convertir
        raise ValueError(f"No se puede convertir de {tipo_origen} a {tipo_destino}")

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

    def _son_tipos_compatibles(self, tipo_destino, tipo_origen):
        """Verifica si un tipo de origen es compatible con un tipo de destino"""
        # Reglas de compatibilidad:
        # 1. Mismos tipos siempre son compatibles
        if tipo_destino == tipo_origen:
            return True

        # 2. Enteros son compatibles con decimales (promoción)
        if tipo_destino == tipoDato.DECIMAL and tipo_origen == tipoDato.ENTERO:
            return True

        # 3. Cualquier cosa puede convertirse a string (representación textual)
        if tipo_destino == tipoDato.STRING:
            return True

        # 4. Todos los demás casos son incompatibles
        return False

    def _aplanar_lista(self, lista):
        """Convierte una lista anidada en una lista plana"""
        resultado = []
        for item in lista:
            if isinstance(item, list):
                resultado.extend(self._aplanar_lista(item))
            else:
                resultado.append(item)
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
        elif self.tipo.getTipo() == tipoDato.CHAR:
            return isinstance(valor, str) and len(valor) == 1
        # Agregar otros tipos según sea necesario
        return False

    def _verificar_dimensiones(self, dims_declaradas, valores):
        """
        Verifica que las dimensiones declaradas coincidan con la estructura de los datos.
        Para 2D, dims_declaradas[0] = columnas, dims_declaradas[1] = filas
        """
        if not isinstance(valores, list):
            return False

        # Para un vector 2D
        if len(dims_declaradas) == 2:
            columnas, filas = (
                dims_declaradas  # Primera dimensión = columnas, segunda = filas
            )

            # Verificar número de filas
            if len(valores) != filas:
                return False

            # Verificar número de columnas en cada fila
            for fila in valores:
                if not isinstance(fila, list) or len(fila) != columnas:
                    return False
            return True

        # Para dimensiones mayores, usar recursión
        return self._verificar_recursivo(dims_declaradas, valores)

    def _verificar_recursivo(self, dims, valores, nivel=0):
        """Verifica recursivamente que una estructura anidada coincida con las dimensiones."""
        if nivel >= len(dims):
            return not isinstance(valores, list)

        # Caso especial para nivel 0 de una matriz 2D
        if nivel == 0 and len(dims) == 2:
            columnas, filas = dims
            if not isinstance(valores, list) or len(valores) != filas:
                return False
            for fila in valores:
                if not isinstance(fila, list) or len(fila) != columnas:
                    return False
            return True

        # Caso especial para nivel 0 de un tensor 3D (nuevo caso)
        if nivel == 0 and len(dims) == 3:
            # dims = [columnas, filas, capas]
            columnas, filas, capas = dims

            # Verificar número de capas
            if not isinstance(valores, list) or len(valores) != capas:
                return False

            # Verificar número de filas en cada capa
            for capa in valores:
                if not isinstance(capa, list) or len(capa) != filas:
                    return False

                # Verificar número de columnas en cada fila
                for fila in capa:
                    if not isinstance(fila, list) or len(fila) != columnas:
                        return False

            return True

        # Caso general para dimensiones 4D o mayores
        # Para estos casos, los índices siguen siendo de exterior a interior
        if not isinstance(valores, list) or len(valores) != dims[nivel]:
            return False
        for v in valores:
            if not self._verificar_recursivo(dims, v, nivel + 1):
                return False
        return True

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
        if hasattr(self, "en_error") and self.en_error:
            return None
        nodoDeclaracionVector = grafo.agregar_nodo("Declaración Vector")
        tipo_str = self.tipo.tipo.name if hasattr(self.tipo, "tipo") else str(self.tipo)
        nodoTipo = grafo.agregar_nodo(f"Tipo: {tipo_str}")
        grafo.agregar_arista(nodoDeclaracionVector, nodoTipo)
        nodoId = grafo.agregar_nodo(f"ID: {self.identificador}")
        grafo.agregar_arista(nodoDeclaracionVector, nodoId)

        # Actualizar el mensaje de dimensiones para aclarar la convención
        dims_str = self.dimensiones
        if len(self.dimensiones) == 2:
            dims_str = f"{self.dimensiones} (columnas, filas)"
        nodoDims = grafo.agregar_nodo(f"Dimensiones: {dims_str}")
        grafo.agregar_arista(nodoDeclaracionVector, nodoDims)

        if self.valores is not None:
            nodoValores = grafo.agregar_nodo("Valores")
            grafo.agregar_arista(nodoDeclaracionVector, nodoValores)
            # Si self.valores es AST, graficar; si es lista literal de ASTs, graficar recursivamente:
            try:
                hijo = self.valores.graficar(grafo, arbol, tabla)
                if hijo is not None:
                    grafo.agregar_arista(nodoValores, hijo)
            except AttributeError:
                pass
        return nodoDeclaracionVector
