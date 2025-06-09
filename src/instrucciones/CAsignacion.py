from src.abstracto.CInstruccion import Instruccion
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CArbol import Arbol
from src.excepciones.CErrores import Errores
from src.simbolo.CTipo import tipoDato


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

        tipo_var = simbolo.getTipo().tipo
        tipo_val = (
            self.valor.tipoDato.getTipo() if hasattr(self.valor, "tipoDato") else None
        )

        # para enteros
        # Si la variable es ENTERO y el valor es DECIMAL, actualiza el tipo de la variable a DECIMAL
        if tipo_var == tipoDato.ENTERO and tipo_val == tipoDato.DECIMAL:
            val = float(val)
            tipo_val = tipoDato.DECIMAL
            simbolo.getTipo().setTipo(tipoDato.DECIMAL)
            tipo_var = tipoDato.DECIMAL  # Se actualiza la variable

        # sumas de decimales
        if tipo_var == tipoDato.DECIMAL and tipo_val == tipoDato.ENTERO:
            val = float(val)
            tipo_val = tipoDato.DECIMAL

        # Suma de caracteres
        if tipo_var == tipoDato.CHAR and tipo_val != tipoDato.CHAR:
            val = str(val)
            tipo_val = tipoDato.CHAR
        if tipo_var == tipoDato.CHAR and tipo_val == tipoDato.STRING:
            val = str(val)
            tipo_val = tipoDato.STRING
        if tipo_var == tipoDato.CHAR and tipo_val == tipoDato.ENTERO:
            val = chr(int(val))
            tipo_val = tipoDato.CHAR
        if tipo_var == tipoDato.CHAR and tipo_val == tipoDato.DECIMAL:
            val = chr(int(val))
            tipo_val = tipoDato.CHAR

        # Suma de cadenas
        if tipo_var == tipoDato.STRING and tipo_val != tipoDato.STRING:
            val = str(val)
            tipo_val = tipoDato.STRING

        if tipo_var != tipo_val:
            return Errores(
                "SEMANTICO",
                f"No se puede asignar un valor de tipo {tipo_val.name if tipo_val else 'desconocido'} a la variable '{self.id}' de tipo {tipo_var.name}",
                self.linea,
                self.col,
            )
        if tipo_var == tipoDato.ENTERO:
            val = int(val)

        simbolo.setValor(val)
        # tipo = simbolo.getTipo().tipo.name if simbolo.getTipo() else "desconocido"
        # arbol.setConsola(
        #    arbol.getConsola()
        #    + f"Asignación: variable '{self.id}' (tipo {tipo}) = {val}\n"
        # )
        return None
