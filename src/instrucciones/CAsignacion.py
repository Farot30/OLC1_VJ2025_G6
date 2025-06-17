from src.abstracto.CInstruccion import Instruccion
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CArbol import Arbol
from src.excepciones.CErrores import Errores
from src.simbolo.CTipo import tipoDato
from src.abstracto.CAST import clasAST


class Asignacion(Instruccion):
    def __init__(self, id, valor, linea, col):
        super().__init__(None, linea, col)
        self.id = id
        self.valor = valor

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        # Busca la variable usando el método getVariable, captura el error si no existe
        try:
            simbolo = tabla.getVariable(self.id)
        except KeyError as e:
            # Retorna un objeto Errores para que el error se agregue a la tabla de errores
            return Errores(
                "SEMANTICO",
                str(e),
                self.linea,
                self.col,
            )
        val = self.valor.interpretar(arbol, tabla)
        if isinstance(val, Errores):
            return val

        tipo_var = simbolo.getTipo().tipo
        tipo_val = None
        if hasattr(self.valor, "tipoDato") and hasattr(self.valor.tipoDato, "getTipo"):
            tipo_val = self.valor.tipoDato.getTipo()

        # para enteros
        if tipo_var == tipoDato.ENTERO and tipo_val == tipoDato.DECIMAL:
            val = float(val)
            tipo_val = tipoDato.DECIMAL
            simbolo.getTipo().setTipo(tipoDato.DECIMAL)
            tipo_var = tipoDato.DECIMAL

        if tipo_var == tipoDato.DECIMAL and tipo_val == tipoDato.ENTERO:
            val = float(val)
            tipo_val = tipoDato.DECIMAL

        if tipo_var == tipoDato.CHAR and tipo_val != tipoDato.CHAR:
            val = str(val)
            tipo_val = tipoDato.CHAR
        if tipo_var == tipoDato.CHAR and tipo_val == tipoDato.STRING:
            val = str(val)
            tipo_val = tipoDato.STRING
        if tipo_var == tipoDato.CHAR and tipo_val == tipoDato.ENTERO:
            val = chr(int(val))
            tipo_val = tipoDato.CHAR
        if tipo_var == tipoDato.CHAR and tipo_val == tipoDato.DECIMAL:
            val = chr(int(val))
            tipo_val = tipoDato.CHAR

        if tipo_var == tipoDato.STRING and tipo_val != tipoDato.STRING:
            val = str(val)
            tipo_val = tipoDato.STRING

        if tipo_val is not None and tipo_var != tipo_val:
            return Errores(
                "SEMANTICO",
                f"No se puede asignar un valor de tipo {tipo_val.name if tipo_val else 'desconocido'} a la variable '{self.id}' de tipo {tipo_var.name}",
                self.linea,
                self.col,
            )
        if tipo_var == tipoDato.ENTERO:
            val = int(val)

        # Siempre actualiza el scope al actual cuando se asigna un nuevo valor
        # simbolo.scope = tabla.current_scope

        simbolo.setValor(val)
        return None

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        asignacion = grafo.agregar_nodo("Asignación")
        nodoID = grafo.agregar_nodo(f"{self.id}")
        nodoval = self.valor.graficar(grafo, arbol, tabla)

        grafo.agregar_arista(asignacion, nodoID)
        if nodoval is not None:  # <-- Solo agrega si el nodo existe
            grafo.agregar_arista(asignacion, nodoval)

        return asignacion
