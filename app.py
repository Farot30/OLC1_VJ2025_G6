import os
from flask import Flask, render_template, request, send_from_directory
from src.gramatica import parse_input, errores_sintacticos_globales
from src.simbolo.CArbol import Arbol
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.excepciones.CErrores import Errores
from src.abstracto.CAST import generarGrafica


app = Flask(__name__, static_folder="static")


@app.route("/report/<path:filename>")
def report(filename):
    return send_from_directory("report", filename)


@app.route("/", methods=["GET", "POST"])
def index():
    entrada = ""
    salida = ""
    errores = ""
    tabla_simbolos = ""
    ast_svg = ""
    if request.method == "POST":
        if "interpretar" in request.form:
            entrada = request.form.get("entrada", "")
            arbol = Arbol([])  # Crea un nuevo árbol
            instrucciones = parse_input(entrada, arbol)
            arbol.set_instrucciones(instrucciones)

            # AÑADIDO: Transferir errores sintácticos al árbol
            if errores_sintacticos_globales:
                arbol.errores.extend(errores_sintacticos_globales)
                errores_sintacticos_globales.clear()

            # Reinicia la tabla de símbolos (nueva instancia)
            tabla = tablaSimbolo()
            tabla.limpiar()
            arbol.setTablaGlobal(tabla)
            arbol.setConsola("")
            # NO limpiar errores aquí: arbol.errores = []  <-- COMENTADO

            # Ejecutar instrucciones
            for instr in arbol.getInstrucciones():
                if instr is None:
                    continue
                resultado = instr.interpretar(arbol, tabla)
                if isinstance(resultado, Errores):
                    arbol.errores.append(resultado)
            salida = arbol.getConsola()

            # Mostrar todos los errores del árbol
            if arbol.errores:
                errores = "#\tTipo\tDescripcion\tLINEA\tCOLUMNA\n"
                for idx, error in enumerate(arbol.errores, 1):
                    errores += f"{idx}\t{error.get_tipo_error()}\t{error.get_desc()}\t{error.get_linea()}\t{error.get_col()}\n"
                salida = (
                    f"Se encontraron {len(arbol.errores)} errores durante la compilación.\n"
                    + salida
                )
            else:
                errores = "Sin errores."

            # Generar tabla de símbolos usando el método de la clase
            tabla_simbolos = tabla.tablaComoString()

            # Generar el AST y el archivo .svg en static/
            if arbol.getInstrucciones():
                try:
                    generarGrafica(arbol, "report/ast_reporte")
                    ast_svg = "ast_reporte.svg"
                except Exception as e:
                    ast_svg = ""
                    print(f"Error al generar AST: {e}")

        elif "archivo" in request.files:
            archivo = request.files["archivo"]
            if archivo and archivo.filename:
                if archivo.filename.lower().endswith(".objc"):
                    entrada = archivo.read().decode("utf-8")
                else:
                    errores = "Solo se permiten archivos con extensión .objc"
    return render_template(
        "index.html",
        entrada=entrada,
        salida=salida,
        errores=errores,
        tabla_simbolos=tabla_simbolos,
        ast_svg=ast_svg,
    )


@app.route("/errores")
def pagina_errores():
    # Puedes guardar los errores en una variable global o en sesión si lo prefieres
    errores = request.args.get("data", "")
    # Si los errores vienen como string, sepáralos por líneas
    errores_lista = []
    if errores:
        for linea in errores.split("\n"):
            if linea.strip() and not linea.startswith("#"):
                partes = linea.split("\t")
                if len(partes) >= 5:
                    errores_lista.append(
                        {
                            "num": partes[0],
                            "tipo": partes[1],
                            "desc": partes[2],
                            "linea": partes[3],
                            "col": partes[4],
                        }
                    )
    return render_template("errores.html", errores=errores_lista)


@app.route("/tabla_simbolos")
def mostrar_tabla_simbolos():
    # Recupera la tabla de símbolos global (ajusta según tu lógica)
    tabla = tablaSimbolo()
    return render_template("tabla_simbolos.html", tabla=tabla.getTabla())


@app.route("/ast")
def mostrar_ast():
    # El archivo SVG se genera en static/ast_reporte.svg
    ast_path = os.path.join("report", "ast_reporte.svg")
    if os.path.exists(ast_path):
        # Puedes mostrar el SVG embebido en HTML
        return render_template("ast.html", ast_svg="ast_reporte.svg")
    else:
        return "AST no generado aún."


if __name__ == "__main__":
    app.run(debug=True)
