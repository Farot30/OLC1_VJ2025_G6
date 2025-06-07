import io
from flask import Flask, render_template, request, send_file
from src.gramatica import parse_input
from src.simbolo.CArbol import Arbol
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.excepciones.CErrores import Errores

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    entrada = ""
    salida = ""
    errores = ""
    tabla_simbolos = ""
    ast = ""
    if request.method == "POST":
        if "interpretar" in request.form:
            entrada = request.form.get("entrada", "")
            instrucciones = parse_input(entrada)
            arbol = Arbol(instrucciones)
            tabla = tablaSimbolo()
            arbol.setTablaGlobal(tabla)
            arbol.setConsola("")
            lista_errores = []
            # Ejecutar instrucciones
            for instr in arbol.getInstrucciones():
                resultado = instr.interpretar(arbol, tabla)
                if isinstance(resultado, Errores):
                    lista_errores.append(str(resultado))
            salida = arbol.getConsola()
            errores = "\n".join(lista_errores) if lista_errores else "Sin errores."
            # Generar tabla de símbolos
            tabla_simbolos = "#\tID\tTIPO\tTIPO2\tENTORNO\tVALOR\tLINEA\tCOLUMNA\n"
            for idx, simbolo in enumerate(tabla.getTabla().values(), 1):
                id_ = simbolo.getId()
                tipo1 = "Variable"
                tipo2 = (
                    simbolo.getTipo().tipo.name if simbolo.getTipo() else "desconocido"
                )
                entorno = tabla.getNombre() if tabla.getNombre() else "Global"
                valor = simbolo.getValor()
                linea = simbolo.getLinea() if hasattr(simbolo, "getLinea") else "-"
                columna = (
                    simbolo.getColumna() if hasattr(simbolo, "getColumna") else "-"
                )
                tabla_simbolos += f"{idx}\t{id_}\t{tipo1}\t{tipo2}\t{entorno}\t{valor}\t{linea}\t{columna}\n"
            # AST (puedes personalizar esto)
            ast = str(arbol)  # O usa tu propio método para mostrar el AST
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
        ast=ast,
    )


@app.route("/descargar/<tipo>")
def descargar(tipo):
    if tipo == "errores":
        contenido = request.args.get("data", "No hay errores.")
        filename = "errores.txt"
    elif tipo == "tabla":
        contenido = request.args.get("data", "No hay tabla de símbolos.")
        filename = "tabla_simbolos.txt"
    elif tipo == "ast":
        contenido = request.args.get("data", "No hay AST.")
        filename = "ast.txt"
    else:
        contenido = "Tipo no válido."
        filename = "reporte.txt"
    buffer = io.BytesIO()
    buffer.write(contenido.encode("utf-8"))
    buffer.seek(0)
    return send_file(
        buffer, as_attachment=True, download_name=filename, mimetype="text/plain"
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
