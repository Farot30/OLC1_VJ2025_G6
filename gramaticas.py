import ply.lex as lex
import ply.yacc as yacc

## Lexico
tokens = (
    "ID",
    "ENTERO",
    "DECIMAL",
    "BOOLEANO",
    "IGUAL",
    "PUNTOYCOMA",
)

# Tokens
t_ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
t_IGUAL = r"="
t_PUNTOYCOMA = r";"


def t_BOOLEANO(t):
    r"(verdadero|falso|true|false|TRUE|FALSE)"
    if t.value in ("verdadero", "true", "TRUE"):
        t.value = True
    else:
        t.value = False
    return t


def t_DECIMAL(t):
    r"-?\d+\.\d+"
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %s", t.value)
        t.value = 0
    return t


def t_ENTERO(t):
    r"-?\d+"
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %s", t.value)
        t.value = 0
    return t


t_ignore = " \t"


def t_newline(t):
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Error de sintaxis")
    t.lexer.skip(1)


lexer = lex.lex()


# Gramática
def p_inicial(t):
    """inicial : asignaciones"""
    pass


def p_asignaciones(t):
    """asignaciones : asignaciones asignacion
    | asignacion"""
    pass


def p_asignacion(t):
    "asignacion : ID IGUAL valor PUNTOYCOMA"
    print(f"Variable '{t[1]}' asignada con valor {t[3]}")


def p_valor(t):
    """valor : ENTERO
    | DECIMAL
    | BOOLEANO"""
    t[0] = t[1]


def p_error(t):
    print("Error de sintaxis")


parser = yacc.yacc()

f = open("./entrada.txt", "r")
input = f.read()
print(input)
parser.parse(input)
