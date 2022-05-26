import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'id',
    'assign',
    'number',
    'semicolon',
    'LESSTHAN',
    'EQUAL',
    'GREATERTHAN'
    'PROHIBITED',
    'PROHIBITED2',
)
t_number = r'[0-9]+'
t_PROHIBITED2 = r'[0-9]+[a-zA-Z_]+'
t_assign = r'\:\='
t_semicolon = r'\;'
t_LESSTHAN = r'\<'
t_EQUAL = r'\='
t_GREATERTHAN = r'\>'
t_PROHIBITED = r'[\!\@\$\%\^\&\*\(\)\,\.\'\"\{\}]'
# t_PROHIBITED2 = r'[\d+[a-zA-Z_][a-zA-Z_0-9]*]'
reserved = {
    'repeat': 'repeat',
    'until': 'until'
}

tokens = ['id', 'assign', 'number', 'semicolon', 'LESSTHAN', 'EQUAL', 'GREATERTHAN', 'PROHIBITED','PROHIBITED2' ] + list(reserved.values())

def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'id')
    return t


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



# data = input("Sentence: ")

def tok(data):
    lexer = lex.lex()
    lexer.input(data)
    # Tokenize
    list_tok = []  # this is list of the saved tokens
    list_tok_DFA = "" #this is for dfa
    counter = 1
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        list_tok.append((counter,tok.type,tok.value))
        list_tok_DFA += (tok.type[0])
        print(tok)
        counter +=1
    return list_tok , list_tok_DFA
#new change

