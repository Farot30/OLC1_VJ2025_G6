####  DEFINICION DE ANALISIS LEXICO -----------------------------------------------------------------

#tokens
tokens = [
    'INT', 'DOUBLE', 'STRING', 'BOOL',
    'TRUE', 'FALSE', 'CHAR',
    'MENOS', 'MULT', 'DIVISION', 'POTENCIA', 'MODULO',
    'PUNTOCOMA', 'MAS', 'MENOR', 
    'PAR1', 'PAR2',
    'IGUAL',
    'DECIMAL', 'ENTERO',
    'CADENA', 'CARACTER',
    'ID'
]

# Simbolos
t_PUNTOCOMA = r';'
t_MAS       = r'\+'
t_MENOS     = r'-'
t_DIVISION  = r'/'
t_POTENCIA  = r'\*\*'
t_MULT      = r'\*'
t_MODULO    = r'%'
t_PAR1      = r'\('
t_PAR2      = r'\)'
t_IGUAL     = r'='
t_ignore    = ' \t\r\f'

reservadas = {
    'int': 'INT',
    'float': 'DOUBLE',
    'str': 'STRING',
    'bool': 'BOOL',
    'char': 'CHAR',
    'true': 'TRUE',
    'false': 'FALSE'
}

def t_ID(t):
    r'[a-z][a-z0-9_]*'
    t.type = reservadas.get(t.value, 'ID')
    return t

def t_CARACTER(t):
    r'\'.\''
    t.value = t.value[1]  # borrar comillas simples
    return t

def t_INT(t):
    r'int'
    return t

def t_DOUBLE(t):
    r'float'
    return t

def t_STRING(t):
    r'str'
    return t

def t_BOOL(t):
    r'bool'
    return t

def t_CHAR(t):
    r'char'
    return t

def t_TRUE(t):
    r'true'
    t.value = True
    return t

def t_FALSE(t):
    r'false'
    t.value = False
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CADENA(t):
    r'\"[^\"\n]*\"'
    t.value = t.value[1:-1]  # quitar comillas
    return t


def t_newline(t):
    r'\n+'
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
lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ('left','MAS','MENOS'),
    ('left','MULT','DIVISION', 'MODULO'),
    ('right', 'POTENCIA'),
    ('right','UMENOS'),
)

#### DEFINICION DE GRAMATICA (ANALISIS SINTACTICO) ----------------------------------------------------------------------------
# Importar tus clases


def p_inicio(t):
    'inicio : instrucciones'
    t[0] = t[1]

def p_instrucciones(t):
    '''instrucciones : instrucciones instruccion
                     | instruccion'''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_instruccion(t):
    '''instruccion : declaracion PUNTOCOMA
            | expresion PUNTOCOMA'''
    t[0] = t[1]

def p_declaracion_cvalor(t):
    'declaracion : tipos ID IGUAL expresion'
    t[0] = Declaracion(t[1], 0, 0, t[2], t[4])

def p_declaracion_sinval(t):
    'declaracion : tipos ID '
    t[0] = Declaracion(t[1], 0, 0, t[2], None)

def p_expresion_binaria(t):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion MULT expresion
                 | expresion DIVISION expresion
                 | expresion POTENCIA expresion
                 | expresion MODULO expresion'''
    
    if t[2] == '+':
        operador = Operadores.SUMA
    elif t[2] == '-':
        operador = Operadores.RESTA
    elif t[2] == '*':
        operador = Operadores.MULTIPLICACION
    elif t[2] == '/':
        operador = Operadores.DIVISION
    elif t[2] == '**':
        operador = Operadores.POTENCIA
    elif t[2] == '%':
        operador = Operadores.MODULO
    else:
        raise SyntaxError(f"Operador no esperado: {t[2]}")

    t[0] = Aritmeticas(operador, 0, 0, t[1], t[3])

def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = -t[2]

def p_expresion_par(t):
    'expresion : PAR1 expresion PAR2'
    t[0] = t[2]

def p_expresion_entero(t):
    'expresion : ENTERO'
    t[0] = Nativo(Tipo(tipoDato.ENTERO), t[1], t.lineno(1), 0)

def p_expresion_decimal(t):
    'expresion : DECIMAL'
    t[0] = Nativo(Tipo(tipoDato.DECIMAL), t[1], t.lineno(1), 0)

def p_expresion_cadena(t):
    'expresion : CADENA'
    t[0] = Nativo(Tipo(tipoDato.STRING), t[1], t.lineno(1), 0)

def p_expresion_bool(t):
    '''expresion : TRUE
                 | FALSE'''
    valor = True if t.slice[1].type == 'TRUE' else False
    t[0] = Nativo(Tipo(tipoDato.BOOL), valor, t.lineno(1), 0)

def p_expresion_char(t):
    'expresion : CHAR'
    t[0] = Nativo(Tipo(tipoDato.CHAR), t[1], t.lineno(1), 0)

def p_expresion_caracter(t):
    'expresion : CARACTER'
    t[0] = Nativo(Tipo(tipoDato.CHAR), t[1], t.lineno(1), 0)

def p_tipos(t):
    '''tipos : INT
             | DOUBLE
             | STRING
             | CHAR'''
    if t[1] == 'int':
        t[0] = Tipo(tipoDato.ENTERO)
    elif t[1] == 'float':
        t[0] = Tipo(tipoDato.DECIMAL)
    elif t[1] == 'str':
        t[0] = Tipo(tipoDato.STRING)
    elif t[1] == 'char':
        t[0] = Tipo(tipoDato.CHAR)

def p_error(t):
    if t:
        print(f"Error de sintaxis en '{t.value}' (línea {t.lineno})")
    else:
        print("Error de sintaxis al final del archivo")


## APLICACION ----------------------------------------------------------------------------
import ply.yacc as yacc

parser = yacc.yacc()


def parse_input(input_text):
    return parser.parse(input_text)
