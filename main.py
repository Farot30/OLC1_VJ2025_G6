from src.gramatica import parse_input, errores_sintacticos_globales
from src.simbolo.CArbol import Arbol
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import generarGrafica
from src.Vectores.ReporteVector import ReporteVectores
from src.instrucciones.CProcedimientos import Procedimientos
from src.simbolo.CInstancia import tabla_S as aTab
import sys


def main(archivo="entrada.txt", usar_singleton=False):
    try:
        # Abrir el archivo especificado
        f = open(archivo, "r", encoding="utf-8")
        entrada = f.read()

        # Inicializar tabla de símbolos
        if usar_singleton:
            tabla = aTab
            tabla.limpiar()
        else:
            tablaSimbolo().setTabla([])
            tabla = tablaSimbolo()

        # Parsear entrada
        ast = Arbol([])
        instrucciones = parse_input(entrada, ast)
        instrucciones = [instr for instr in instrucciones if instr is not None]
        ast.set_instrucciones(instrucciones)

        if not instrucciones:
            print("No hay instrucciones válidas para ejecutar.")
            return None

        # Configurar árbol
        ast.setTablaGlobal(tabla)
        ast.setConsola("")

        # Procesar errores sintácticos
        if errores_sintacticos_globales:
            ast.errores.extend(errores_sintacticos_globales)
            errores_sintacticos_globales.clear()

        # EJECUCIÓN EN DOS FASES

        # FASE 1: Registrar todos los procedimientos
        for instr in ast.getInstrucciones():
            if isinstance(instr, Procedimientos):
                if ast.getFuncion(instr.id) is None:
                    ast.setFuncion(instr)
                else:
                    error = Errores(
                        "SEMANTICO",
                        f"El procedimiento '{instr.id}' ya ha sido declarado",
                        instr.linea,
                        instr.col,
                    )
                    ast.errores.append(error)

        # FASE 2: Ejecutar instrucciones no-procedimiento
        for instr in ast.getInstrucciones():
            if not isinstance(instr, Procedimientos):
                resultado = instr.interpretar(ast, tabla)
                if isinstance(resultado, Errores) and resultado not in ast.errores:
                    ast.errores.append(resultado)

        # Mostrar resultados
        print(ast.getConsola())

        # Generar AST
        try:
            if ast.getInstrucciones():
                generarGrafica(ast, "reporteAST")
                print("AST generado correctamente en reporteAST.dot y reporteAST.svg")
        except Exception as e:
            print(f"Error al generar el AST: {e}")

        return ast

    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        return None


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
    # Determinar qué archivo ejecutar
    if len(sys.argv) > 1:
        # Usar el archivo especificado por línea de comandos
        archivo = sys.argv[1]
        ast = main(archivo, usar_singleton=True)
    else:
        # Modo vectores (predeterminado)
        ast = main()

    if ast is not None:
        # Imprimir tablas
        if hasattr(ast.get_tabla_global(), "ImprimirTabla"):
            ast.get_tabla_global().ImprimirTabla()
        else:
            imprimir_tabla_simbolos(ast.get_tabla_global())

        imprimir_tabla_errores(ast.get_errores())

        # Generar reporte de vectores si existen
        if hasattr(ast, "vectores") and ast.vectores:
            reporte = ReporteVectores(ast)
            reporte.generar_reporte_consola()
