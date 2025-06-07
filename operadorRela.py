import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = (
    'REVALUAR',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'PTCOMA',
    'MENOR_IGUAL',
    'MAYOR_IGUAL',
    'MENOR_QUE',
    'MAYOR_QUE',
    'IGUAL_IGUAL',
    'DIFERENTE',
    'DECIMAL',
    'ENTERO',
    'CARACTER'
)

# Reglas de expresión regular
t_REVALUAR     = r'Evaluar'
t_PARIZQ       = r'\('
t_PARDER       = r'\)'
t_CORIZQ       = r'\['
t_CORDER       = r'\]'
t_MAS          = r'\+'
t_MENOS        = r'-'
t_POR          = r'\*'
t_DIVIDIDO     = r'/'
t_PTCOMA       = r';'
t_MENOR_IGUAL  = r'<='
t_MAYOR_IGUAL  = r'>='
t_IGUAL_IGUAL  = r'=='
t_DIFERENTE    = r'!='
t_MENOR_QUE    = r'<'
t_MAYOR_QUE    = r'>'

# Reglas con acciones
def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CARACTER(t):
    r"'(\\.|[^\\'])'"
    t.value = t.value[1:-1]  # quitar comillas
    return t

# Comentario de una línea
def t_COMMENT(t):
    r'//.*'
    pass

# Ignorar espacios y tabs
t_ignore = " \t"

# Nueva línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()

# === GRAMÁTICA ===
precedence = (
    ('right', 'UMENOS'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('left', 'MENOR_IGUAL', 'MENOR_QUE', 'MAYOR_IGUAL', 'MAYOR_QUE', 'IGUAL_IGUAL', 'DIFERENTE')
)

def p_instrucciones_lista(t):
    '''instrucciones : instruccion instrucciones
                     | instruccion'''

def p_instruccion_evaluar(t):
    'instruccion : REVALUAR CORIZQ expresion CORDER PTCOMA'
    print("El valor de la expresión es:", t[3])

def p_expresion_binaria(t):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIDO expresion'''
    if t[2] == '+': t[0] = t[1] + t[3]
    elif t[2] == '-': t[0] = t[1] - t[3]
    elif t[2] == '*': t[0] = t[1] * t[3]
    elif t[2] == '/': t[0] = t[1] / t[3]

def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = -t[2]

def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

def p_expresion_valor(t):
    '''expresion : ENTERO
                 | DECIMAL'''
    t[0] = t[1]

def p_expresion_caracter(t):
    'expresion : CARACTER'
    t[0] = ord(t[1])  # Convertir char a ASCII para poder comparar

def p_expresion_relacional(t):
    '''expresion : expresion MENOR_IGUAL expresion
                 | expresion MAYOR_IGUAL expresion
                 | expresion MENOR_QUE expresion
                 | expresion MAYOR_QUE expresion
                 | expresion IGUAL_IGUAL expresion
                 | expresion DIFERENTE expresion'''
    
    if t[2] == '<=': t[0] = t[1] <= t[3]
    elif t[2] == '>=': t[0] = t[1] >= t[3]
    elif t[2] == '<': t[0] = t[1] < t[3]
    elif t[2] == '>': t[0] = t[1] > t[3]
    elif t[2] == '==': t[0] = t[1] == t[3]
    elif t[2] == '!=': t[0] = t[1] != t[3]

def p_error(t):
    print("Error de sintaxis")

# Crear el parser
parser = yacc.yacc()

# === PRUEBAS ===
entrada = """
Evaluar [1 == 1];
Evaluar [1 != 2];
Evaluar [5.5 < 3050 < 'F'];
Evaluar [125.654 == 54.34];
Evaluar ['C' <= 90];
Evaluar [3 + 5 * 2 > 10];
"""

parser.parse(entrada)
