from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


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
        return self.valor

    def graficar(self, grafo: clasAST, arbol=None, tabla=None):
        # Si tienes contexto y es identificador, muestra el valor actual
        if (
            arbol is not None
            and tabla is not None
            and getattr(self, "es_identificador", False)
        ):
            valor = self.interpretar(arbol, tabla)
            return grafo.agregar_nodo(str(valor))
        return grafo.agregar_nodo(str(self.valor))
