from src.gramatica import parse_input, errores_sintacticos_globales
from src.simbolo.CArbol import Arbol
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.excepciones.CErrores import Errores


def main():
    try:
        f = open("entrada.txt", "r")
        entrada = f.read()

        ast = Arbol([])  # Crea el árbol antes de parsear
        instrucciones = parse_input(entrada, ast)  # Pasa el árbol aquí
        ast.set_instrucciones(instrucciones)

        tabla = tablaSimbolo()
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

    except Exception as e:
        print(f"Error durante la ejecución: {e}")


def imprimir_tabla_errores(errores):
    print("#\tTipo\t\tDescripcion\t\t\tLINEA\tCOLUMNA")
    for idx, error in enumerate(errores, 1):
        print(
            f"{idx}\t{error.get_tipo_error()}\t{error.get_desc()}\t{error.get_linea()}\t{error.get_col()}"
        )


if __name__ == "__main__":
    ast = main()
    if ast is not None:
        ast.get_tabla_global().ImprimirTabla()  # Usa el método de la clase
        imprimir_tabla_errores(ast.get_errores())
