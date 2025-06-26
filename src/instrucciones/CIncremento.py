from src.abstracto.CInstruccion import Instruccion
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CArbol import Arbol
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


class Incremento(Instruccion):
    def __init__(self, id, linea, col, dimensiones=None):
        super().__init__(None, linea, col)
        self.id = id
        self.dimensiones = (
            dimensiones  # None para variables simples, lista para acceso a vectores
        )

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        # Determinar si es incremento de vector o variable simple
        if self.dimensiones is not None:
            # CASO: INCREMENTO DE VECTOR
            return self._incrementar_vector(arbol, tabla)
        else:
            # CASO: INCREMENTO DE VARIABLE SIMPLE
            return self._incrementar_variable(arbol, tabla)

    def _incrementar_variable(self, arbol, tabla):
        # Lógica original para incrementar variables
        simbolo = None
        for sym in reversed(tabla.getTabla()):
            if sym.entidad == "variable" and sym.id == self.id.lower():
                simbolo = sym
                break

        if simbolo is None:
            self.error = True
            return Errores(
                "SEMANTICO", f"Variable '{self.id}' no declarada", self.linea, self.col
            )

        valor = simbolo.getValor()
        if not isinstance(valor, (int, float)):
            self.error = True
            return Errores(
                "SEMANTICO",
                f"No se puede incrementar un valor no numérico",
                self.linea,
                self.col,
            )

        simbolo.setValor(valor + 1)
        self.error = False
        return None

    def _incrementar_vector(self, arbol, tabla):
        # Nueva lógica para incrementar elementos de vectores
        if not hasattr(arbol, "vectores") or self.id not in arbol.vectores:
            self.error = True
            return Errores(
                "SEMANTICO",
                f"El vector '{self.id}' no ha sido declarado",
                self.linea,
                self.col,
            )

        vector = arbol.vectores[self.id]

        # Evaluar índices
        indices = []
        for dim in self.dimensiones:
            val = dim.interpretar(arbol, tabla) if hasattr(dim, "interpretar") else dim
            if isinstance(val, Errores):
                self.error = True
                return val
            if not isinstance(val, int):
                self.error = True
                return Errores(
                    "SEMANTICO",
                    f"Índice debe ser entero, no {type(val).__name__}",
                    self.linea,
                    self.col,
                )
            indices.append(val)

        # Obtener el valor actual
        try:
            contenedor = vector.valores
            for i in range(len(indices) - 1):
                contenedor = contenedor[indices[i]]
            valor_actual = contenedor[indices[-1]]
        except (IndexError, TypeError):
            self.error = True
            return Errores(
                "SEMANTICO",
                f"Índice fuera de límites o tipo inválido",
                self.linea,
                self.col,
            )

        # Incrementar si es numérico
        if isinstance(valor_actual, (int, float)):
            nuevo_valor = valor_actual + 1
            contenedor[indices[-1]] = nuevo_valor
            self.error = False
            return None
        else:
            self.error = True
            return Errores(
                "SEMANTICO",
                f"No se puede incrementar un valor de tipo {type(valor_actual).__name__}",
                self.linea,
                self.col,
            )

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        if getattr(self, "error", False):
            return None

        if self.dimensiones is not None:
            # Graficar incremento de vector
            nodoInc = grafo.agregar_nodo("IncrementoVector")
            nodoID = grafo.agregar_nodo(f"ID: {self.id}")
            grafo.agregar_arista(nodoInc, nodoID)

            # Agregar los índices
            nodoIndices = grafo.agregar_nodo("Indices")
            grafo.agregar_arista(nodoInc, nodoIndices)

            for i, dim in enumerate(self.dimensiones):
                if hasattr(dim, "graficar"):
                    nodoDim = dim.graficar(grafo, arbol, tabla)
                else:
                    nodoDim = grafo.agregar_nodo(f"[{dim}]")
                grafo.agregar_arista(nodoIndices, nodoDim)
        else:
            # Graficar incremento normal
            nodoInc = grafo.agregar_nodo("Incremento")
            nodoID = grafo.agregar_nodo(f"ID: {self.id}")
            grafo.agregar_arista(nodoInc, nodoID)

        return nodoInc


class Decremento(Instruccion):
    def __init__(self, id, linea, col, dimensiones=None):
        super().__init__(None, linea, col)
        self.id = id
        self.dimensiones = (
            dimensiones  # None para variables simples, lista para acceso a vectores
        )

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        # Determinar si es decremento de vector o variable simple
        if self.dimensiones is not None:
            # CASO: DECREMENTO DE VECTOR
            return self._decrementar_vector(arbol, tabla)
        else:
            # CASO: DECREMENTO DE VARIABLE SIMPLE
            return self._decrementar_variable(arbol, tabla)

    def _decrementar_variable(self, arbol, tabla):
        # Lógica original para decrementar variables
        simbolo = None
        for sym in reversed(tabla.getTabla()):
            if sym.entidad == "variable" and sym.id == self.id.lower():
                simbolo = sym
                break

        if simbolo is None:
            self.error = True
            return Errores(
                "SEMANTICO", f"Variable '{self.id}' no declarada", self.linea, self.col
            )

        valor = simbolo.getValor()
        if not isinstance(valor, (int, float)):
            self.error = True
            return Errores(
                "SEMANTICO",
                f"No se puede decrementar un valor no numérico",
                self.linea,
                self.col,
            )

        simbolo.setValor(valor - 1)
        self.error = False
        return None

    def _decrementar_vector(self, arbol, tabla):
        # Nueva lógica para decrementar elementos de vectores
        if not hasattr(arbol, "vectores") or self.id not in arbol.vectores:
            self.error = True
            return Errores(
                "SEMANTICO",
                f"El vector '{self.id}' no ha sido declarado",
                self.linea,
                self.col,
            )

        vector = arbol.vectores[self.id]

        # Evaluar índices
        indices = []
        for dim in self.dimensiones:
            val = dim.interpretar(arbol, tabla) if hasattr(dim, "interpretar") else dim
            if isinstance(val, Errores):
                self.error = True
                return val
            if not isinstance(val, int):
                self.error = True
                return Errores(
                    "SEMANTICO",
                    f"Índice debe ser entero, no {type(val).__name__}",
                    self.linea,
                    self.col,
                )
            indices.append(val)

        # Obtener el valor actual
        try:
            contenedor = vector.valores
            for i in range(len(indices) - 1):
                contenedor = contenedor[indices[i]]
            valor_actual = contenedor[indices[-1]]
        except (IndexError, TypeError):
            self.error = True
            return Errores(
                "SEMANTICO",
                f"Índice fuera de límites o tipo inválido",
                self.linea,
                self.col,
            )

        # Decrementar si es numérico
        if isinstance(valor_actual, (int, float)):
            nuevo_valor = valor_actual - 1
            contenedor[indices[-1]] = nuevo_valor
            self.error = False
            return None
        else:
            self.error = True
            return Errores(
                "SEMANTICO",
                f"No se puede decrementar un valor de tipo {type(valor_actual).__name__}",
                self.linea,
                self.col,
            )

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        if getattr(self, "error", False):
            return None

        if self.dimensiones is not None:
            # Graficar decremento de vector
            nodoDec = grafo.agregar_nodo("DecrementoVector")
            nodoID = grafo.agregar_nodo(f"ID: {self.id}")
            grafo.agregar_arista(nodoDec, nodoID)

            # Agregar los índices
            nodoIndices = grafo.agregar_nodo("Indices")
            grafo.agregar_arista(nodoDec, nodoIndices)

            for i, dim in enumerate(self.dimensiones):
                if hasattr(dim, "graficar"):
                    nodoDim = dim.graficar(grafo, arbol, tabla)
                else:
                    nodoDim = grafo.agregar_nodo(f"[{dim}]")
                grafo.agregar_arista(nodoIndices, nodoDim)
        else:
            # Graficar decremento normal
            nodoDec = grafo.agregar_nodo("Decremento")
            nodoID = grafo.agregar_nodo(f"ID: {self.id}")
            grafo.agregar_arista(nodoDec, nodoID)

        return nodoDec
