# src/semantic_analyzer.py

from collections import OrderedDict

class SymbolTable:
    """Tabela de Símbolos para gerenciar escopo."""
    def __init__(self, parent=None):
        self.symbols = OrderedDict()
        self.parent = parent

    def insert(self, name, type, details=None):
        """Insere um novo símbolo no escopo atual."""
        if name in self.symbols:
            raise Exception(f"Erro Semântico: Símbolo '{name}' já declarado neste escopo.")
        self.symbols[name] = {'type': type, 'details': details if details is not None else {}}

    def lookup(self, name):
        """Procura um símbolo, começando pelo escopo atual e subindo para os pais."""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

class SemanticAnalyzer:
    """Analisador Semântico que percorre a AST para verificação de tipos e escopo."""
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope

    def analyze(self, ast):
        """Inicia a análise semântica a partir do nó raiz da AST."""
        print("--- Análise Semântica ---")
        self.visit(ast)
        print("Análise Semântica Concluída com Sucesso.")

    def visit(self, node):
        """Método genérico de visita."""
        method_name = 'visit_' + node.type
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Visita todos os filhos de um nó."""
        for child in node.children:
            self.visit(child)

    def visit_Programa(self, node):
        self.visit(node.children[0]) # Visita Sentencas

    def visit_Sentencas(self, node):
        self.generic_visit(node)

    def visit_Atribuicao(self, node):
        var_id = node.children[0].leaf
        expr_type = self.visit(node.children[1])

        # Simplesmente insere ou atualiza a variável no escopo global (escopo simples)
        if self.global_scope.lookup(var_id) is None:
            self.global_scope.insert(var_id, 'NUMERICO')
        
        # A verificação de tipo é simplificada para 'NUMERICO'
        if expr_type != 'NUMERICO':
            raise Exception(f"Erro Semântico: Atribuição de tipo incompatível para '{var_id}'. Esperado NUMERICO, encontrado {expr_type}.")
        
        return 'NUMERICO'

    def visit_DeclaracaoFuncao(self, node):
        func_id = node.children[0].leaf
        params_node = node.children[1]
        expr_node = node.children[2]

        # 1. Insere a função no escopo global
        if self.global_scope.lookup(func_id):
            raise Exception(f"Erro Semântico: Função '{func_id}' já declarada.")
        
        # Cria um novo escopo para os parâmetros da função
        function_scope = SymbolTable(parent=self.global_scope)
        self.current_scope = function_scope
        
        param_count = 0
        if params_node.type == 'ListaIDs':
            for param_id_node in params_node.children:
                param_name = param_id_node.leaf
                function_scope.insert(param_name, 'NUMERICO', {'kind': 'param'})
                param_count += 1
        
        self.global_scope.insert(func_id, 'FUNCAO', {'params': param_count, 'scope': function_scope})

        # 2. Analisa o corpo da função (expressão)
        expr_type = self.visit(expr_node)
        
        if expr_type != 'NUMERICO':
            raise Exception(f"Erro Semântico: Função '{func_id}' deve retornar um tipo NUMERICO.")

        # Retorna ao escopo anterior
        self.current_scope = self.global_scope

    def visit_OperacaoBinaria(self, node):
        left_type = self.visit(node.children[0])
        right_type = self.visit(node.children[1])

        if left_type != 'NUMERICO' or right_type != 'NUMERICO':
            raise Exception(f"Erro Semântico: Operação binária com tipos incompatíveis: {left_type} {node.leaf} {right_type}")
        
        return 'NUMERICO'

    def visit_OperacaoUnaria(self, node):
        expr_type = self.visit(node.children[0])
        if expr_type != 'NUMERICO':
            raise Exception(f"Erro Semântico: Operação unária com tipo incompatível: {expr_type}")
        return 'NUMERICO'

    def visit_Literal(self, node):
        # Simplificando: todos os literais são numéricos (int ou float)
        return 'NUMERICO'

    def visit_ID(self, node):
        symbol = self.current_scope.lookup(node.leaf)
        if symbol is None:
            raise Exception(f"Erro Semântico: Identificador '{node.leaf}' não declarado.")
        
        if symbol['type'] == 'FUNCAO':
            raise Exception(f"Erro Semântico: Uso de função '{node.leaf}' como variável.")
            
        return symbol['type']

    def visit_ChamadaFuncao(self, node):
        func_id = node.children[0].leaf
        args_node = node.children[1]
        
        symbol = self.global_scope.lookup(func_id)
        if symbol is None or symbol['type'] != 'FUNCAO':
            raise Exception(f"Erro Semântico: Função '{func_id}' não declarada.")
        
        expected_params = symbol['details']['params']
        
        actual_args = []
        if args_node.type == 'ListaExpressoes':
            actual_args = args_node.children
        
        actual_params = len(actual_args)
        
        if actual_params != expected_params:
            raise Exception(f"Erro Semântico: Chamada de função '{func_id}' com número incorreto de argumentos. Esperado {expected_params}, encontrado {actual_params}.")
            
        # Verifica o tipo de cada argumento
        for arg_node in actual_args:
            arg_type = self.visit(arg_node)
            if arg_type != 'NUMERICO':
                raise Exception(f"Erro Semântico: Argumento de função deve ser NUMERICO, encontrado {arg_type}.")
                
        return 'NUMERICO' # Funções retornam NUMERICO

    def visit_ListaIDs(self, node):
        # Usado apenas na declaração de função, não precisa de verificação de tipo aqui
        pass
        
    def visit_ListaExpressoes(self, node):
        # Usado apenas na chamada de função, a verificação é feita em visit_ChamadaFuncao
        pass

    def visit_Empty(self, node):
        pass

# Exemplo de uso (para testes internos)
if __name__ == '__main__':
    # Este módulo não deve ser executado diretamente, mas sim integrado ao main.py
    print("Módulo de Análise Semântica pronto para integração.")
