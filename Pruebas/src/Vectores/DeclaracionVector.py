from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import tipoDato
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST
from src.Vectores.Vector import Vector


def _es_anidada(valores, dimensiones):
    if len(dimensiones) == 0:
        return not isinstance(valores, list)
    if not isinstance(valores, list) or len(valores) != dimensiones[0]:
        return False
    for v in valores:
        if not _es_anidada(v, dimensiones[1:]):
            return False
    return True


def _reconstruir_anidado(lista, dimensiones):
    if len(dimensiones) == 1:
        return lista
    if len(dimensiones) == 2:
        filas, columnas = dimensiones
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
    return lista


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
        # 1. Evaluar dimensiones declaradas
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

        # 2. Si hay RHS
        if self.valores is not None:
            if isinstance(self.valores, list):
                valores_evaluados = self._evaluar_valores(self.valores, arbol, tabla)
                if isinstance(valores_evaluados, Errores):
                    self.en_error = True
                    return valores_evaluados
                vals = valores_evaluados
                if _es_anidada(vals, dimensiones_evaluadas):
                    dims_res = dimensiones_evaluadas
                else:
                    dims_res = dimensiones_evaluadas
            else:
                res = self.valores.interpretar(arbol, tabla)
                if isinstance(res, Errores):
                    self.en_error = True
                    return res
                if isinstance(res, Vector):
                    vals = res.valores
                    dims_res = res.dimensiones
                    # Validar Sort: solo para vectores unidimensionales y numéricos
                    if len(dims_res) != 1:
                        return Errores(
                            "SEMANTICO",
                            "Sort solo puede aplicarse a vectores unidimensionales",
                            self.linea,
                            self.col
                        )
                    if self.tipo.getTipo() not in [tipoDato.ENTERO, tipoDato.DECIMAL]:
                        return Errores(
                            "SEMANTICO",
                            "Sort solo admite vectores numéricos (int o float)",
                            self.linea,
                            self.col
                        )
                elif isinstance(res, list):
                    vals = res
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

            if dims_res != dimensiones_evaluadas:
                self.en_error = True
                return Errores(
                    "SEMANTICO",
                    "Dimensiones no coinciden en declaración",
                    self.linea,
                    self.col,
                )
            if isinstance(vals, list) and not _es_anidada(vals, dimensiones_evaluadas):
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
                    f"No se pudo crear vector: {e}",
                    self.linea,
                    self.col,
                )
            if not hasattr(arbol, "vectores"):
                arbol.vectores = {}
            arbol.vectores[self.identificador] = vector
            return None

        # 6. Caso sin RHS: inicializar con ceros
        prod = 1
        for d in dimensiones_evaluadas:
            prod *= d
        default = 0
        if self.tipo.getTipo() == tipoDato.DECIMAL:
            default = 0.0
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

    def _evaluar_valores(self, valores, arbol, tabla, nivel=0):
        """Evalúa recursivamente valores de vectores multidimensionales"""
        if not isinstance(valores, list):
            valor = valores.interpretar(arbol, tabla)
            if isinstance(valor, Errores):
                return valor
            if not self._es_tipo_compatible(valor):
                return Errores(
                    "SEMANTICO",
                    f"El valor '{valor}' no es compatible con el tipo {self.tipo.tipo.name}",
                    self.linea,
                    self.col,
                )
            return valor

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
        return False

    def _verificar_dimensiones(self, dims_declaradas, valores):
        def verificar_nivel(dims, vals, nivel=0):
            if nivel >= len(dims):
                return not isinstance(vals, list)
            if not isinstance(vals, list) or len(vals) != dims[nivel]:
                return False
            for v in vals:
                if not verificar_nivel(dims, v, nivel + 1):
                    return False
            return True

        return verificar_nivel(dims_declaradas, valores)

    def _obtener_representacion_valores(self, valores):
        """Obtiene una representación legible de los valores para graficar"""
        if isinstance(valores, list):
            elementos = [self._obtener_representacion_valores(v) for v in valores]
            return f"[{', '.join(elementos)}]"
        else:
            if hasattr(valores, "valor"):
                return str(valores.valor)
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
        nodoDims = grafo.agregar_nodo(f"Dimensiones: {self.dimensiones}")
        grafo.agregar_arista(nodoDeclaracionVector, nodoDims)
        if self.valores is not None:
            nodoValores = grafo.agregar_nodo("Valores")
            grafo.agregar_arista(nodoDeclaracionVector, nodoValores)
            try:
                hijo = self.valores.graficar(grafo, arbol, tabla)
                if hijo is not None:
                    grafo.agregar_arista(nodoValores, hijo)
            except AttributeError:
                pass
        return nodoDeclaracionVector
