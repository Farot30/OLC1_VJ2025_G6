import ply.lex as lex

tokens = (
    'ID',
    'COMENTARIO_MULTILINEA',
)

t_ignore = ' \t'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    return t 


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()

# Probando el lexer con un comentario multilinea
data = '''/* Probando comentario */12312
'''

lexer.input(data)

print("Tokens encontrados:")
for tok in lexer:
    print(f"Tipo: {tok.type}, Valor: {tok.value}")
