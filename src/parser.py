# src/parser.py

import ply.yacc as yacc
from .lexer import tokens # Importa os tokens do lexer

# Definição da Estrutura da Árvore de Sintaxe Abstrata (AST)
class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf

    def __repr__(self):
        return f"Node(type='{self.type}', leaf={self.leaf}, children={len(self.children)})"

# Precedência de operadores (da menor para a maior)
precedence = (
    ('left', 'SOMA', 'SUBTRACAO'),
    ('left', 'MULTIPLICACAO', 'DIVISAO'),
    ('right', 'POTENCIA'),
)

# Gramática da Linguagem (Regras de Produção)

def p_programa(p):
    '''
    programa : sentencas
    '''
    p[0] = Node('Programa', [p[1]])

def p_sentencas(p):
    '''
    sentencas : sentenca sentencas
              | sentenca
    '''
    if len(p) == 3:
        p[0] = Node('Sentencas', [p[1]] + p[2].children)
    else:
        p[0] = Node('Sentencas', [p[1]])

def p_sentenca(p):
    '''
    sentenca : atribuicao
             | declaracao_funcao
    '''
    p[0] = p[1]

def p_atribuicao(p):
    '''
    atribuicao : ID IGUAL expressao
    '''
    p[0] = Node('Atribuicao', [Node('ID', leaf=p[1]), p[3]])

def p_declaracao_funcao(p):
    '''
    declaracao_funcao : FUNCAO ID ABRE_PARENTESES parametros_formais FECHA_PARENTESES IGUAL expressao
    '''
    p[0] = Node('DeclaracaoFuncao', [Node('ID', leaf=p[2]), p[4], p[7]])

def p_parametros_formais(p):
    '''
    parametros_formais : lista_ids
                       | empty
    '''
    p[0] = p[1]

def p_lista_ids(p):
    '''
    lista_ids : ID VIRGULA lista_ids
              | ID
    '''
    if len(p) == 4:
        p[0] = Node('ListaIDs', [Node('ID', leaf=p[1])] + p[3].children)
    else:
        p[0] = Node('ListaIDs', [Node('ID', leaf=p[1])])

def p_expressao_binaria(p):
    '''
    expressao : expressao SOMA expressao
              | expressao SUBTRACAO expressao
              | expressao MULTIPLICACAO expressao
              | expressao DIVISAO expressao
              | expressao POTENCIA expressao
    '''
    p[0] = Node('OperacaoBinaria', [p[1], p[3]], leaf=p[2])

def p_expressao_unaria(p):
    '''
    expressao : SUBTRACAO expressao %prec SOMA
    '''
    p[0] = Node('OperacaoUnaria', [p[2]], leaf=p[1])

def p_expressao_grupo(p):
    '''
    expressao : ABRE_PARENTESES expressao FECHA_PARENTESES
    '''
    p[0] = p[2]

def p_expressao_numero(p):
    '''
    expressao : NUM_INT
              | NUM_FLOAT
    '''
    p[0] = Node('Literal', leaf=p[1])

def p_expressao_id(p):
    '''
    expressao : ID
    '''
    p[0] = Node('ID', leaf=p[1])

def p_expressao_chamada_funcao(p):
    '''
    expressao : ID ABRE_PARENTESES argumentos FECHA_PARENTESES
    '''
    p[0] = Node('ChamadaFuncao', [Node('ID', leaf=p[1]), p[3]])

def p_argumentos(p):
    '''
    argumentos : lista_expressoes
               | empty
    '''
    p[0] = p[1]

def p_lista_expressoes(p):
    '''
    lista_expressoes : expressao VIRGULA lista_expressoes
                     | expressao
    '''
    if len(p) == 4:
        p[0] = Node('ListaExpressoes', [p[1]] + p[3].children)
    else:
        p[0] = Node('ListaExpressoes', [p[1]])

def p_empty(p):
    '''
    empty :
    '''
    p[0] = Node('Empty')

# Tratamento de erros sintáticos
def p_error(p):
    if p:
        print(f"Erro de sintaxe no token '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe no final do arquivo")

# Constrói o parser
parser = yacc.yacc()

if __name__ == '__main__':
    from .lexer import lexer
    data = """
    funcao f(x, y) = x^2 + y
    a = 10
    b = 3.14
    c = f(a, b) / 2
    """
    try:
        result = parser.parse(data, lexer=lexer)
        print("Análise Sintática Concluída com Sucesso. AST:")
        # Função auxiliar para imprimir a AST (apenas para debug)
        def print_ast(node, level=0):
            indent = "  " * level
            print(f"{indent}{node.type} (Leaf: {node.leaf})")
            for child in node.children:
                print_ast(child, level + 1)
        print_ast(result)
    except Exception as e:
        print(f"Erro durante a análise: {e}")
