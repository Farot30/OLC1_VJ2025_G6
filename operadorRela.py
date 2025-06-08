import ply.lex as lex
import ply.yacc as yacc

# === TOKENS ===
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

# === EXPRESIONES REGULARES DE TOKENS ===
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

# === ACCIONES DE TOKENS ===
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
    t.value = t.value[1:-1]
    return t

def t_COMMENT(t):
    r'//.*'
    pass

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# === JERARQUÍA DE OPERADORES ===
precedence = (
    ('right', 'UMENOS'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('left', 'MENOR_IGUAL', 'MENOR_QUE', 'MAYOR_IGUAL', 'MAYOR_QUE', 'IGUAL_IGUAL', 'DIFERENTE')
)

# === LISTA DE INSTRUCCIONES PARSEADAS ===
instrucciones = []

# === IMPORTACIONES DE CLASES INTERNAS ===
from src.instrucciones.Evaluar import Evaluar
from src.instrucciones.Nativo import Nativo
from src.instrucciones.Aritmeticas import Aritmeticas, Operadores
from src.instrucciones.Relacional import Relacional, OperadoresRel
from src.instrucciones.Unario import Unario
from src.simbolo.CTipo import Tipo, tipoDato

# === PRODUCCIONES ===
def p_instrucciones_lista(t):
    '''instrucciones : instruccion instrucciones
                     | instruccion'''
    global instrucciones
    if len(t) == 3:
        instrucciones.append(t[1])
        t[0] = instrucciones
    else:
        instrucciones = [t[1]]
        t[0] = instrucciones

def p_instruccion_evaluar(t):
    'instruccion : REVALUAR CORIZQ expresion CORDER PTCOMA'
    t[0] = Evaluar(t[3], t.lineno(1), t.lexpos(1))

def p_expresion_binaria(t):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIDO expresion'''
    op_map = {'+': Operadores.SUMA, '-': Operadores.RESTA,
              '*': Operadores.MULTIPLICACION, '/': Operadores.DIVISION}
    t[0] = Aritmeticas(op_map[t[2]], t.lineno(2), t.lexpos(2), t[1], t[3])

def p_expresion_relacional(t):
    '''expresion : expresion MENOR_IGUAL expresion
                 | expresion MAYOR_IGUAL expresion
                 | expresion MENOR_QUE expresion
                 | expresion MAYOR_QUE expresion
                 | expresion IGUAL_IGUAL expresion
                 | expresion DIFERENTE expresion'''
    op_map = {
        '<=': OperadoresRel.MENOR_IGUAL,
        '>=': OperadoresRel.MAYOR_IGUAL,
        '<': OperadoresRel.MENOR_QUE,
        '>': OperadoresRel.MAYOR_QUE,
        '==': OperadoresRel.IGUAL_IGUAL,
        '!=': OperadoresRel.DIFERENTE
    }
    t[0] = Relacional(op_map[t[2]], t.lineno(2), t.lexpos(2), t[1], t[3])

def p_expresion_valor(t):
    '''expresion : ENTERO
                 | DECIMAL'''
    tipo = tipoDato.ENTERO if isinstance(t[1], int) else tipoDato.DECIMAL
    t[0] = Nativo(Tipo(tipo), t[1], t.lineno(1), t.lexpos(1))

def p_expresion_caracter(t):
    'expresion : CARACTER'
    t[0] = Nativo(Tipo(tipoDato.CHAR), t[1], t.lineno(1), t.lexpos(1))

def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = Unario('-', t[2], t.lineno(1), t.lexpos(1))

def p_error(t):
    print("Error de sintaxis")

parser = yacc.yacc()

# === FUNCIÓN PRINCIPAL ===
def parse_input(input_text: str):
    global instrucciones
    instrucciones = []
    parser.parse(input_text)
    return instrucciones
