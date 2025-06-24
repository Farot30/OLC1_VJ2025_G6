from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.Vectores.Vector import Vector


def _aplanar(valores):
    if not isinstance(valores, list):
        return [valores]
    out = []
    for x in valores:
        out += _aplanar(x)
    return out


def _reconstruir_anidado(lista, dimensiones):
    # Reconstruye lista plana a lista anidada según dimensiones dadas
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
    # Para >2D no implementado
    return lista


class Shuffle(Instruccion):
    def __init__(self, id_vec, linea, col):
        super().__init__(None, linea, col)
        self.id_vec = id_vec.lower()
        self.linea = linea
        self.col = col

    def interpretar(self, arbol, tabla):
        # 1. Obtener vector
        vec = None
        if hasattr(arbol, "vectores") and self.id_vec in arbol.vectores:
            vec = arbol.vectores[self.id_vec]
        else:
            try:
                vec = tabla.getVector(self.id_vec)
            except:
                vec = None
        if vec is None:
            return Errores(
                "SEMANTICO",
                f"El vector '{self.id_vec}' no existe.",
                self.linea,
                self.col,
            )
        # 2. Verificar 2D
        if not hasattr(vec, "dimensiones") or len(vec.dimensiones) != 2:
            return Errores(
                "SEMANTICO", "Shuffle requiere vectores 2D.", self.linea, self.col
            )
        filas, columnas = vec.dimensiones
        # 3. Aplanar datos en row-major
        datos = _aplanar(vec.valores)
        if len(datos) != filas * columnas:
            return Errores(
                "SEMANTICO",
                f"Estructura interna inconsistente en '{self.id_vec}'.",
                self.linea,
                self.col,
            )
        # 4. Reordenar a column-major linear
        nuevo_lineal = []
        for c in range(columnas):
            for f in range(filas):
                nuevo_lineal.append(datos[f * columnas + c])
        # 5. Invertir dimensiones para la reconstrucción: [columnas, filas]
        nuevas_dims = [columnas, filas]
        vals_anidado = _reconstruir_anidado(nuevo_lineal, nuevas_dims)
        # 6. Crear nuevo Vector con dimensiones invertidas
        try:
            nuevo_vec = Vector(
                tipo=vec.tipo,
                id=self.id_vec,  # id no importa o podrías usar otro
                dimensiones=nuevas_dims,
                valores=vals_anidado,
                linea=self.linea,
                col=self.col,
                scope=vec.scope,
            )
            return nuevo_vec
        except Exception:
            return vals_anidado

    def graficar(self, grafo, arbol=None, tabla=None):
        nodo = grafo.agregar_nodo("Shuffle")
        nodoId = grafo.agregar_nodo(self.id_vec)
        grafo.agregar_arista(nodo, nodoId)
        return nodo
