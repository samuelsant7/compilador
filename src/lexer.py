# src/lexer.py

import ply.lex as lex

# Lista de palavras reservadas
reserved = {
    'funcao': 'FUNCAO',
}

# Lista de tokens
tokens = [
    'ID',
    'NUM_INT',
    'NUM_FLOAT',
    'ATRIBUICAO',
    'SOMA',
    'SUBTRACAO',
    'MULTIPLICACAO',
    'DIVISAO',
    'POTENCIA',
    'ABRE_PARENTESES',
    'FECHA_PARENTESES',
    'VIRGULA',
    'IGUAL',
] + list(reserved.values())

# Expressões regulares para tokens simples
t_SOMA = r'\+'
t_SUBTRACAO = r'-'
t_MULTIPLICACAO = r'\*'
t_DIVISAO = r'/'
t_POTENCIA = r'\^'
t_ABRE_PARENTESES = r'\('
t_FECHA_PARENTESES = r'\)'
t_VIRGULA = r','
t_IGUAL = r'='
t_ATRIBUICAO = r'=' # Reutilizando para atribuição, a gramática definirá o contexto

# Expressão regular para identificadores e palavras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica se é palavra reservada
    return t

# Expressão regular para números de ponto flutuante
def t_NUM_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Expressão regular para números inteiros
def t_NUM_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Caracteres ignorados (espaços e tabulações)
t_ignore = ' \t'

# Tratamento de quebras de linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()

if __name__ == '__main__':
    data = """
    funcao f(x, y) = x^2 + y
    a = 10
    b = 3.14
    c = f(a, b) / 2
    """
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
