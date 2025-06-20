from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST
from src.simbolo.CTipo import tipoDato


class Nativo(Instruccion):
    def __init__(self, tipo: Tipo, valor: any, linea: int, col: int):
        super().__init__(tipo, linea, col)
        self.valor = valor
        self.es_identificador = False  # Por defecto, no es identificador

    def __str__(self):
        return str(self.valor)

    def interpretar(self, arbol, tabla):
        # Si es un identificador, busca el valor en la tabla de símbolos SIEMPRE
        if getattr(self, "es_identificador", False):
            if hasattr(arbol, "vectores") and self.valor in arbol.vectores:
                # Si es un vector, devuelve el vector completo
                return arbol.vectores[self.valor]

            try:
                simbolo = tabla.getVariable(self.valor)
                self.tipoDato = simbolo.getTipo()
                return simbolo.getValor()
            except KeyError as e:
                return Errores(
                    "SEMANTICO",
                    str(e),
                    self.linea,
                    self.col,
                )
        # --- CORRECCIÓN: Forzar booleano si el tipo es BOOL ---
        if hasattr(self, "tipo") and hasattr(self.tipoDato, "tipo"):

            if self.tipoDato.tipo == tipoDato.BOOL:
                if self.valor is True or self.valor is False:
                    return self.valor
                if str(self.valor).lower() == "true":
                    return True
                if str(self.valor).lower() == "false":
                    return False
                if self.valor == 1:
                    return True
                if self.valor == 0:
                    return False
        return self.valor

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        return grafo.agregar_nodo(str(self.valor))
