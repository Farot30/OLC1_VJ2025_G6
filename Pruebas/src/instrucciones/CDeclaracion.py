from src.simbolo.CSimbolo import Simbolo
from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.simbolo.CTipo import Tipo, tipoDato
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CArbol import Arbol
from src.abstracto.CAST import clasAST

class Declaracion(Instruccion):
    def __init__(
        self,
        tipo: Tipo,
        linea: int,
        col: int,
        identificador: str,
        valor: Instruccion = None,
    ):
        super().__init__(tipo, linea, col)
        self.identificador = identificador
        self.valor = valor

    def _obtener_valor_por_defecto(self, tipo):
        """Devuelve el valor por defecto según el tipo de dato"""
        tipo_enum = tipo.getTipo()

        if tipo_enum == tipoDato.ENTERO:
            return 0
        elif tipo_enum == tipoDato.DECIMAL:
            return 0.0
        elif tipo_enum == tipoDato.BOOL:
            return False
        elif tipo_enum == tipoDato.STRING:
            return ""
        elif tipo_enum == tipoDato.CHAR:
            return ""
        else:
            return None  # Para tipos no especificados o personalizados

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        scope_actual = tabla.current_scope  # obtiene el scope actual (entorno)

        # Procesar el valor a asignar
        if self.valor:
            res_valor = self.valor.interpretar(arbol, tabla)
            if isinstance(res_valor, Errores):
                return res_valor

            # Validar compatibilidad de tipo
            if not self._es_tipo_compatible(res_valor):
                return Errores(
                    "SEMANTICO",
                    f"El valor asignado no es compatible con el tipo {self.tipoDato.getTipo().name}",
                    self.linea,
                    self.col
                )
        else:
            # Usar valor por defecto
            res_valor = self._obtener_valor_por_defecto(self.tipoDato)

        # Crear símbolo para la nueva variable
        sim = Simbolo(
            tipo=self.tipoDato,
            id=self.identificador,
            entidad="variable",
            valor=res_valor,
            scope=scope_actual,
            linea=self.linea,
            columna=self.col,
        )

        # Intentar agregar la variable a la tabla
        if not tabla.setVariable(sim):
            try:
                # La variable existe, actualizarla en lugar de mostrar error
                tabla.actualizarVariable(
                    name=self.identificador,
                    nevValor=res_valor,
                    nevTipo=self.tipoDato,
                    linea=self.linea,
                    columna=self.col,
                    scope=scope_actual,
                )
            except KeyError:
                return Errores(
                    "SEMANTICO",
                    f"Error al redeclarar la variable '{self.identificador}'",
                    self.linea,
                    self.col,
                )

        return None

    def _es_tipo_compatible(self, valor):
        tipo = self.tipoDato.getTipo()
        if tipo == tipoDato.ENTERO:
            return isinstance(valor, int)
        elif tipo == tipoDato.DECIMAL:
            return isinstance(valor, (int, float))
        elif tipo == tipoDato.STRING:
            return isinstance(valor, str)
        elif tipo == tipoDato.BOOL:
            return isinstance(valor, bool)
        elif tipo == tipoDato.CHAR:
            return isinstance(valor, str) and len(valor) == 1
        return False

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        nodoDeclaracion = grafo.agregar_nodo("Declaración")

        # identificador
        nodoID = grafo.agregar_nodo(f"ID: {self.identificador}")
        grafo.agregar_arista(nodoDeclaracion, nodoID)

        # tipo
        nodoTipo = grafo.agregar_nodo(f"Tipo: {self.tipoDato.getTipo().name}")
        grafo.agregar_arista(nodoDeclaracion, nodoTipo)

        # valor si fuera declaracion de variable con valor
        if self.valor is not None:
            nodoValor = grafo.agregar_nodo("Valor")
            grafo.agregar_arista(nodoDeclaracion, nodoValor)
            hijValor = self.valor.graficar(grafo, arbol, tabla)
            grafo.agregar_arista(nodoValor, hijValor)

        return nodoDeclaracion