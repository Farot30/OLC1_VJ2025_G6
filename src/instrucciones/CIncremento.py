from src.abstracto.CInstruccion import Instruccion
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.simbolo.CArbol import Arbol
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import clasAST


class Incremento(Instruccion):
    def __init__(self, id, linea, col):
        super().__init__(None, linea, col)
        self.id = id

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        simbolo = None
        for sym in reversed(tabla.getTabla()):
            if sym.entidad == "variable" and sym.id == self.id.lower():
                simbolo = sym
                break
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
        # Siempre actualiza el scope al actual cuando se incrementa
        # simbolo.scope = tabla.current_scope

        simbolo.setValor(valor + 1)
        return None

    def graficar(self, grafo: clasAST):
        nodoInc = grafo.agregar_nodo("Incremento")
        nodoID = grafo.agregar_nodo(f"ID: {self.id}")
        grafo.agregar_arista(nodoInc, nodoID)
        return nodoInc


class Decremento(Instruccion):
    def __init__(self, id, linea, col):
        super().__init__(None, linea, col)
        self.id = id

    def interpretar(self, arbol: Arbol, tabla: tablaSimbolo):
        simbolo = None
        for sym in reversed(tabla.getTabla()):
            if sym.entidad == "variable" and sym.id == self.id.lower():
                simbolo = sym
                break
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
        # Siempre actualiza el scope al actual cuando se decrementa
        # simbolo.scope = tabla.current_scope

        simbolo.setValor(valor - 1)
        return None

    def graficar(self, grafo: clasAST):
        nodoDec = grafo.agregar_nodo("Decremento")
        nodoID = grafo.agregar_nodo(f"ID: {self.id}")
        grafo.agregar_arista(nodoDec, nodoID)
        return nodoDec
