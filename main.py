from src.gramatica import parse_input, errores_sintacticos_globales
from src.simbolo.CArbol import Arbol
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import generarGrafica


def main():
    try:
        f = open("pruebaVector.txt", "r", encoding="utf-8")
        entrada = f.read()
        tablaSimbolo().setTabla([])
        ast = Arbol([])  # Crea el árbol antes de parsear
        instrucciones = parse_input(entrada, ast)
        # Filtra instrucciones válidas
        instrucciones = [instr for instr in instrucciones if instr is not None]
        ast.set_instrucciones(instrucciones)

        if not instrucciones:
            print("No hay instrucciones válidas para ejecutar.")
            return

        tabla = tablaSimbolo()
        ast.setTablaGlobal(tabla)
        ast.setConsola("")

        # Agrega errores sintácticos globales al árbol antes de imprimir
        if errores_sintacticos_globales:
            ast.errores.extend(errores_sintacticos_globales)
            errores_sintacticos_globales.clear()

        # Imprime errores ANTES de ejecutar instrucciones
        # if ast.errores:
        #    print("Errores encontrados durante el análisis sintáctico:")
        #    for idx, error in enumerate(ast.errores, 1):
        #        print(
        #           f"{idx}\t{error.get_tipo_error()}\t{error.get_desc()}\t{error.get_linea()}\t{error.get_col()}"
        #        )

        for instr in ast.getInstrucciones():
            if instr is None:
                continue
            resultado = instr.interpretar(ast, tabla)
            # Solo agrega el error si no está ya en ast.errores
            if isinstance(resultado, Errores) and resultado not in ast.errores:
                ast.errores.append(resultado)
            # No imprimas aquí, solo imprime al final

        print(ast.getConsola())

        # Generar el AST y el archivo .dot/.svg
        try:
            if ast is not None and ast.getInstrucciones():
                generarGrafica(ast, "reporteAST")
                print("AST generado correctamente en reporteAST.dot y reporteAST.svg")
        except Exception as e:
            print(f"Error al generar el AST: {e}")

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
