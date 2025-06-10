tokens = [
    ...
    "CONTINUE",
    ...
]

reservadas = {
    ...
    "continue": "CONTINUE",
}

from src.instrucciones.CContinue import Continue  

def p_SContinue(t):
    """instruccion : CONTINUE PUNTOCOMA"""
    t[0] = Continue(t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))
