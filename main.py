from src.gramatica import parse_input
from src.simbolo.CArbol import Arbol
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.excepciones.CErrores import Errores
from src.simbolo.CInstancia import tabla_S as aTab

from src.gramatica import parse_input, errores_sintacticos_globales


def main():
    try:
        f = open("pp.txt", "r")
        entrada = f.read()

        ast = Arbol([])  # Crea el árbol antes de parsear
        instrucciones = parse_input(entrada, ast)  # Pasa el árbol aquí
        ast.set_instrucciones(instrucciones)
        
        tabla = aTab
        ast.setTablaGlobal(tabla)
        ast.setConsola("")

        # Agrega errores sintácticos globales al árbol antes de imprimir
        if errores_sintacticos_globales:
            ast.errores.extend(errores_sintacticos_globales)
            errores_sintacticos_globales.clear()

        # Imprime errores ANTES de ejecutar instrucciones
        if ast.errores:
            print("Errores encontrados durante el análisis sintáctico:")
            for idx, error in enumerate(ast.errores, 1):
                print(
                    f"{idx}\t{error.get_tipo_error()}\t{error.get_desc()}\t{error.get_linea()}\t{error.get_col()}"
                )

        for instr in ast.getInstrucciones():
            resultado = instr.interpretar(ast, tabla)
            if isinstance(resultado, Errores):
                print(resultado)
                ast.errores.append(resultado)
            elif resultado is not None:
                print("Prueba:", resultado)

        print(ast.getConsola())
        return ast
        """
        entrada = ''' 1-2;'''
        instrucciones = parse_input(entrada)
        
        ast = Arbol(instrucciones)
        tabla = tablaSimbolo()
        ast.setTablaGlobal(tabla)
        ast.setConsola("")

        for instr in ast.getInstrucciones():
            resultado = instr.interpretar(ast, tabla)
            if isinstance(resultado, Errores):
                print(resultado)
            else:
                print("Prueba:", resultado)
        
        # Imprimir consola 
        print(ast.getConsola())"""

    except Exception as e:
        print(f"Error durante la ejecución: {e}")



def imprimir_tabla_simbolos(tabla: tablaSimbolo):
    print("#\tID\tTIPO\t\tTIPO2\tENTORNO\tVALOR\tLINEA\tCOLUMNA")
    for idx, simbolo in enumerate(tabla.getTabla(), 1):
        id_ = simbolo.getId()
        tipo1 = "Variable"  # Si solo manejas variables, si tienes funciones/campos, cámbialo
        tipo2 = simbolo.getTipo().tipo.name if simbolo.getTipo() else "desconocido"
        entorno = tabla.getNombre() if tabla.getNombre() else "Global"
        valor = simbolo.getValor()
        linea = simbolo.getLinea() if hasattr(simbolo, "getLinea") else "-"
        columna = simbolo.getColumna() if hasattr(simbolo, "getColumna") else "-"
        print(f"{idx}\t{id_}\t{tipo1}\t{tipo2}\t{entorno}\t{valor}\t{linea}\t{columna}")


def imprimir_tabla_errores(errores):
    print("#\tTipo\t\tDescripcion\t\t\tLINEA\tCOLUMNA")
    for idx, error in enumerate(errores, 1):
        print(
            f"{idx}\t{error.get_tipo_error()}\t{error.get_desc()}\t{error.get_linea()}\t{error.get_col()}"
        )


if __name__ == "__main__":
    ast = main()
    if ast is not None:
        imprimir_tabla_simbolos(ast.get_tabla_global())
        imprimir_tabla_errores(ast.get_errores())