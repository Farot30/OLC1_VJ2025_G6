from src.simbolo.CSimbolo import Simbolo
from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.simbolo.CTipo import Tipo, tipoDato
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CInstancia import tabla_S as aTab
from src.abstracto.CAST import clasAST

class Procedimientos(Instruccion):
    def __init__(self, id_: str, parametros:list, inst: list, linea: int, col: int):
        super().__init__(Tipo(tipoDato.VOID), linea, col)
        self.id = id_
        self.parametros = parametros
        self.inst = inst

    def interpretar(self, arbol, tabla: tablaSimbolo):
        tabla.nuevoScope("Procedimiento")
        for instr in self.inst:
            resultado = instr.interpretar(arbol, tabla)
            if isinstance(resultado, Errores):
                arbol.errores.append(resultado)
        tabla.borrarScope()

        """if arbol.getFuncion(self.id):
            return Errores("Semantico", f"El procedimiento '{self.id}' ya ha sido declarado", self.linea, self.col)

        arbol.setFuncion(self)
        scope_name = tabla.nuevoScope("Procedimiento")

        for tipo, ident in self.parametros:
            simbolo = Simbolo(
                tipo, 
                ident, 
                "variable", 
                None, 
                scope_name, 
                self.linea, self.col)
            if not tabla.setVariable(simbolo):
                return Errores("Semantico", f"El parámetro '{ident}' ya existe en el entorno", self.linea, self.col)

        for instr in self.inst:
            res = instr.interpretar(arbol, tabla)
            if isinstance(res, Errores):
                arbol.errores.append(res)

        tabla.borrarScope()
        return None"""

    
    def graficar(self, grafo):
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
        for instruccion in self.inst:
            if hasattr(instruccion, "graficar"):
                hijo = instruccion.graficar(grafo)
                grafo.agregar_arista(nodo_instrucciones, hijo)

        return nodo_procedimiento
