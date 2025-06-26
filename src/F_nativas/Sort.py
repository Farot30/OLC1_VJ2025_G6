from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import tipoDato
from src.Vectores.Vector import Vector
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


class FuncionSort(Instruccion):
    def __init__(self, vector_expr, reverse_expr, linea, col):
        super().__init__(tipoDato.VECTOR, linea, col)
        self.vector_expr = vector_expr
        self.reverse_expr = reverse_expr

    def interpretar(self, arbol, tabla):
        vector = None

        # Obtener el vector original
        if isinstance(self.vector_expr, str):
            if (
                not hasattr(arbol, "vectores")
                or self.vector_expr.lower() not in arbol.vectores
            ):
                return Errores(
                    "SEMANTICO",
                    f"Vector '{self.vector_expr}' no encontrado",
                    self.linea,
                    self.col,
                )
            vector = arbol.vectores[self.vector_expr.lower()]
        else:
            vector = self.vector_expr.interpretar(arbol, tabla)

        if isinstance(vector, Errores):
            return vector

        if not isinstance(vector, Vector):
            return Errores(
                "SEMANTICO",
                "Sort solo puede aplicarse a vectores",
                self.linea,
                self.col,
            )

        if len(vector.dimensiones) != 1:
            return Errores(
                "SEMANTICO",
                "Sort solo se permite en vectores unidimensionales",
                self.linea,
                self.col,
            )

        if vector.tipo.getTipo() not in [tipoDato.ENTERO, tipoDato.DECIMAL]:
            return Errores(
                "SEMANTICO", "Sort solo admite vectores numéricos", self.linea, self.col
            )

        # Determinar si es descendente
        reverse = False
        if self.reverse_expr:
            reverse_val = self.reverse_expr.interpretar(arbol, tabla)
            if isinstance(reverse_val, Errores):
                return reverse_val
            if not isinstance(reverse_val, bool):
                return Errores(
                    "SEMANTICO",
                    "El segundo parámetro de Sort debe ser booleano",
                    self.linea,
                    self.col,
                )
            reverse = reverse_val

        # Crear copia ordenada
        valores_ordenados = sorted(vector.valores[:], reverse=reverse)

        return Vector(
            tipo=vector.tipo,
            id="t",  # <--- identificador temporal para evitar error
            dimensiones=vector.dimensiones,
            valores=valores_ordenados,
            linea=self.linea,
            col=self.col,
            scope=tabla.current_scope,
        )

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        nodoPrincipal = grafo.agregar_nodo("Sort")
        hijo1 = self.vector_expr.graficar(grafo, arbol, tabla)
        grafo.agregar_arista(nodoPrincipal, hijo1)

        if self.reverse_expr:  # Cambiar de descendente_expr a reverse_expr
            hijo2 = self.reverse_expr.graficar(grafo, arbol, tabla)
            grafo.agregar_arista(nodoPrincipal, hijo2)

        return nodoPrincipal
