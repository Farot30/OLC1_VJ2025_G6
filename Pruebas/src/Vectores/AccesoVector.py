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
            return Errores("SEMANTICO", f"El vector '{self.id}' no ha sido declarado", self.linea, self.col)

        vector = arbol.vectores[self.id]

        # Si el valor guardado no es una instancia de Vector (puede ser lista literal por alguna operación)
        if hasattr(vector, 'valores'):
            valores = vector.valores
        else:
            valores = vector

        # Navegar por los índices para obtener el valor deseado
        try:
            for i in self.indices:
                if not isinstance(valores, list):
                    return Errores("SEMANTICO", "Acceso inválido: se intentó indexar sobre un valor no indexable", self.linea, self.col)
                if not isinstance(i, int):
                    return Errores("SEMANTICO", f"Índice no es un entero: {i}", self.linea, self.col)
                if i < 0 or i >= len(valores):
                    return Errores("SEMANTICO", "Índice fuera de rango", self.linea, self.col)
                valores = valores[i]
            return valores

        except Exception as e:
            return Errores("SEMANTICO", f"Error inesperado al acceder al vector: {str(e)}", self.linea, self.col)

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        nodo_acceso = grafo.agregar_nodo(f"AccesoVector({self.id})")
        for idx in self.indices:
            nodo_indice = grafo.agregar_nodo(f"[{idx}]")
            grafo.agregar_arista(nodo_acceso, nodo_indice)
        return nodo_acceso
