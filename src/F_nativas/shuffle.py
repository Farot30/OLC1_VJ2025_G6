from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.Vectores.Vector import Vector
import itertools
import functools
import operator


def _product(iterable):
    return functools.reduce(operator.mul, iterable, 1)


def _aplanar(valores):
    if not isinstance(valores, list):
        return [valores]
    out = []
    for x in valores:
        out += _aplanar(x)
    return out


def _reconstruir_anidado(flat, dims):
    if len(dims) == 1:
        return flat[:]
    head, *tail = dims
    size_tail = _product(tail)
    return [
        _reconstruir_anidado(flat[i * size_tail : (i + 1) * size_tail], tail)
        for i in range(head)
    ]


class Shuffle(Instruccion):
    def __init__(self, id_vec, linea, col):
        super().__init__(None, linea, col)
        self.id_vec = id_vec.lower()
        self.linea = linea
        self.col = col

    def interpretar(self, arbol, tabla):
        # 1) Recuperar vector
        vec = getattr(arbol, "vectores", {}).get(self.id_vec) or tabla.getVector(
            self.id_vec
        )
        if vec is None:
            return Errores(
                "SEMANTICO",
                f"El vector '{self.id_vec}' no existe.",
                self.linea,
                self.col,
            )

        # 2) Obtener dimensiones y total de elementos
        dims = getattr(vec, "dimensiones", None)
        if not isinstance(dims, list) or any(
            not isinstance(d, int) or d <= 0 for d in dims
        ):
            return Errores(
                "SEMANTICO",
                "Shuffle requiere vector con dimensiones positivas.",
                self.linea,
                self.col,
            )
        total = _product(dims)

        # 3) Aplanar en row-major
        flat = _aplanar(vec.valores)
        if len(flat) != total:
            return Errores(
                "SEMANTICO",
                f"Estructura inconsistente en '{self.id_vec}'.",
                self.linea,
                self.col,
            )

        # 4) Reordenar a column-major
        new_flat = []
        for idx_rev in itertools.product(*(range(d) for d in reversed(dims))):
            idx = idx_rev[::-1]  # invierte para mapear a row-major
            offset = 0
            for k, i in enumerate(idx):
                mul = _product(dims[k + 1 :]) if k + 1 < len(dims) else 1
                offset += i * mul
            new_flat.append(flat[offset])
        # 5) Invertir dimensiones
        new_dims = list(reversed(dims))
        # 6) Reconstruir estructura anidada
        new_vals = _reconstruir_anidado(new_flat, new_dims)
        # 7) Devolver nuevo Vector
        try:
            return Vector(
                tipo=vec.tipo,
                id=self.id_vec,
                dimensiones=new_dims,
                valores=new_vals,
                linea=self.linea,
                col=self.col,
                scope=vec.scope,
            )
        except Exception:
            return new_vals

    def graficar(self, grafo, arbol=None, tabla=None):
        nodo = grafo.agregar_nodo("Shuffle")
        hijo = grafo.agregar_nodo(self.id_vec)
        grafo.agregar_arista(nodo, hijo)
        return nodo
