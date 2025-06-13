from src.simbolo.CSimbolo import Simbolo
from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.simbolo.CTipo import Tipo
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

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        scope_actual = tabla.current_scope  # obtiene el scope actual (entorno)
        # caso: <TIPO> <ID> = <EXPRESIÓN>;
        if self.valor:
            res_valor = self.valor.interpretar(arbol, tabla)
            if isinstance(res_valor, Errores):
                return res_valor

            # Validar tipo solo si self.valor tiene tipoDato y getTipo
            tipo_valor = None
            if hasattr(self.valor, "tipoDato") and hasattr(
                self.valor.tipoDato, "getTipo"
            ):
                tipo_valor = self.valor.tipoDato.getTipo()
            if tipo_valor != self.tipoDato.getTipo():
                return Errores(
                    "SEMANTICO",
                    "El tipo y el valor de la variable no coinciden",
                    self.linea,
                    self.col,
                )

            # entidad="variable"
            sim = Simbolo(
                tipo=self.tipoDato,
                id=self.identificador,
                entidad="variable",
                valor=res_valor,
                scope=scope_actual,
                linea=self.linea,
                columna=self.col,
            )
            if not tabla.setVariable(sim):
                return Errores(
                    "SEMANTICO",
                    f"La variable '{self.identificador}' ya existe",
                    self.linea,
                    self.col,
                )
            # arbol.setConsola(
            #    arbol.getConsola()
            #    + f"Declaración '{self.identificador}' = {res_valor}\n"
            # )

        # caso <TIPO> <ID>;
        else:
            sim = Simbolo(
                tipo=self.tipoDato,
                id=self.identificador,
                entidad="variable",
                valor=None,
                scope=scope_actual,
                linea=self.linea,
                columna=self.col,
            )
            if not tabla.setVariable(sim):
                return Errores(
                    "SEMANTICO",
                    f"La variable '{self.identificador}' ya existe",
                    self.linea,
                    self.col,
                )
            # arbol.setConsola(
            #    arbol.getConsola() + f"Declaración '{self.identificador}'  sin valor\n"
            # )

        return None

    def graficar(self, grafo: clasAST):
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
            hijValor = self.valor.graficar(grafo)
            grafo.agregar_arista(nodoValor, hijValor)

        return nodoDeclaracion
