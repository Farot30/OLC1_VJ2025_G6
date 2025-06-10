tokens = (
    
    'SWITCH', 'CASE', 'DEFAULT', 'BREAK', 'DOSPT', 'LLAVEIZQ', 'LLAVEDE'
)

t_SWITCH     = r'switch'
t_CASE       = r'case'
t_DEFAULT    = r'default'
t_BREAK      = r'break'
t_DOSPT      = r':'
t_LLAVEIZQ   = r'\{'
t_LLAVEDE    = r'\}'


reservadas = {
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
}

from src.instrucciones.CSwitch import Switch, Case 

def p_instruccion_switch(t):
    "instruccion : SWITCH PAR1 expresion PAR2 LLAVE1 lista_casos LLAVE2"
    casos = []
    defecto = []
    for c in t[6]:
        if isinstance(c, Case):
            casos.append(c)
        elif isinstance(c, tuple) and c[0] == 'default':
            defecto = c[1]
    t[0] = Switch(t[3], casos, defecto, t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))

def p_lista_casos(t):
    '''lista_casos : lista_casos caso
                   | caso'''
    t[0] = t[1] + [t[2]] if len(t) == 3 else [t[1]]

def p_caso_case(t):
    "caso : CASE expresion DOSPT instrucciones BREAK PUNTOCOMA"
    from src.instrucciones.CBreak import Break
    t[0] = Case(t[2], t[4] + [Break(t.lineno(5), find_column(t.lexer.lexdata, t.slice[5]))])

def p_caso_default(t):
    "caso : DEFAULT DOSPT instrucciones BREAK PUNTOCOMA"
    from src.instrucciones.CBreak import Break
    t[0] = ('default', t[3] + [Break(t.lineno(4), find_column(t.lexer.lexdata, t.slice[4]))])

