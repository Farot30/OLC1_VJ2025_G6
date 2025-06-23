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

    def interpretar(self, arbol, tabla: tablaSimbolo):
        proc = arbol.getFuncion(self.id)
        if proc is None:
            return Errores("SEMANTICO", f"El procedimiento '{self.id}' no existe", self.linea, self.col)

        # Detectar recursividad directa
        nombre_proc_actual = None
        for scope in reversed(tabla.scopes):
            if scope.startswith("procedimiento_") or scope.startswith("llamada_"):
                if scope.startswith("procedimiento_"):
                    nombre_proc_actual = scope[len("procedimiento_"):]
                else:
                    nombre_proc_actual = scope[len("llamada_"):]
                break

        if nombre_proc_actual is not None and nombre_proc_actual.lower() == self.id.lower():
            return Errores("SEMANTICO", "No se permite la recursividad directa", self.linea, self.col)

        if not isinstance(proc, Procedimientos):
            return Errores("SEMANTICO", f"'{self.id}' no es un procedimiento válido", self.linea, self.col)

        if len(proc.parametros) != len(self.parametros):
            return Errores("SEMANTICO", f"Número incorrecto de parámetros para '{self.id}'", self.linea, self.col)

        nuevo_scope = tabla.nuevoScope(f"procedimiento_{self.id.lower()}")

        for (tipo_def, id_def), valor_ast in zip(proc.parametros, self.parametros):
            valor_interpretado = None
            tipo_val = None

            if hasattr(valor_ast, "interpretar"):
                valor_interpretado = valor_ast.interpretar(arbol, tabla)
                tipo_val = valor_ast.tipoDato.getTipo()
            elif isinstance(valor_ast, str):  # Es ID
                try:
                    simbolo = tabla.getVariable(valor_ast)
                    tipo_val = simbolo.getTipo().getTipo()
                    valor_interpretado = simbolo.getValor()
                except KeyError:
                    tabla.borrarScope()
                    return Errores("SEMANTICO", f"Variable '{valor_ast}' no encontrada", self.linea, self.col)
            else:
                tabla.borrarScope()
                return Errores("SEMANTICO", "Solo se permiten literales o IDs como parámetros", self.linea, self.col)

            if tipo_val != tipo_def.getTipo():
                tabla.borrarScope()
                return Errores("SEMANTICO", f"Tipo de parámetro incorrecto para '{id_def}'", self.linea, self.col)

            simbolo = Simbolo(tipo_def, id_def, "variable", valor_interpretado, tabla.current_scope, self.linea, self.col)
            if not tabla.setVariable(simbolo):
                tabla.borrarScope()
                return Errores("SEMANTICO", f"El parámetro '{id_def}' ya existe en el entorno", self.linea, self.col)

        resultado = proc.interpretar(arbol, tabla)
        tabla.borrarScope()
        if isinstance(resultado, Errores):
            return resultado


    def graficar(self, grafo):
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