from src.expresiones.CAritmeticas import Aritmeticas, Operadores
from src.expresiones.CNativo import Nativo
from src.instrucciones.CDeclaracion import Declaracion
from src.simbolo.CTipo import Tipo, tipoDato
from src.instrucciones.CAsignacion import Asignacion
from src.instrucciones.CIncremento import Incremento, Decremento
from src.expresiones.CUnitario import Unario
from src.expresiones.CRelacionales import Relacional, OperadoresRel
from src.instrucciones.CPrintln import Println
from src.expresiones.COr import Or
from src.expresiones.CAnd import And
from src.expresiones.CXor import Xor
from src.expresiones.CNot import Not
from src.excepciones.CErrores import Errores
from src.expresiones.CFor import For
from src.instrucciones.SetenciaIF import sentIF
from src.instrucciones.CBreak import Break
from src.instrucciones.CWhile import While
from src.instrucciones.CDoWhile import DoWhile


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
    "IF",
    "ELSE",
    "INCREMENTO",
    "DECREMENTO",
    "BOOLEANO",
    "MENOR_IGUAL",
    "MAYOR_QUE",
    "MAYOR_IGUAL",
    "MENOR_QUE",
    "IGUAL_IGUAL",
    "DIFERENTE",
    "PRINTLN",
    "OR",
    "AND",
    "XOR",
    "NOT",
    "FOR",
    "LLAVE1",
    "LLAVE2",
    "BREAK",
    "DO",
    "WHILE",
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
t_MENOR_QUE = r"<"
t_IGUAL_IGUAL = r"=="
t_DIFERENTE = r"!="
t_OR = r"\|\|"
t_AND = r"&&"
t_XOR = r"\^"
t_NOT = r"!"
t_LLAVE1 = r"\{"
t_LLAVE2 = r"\}"

reservadas = {
    "int": "INT",
    "float": "DOUBLE",
    "str": "STRING",
    "bool": "BOOL",
    "char": "CHAR",
    "true": "TRUE",
    "false": "FALSE",
    "println": "PRINTLN",
    "for": "FOR",
    "if": "IF",
    "break": "BREAK",
    "do": "DO",
    "while": "WHILE",
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


def t_CADENA(t):
    r'"([^"\\\n]|(\\.))*"'
    t.value = bytes(t.value[1:-1], "utf-8").decode("unicode_escape")
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


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# En t_error (léxico)
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

lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ("right", "UMENOS"),  # - unario
    ("right", "POTENCIA"),  # **
    ("left", "MULT", "DIVISION", "MODULO"),
    ("left", "MAS", "MENOS"),
    (
        "left",
        "MENOR_IGUAL",
        "MAYOR_QUE",
        "MAYOR_IGUAL",
        "IGUAL_IGUAL",
        "DIFERENTE",
        "MENOR_QUE",
    ),  # relacionales
    ("right", "NOT"),  # !
    ("left", "XOR"),  # ^
    ("left", "AND"),  # &&
    ("left", "OR"),  # ||
)

#### DEFINICION DE GRAMATICA (ANALISIS SINTACTICO) ----------------------------------------------------------------------------


def p_inicio(t):
    "inicio : instrucciones"
    t[0] = t[1]


def p_for(t):
    """instruccion : FOR PAR1 for_init PUNTOCOMA expresion PUNTOCOMA for_update PAR2 LLAVE1 instrucciones LLAVE2"""
    t[0] = For(
        t[3],  # inicialización (puede ser asignación o incremento)
        t[5],  # condición (expresión booleana)
        t[7],  # actualización (puede ser asignación o incremento)
        t[10],  # instrucciones dentro del for
        t.lineno(1),
        find_column(t.lexer.lexdata, t.slice[1]),
    )


def p_for_init(t):
    """for_init : ID IGUAL expresion
    | ID INCREMENTO
    | ID DECREMENTO
    | declaracion"""
    if len(t) == 4:
        t[0] = Asignacion(
            t[1], t[3], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1])
        )
    elif len(t) == 2 and isinstance(t[1], Declaracion):
        t[0] = t[1]
    elif t[2] == "++":
        t[0] = Incremento(t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))
    elif t[2] == "--":
        t[0] = Decremento(t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


def p_for_update(t):
    """for_update : ID IGUAL expresion
    | ID INCREMENTO
    | ID DECREMENTO"""
    if len(t) == 4:
        t[0] = Asignacion(
            t[1], t[3], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1])
        )
    elif t[2] == "++":
        t[0] = Incremento(t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))
    elif t[2] == "--":
        t[0] = Decremento(t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


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
    nodo = Nativo(
        Tipo(None), t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1])
    )
    nodo.es_identificador = True
    t[0] = nodo


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
    | expresion PUNTOCOMA
    | sent_IF
    | SBreak"""
    t[0] = t[1]


def p_SBreak(t):
    """SBreak : BREAK PUNTOCOMA"""
    t[0] = Break(0, 0)


def p_sent_IF(t):
    """sent_IF : if_simple
    | if_else
    | if_elseif"""
    t[0] = t[1]


# if (expresion) { instrucciones }
def p_if_simple(t):
    """if_simple : IF PAR1 expresion PAR2 LLAVE1 instrucciones LLAVE2"""
    t[0] = sentIF(t[3], t[6], 0, 0)


# if (expresion) { instrucciones } else { instrucciones }
def p_if_else(t):
    """if_else : IF PAR1 expresion PAR2 LLAVE1 instrucciones LLAVE2 ELSE LLAVE1 instrucciones LLAVE2"""
    t[0] = sentIF(t[3], t[6], 0, 0, sentIF(None, t[10], 0, 0))  # else sin condición


# if (expresion) { instrucciones } else if (expresion) { instrucciones }
def p_if_elseif(t):
    """if_elseif : IF PAR1 expresion PAR2 LLAVE1 instrucciones LLAVE2 ELSE if_simple"""
    t[0] = sentIF(t[3], t[6], 0, 0, t[9])


def p_instruccion_while(t):
    "instruccion : WHILE PAR1 expresion PAR2 LLAVE1 instrucciones LLAVE2"
    t[0] = While(
        t[3],  # condición
        t[6],  # lista de instrucciones
        t.lineno(1),
        find_column(t.lexer.lexdata, t.slice[1]),
    )


def p_instruccion_dowhile(t):
    "instruccion : DO LLAVE1 instrucciones LLAVE2 WHILE PAR1 expresion PAR2 PUNTOCOMA"
    t[0] = DoWhile(
        t[3],  # lista de instrucciones
        t[7],  # condición
        t.lineno(1),
        find_column(t.lexer.lexdata, t.slice[1]),
    )


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


def p_instruccion_error(t):
    "instruccion : error PUNTOCOMA"
    # No ejecuta nada, pero evita que el parser se detenga
    t[0] = None


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
