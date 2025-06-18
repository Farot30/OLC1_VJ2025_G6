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
        if padre_id is None or hijo_id is None:
            return  # Evitar error si algún nodo es None
        self.graph.edge(str(padre_id), str(hijo_id))

    def renderizar(self, nombre_archivo="reporteAST"):
        try:
            self.graph.render(nombre_archivo, view=True)
            print(
                f"AST generado correctamente en {nombre_archivo}.dot y {nombre_archivo}.svg"
            )
        except Exception as e:
            print(f"Error al generar AST: {e}")


def generarGrafica(arbol, nombre_archivo="report/ast_reporte"):
    try:
        grafo = clasAST()

        # 1) Nodo raíz
        nodo_reporte = grafo.agregar_nodo(
            "Reporte", color="black", fillcolor="lightgray"
        )

        # 2) Recoger líneas con errores
        lineas_err = {err.get_linea() for err in arbol.get_errores()}

        # 3) Iterar instrucciones de nivel superior
        for instr in arbol.getInstrucciones():
            if instr is None:
                continue
            # Si la línea de esta instrucción está en errores, la saltamos
            if instr.linea in lineas_err:
                continue
            # Graficar la instrucción y conectar con la raíz
            nodo_instr = instr.graficar(grafo, arbol, arbol.get_tabla_global())
            if nodo_instr is not None:
                grafo.agregar_arista(nodo_reporte, nodo_instr)

        # 4) Renderizar el SVG
        grafo.renderizar(nombre_archivo)
    except Exception as e:
        print(f"Error al generar el AST: {e}")
