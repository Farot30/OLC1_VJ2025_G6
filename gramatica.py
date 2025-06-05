####  DEFINICION DE ANALISIS LEXICO -----------------------------------------------------------------


# Construyendo el analizador léxico
import ply.lex as lex

lexer = lex.lex()

# Asociación de operadores y precedencia


#### DEFINICION DE GRAMATICA (ANALISIS SINTACTICO) ----------------------------------------------------------------------------


## APLICACION ----------------------------------------------------------------------------
import ply.yacc as yacc

parser = yacc.yacc()


f = open("./entrada.txt", "r")
input = f.read()
print(input)
parser.parse(input)
