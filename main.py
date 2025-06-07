from src.gramatica import parse_input
from src.simbolo.CArbol import Arbol
from src.simbolo.TablaSimbolo import tablaSimbolo
from src.excepciones.CErrores import Errores

def main():
    try:
        entrada = 'false+"q";'
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
        print(ast.getConsola())

    except Exception as e:
        print(f"Error durante la ejecución: {e}")

if __name__ == "__main__":
    main()
