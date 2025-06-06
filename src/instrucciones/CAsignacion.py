from src.abstracto.CInstruccion import Instruccion
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CArbol import Arbol
from src.excepciones.CErrores import Errores


class Asignacion(Instruccion):
    def __init__(self, id, valor, linea, col):
        super().__init__(None, linea, col)
        self.id = id
        self.valor = valor

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        simbolo = tabla.getVariable(self.id)
        if simbolo is None:
            return Errores(
                "SEMANTICO", f"Variable '{self.id}' no declarada", self.linea, self.col
            )
        val = self.valor.interpretar(arbol, tabla)
        if isinstance(val, Errores):
            return val
        simbolo.setValor(val)
        tipo = simbolo.getTipo().tipo.name if simbolo.getTipo() else "desconocido"
        arbol.setConsola(
            arbol.getConsola()
            + f"Asignación: variable '{self.id}' (tipo {tipo}) = {val}\n"
        )
        return None
