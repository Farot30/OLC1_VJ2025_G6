from src.simbolo.CSimbolo import Simbolo
from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores
from src.simbolo.CTipo import Tipo
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CArbol import Arbol


class Declaracion(Instruccion):
    def __init__(self, tipo: Tipo, linea: int, col: int, identificador: str, valor: Instruccion = None):
        super().__init__(tipo, linea, col)
        self.identificador = identificador
        self.valor = valor

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        # caso: <TIPO> <ID> = <EXPRESIÓN>;
        if self.valor:
            res_valor = self.valor.interpretar(arbol, tabla)
            if isinstance(res_valor, Errores):
                return res_valor

            # TIPOS IGUALES
            if self.valor.tipoDato.getTipo() != self.tipoDato.getTipo():
                return Errores("SEMANTICO", "El tipo y el valor de la variable no coinciden", self.linea, self.col)

            if not tabla.setVariable(Simbolo(self.tipoDato, self.identificador, res_valor)):
                return Errores("SEMANTICO", "No se puede declarar la variable", self.linea, self.col)
            
            arbol.setConsola(arbol.getConsola() + f"Declaración '{self.identificador}' = {res_valor}\n")

        #caso <TIPO> <ID>; 
        else:
            if not tabla.setVariable(Simbolo(self.tipoDato, self.identificador, None)):
                return Errores("SEMANTICO", f"No se puede declarar la variable '{self.identificador}'", self.linea, self.col)

            arbol.setConsola(arbol.getConsola() + f"Declaración '{self.identificador}'  sin valor\n")

        return None
