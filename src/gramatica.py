####  DEFINICION DE ANALISIS LEXICO -----------------------------------------------------------------

# tokens
tokens = [
    "INT",
    "DOUBLE",
    "STRING",
    "BOOL",
    "TRUE",
    "FALSE",
    "CHAR",
    "MENOS",
    "MULT",
    "DIVISION",
    "POTENCIA",
    "MODULO",
    "PUNTOCOMA",
    "MAS",
    "PAR1",
    "PAR2",
    "IGUAL",
    "DECIMAL",
    "ENTERO",
    "CADENA",
    "CARACTER",
    "ID",
    "INCREMENTO",
    "DECREMENTO",
    "BOOLEANO",
    "MENOR_IGUAL",
    "MAYOR_QUE",
    "MAYOR_IGUAL",
    "PRINT",
    "PRINTLN",
    "OR",
    "AND",
    "XOR",
    "NOT",
]

# Simbolos
t_PUNTOCOMA = r";"
t_MAS = r"\+"
t_MENOS = r"-"
t_MULT = r"\*"
t_DIVISION = r"/"
t_POTENCIA = r"\*\*"
t_MODULO = r"%"
t_PAR1 = r"\("
t_PAR2 = r"\)"
t_IGUAL = r"="
t_ignore = " \t\r\f"
t_INCREMENTO = r"\+\+"
t_DECREMENTO = r"--"
t_MENOR_IGUAL = r"<="
t_MAYOR_QUE = r">"
t_MAYOR_IGUAL = r">="
t_OR = r"\|\|"
t_AND = r"&&"
t_XOR = r"\^"
t_NOT = r"!"

reservadas = {
    "int": "INT",
    "float": "DOUBLE",
    "str": "STRING",
    "bool": "BOOL",
    "char": "CHAR",
    "true": "TRUE",
    "false": "FALSE",
    "print": "PRINT",
    "println": "PRINTLN",
}


def t_COMMENT_SINGLELINE(t):
    r"//.*"
    pass


def t_COMMENT_MULTILINE(t):
    r"/\*(.|\n)*?\*/"
    t.lexer.lineno += t.value.count("\n")
    pass


def t_BOOLEANO(t):
    r"(verdadero|falso|true|false|TRUE|FALSE)"
    t.value = t.value.lower() in ("verdadero", "true")
    return t


def t_ID(t):
    r"[a-zA-Z][a-zA-Z0-9_]*"
    t.type = reservadas.get(t.value, "ID")
    return t


def t_CARACTER(t):
    r"\'(.)\'"
    t.value = t.value[1:-1]
    return t


def t_INT(t):
    r"int"
    return t


def t_DOUBLE(t):
    r"float"
    return t


def t_STRING(t):
    r"str"
    return t


def t_BOOL(t):
    r"bool"
    return t


def t_CHAR(t):
    r"char"
    return t


def t_TRUE(t):
    r"true"
    t.value = True
    return t


def t_FALSE(t):
    r"false"
    t.value = False
    return t


def t_DECIMAL(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t


def t_ENTERO(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_CADENA(t):
    r'"([^"\\\n]|(\\.))*"'  # Permite secuencias de escape dentro de la cadena
    t.value = bytes(t.value[1:-1], "utf-8").decode("unicode_escape")
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"[LEX ERROR] Carácter ilegal: {t.value[0]}")
    t.lexer.skip(1)


# Construyendo el analizador léxico
import ply.lex as lex

from src.expresiones.CAritmeticas import Aritmeticas, Operadores
from src.expresiones.CNativo import Nativo
from src.instrucciones.CDeclaracion import Declaracion
from src.simbolo.CTipo import Tipo, tipoDato
from src.instrucciones.CAsignacion import Asignacion
from src.instrucciones.CIncremento import Incremento, Decremento
from src.expresiones.CUnitario import Unario
from src.expresiones.CRelacionales import Relacional, OperadoresRel
from src.instrucciones.CPrint import Print
from src.instrucciones.CPrintln import Println
from src.expresiones.COr import Or
from src.expresiones.CAnd import And
from src.expresiones.CXor import Xor
from src.expresiones.CNot import Not

lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ("left", "OR"),
    ("left", "AND", "XOR"),
    ("right", "NOT"),
    ("left", "MAS", "MENOS"),
    ("left", "MULT", "DIVISION", "MODULO"),
    ("right", "POTENCIA"),
    ("right", "UMENOS"),
    ("left", "MENOR_IGUAL", "MAYOR_QUE", "MAYOR_IGUAL"),
)

#### DEFINICION DE GRAMATICA (ANALISIS SINTACTICO) ----------------------------------------------------------------------------


def p_inicio(t):
    "inicio : instrucciones"
    t[0] = t[1]


def p_expresion_or(t):
    "expresion : expresion OR expresion"
    t[0] = Or(t[1], t[3], t.lineno(2), find_column(t.lexer.lexdata, t.slice[2]))


def p_expresion_and(t):
    "expresion : expresion AND expresion"
    t[0] = And(t[1], t[3], t.lineno(2), find_column(t.lexer.lexdata, t.slice[2]))


def p_expresion_xor(t):
    "expresion : expresion XOR expresion"
    t[0] = Xor(t[1], t[3], t.lineno(2), find_column(t.lexer.lexdata, t.slice[2]))


def p_expresion_not(t):
    "expresion : NOT expresion"
    t[0] = Not(t[2], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


def p_expresion_id(t):
    "expresion : ID"
    t[0] = Nativo(
        Tipo(None), t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1])
    )


def p_instrucciones(t):
    """instrucciones : instrucciones instruccion
    | instruccion"""
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]


def p_instruccion_asignacion(t):
    "instruccion : ID IGUAL expresion PUNTOCOMA"
    t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


def p_instruccion_incremento(t):
    "instruccion : ID INCREMENTO PUNTOCOMA"
    t[0] = Incremento(t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


def p_instruccion_decremento(t):
    "instruccion : ID DECREMENTO PUNTOCOMA"
    t[0] = Decremento(t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


def p_expresion_booleano(t):
    "expresion : BOOLEANO"
    t[0] = Nativo(
        Tipo(tipoDato.BOOL), t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1])
    )


def p_instruccion(t):
    """instruccion : declaracion PUNTOCOMA
    | expresion PUNTOCOMA"""
    t[0] = t[1]


def find_column(input, token):
    last_cr = input.rfind("\n", 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    return token.lexpos - last_cr


def p_declaracion_cvalor(t):
    "declaracion : tipos ID IGUAL expresion"
    t[0] = Declaracion(
        t[1], t.lineno(2), find_column(t.lexer.lexdata, t.slice[2]), t[2], t[4]
    )


def p_declaracion_sinval(t):
    "declaracion : tipos ID"
    t[0] = Declaracion(
        t[1], t.lineno(2), find_column(t.lexer.lexdata, t.slice[2]), t[2], None
    )


def p_expresion_binaria(t):
    """expresion : expresion MAS expresion
    | expresion MENOS expresion
    | expresion MULT expresion
    | expresion DIVISION expresion
    | expresion POTENCIA expresion
    | expresion MODULO expresion"""

    if t[2] == "+":
        operador = Operadores.SUMA
    elif t[2] == "-":
        operador = Operadores.RESTA
    elif t[2] == "*":
        operador = Operadores.MULTIPLICACION
    elif t[2] == "/":
        operador = Operadores.DIVISION
    elif t[2] == "**":
        operador = Operadores.POTENCIA
    elif t[2] == "%":
        operador = Operadores.MODULO
    else:
        raise SyntaxError(f"Operador no esperado: {t[2]}")

    t[0] = Aritmeticas(
        operador,
        t.lineno(2),  # línea del operador
        find_column(t.lexer.lexdata, t.slice[2]),  # columna del operador
        t[1],
        t[3],
    )


def p_expresion_unaria(t):
    "expresion : MENOS expresion %prec UMENOS"
    t[0] = Unario("-", t[2], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


def p_instruccion_print(t):
    "instruccion : PRINT PAR1 expresion PAR2 PUNTOCOMA"

    t[0] = Print(t[3], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


def p_instruccion_println(t):
    "instruccion : PRINTLN PAR1 expresion PAR2 PUNTOCOMA"
    t[0] = Println(t[3], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


def p_expresion_par(t):
    "expresion : PAR1 expresion PAR2"
    t[0] = t[2]


def p_expresion_entero(t):
    "expresion : ENTERO"
    t[0] = Nativo(
        Tipo(tipoDato.ENTERO),
        t[1],
        t.lineno(1),
        find_column(t.lexer.lexdata, t.slice[1]),
    )


def p_expresion_decimal(t):
    "expresion : DECIMAL"
    t[0] = Nativo(
        Tipo(tipoDato.DECIMAL),
        t[1],
        t.lineno(1),
        find_column(t.lexer.lexdata, t.slice[1]),
    )


def p_expresion_cadena(t):
    "expresion : CADENA"
    t[0] = Nativo(
        Tipo(tipoDato.STRING),
        t[1],
        t.lineno(1),
        find_column(t.lexer.lexdata, t.slice[1]),
    )


def p_expresion_bool(t):
    """expresion : TRUE
    | FALSE"""
    valor = True if t.slice[1].type == "TRUE" else False
    t[0] = Nativo(
        Tipo(tipoDato.BOOL),
        valor,
        t.lineno(1),
        find_column(t.lexer.lexdata, t.slice[1]),
    )


def p_expresion_char(t):
    "expresion : CHAR"
    t[0] = Nativo(
        Tipo(tipoDato.CHAR), t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1])
    )


def p_expresion_caracter(t):
    "expresion : CARACTER"
    t[0] = Nativo(
        Tipo(tipoDato.CHAR), t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1])
    )


def p_expresion_relacional(t):
    """expresion : expresion MENOR_IGUAL expresion
    | expresion MAYOR_QUE expresion
    | expresion MAYOR_IGUAL expresion"""
    if t[2] == "<=":
        operador = OperadoresRel.MENOR_IGUAL
    elif t[2] == ">":
        operador = OperadoresRel.MAYOR_QUE
    elif t[2] == ">=":
        operador = OperadoresRel.MAYOR_IGUAL
    else:
        raise SyntaxError(f"Operador no esperado: {t[2]}")
    t[0] = Relacional(
        operador,
        t.lineno(2),
        find_column(t.lexer.lexdata, t.slice[2]),
        t[1],
        t[3],
    )


def p_tipos(t):
    """tipos : INT
    | DOUBLE
    | STRING
    | CHAR
    | BOOL"""
    if t[1] == "int":
        t[0] = Tipo(tipoDato.ENTERO)
    elif t[1] == "float":
        t[0] = Tipo(tipoDato.DECIMAL)
    elif t[1] == "str":
        t[0] = Tipo(tipoDato.STRING)
    elif t[1] == "char":
        t[0] = Tipo(tipoDato.CHAR)
    elif t[1] == "bool":
        t[0] = Tipo(tipoDato.BOOL)


def p_error(t):
    if t:
        print(f"Error de sintaxis en '{t.value}' (línea {t.lineno})")
    else:
        print("Error de sintaxis al final del archivo")


## APLICACION ----------------------------------------------------------------------------
import ply.yacc as yacc

start = "inicio"  # Agrega esto antes de parser = yacc.yacc()

parser = yacc.yacc()


def parse_input(input_text):
    return parser.parse(input_text)
