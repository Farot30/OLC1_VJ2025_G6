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
        # Evitar recursividad directa
        if arbol.getProc() and arbol.getProc().lower() == self.id.lower():
            self.enErrores = True
            return Errores("SEMANTICO", f"No se permite recursividad directa en procedimiento '{self.id}'", self.linea, self.col)

        funcion = arbol.getFuncion(self.id)
        if funcion is None:
            self.enErrores = True
            return Errores("SEMANTICO", f"Procedimiento '{self.id}' no existe", self.linea, self.col)

        tabla.nuevoScope("llamada")
        tabla.setNombre("LLAMADA")
        arbol.setProc(self.id)
        
        try:
            # Declarar y asignar parámetros
            for i, parametro_formal in enumerate(funcion.parametros):
                parametro_real = self.parametros[i]

                if not parametro_real.esDatoNativo():
                    self.enErrores = True
                    return Errores("SEMANTICO", "Parámetros deben ser ID, INT, CHAR, etc., no expresiones", self.linea, self.col)

                valor = parametro_real.interpretar(arbol, tabla)
                if isinstance(valor, Errores):
                    return valor

                if parametro_formal[0].getTipo() != parametro_real.tipoDato.tipo:
                    self.enErrores = True
                    return Errores("SEMANTICO", f"Tipo incorrecto para parámetro '{parametro_formal[1]}'", self.linea, self.col)

                tabla.agregarVariable(parametro_formal[1], parametro_formal[0], valor, self.linea, self.col)

            resultado = funcion.interpretar(arbol, tabla)
            if isinstance(resultado, Errores):
                return resultado
            return resultado
        finally:
            # Siempre limpiar el procedimiento actual y entorno
            arbol.setProc(None)
            tabla.borrarScope()
    
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