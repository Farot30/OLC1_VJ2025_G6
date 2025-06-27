from src.simbolo.CSimbolo import Simbolo
from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.simbolo.CTipo import Tipo, tipoDato
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CInstancia import tabla_S as aTab
from src.abstracto.CAST import clasAST


class Procedimientos(Instruccion):
    def __init__(
        self, id_: str, parametros: list, instrucciones: list, linea: int, col: int
    ):
        super().__init__(Tipo(tipoDato.VOID), linea, col)
        self.id = id_
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.enErrores = False

    def interpretar(self, arbol, tabla: tablaSimbolo):
        arbol.setFuncion(self)
        tabla.nuevoScope("procedimiento")
        tabla.setNombre(f"PROC_{self.id}")

        for instruccion in self.instrucciones:
            resultado = instruccion.interpretar(arbol, tabla)
            if isinstance(resultado, Errores):
                self.enErrores = True
                arbol.get_errores().append(resultado)

        tabla.borrarScope()

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        if self.enErrores:
            return None

        nodo_procedimiento = grafo.agregar_nodo("Procedimiento")

        nodo_id = grafo.agregar_nodo(f"ID: {self.id}")
        grafo.agregar_arista(nodo_procedimiento, nodo_id)

        nodo_parametros = grafo.agregar_nodo("Parámetros")
        grafo.agregar_arista(nodo_procedimiento, nodo_parametros)
        for tipo_param, id_param in self.parametros:
            nodo_param = grafo.agregar_nodo(f"{tipo_param.getTipo().name} : {id_param}")
            grafo.agregar_arista(nodo_parametros, nodo_param)

        nodo_instrucciones = grafo.agregar_nodo("Instrucciones")
        grafo.agregar_arista(nodo_procedimiento, nodo_instrucciones)
        for instruccion in self.instrucciones:
            if hasattr(instruccion, "graficar"):
                hijo = instruccion.graficar(grafo)
                grafo.agregar_arista(nodo_instrucciones, hijo)

        return nodo_procedimiento
