from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


class AccesoVector(Instruccion):
    def __init__(self, id, indices, linea, col):
        super().__init__(Tipo(None), linea, col)
        self.id = id.lower()
        self.indices = indices

    def interpretar(self, arbol, tabla):
        # Verificar que el vector exista
        if not hasattr(arbol, "vectores") or self.id not in arbol.vectores:
            return Errores(
                "SEMANTICO",
                f"El vector '{self.id}' no ha sido declarado",
                self.linea,
                self.col,
            )

        vector = arbol.vectores[self.id]

        # Si el valor guardado no es una instancia de Vector (puede ser lista literal por alguna operación)
        if hasattr(vector, "valores"):
            valores = vector.valores
        else:
            valores = vector

        # NUEVA LÓGICA: Verificar si tenemos una matriz 2D y la convención es (columnas, filas)
        es_matriz_2d = hasattr(vector, "dimensiones") and len(vector.dimensiones) == 2

        # Navegar por los índices para obtener el valor deseado
        try:
            # CASO 1: Vector 2D (Matriz)
            if (
                hasattr(vector, "dimensiones")
                and len(vector.dimensiones) == 2
                and len(self.indices) == 2
            ):
                # En dd[columna][fila], queremos acceder a valores[fila][columna]
                columna = self.indices[0]
                fila = self.indices[1]

                # Verificar límites según las dimensiones declaradas
                columnas_totales = vector.dimensiones[0]
                filas_totales = vector.dimensiones[1]

                # Verificar que columna esté en rango
                if columna < 0 or columna >= columnas_totales:
                    return Errores(
                        "SEMANTICO",
                        f"Índice de columna fuera de rango (0-{columnas_totales-1})",
                        self.linea,
                        self.col,
                    )

                # Verificar que fila esté en rango
                if fila < 0 or fila >= filas_totales:
                    return Errores(
                        "SEMANTICO",
                        f"Índice de fila fuera de rango (0-{filas_totales-1})",
                        self.linea,
                        self.col,
                    )

                # Acceder con los índices invertidos
                return valores[fila][columna]

            # CASO 2: Vector 3D
            elif (
                hasattr(vector, "dimensiones")
                and len(vector.dimensiones) == 3
                and len(self.indices) == 3
            ):
                # Extraer dimensiones: [columnas, filas, capas]
                columnas, filas, capas = vector.dimensiones

                # Extraer índices proporcionados
                idx_capa, idx_fila, idx_columna = self.indices

                # Verificar límites de índices
                if idx_capa < 0 or idx_capa >= capas:
                    return Errores(
                        "SEMANTICO",
                        f"Índice de capa fuera de rango (0-{capas-1})",
                        self.linea,
                        self.col,
                    )

                if idx_fila < 0 or idx_fila >= filas:
                    return Errores(
                        "SEMANTICO",
                        f"Índice de fila fuera de rango (0-{filas-1})",
                        self.linea,
                        self.col,
                    )

                if idx_columna < 0 or idx_columna >= columnas:
                    return Errores(
                        "SEMANTICO",
                        f"Índice de columna fuera de rango (0-{columnas-1})",
                        self.linea,
                        self.col,
                    )

                # Acceder con el orden correcto
                return valores[idx_capa][idx_fila][idx_columna]

            # CASO 3: Vector 4D
            elif (
                hasattr(vector, "dimensiones")
                and len(vector.dimensiones) == 4
                and len(self.indices) == 4
            ):
                # Extraer dimensiones: [dim1, dim2, dim3, dim4]
                dim1, dim2, dim3, dim4 = vector.dimensiones

                # Extraer índices
                idx1, idx2, idx3, idx4 = self.indices

                # Verificar límites
                if (
                    idx1 < 0 or idx1 >= dim4
                ):  # La última dimensión declarada es la primera en indexación
                    return Errores(
                        "SEMANTICO",
                        f"Primer índice fuera de rango (0-{dim4-1})",
                        self.linea,
                        self.col,
                    )

                if idx2 < 0 or idx2 >= dim3:
                    return Errores(
                        "SEMANTICO",
                        f"Segundo índice fuera de rango (0-{dim3-1})",
                        self.linea,
                        self.col,
                    )

                if idx3 < 0 or idx3 >= dim2:
                    return Errores(
                        "SEMANTICO",
                        f"Tercer índice fuera de rango (0-{dim2-1})",
                        self.linea,
                        self.col,
                    )

                if idx4 < 0 or idx4 >= dim1:
                    return Errores(
                        "SEMANTICO",
                        f"Cuarto índice fuera de rango (0-{dim1-1})",
                        self.linea,
                        self.col,
                    )

                # Acceder con el orden correcto
                return valores[idx1][idx2][idx3][idx4]

            # CASO GENERAL: Para otras dimensiones o cuando no coincide número de índices
            else:
                resultado = valores
                for i in self.indices:
                    if not isinstance(resultado, list):
                        return Errores(
                            "SEMANTICO",
                            "Acceso inválido: se intentó indexar sobre un valor no indexable",
                            self.linea,
                            self.col,
                        )
                    if i < 0 or i >= len(resultado):
                        return Errores(
                            "SEMANTICO", "Índice fuera de rango", self.linea, self.col
                        )

                    resultado = resultado[i]

                return resultado

        except Exception as e:
            return Errores(
                "SEMANTICO",
                f"Error inesperado al acceder al vector: {str(e)}",
                self.linea,
                self.col,
            )

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        # Verificar que no haya errores previos
        try:
            # Intentar evaluar los índices para detectar posibles errores
            if arbol and tabla:
                for idx in self.indices:
                    if hasattr(idx, "interpretar"):
                        val = idx.interpretar(arbol, tabla)
                        if isinstance(val, Errores):
                            return None  # No graficar si hay error

            nodo_acceso = grafo.agregar_nodo(f"AccesoVector({self.id})")

            for idx in self.indices:
                # Manejar el caso donde idx puede ser un nodo AST
                if hasattr(idx, "graficar"):
                    nodo_indice = idx.graficar(grafo, arbol, tabla)
                    if nodo_indice:  # Verificar que no sea None
                        grafo.agregar_arista(nodo_acceso, nodo_indice)
                else:
                    # Para índices literales
                    nodo_indice = grafo.agregar_nodo(f"[{idx}]")
                    grafo.agregar_arista(nodo_acceso, nodo_indice)

            return nodo_acceso
        except Exception as e:
            print(f"Error al graficar AccesoVector: {e}")
            return (
                None  # Retornar None para que el nodo padre no intente crear una arista
            )
