class ReporteVectores:
    def __init__(self, arbol):
        self.arbol = arbol

    def _linearizar_vector(self, vector, dimensiones):
        """Convierte un vector multidimensional a su representación lineal"""
        # Para vectores de 1 dimensión, ya están lineales
        if len(dimensiones) == 1:
            return vector

        # Para vectores de más dimensiones
        resultado = []
        self._aplanar_recursivo(vector, resultado)
        return resultado

    def _aplanar_recursivo(self, array, resultado):
        """Función auxiliar para aplanar arrays anidados"""
        for item in array:
            if isinstance(item, list):
                self._aplanar_recursivo(item, resultado)
            else:
                resultado.append(item)

    # Añadir al final de la clase actual
    def _calcular_indice_lineal(self, indices, dimensiones):
        """Calcula el índice lineal a partir de índices multidimensionales"""
        indice = 0
        multiplicador = 1

        # Fórmula row-major: índice = i₁ × (d₂ × ... × dₙ) + i₂ × (d₃ × ... × dₙ) + ... + iₙ
        for i in range(len(indices) - 1, -1, -1):
            indice += indices[i] * multiplicador
            if i > 0:
                multiplicador *= dimensiones[i]

        return indice

    def _calcular_indices_originales(self, indice_lineal, dimensiones):
        """Convierte un índice lineal a índices multidimensionales"""
        indices = []
        temp = indice_lineal

        # Calcular los multiplicadores para cada dimensión
        multiplicadores = [1]
        for i in range(len(dimensiones) - 1, 0, -1):
            multiplicadores.insert(0, multiplicadores[0] * dimensiones[i])

        # Calcular los índices para cada dimensión
        for i in range(len(dimensiones)):
            if i < len(dimensiones) - 1:
                indices.append(temp // multiplicadores[i])
                temp %= multiplicadores[i]
            else:
                indices.append(temp)

        return indices

    def preparar_datos_vectores(self):
        """Prepara los datos de vectores para la plantilla"""
        if not hasattr(self.arbol, "vectores") or not self.arbol.vectores:
            return {}

        vectores_data = {}

        for id_vector, vector in self.arbol.vectores.items():
            # Prepara datos para este vector
            vector_info = {
                "tipo": (
                    vector.tipo.tipo.name
                    if hasattr(vector.tipo, "tipo")
                    else str(vector.tipo)
                ),
                "dimensiones": vector.dimensiones,
                "representacion_original": vector._formato_vector(vector.valores),
                "entorno": vector.entorno,  # if hasattr(vector, "entorno") else None
                "datos_lineales": [],
            }

            # Linearizar el vector
            datos_lineales = []
            self._aplanar_recursivo(vector.valores, datos_lineales)

            # Preparar datos lineales
            for i, valor in enumerate(datos_lineales):
                indices_orig = self._calcular_indices_originales(i, vector.dimensiones)
                vector_info["datos_lineales"].append(
                    {"indice": i, "valor": valor, "indices_orig": indices_orig}
                )

            vectores_data[id_vector] = vector_info

        return vectores_data

    def generar_reporte_consola(self):
        """Genera un reporte de vectores en la consola"""
        if not hasattr(self.arbol, "vectores") or not self.arbol.vectores:
            print("No hay vectores para reportar")
            return

        print("\n===== REPORTE DE VECTORES =====\n")

        # Para evitar procesar vectores duplicados
        vectores_procesados = set()

        for id_vector, vector in self.arbol.vectores.items():
            # Evitar vectores temporales o ya procesados
            if id_vector in vectores_procesados or id_vector == "sort_result":
                continue

            vectores_procesados.add(id_vector)

            # Verificar que el vector sea válido
            if not hasattr(vector, "dimensiones") or not hasattr(vector, "valores"):
                continue

            print(f"Vector: {id_vector}")
            tipo_str = (
                vector.tipo.tipo.name
                if hasattr(vector.tipo, "tipo")
                else str(vector.tipo)
            )
            print(f"Tipo: {tipo_str}")
            print(f"Dimensiones: {vector.dimensiones}")

            # Usar getattr para manejar atributos que pueden no existir
            print(f"Entorno: {getattr(vector, 'entorno', 'Global')}")

            print("\nRepresentación Original:")
            print(vector._formato_vector(vector.valores))

            # Resto del código...

            print("\nRepresentación Lineal (Row-major):")

            # Linearizar el vector (creamos una nueva lista para evitar modificar la original)
            datos_lineales = []
            self._aplanar_recursivo(vector.valores, datos_lineales)

            # Imprimir cabecera de tabla
            print(f"{'Índice':<10}{'Valor':<15}{'Índices Originales':<20}")
            print("-" * 45)

            # Imprimir datos
            for i, valor in enumerate(datos_lineales):
                indices_orig = self._calcular_indices_originales(i, vector.dimensiones)
                print(f"{i:<10}{str(valor):<15}{str(indices_orig):<20}")

            print("\n" + "=" * 50 + "\n")
