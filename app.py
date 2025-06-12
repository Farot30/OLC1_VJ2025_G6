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
            arbol = Arbol([])  # Crea un nuevo árbol
            instrucciones = parse_input(entrada, arbol)
            arbol.set_instrucciones(instrucciones)
            # Reinicia la tabla de símbolos (nueva instancia)
            tabla = tablaSimbolo()
            tabla.limpiar()  # <-- Agrega este método en tu clase tablaSimbolo si no existe
            arbol.setTablaGlobal(tabla)
            arbol.setConsola("")
            arbol.errores = []  # Limpia errores previos
            # Ejecutar instrucciones
            for instr in arbol.getInstrucciones():
                if instr is None:
                    continue
                resultado = instr.interpretar(arbol, tabla)
                if isinstance(resultado, Errores):
                    arbol.errores.append(resultado)
            salida = arbol.getConsola()
            # 3. Mostrar todos los errores del árbol
            if arbol.errores:
                errores = "#\tTipo\tDescripcion\tLINEA\tCOLUMNA\n"
                for idx, error in enumerate(arbol.errores, 1):
                    errores += f"{idx}\t{error.get_tipo_error()}\t{error.get_desc()}\t{error.get_linea()}\t{error.get_col()}\n"
                # Agrega el conteo de errores al inicio de la salida
                salida = (
                    f"Se encontraron {len(arbol.errores)} errores durante la compilación.\n"
                    + salida
                )
            else:
                errores = "Sin errores."
            # Generar tabla de símbolos usando el método de la clase
            tabla_simbolos = tabla.tablaComoString()
            ast = str(arbol)
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


if __name__ == "__main__":
    app.run(debug=True)
