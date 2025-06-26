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
        """Obtiene el valor en la posición indicada por los índices"""
        contenedor, indice_final, tipo, error = self.obtener_referencia(arbol, tabla)

        if error:
            return error

        # Devolver el valor
        return contenedor[indice_final]

    def obtener_referencia(self, arbol, tabla):
        """
        Obtiene una referencia al elemento accedido.
        Retorna una tupla (contenedor, indice_final, tipo, error)
        donde:
        """
        # Verificar que el vector exista
        if not hasattr(arbol, "vectores") or self.id not in arbol.vectores:
            return (
                None,
                None,
                None,
                Errores(
                    "SEMANTICO",
                    f"El vector '{self.id}' no ha sido declarado",
                    self.linea,
                    self.col,
                ),
            )

        vector = arbol.vectores[self.id]
        tipo = vector.tipo if hasattr(vector, "tipo") else None

        # Si el valor guardado no es una instancia de Vector
        if hasattr(vector, "valores"):
            valores = vector.valores
        else:
            valores = vector

        try:
            # CASO 1: Vector 2D (Matriz)
            if (
                hasattr(vector, "dimensiones")
                and len(vector.dimensiones) == 2
                and len(self.indices) == 2
            ):
                columna = self.indices[0]
                fila = self.indices[1]

                # Verificar límites
                columnas_totales = vector.dimensiones[0]
                filas_totales = vector.dimensiones[1]

                if columna < 0 or columna >= columnas_totales:
                    return (
                        None,
                        None,
                        tipo,
                        Errores(
                            "SEMANTICO",
                            f"Índice de columna fuera de rango (0-{columnas_totales-1})",
                            self.linea,
                            self.col,
                        ),
                    )

                if fila < 0 or fila >= filas_totales:
                    return (
                        None,
                        None,
                        tipo,
                        Errores(
                            "SEMANTICO",
                            f"Índice de fila fuera de rango (0-{filas_totales-1})",
                            self.linea,
                            self.col,
                        ),
                    )

                # Devolver la fila como contenedor y la columna como índice (inversión)
                return valores[fila], columna, tipo, None

            # CASO 2: Vector 3D
            elif (
                hasattr(vector, "dimensiones")
                and len(vector.dimensiones) == 3
                and len(self.indices) == 3
            ):
                # Extraer dimensiones: [columnas, filas, capas]
                columnas, filas, capas = vector.dimensiones

                # Extraer índices proporcionados
                idx_columna, idx_fila, idx_capa = self.indices

                # Validar todos los índices
                if idx_columna < 0 or idx_columna >= columnas:
                    return (
                        None,
                        None,
                        tipo,
                        Errores(
                            "SEMANTICO",
                            f"Índice de columna fuera de rango (0-{columnas-1})",
                            self.linea,
                            self.col,
                        ),
                    )

                if idx_fila < 0 or idx_fila >= filas:
                    return (
                        None,
                        None,
                        tipo,
                        Errores(
                            "SEMANTICO",
                            f"Índice de fila fuera de rango (0-{filas-1})",
                            self.linea,
                            self.col,
                        ),
                    )

                if idx_capa < 0 or idx_capa >= capas:
                    return (
                        None,
                        None,
                        tipo,
                        Errores(
                            "SEMANTICO",
                            f"Índice de capa fuera de rango (0-{capas-1})",
                            self.linea,
                            self.col,
                        ),
                    )

                # Devolver el elemento adecuado para acceso
                return valores[idx_columna][idx_fila], idx_capa, tipo, None

            # CASO 3: Vector 4D
            elif (
                hasattr(vector, "dimensiones")
                and len(vector.dimensiones) == 4
                and len(self.indices) == 4
            ):
                # Similar a 2D y 3D, con validación para 4 dimensiones
                dim1, dim2, dim3, dim4 = vector.dimensiones
                idx1, idx2, idx3, idx4 = self.indices

                # Validación de límites
                if idx1 < 0 or idx1 >= dim1:
                    return (
                        None,
                        None,
                        tipo,
                        Errores(
                            "SEMANTICO",
                            f"Primer índice fuera de rango (0-{dim1-1})",
                            self.linea,
                            self.col,
                        ),
                    )

                if idx2 < 0 or idx2 >= dim2:
                    return (
                        None,
                        None,
                        tipo,
                        Errores(
                            "SEMANTICO",
                            f"Segundo índice fuera de rango (0-{dim2-1})",
                            self.linea,
                            self.col,
                        ),
                    )

                if idx3 < 0 or idx3 >= dim3:
                    return (
                        None,
                        None,
                        tipo,
                        Errores(
                            "SEMANTICO",
                            f"Tercer índice fuera de rango (0-{dim3-1})",
                            self.linea,
                            self.col,
                        ),
                    )

                if idx4 < 0 or idx4 >= dim4:
                    return (
                        None,
                        None,
                        tipo,
                        Errores(
                            "SEMANTICO",
                            f"Cuarto índice fuera de rango (0-{dim4-1})",
                            self.linea,
                            self.col,
                        ),
                    )

                # Devolver referencia para 4D
                return valores[idx1][idx2][idx3], idx4, tipo, None

            # CASO GENERAL: Para otras dimensiones
            else:
                # Verificar número de dimensiones
                if hasattr(vector, "dimensiones") and len(self.indices) != len(
                    vector.dimensiones
                ):
                    return (
                        None,
                        None,
                        tipo,
                        Errores(
                            "SEMANTICO",
                            f"El vector tiene {len(vector.dimensiones)} dimensiones pero se proporcionaron {len(self.indices)} índices",
                            self.linea,
                            self.col,
                        ),
                    )

                # Navegar por la estructura hasta el penúltimo índice
                contenedor = valores
                for i in range(len(self.indices) - 1):
                    if (
                        not isinstance(contenedor, list)
                        or self.indices[i] < 0
                        or self.indices[i] >= len(contenedor)
                    ):
                        return (
                            None,
                            None,
                            tipo,
                            Errores(
                                "SEMANTICO",
                                "Índice fuera de rango o estructura inválida",
                                self.linea,
                                self.col,
                            ),
                        )
                    contenedor = contenedor[self.indices[i]]

                # Verificar el último índice
                if not isinstance(contenedor, list):
                    return (
                        None,
                        None,
                        tipo,
                        Errores(
                            "SEMANTICO",
                            "Acceso inválido: se intentó indexar sobre un valor no indexable",
                            self.linea,
                            self.col,
                        ),
                    )

                ultimo_indice = self.indices[-1]
                if ultimo_indice < 0 or ultimo_indice >= len(contenedor):
                    return (
                        None,
                        None,
                        tipo,
                        Errores(
                            "SEMANTICO",
                            f"Índice fuera de rango (0-{len(contenedor)-1})",
                            self.linea,
                            self.col,
                        ),
                    )

                return contenedor, ultimo_indice, tipo, None

        except Exception as e:
            return (
                None,
                None,
                tipo,
                Errores(
                    "SEMANTICO",
                    f"Error inesperado al acceder al vector: {str(e)}",
                    self.linea,
                    self.col,
                ),
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
