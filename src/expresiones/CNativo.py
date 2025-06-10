from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo
from src.excepciones.CErrores import Errores


class Nativo(Instruccion):
    def __init__(self, tipo: Tipo, valor: any, linea: int, col: int):
        super().__init__(tipo, linea, col)
        self.valor = valor
        self.es_identificador = False  # Por defecto, no es identificador

    def interpretar(self, arbol, tabla):
        # Si es un identificador, busca el valor en la tabla de símbolos SIEMPRE
        if getattr(self, "es_identificador", False):
            simbolo = tabla.getVariable(self.valor)
            if simbolo is not None:
                self.tipoDato = simbolo.getTipo()
                return simbolo.getValor()
            else:
                return Errores(
                    "SEMANTICO",
                    f"Variable '{self.valor}' no definida",
                    self.linea,
                    self.col,
                )
        return self.valor
