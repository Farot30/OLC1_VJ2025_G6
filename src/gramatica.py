# 1. IMPORTS
import re
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
from src.instrucciones.CFor import For
from src.instrucciones.SetenciaIF import sentIF
from src.instrucciones.CBreak import Break
from src.instrucciones.CWhile import While
from src.instrucciones.CDoWhile import DoWhile
from src.instrucciones.CSwitch import Switch, Case
from src.instrucciones.CContinue import Continue

# 2. TOKENS Y RESERVADAS
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
    "SWITCH",
    "CASE",
    "DEFAULT",
    "DOSPT",
    "CONTINUE",
]

reservadas = {
    "int": "INT",
    "float": "DOUBLE",
    "str": "STRING",
    "bool": "BOOL",
    "char": "CHAR",
    "true": "TRUE",
    "false": "FALSE",
    "for": "FOR",
    "if": "IF",
    "break": "BREAK",
    "do": "DO",
    "while": "WHILE",
    "else": "ELSE",
    "switch": "SWITCH",
    "case": "CASE",
    "default": "DEFAULT",
    "continue": "CONTINUE",
    "println": "PRINTLN",
}

# 3. EXPRESIONES REGULARES DE TOKENS
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
t_DOSPT = r":"
t_ignore = " \t\r\f"


# 4. FUNCIONES DE TOKENS ESPECIALES
def t_COMMENT_SINGLELINE(t):
    r"//.*"
    pass


def t_NEWLINE(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


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
    t_lower = t.value.lower()
    t.type = reservadas.get(t_lower, "ID")
    t.value = t_lower if t.type != "ID" else t.value
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


def t_error(t):
    error = Errores(
        "Léxico",
        f"El carácter '{t.value[0]}' no pertenece al lenguaje",
        t.lineno,
        t.lexpos,
    )
    arbol = getattr(t.lexer, "arbol", None)
    if arbol:
        arbol.errores.append(error)
    print(error)
    t.lexer.skip(1)


# 5. CONSTRUCCIÓN DEL LEXER
import ply.lex as lex

lexer = lex.lex()

# 6. PRECEDENCIA
precedence = (
    ("left", "OR"),
    ("left", "AND"),
    ("left", "XOR"),
    ("right", "NOT"),
    (
        "left",
        "MENOR_IGUAL",
        "MAYOR_QUE",
        "MAYOR_IGUAL",
        "IGUAL_IGUAL",
        "DIFERENTE",
        "MENOR_QUE",
    ),
    ("left", "MAS", "MENOS"),
    ("left", "MULT", "DIVISION", "MODULO"),
    ("right", "POTENCIA"),
    ("right", "UMENOS"),
)


# 7. REGLAS DE GRAMÁTICA (SINTAXIS)
def p_inicio(t):
    "inicio : instrucciones"
    t[0] = t[1]


def p_instrucciones(t):
    """instrucciones : instrucciones instruccion
    | instruccion"""
    if len(t) == 2:
        t[0] = [t[1]] if t[1] is not None else []
    else:
        t[0] = t[1] + ([t[2]] if t[2] is not None else [])


def p_instrucciones_vacia(t):
    "instrucciones : empty"
    t[0] = []


def p_instruccion_vacia(t):
    "instruccion : PUNTOCOMA"
    t[0] = None


# --- Instrucción principal ---
def p_instruccion(t):
    """instruccion : declaracion PUNTOCOMA
    | asignacion PUNTOCOMA
    | incremento PUNTOCOMA
    | decremento PUNTOCOMA
    | sent_if
    | sent_while
    | sent_do_while
    | sent_for
    | sent_switch
    | sent_break PUNTOCOMA
    | sent_continue PUNTOCOMA
    | sent_println PUNTOCOMA
    | bloque"""
    if len(t) == 2:
        if t[1] == ";":
            t[0] = None  # Instrucción vacía
        else:
            t[0] = t[1]
    else:
        t[0] = t[1]


# --- Declaraciones ---
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


# --- Asignación ---
def p_asignacion(t):
    "asignacion : ID IGUAL expresion"
    t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


# --- Incremento y decremento ---
def p_incremento(t):
    "incremento : ID INCREMENTO"
    t[0] = Incremento(t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


def p_decremento(t):
    "decremento : ID DECREMENTO"
    t[0] = Decremento(t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


# --- Bloque ---
def p_bloque(t):
    "bloque : LLAVE1 instrucciones LLAVE2"
    t[0] = t[2]


# --- IF ---


# 2. Mantén la función p_sent_if, pero ajusta las reglas para manejar IF en mayúsculas
def p_sent_if(t):
    """sent_if : if_simple
    | if_else
    | if_elseif"""
    t[0] = t[1]


# 3. Modifica la regla if_simple para usar IF en mayúsculas
def p_if_simple(t):
    """if_simple : IF PAR1 expresion PAR2 LLAVE1 instrucciones LLAVE2"""
    t[0] = sentIF(t[3], t[6], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


# 4. Modifica la regla if_else para usar IF y ELSE en mayúsculas
def p_if_else(t):
    """if_else : IF PAR1 expresion PAR2 LLAVE1 instrucciones LLAVE2 ELSE LLAVE1 instrucciones LLAVE2"""
    t[0] = sentIF(
        t[3],
        t[6],
        t.lineno(1),
        find_column(t.lexer.lexdata, t.slice[1]),
        sentIF(None, t[10], t.lineno(8), find_column(t.lexer.lexdata, t.slice[8])),
    )


# 5. Añadir una nueva regla específica para ELSE IF (como se usa en tu código)
def p_if_elseif(t):
    """if_elseif : IF PAR1 expresion PAR2 LLAVE1 instrucciones LLAVE2 ELSE IF PAR1 expresion PAR2 LLAVE1 instrucciones LLAVE2"""
    # Esta implementación maneja explícitamente la secuencia "ELSE IF"
    t[0] = sentIF(
        t[3],  # Condición del IF
        t[6],  # Cuerpo del IF
        t.lineno(1),
        find_column(t.lexer.lexdata, t.slice[1]),
        sentIF(
            t[11],  # Condición del ELSE IF
            t[14],  # Cuerpo del ELSE IF
            t.lineno(9),
            find_column(t.lexer.lexdata, t.slice[9]),
        ),
    )


# 6. Añadir una regla para IF-ELSE IF-ELSE completo
def p_if_elseif_else(t):
    """if_elseif : IF PAR1 expresion PAR2 LLAVE1 instrucciones LLAVE2 ELSE IF PAR1 expresion PAR2 LLAVE1 instrucciones LLAVE2 ELSE LLAVE1 instrucciones LLAVE2"""
    # Maneja: IF (...) {...} ELSE IF (...) {...} ELSE {...}
    elseif_node = sentIF(
        t[11],  # Condición del ELSE IF
        t[14],  # Cuerpo del ELSE IF
        t.lineno(9),
        find_column(t.lexer.lexdata, t.slice[9]),
    )

    else_node = sentIF(
        None,  # No hay condición en ELSE
        t[18],  # Cuerpo del ELSE
        t.lineno(16),
        find_column(t.lexer.lexdata, t.slice[16]),
    )

    # Conectar el ELSE al ELSE IF
    elseif_node.else_st = else_node

    # Crear el nodo principal IF con su rama ELSE IF+ELSE
    t[0] = sentIF(
        t[3],  # Condición del IF
        t[6],  # Cuerpo del IF
        t.lineno(1),
        find_column(t.lexer.lexdata, t.slice[1]),
        elseif_node,
    )


# --- WHILE ---
def p_sent_while(t):
    "sent_while : WHILE PAR1 expresion PAR2 bloque"
    t[0] = While(t[3], t[5], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


# --- DO-WHILE ---
def p_sent_do_while(t):
    "sent_do_while : DO bloque WHILE PAR1 expresion PAR2 PUNTOCOMA"
    t[0] = DoWhile(t[2], t[5], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


# --- FOR ---
def p_sent_for(t):
    "sent_for : FOR PAR1 for_init PUNTOCOMA expresion PUNTOCOMA for_update PAR2 bloque"
    t[0] = For(
        t[3],
        t[5],
        t[7],
        t[9],
        t.lineno(1),
        find_column(t.lexer.lexdata, t.slice[1]),
    )


def p_for_init(t):
    """for_init : declaracion
    | asignacion
    | incremento
    | decremento
    | empty"""
    t[0] = t[1]


def p_for_update(t):
    """for_update : asignacion
    | incremento
    | decremento
    | empty"""
    t[0] = t[1]


# --- SWITCH ---
def p_sent_switch(t):
    "sent_switch : SWITCH PAR1 expresion PAR2 LLAVE1 lista_casos LLAVE2"
    casos = []
    defecto = []
    for c in t[6]:
        if isinstance(c, Case):
            casos.append(c)
        elif isinstance(c, tuple) and c[0] == "default":
            defecto = c[1]
    t[0] = Switch(
        t[3], casos, defecto, t.lineno(1), find_column(t.lexer.lexdata, t.slice[1])
    )


def p_lista_casos(t):
    """lista_casos : lista_casos caso
    | caso"""
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[2]]


def p_caso_case(t):
    "caso : CASE expresion DOSPT instrucciones"
    t[0] = Case(t[2], t[4])


def p_caso_default(t):
    "caso : DEFAULT DOSPT instrucciones"
    t[0] = ("default", t[3])


# --- BREAK ---
def p_sent_break(t):
    "sent_break : BREAK"
    t[0] = Break(t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


# --- CONTINUE ---
def p_sent_continue(t):
    "sent_continue : CONTINUE"
    t[0] = Continue(t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


# --- PRINTLN ---
def p_sent_println(t):
    "sent_println : PRINTLN PAR1 expresion PAR2"
    t[0] = Println(t[3], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


# --- Expresiones ---
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
        operador, t.lineno(2), find_column(t.lexer.lexdata, t.slice[2]), t[1], t[3]
    )


def p_expresion_unaria(t):
    "expresion : MENOS expresion %prec UMENOS"
    t[0] = Unario("-", t[2], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))


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


def p_expresion_booleano(t):
    "expresion : BOOLEANO"
    t[0] = Nativo(
        Tipo(tipoDato.BOOL), t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1])
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


def p_expresion_id(t):
    "expresion : ID"
    nodo = Nativo(
        Tipo(None), t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1])
    )
    nodo.es_identificador = True
    t[0] = nodo


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
        operador, t.lineno(2), find_column(t.lexer.lexdata, t.slice[2]), t[1], t[3]
    )


# --- TIPOS ---
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


# --- VACÍO ---
def p_empty(t):
    "empty :"
    t[0] = None


# --- ERRORES ---
errores_sintacticos_globales = []


def p_error(t):
    global errores_sintacticos_globales
    if t:
        try:
            arbol = getattr(t.lexer, "arbol", None)
        except Exception:
            arbol = None

        # Mensaje de error para el token encontrado
        error = Errores(
            "Sintáctico",
            f"Se encontró {t.type} ('{t.value}') y se esperaba una expresión o instrucción válida.",
            t.lineno,
            find_column(t.lexer.lexdata, t) if hasattr(t.lexer, "lexdata") else 1,
        )

        if arbol is not None:
            arbol.errores.append(error)
        else:
            errores_sintacticos_globales.append(error)

        print(error)

        # Recuperación de errores más inteligente
        # Intentamos sincronizar con el siguiente punto y coma, llave o final de bloque
        next_token = t
        while True:
            next_token = parser.token()  # Obtener siguiente token
            if not next_token or next_token.type in ["PUNTOCOMA", "LLAVE1", "LLAVE2"]:
                break

        # Indícale al parser que ya manejaste el error
        parser.errok()

        # Si encontramos un punto y coma, regresamos ese token para continuar
        if next_token and next_token.type == "PUNTOCOMA":
            return next_token
    else:
        # EOF
        try:
            lexer_obj = parser.lexer
            arbol = getattr(lexer_obj, "arbol", None)
            lexdata = getattr(lexer_obj, "lexdata", "")
            lexpos = getattr(lexer_obj, "lexpos", len(lexdata))
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
        else:
            errores_sintacticos_globales.append(error)
        print(error)


# Añade esta nueva regla para capturar identificadores sueltos como instrucciones inválidas
def p_instruccion_invalida(t):
    "instruccion : ID"
    # Un ID suelto como instrucción es un error
    error = Errores(
        "Sintáctico",
        f"La palabra '{t[1]}' no es una instrucción válida",
        t.lineno(1),
        find_column(t.lexer.lexdata, t.slice[1]),
    )

    # Registra el error
    arbol = getattr(t.lexer, "arbol", None)
    if arbol:
        arbol.errores.append(error)
    else:
        errores_sintacticos_globales.append(error)

    print(
        f"----- Error Sintáctico: La palabra '{t[1]}' no es una instrucción válida. en la linea {t.lineno(1)} y columna {find_column(t.lexer.lexdata, t.slice[1])} ----"
    )

    # Devolvemos None para que no se agregue al AST
    t[0] = None


# --- FUNCIONES AUXILIARES ---
def find_column(input, token):
    last_cr = input.rfind("\n", 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    return token.lexpos - last_cr


# 8. PARSER Y FUNCIÓN DE ENTRADA
import ply.yacc as yacc

start = "inicio"
parser = yacc.yacc(debug=True)


def parse_input(input_text, arbol):
    setattr(lexer, "arbol", arbol)
    lexer.lineno = 1
    result = parser.parse(input_text, lexer=lexer)
    if result is None:
        return []
    # Filtra instrucciones válidas
    return [instr for instr in result if instr is not None]
