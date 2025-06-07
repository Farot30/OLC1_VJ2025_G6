from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo
from src.simbolo.CArbol import Arbol
from src.simbolo.TablaSimbolo import tablaSimbolo


class Nativo(Instruccion):
    def __init__(self, tipo: Tipo, valor: any, linea: int, col: int):
        super().__init__(tipo, linea, col)
        self.valor = valor

    def interpretar(self, arbol, tabla):
        # Si es un identificador, busca el valor en la tabla de símbolos
        if isinstance(self.valor, str) and self.tipoDato.getTipo() is None:
            simbolo = tabla.getVariable(self.valor)
            if simbolo is not None:
                self.tipoDato = simbolo.getTipo()
                return simbolo.getValor()
            else:
                return None
        return self.valor
