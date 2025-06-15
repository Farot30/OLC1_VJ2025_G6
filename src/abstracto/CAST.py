from graphviz import Digraph


class clasAST:
    def __init__(self):
        self.graph = Digraph("ReporteAST", format="svg")
        self.counter = 0

    def _get_id(self):
        self.counter += 1
        return f"node{self.counter}"

    def agregar_nodo(self, label, color="purple", style="filled", fillcolor="white"):
        node_id = self._get_id()
        self.graph.node(node_id, label, color=color, style=style, fillcolor=fillcolor)
        return node_id

    def agregar_arista(self, padre_id, hijo_id):
        self.graph.edge(padre_id, hijo_id)

    def renderizar(self, nombre_archivo="reporteAST"):
        self.graph.render(nombre_archivo, view=True)


def generarGrafica(nodo_raiz, nombre_archivo="reporteAST"):
    grafo = clasAST()
    nodo_raiz.graficar(grafo)
    grafo.renderizar(nombre_archivo)
