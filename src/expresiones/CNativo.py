
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST
from src.abstracto.CInstruccion import Instruccion
from src.simbolo.CTipo import Tipo, tipoDato
from src.simbolo.CArbol import Arbol
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CInstancia import tabla_S as aTab


class Nativo(Instruccion):
    def __init__(self, tipo: Tipo, valor: any, linea: int, col: int):
        super().__init__(tipo, linea, col)
        self.valor = valor
        self.es_identificador = False

    def interpretar(self, arbol: Arbol, tabla):
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
    
    def esDatoNativo(self):
        return True


    def graficar(self, grafo:clasAST):
        return grafo.agregar_nodo(str(self.valor))
