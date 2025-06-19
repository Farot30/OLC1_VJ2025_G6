from src.simbolo.CSimbolo import Simbolo
from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.simbolo.CTipo import Tipo, tipoDato
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CArbol import Arbol
from src.abstracto.CAST import clasAST


class Declaracion(Instruccion):
    def __init__(self, tipo, identificador, valor, linea, col):
        super().__init__(tipo, linea, col)
        self.tipoDato = tipo
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

            # MODIFICADO: Actualizar la variable si ya existe
            try:
                var_existente = tabla.getVariable(self.identificador)
                var_existente.valor = res_valor
                var_existente.tipo = self.tipoDato
                var_existente.linea = self.linea
                var_existente.columna = self.col
            except:
                # La variable no existe, crearla normalmente
                tabla.setVariable(sim)

        # caso <TIPO> <ID>; (Con valores por defecto)
        else:
            # Asignar valor por defecto según el tipo
            valor_default = self._obtener_valor_default(self.tipoDato.getTipo())

            sim = Simbolo(
                tipo=self.tipoDato,
                id=self.identificador,
                entidad="variable",
                valor=valor_default,
                scope=scope_actual,
                linea=self.linea,
                columna=self.col,
            )

            # MODIFICADO: Actualizar la variable si ya existe
            try:
                var_existente = tabla.getVariable(self.identificador)
                var_existente.valor = valor_default
                var_existente.tipo = self.tipoDato
                var_existente.linea = self.linea
                var_existente.columna = self.col
            except:
                # La variable no existe, crearla normalmente
                tabla.setVariable(sim)

        return None

    def _obtener_valor_default(self, tipo):
        """Devuelve el valor por defecto según el tipo de dato"""
        if tipo == tipoDato.ENTERO:
            return 0
        elif tipo == tipoDato.DECIMAL:
            return 0.0
        elif tipo == tipoDato.BOOL:
            return False
        elif tipo == tipoDato.STRING:
            return ""
        elif tipo == tipoDato.CHAR:
            return "\0"  # Carácter nulo
        elif tipo == tipoDato.VOID:
            return None
        else:
            return None

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        # Nodo principal de la declaración
        nodoDeclaracion = grafo.agregar_nodo("Declaración")

        # Nodo para el tipo
        tipo_str = (
            self.tipoDato.tipo.name
            if hasattr(self.tipoDato, "tipo")
            else str(self.tipoDato)
        )
        nodoTipo = grafo.agregar_nodo(f"Tipo: {tipo_str}")
        grafo.agregar_arista(nodoDeclaracion, nodoTipo)

        # Nodo para el identificador
        nodoId = grafo.agregar_nodo(f"ID: {self.identificador}")
        grafo.agregar_arista(nodoDeclaracion, nodoId)

        # Si hay un valor, graficarlo
        if self.valor:
            nodoValor = self.valor.graficar(grafo, arbol, tabla)
            if nodoValor is not None:
                grafo.agregar_arista(nodoDeclaracion, nodoValor)

        return nodoDeclaracion
