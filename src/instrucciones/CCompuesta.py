from src.abstracto.CInstruccion import Instruccion
from src.excepciones.CErrores import Errores


class Compuesta(Instruccion):
    def __init__(self, instrucciones):
        super().__init__(None, 0, 0)
        self.instrucciones = instrucciones

    def interpretar(self, arbol, tabla):
        for instru in self.instrucciones:
            resultado = instru.interpretar(arbol, tabla)
            if resultado is not None and isinstance(resultado, Errores):
                arbol.get_errores().append(resultado)
