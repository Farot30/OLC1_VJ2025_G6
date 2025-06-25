from src.expresiones.CNativo import Nativo
from src.instrucciones.CDeclaracion import Declaracion
from src.instrucciones.CProcedimientos import Procedimientos
from src.simbolo.CSimbolo import Simbolo
from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.simbolo.CTipo import Tipo, tipoDato
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CArbol import Arbol
from src.simbolo.CInstancia import tabla_S as aTab
from src.abstracto.CAST import clasAST

class Llamada(Instruccion):
    def __init__(self, id: str, params:list, linea: int, col: int):
        super().__init__(Tipo(tipoDato.VOID), linea, col)
        self.id = id
        self.parametros = params
        self.enErrores = False

    def interpretar(self, arbol, tabla: tablaSimbolo):
        proc = arbol.getFuncion(self.id)
        if proc is None:
            self.enErrores = True
            return Errores("SEMANTICO", f"El procedimiento '{self.id}' no existe", self.linea, self.col)

        nombre_proc_actual = tabla.getProc()
        if nombre_proc_actual is not None and nombre_proc_actual == self.id:
            self.enErrores = True
            return Errores("SEMANTICO", f"No se permite llamada al procedimiento '{self.id}' desde sí mismo", self.linea, self.col)

        if len(proc.parametros) != len(self.parametros):
            self.enErrores = True
            return Errores("SEMANTICO", f"Número incorrecto de parámetros para '{self.id}'", self.linea, self.col)

        if not isinstance(proc, Procedimientos):
            self.enErrores = True
            return Errores("SEMANTICO", f"'{self.id}' no es un procedimiento válido", self.linea, self.col)

        tabla.nuevoScope(self.id.lower())
        tabla.setProc(self.id)

        for (tipo_def, id_def), valor_ast in zip(proc.parametros, self.parametros):
            valor_interpretado = None
            tipo_val = None

            if hasattr(valor_ast, "interpretar"):
                valor_interpretado = valor_ast.interpretar(arbol, tabla)
                tipo_val = valor_ast.tipoDato.getTipo()
            elif isinstance(valor_ast, str):  # Es ID
                simbolo = tabla.getVariable(valor_ast)
                if simbolo is None:
                    self.enErrores = True
                    tabla.borrarScope()
                    tabla.setProc(None)
                    return Errores("SEMANTICO", f"Variable '{valor_ast}' no encontrada", self.linea, self.col)
                tipo_val = simbolo.getTipo().getTipo()
                valor_interpretado = simbolo.getValor()
            else:
                self.enErrores = True
                tabla.borrarScope()
                tabla.setProc(None)
                return Errores("SEMANTICO", "Solo se permiten literales o IDs como parámetros", self.linea, self.col)

            if tipo_val != tipo_def.getTipo():
                self.enErrores = True
                tabla.borrarScope()
                tabla.setProc(None)
                return Errores("SEMANTICO", f"Tipo de parámetro incorrecto para '{id_def}'", self.linea, self.col)

            simbolo = Simbolo(tipo_def, id_def, "variable", valor_interpretado, tabla.current_scope, self.linea, self.col)
            if not tabla.setVariable(simbolo):
                self.enErrores = True
                tabla.borrarScope()
                tabla.setProc(None)
                return Errores("SEMANTICO", f"El parámetro '{id_def}' ya existe en el entorno llamada", self.linea, self.col)

        resultado = proc.interpretar(arbol, tabla)

        tabla.borrarScope()
        tabla.setProc(None)

        if isinstance(resultado, Errores):
            return resultado



    def graficar(self, grafo):
        if self.enErrores:
            return None
        nodo_llamada = grafo.agregar_nodo("Llamada")

        nodo_id = grafo.agregar_nodo(f"ID: {self.id}")
        grafo.agregar_arista(nodo_llamada, nodo_id)

        nodo_args = grafo.agregar_nodo("Parametros")
        grafo.agregar_arista(nodo_llamada, nodo_args)

        for param in self.parametros:
            if hasattr(param, "graficar"):
                hijo = param.graficar(grafo)
                grafo.agregar_arista(nodo_args, hijo)
            else:
                literal = grafo.agregar_nodo(f"{param}")
                grafo.agregar_arista(nodo_args, literal)

        return nodo_llamada