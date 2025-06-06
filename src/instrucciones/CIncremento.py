from src.abstracto.CInstruccion import Instruccion
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CArbol import Arbol
from src.excepciones.CErrores import Errores


class Incremento(Instruccion):
    def __init__(self, id, linea, col):
        super().__init__(None, linea, col)
        self.id = id

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        simbolo = tabla.getVariable(self.id)
        if simbolo is None:
            return Errores(
                "SEMANTICO", f"Variable '{self.id}' no declarada", self.linea, self.col
            )
        valor = simbolo.getValor()
        if not isinstance(valor, (int, float)):
            return Errores(
                "SEMANTICO",
                f"No se puede incrementar un valor no numérico",
                self.linea,
                self.col,
            )
        simbolo.setValor(valor + 1)
        tipo = simbolo.getTipo().tipo.name if simbolo.getTipo() else "desconocido"
        arbol.setConsola(
            arbol.getConsola()
            + f"Incremento: variable '{self.id}' (tipo {tipo}) ahora vale {valor + 1}\n"
        )
        return None


class Decremento(Instruccion):
    def __init__(self, id, linea, col):
        super().__init__(None, linea, col)
        self.id = id

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        simbolo = tabla.getVariable(self.id)
        if simbolo is None:
            return Errores(
                "SEMANTICO", f"Variable '{self.id}' no declarada", self.linea, self.col
            )
        valor = simbolo.getValor()
        if not isinstance(valor, (int, float)):
            return Errores(
                "SEMANTICO",
                f"No se puede decrementar un valor no numérico",
                self.linea,
                self.col,
            )
        simbolo.setValor(valor - 1)
        tipo = simbolo.getTipo().tipo.name if simbolo.getTipo() else "desconocido"
        arbol.setConsola(
            arbol.getConsola()
            + f"Decremento: variable '{self.id}' (tipo {tipo}) ahora vale {valor - 1}\n"
        )
        return None
