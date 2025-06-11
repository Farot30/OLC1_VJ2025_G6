####  DEFINICION DE ANALISIS LEXICO -----------------------------------------------------------------

#tokens
tokens = [
    'INT', 'DOUBLE', 'STRING', 'BOOL',
    'TRUE', 'FALSE', 'CHAR',
    'MENOS', 'MULT', 'DIVISION', 'POTENCIA', 'MODULO',
    'PUNTOCOMA', 'MAS', 
    'PAR1', 'PAR2',
    'IGUAL',
    'DECIMAL', 'ENTERO',
    'CADENA', 'CARACTER',
    'ID', 'IF', 'ELSE',
    'LLAVE1',
    "LLAVE2","BOOLEANO","MENOR_IGUAL", "MAYOR_QUE",
    "MAYOR_IGUAL",  "MENOR_QUE", "IGUAL_IGUAL",
    "DIFERENTE", "PRINT",  "PRINTLN", 'BREAK'
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
t_MENOR_IGUAL = r"<="
t_MAYOR_QUE = r">"
t_MAYOR_IGUAL = r">="
t_MENOR_QUE = r"<"
t_IGUAL_IGUAL = r"=="
t_DIFERENTE = r"!="
t_LLAVE1    = r'\{'
t_LLAVE2    = r'\}'
t_ignore    = ' \t\r\f'

reservadas = {
    'int': 'INT',
    'float': 'DOUBLE',
    'str': 'STRING',
    'bool': 'BOOL',
    'char': 'CHAR',
    'true': 'TRUE',
    'false': 'FALSE',
    'if' : 'IF',
    "print": "PRINT",
    "println": "PRINTLN",
    'break': 'BREAK'
}

def t_ID(t):
    r'[a-z][a-z0-9_]*'
    t.type = reservadas.get(t.value, 'ID')
    return t

def t_CARACTER(t):
    r'\'.\''
    t.value = t.value[1]  # borrar comillas simples
    return t

def t_BOOLEANO(t):
    r"(verdadero|falso|true|false|TRUE|FALSE)"
    t.value = t.value.lower() in ("verdadero", "true")
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
    error = Errores(
        "Léxico",
        f"El carácter “{t.value[0]}” no pertenece al lenguaje",
        t.lineno,
        t.lexpos,
    )
    arbol = getattr(t.lexer, "arbol", None)
    if arbol:
        arbol.errores.append(error)
    print(error)
    t.lexer.skip(1)

    
# Construyendo el analizador léxico
import ply.lex as lex

from src.simbolo.CInstancia import tabla_S as aTab

from src.instrucciones.CPrint import Print
from src.instrucciones.CPrintln import Println
from src.expresiones.CRelacionales import OperadoresRel, Relacional
from src.instrucciones.SentenciaIF import sentIF
from src.expresiones.CAritmeticas import Aritmeticas, Operadores
from src.expresiones.CNativo import Nativo
from src.instrucciones.CDeclaracion import Declaracion
from src.simbolo.CTipo import Tipo, tipoDato
from src.excepciones.CErrores import Errores
from src.instrucciones.CBreak import Break
lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ('left','MAS','MENOS'),
    ('left','MULT','DIVISION', 'MODULO'),
    ('right', 'POTENCIA'),
    ('right','UMENOS'),
    ('left', 'MENOR_IGUAL',
        "MAYOR_QUE",
        "MAYOR_IGUAL",
        "IGUAL_IGUAL",
        "DIFERENTE",
        "MENOR_QUE",
    ),  
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
       # aTab.ImprimirTabla()
    else:
        t[0] = [t[1]]

def p_instruccion(t):
    '''instruccion : declaracion PUNTOCOMA
            | expresion PUNTOCOMA
            | sent_IF
            | SBreak '''
    t[0] = t[1]

def p_SBreak(t):
    ''' SBreak : BREAK PUNTOCOMA'''
    t[0] = Break(0,0)

def p_sent_IF(t): 
    '''sent_IF : if_simple
            | if_else
            | if_elseif'''
    t[0] = t[1]

# if (expresion) { instrucciones }
def p_if_simple(t):
    '''if_simple : IF PAR1 expresion PAR2 LLAVE1 instrucciones LLAVE2'''
    t[0] = sentIF(t[3], t[6],0,0)

# if (expresion) { instrucciones } else { instrucciones }
def p_if_else(t):
    '''if_else : IF PAR1 expresion PAR2 LLAVE1 instrucciones LLAVE2 ELSE LLAVE1 instrucciones LLAVE2'''
    t[0] = sentIF(t[3], t[6], 0, 0, sentIF(None, t[10], 0,0))  # else sin condición

# if (expresion) { instrucciones } else if (expresion) { instrucciones }
def p_if_elseif(t):
    '''if_elseif : IF PAR1 expresion PAR2 LLAVE1 instrucciones LLAVE2 ELSE if_simple'''
    t[0] = sentIF(t[3], t[6],0, 0, t[9])

def p_declaracion_cvalor(t):
    'declaracion : tipos ID IGUAL expresion'
    t[0] = Declaracion(t[1], 0, 0, t[2], t[4])
    #aTab.agregarVariable(id=t[2], tipo=t[1], valor=t[4],linea=0,columna=0)

def p_declaracion_sinval(t):
    'declaracion : tipos ID '
    t[0] = Declaracion(t[1], 0, 0, t[2], None)
   # aTab.agregarVariable(id=t[2], tipo=t[1], valor=None,linea=0,columna=0)

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

def p_instruccion_print(t):
    "instruccion : PRINT PAR1 expresion PAR2 PUNTOCOMA"

    t[0] = Print(t[3], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


def p_instruccion_println(t):
    "instruccion : PRINTLN PAR1 expresion PAR2 PUNTOCOMA"
    t[0] = Println(t[3], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


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

def p_expresion_relacional(t):
    """expresion : expresion MENOR_IGUAL expresion
    | expresion MAYOR_QUE expresion
    | expresion MAYOR_IGUAL expresion
    | expresion MENOR_QUE expresion
    | expresion IGUAL_IGUAL expresion
    | expresion DIFERENTE expresion"""

    if t[2] == "<=":
        operador = OperadoresRel.MENOR_IGUAL
    elif t[2] == ">":
        operador = OperadoresRel.MAYOR_QUE
    elif t[2] == ">=":
        operador = OperadoresRel.MAYOR_IGUAL
    elif t[2] == "<":
        operador = OperadoresRel.MENOR_QUE
    elif t[2] == "==":
        operador = OperadoresRel.IGUAL_IGUAL
    elif t[2] == "!=":
        operador = OperadoresRel.DIFERENTE
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

def find_column(input, token):
    last_cr = input.rfind("\n", 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    return token.lexpos - last_cr

errores_sintacticos_globales = []

def p_error(t):
    global errores_sintacticos_globales
    if t:
        try:
            arbol = getattr(t.lexer, "arbol", None)
        except Exception:
            arbol = None
        error = Errores(
            "Sintáctico",
            f"Se encontró {t.type} ('{t.value}') y se esperaba una expresión o instrucción válida.",
            t.lineno,
            t.lexpos,
        )
        if arbol is not None:
            arbol.errores.append(error)
        else:
            errores_sintacticos_globales.append(error)
        print(error)
    else:
        try:
            lexer = parser.lexer  # type: ignore
            arbol = getattr(lexer, "arbol", None)
            lexdata = getattr(lexer, "lexdata", "")
            lexpos = getattr(lexer, "lexpos", len(lexdata))
            lineno = lexdata.count("\n", 0, lexpos) + 1
            last_cr = lexdata.rfind("\n", 0, lexpos)
            if last_cr < 0:
                last_cr = -1
            col = lexpos - last_cr
        except Exception:
            arbol = None
            lineno = 1
            col = 1

        error = Errores(
            "Sintáctico",
            "Error de sintaxis al final del archivo. Se esperaba una expresión o instrucción válida.",
            lineno,
            col,
        )
        if arbol is not None:
            arbol.errores.append(error)
            print("Error agregado a arbol.errores")  # <-- Depuración
        else:
            errores_sintacticos_globales.append(error)
        print(error)
    parser.restart()
    return []


## APLICACION ----------------------------------------------------------------------------
import ply.yacc as yacc


start = "inicio"

parser = yacc.yacc()


def parse_input(input_text, arbol):
    setattr(lexer, "arbol", arbol)
    result = parser.parse(input_text, lexer=lexer)
    if result is None:
        return []
    return result