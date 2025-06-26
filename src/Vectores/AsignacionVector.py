from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import tipoDato
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST
from src.Vectores.Vector import Vector


class AsignacionVector(Instruccion):
    def __init__(self, identificador, dimensiones, valores, linea, col):
        super().__init__(tipoDato.VECTOR, linea, col)
        self.identificador = identificador
        self.dimensiones = dimensiones
        self.valores = valores
        self.en_error = False  # Agregar bandera para rastrear errores

    def __str__(self):
        return (
            super().__str__()
            + f"IDENTIFICADOR: {self.identificador}\nDIMENSIONES: {self.dimensiones}\nVALORES: {self.valores}"
        )

    def _obtener_representacion_valores(self, valores):
        """Obtiene una representación legible de los valores para imprimir"""
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

    def interpretar(self, arbol, tabla):
        # Buscar el vector en arbol.vectores en lugar de la tabla de símbolos
        if not hasattr(arbol, "vectores") or self.identificador not in arbol.vectores:
            self.en_error = True
            return Errores(
                "SEMANTICO",
                f"El vector '{self.identificador}' no ha sido declarado",
                self.linea,
                self.col,
            )

        vector = arbol.vectores[self.identificador]

        # Validar que sea un Vector
        if not isinstance(vector, Vector):
            self.en_error = True
            return Errores(
                "SEMANTICO",
                f"'{self.identificador}' no es un vector",
                self.linea,
                self.col,
            )

        return vector.asignar_valores(self.dimensiones, self.valores, arbol, tabla)

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        try:
            # No graficar si hay error semántico
            if hasattr(self, "en_error") and self.en_error:
                return None

            nodoAsignacionVector = grafo.agregar_nodo("Asignación Vector")

            nodoId = grafo.agregar_nodo(f"ID: {self.identificador}")
            grafo.agregar_arista(nodoAsignacionVector, nodoId)

            # Graficar dimensiones (índices)
            if self.dimensiones:
                nodoDimensiones = grafo.agregar_nodo("Índices")
                grafo.agregar_arista(nodoAsignacionVector, nodoDimensiones)

                for dim in self.dimensiones:
                    if hasattr(dim, "graficar"):
                        nodoDim = dim.graficar(grafo, arbol, tabla)
                        if nodoDim:  # Verificar que no sea None
                            grafo.agregar_arista(nodoDimensiones, nodoDim)
                    else:
                        nodoDim = grafo.agregar_nodo(f"[{dim}]")
                        grafo.agregar_arista(nodoDimensiones, nodoDim)

            # Graficar valor a asignar
            if self.valores:
                nodoValor = (
                    self.valores.graficar(grafo, arbol, tabla)
                    if hasattr(self.valores, "graficar")
                    else None
                )
                if nodoValor:  # Verificar explícitamente que no sea None
                    grafo.agregar_arista(nodoAsignacionVector, nodoValor)

            return nodoAsignacionVector
        except Exception as e:
            print(f"Error al graficar AsignacionVector: {e}")
            return None
