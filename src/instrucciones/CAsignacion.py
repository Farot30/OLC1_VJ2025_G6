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

        # --- Validación de tipo ---
        tipo_var = simbolo.getTipo().tipo
        tipo_val = (
            self.valor.tipoDato.getTipo() if hasattr(self.valor, "tipoDato") else None
        )
        if tipo_var != tipo_val:
            return Errores(
                "SEMANTICO",
                f"No se puede asignar un valor de tipo {tipo_val.name if tipo_val else 'desconocido'} a la variable '{self.id}' de tipo {tipo_var.name}",
                self.linea,
                self.col,
            )
        # --------------------------

        simbolo.setValor(val)
        tipo = simbolo.getTipo().tipo.name if simbolo.getTipo() else "desconocido"
        arbol.setConsola(
            arbol.getConsola()
            + f"Asignación: variable '{self.id}' (tipo {tipo}) = {val}\n"
        )
        return None
