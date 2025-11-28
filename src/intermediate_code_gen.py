# src/intermediate_code_gen.py

class IntermediateCodeGenerator:
    """Gera código intermediário (três endereços) a partir da AST."""
    def __init__(self):
        self.code = []
        self.temp_count = 0
        self.label_count = 0
        self.function_signatures = {} # Para armazenar as assinaturas das funções

    def new_temp(self):
        """Gera uma nova variável temporária."""
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        """Gera um novo rótulo."""
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, op, arg1, arg2, result):
        """Emite uma instrução de três endereços."""
        self.code.append((op, arg1, arg2, result))

    def generate(self, ast):
        """Inicia a geração de código a partir do nó raiz da AST."""
        print("--- Geração de Código Intermediário ---")
        self.code = []
        self.temp_count = 0
        self.label_count = 0
        self.function_signatures = {}
        self.visit(ast)
        print("Geração de Código Intermediário Concluída.")
        return self.code

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
        expr_temp = self.visit(node.children[1])
        self.emit('=', expr_temp, None, var_id)
        return var_id

    def visit_DeclaracaoFuncao(self, node):
        func_id = node.children[0].leaf
        params_node = node.children[1]
        expr_node = node.children[2]
        
        # 1. Define o rótulo de início da função
        start_label = f"FUNC_{func_id}"
        self.emit('LABEL', None, None, start_label)
        
        # 2. Processa os parâmetros
        params = []
        if params_node.type == 'ListaIDs':
            for param_id_node in params_node.children:
                params.append(param_id_node.leaf)
        
        self.function_signatures[func_id] = {'params': params}
        
        # 3. Gera código para o corpo da função
        return_temp = self.visit(expr_node)
        
        # 4. Emite a instrução de retorno
        self.emit('RETURN', return_temp, None, None)
        
        # 5. Emite o rótulo de fim da função (opcional, mas útil)
        self.emit('END_FUNC', None, None, func_id)

    def visit_OperacaoBinaria(self, node):
        left_temp = self.visit(node.children[0])
        right_temp = self.visit(node.children[1])
        op = node.leaf
        
        temp = self.new_temp()
        self.emit(op, left_temp, right_temp, temp)
        return temp

    def visit_OperacaoUnaria(self, node):
        expr_temp = self.visit(node.children[0])
        op = node.leaf # Deve ser '-'
        
        temp = self.new_temp()
        # Representa a negação como 0 - expr_temp
        self.emit('-', 0, expr_temp, temp)
        return temp

    def visit_Literal(self, node):
        # O literal é o próprio resultado
        return node.leaf

    def visit_ID(self, node):
        # O ID é o próprio resultado (variável)
        return node.leaf

    def visit_ChamadaFuncao(self, node):
        func_id = node.children[0].leaf
        args_node = node.children[1]
        
        # 1. Processa os argumentos
        args_temps = []
        if args_node.type == 'ListaExpressoes':
            for arg_node in args_node.children:
                args_temps.append(self.visit(arg_node))
        
        # 2. Emite instruções PARAM
        for arg_temp in args_temps:
            self.emit('PARAM', arg_temp, None, None)
            
        # 3. Emite a instrução CALL
        result_temp = self.new_temp()
        self.emit('CALL', func_id, len(args_temps), result_temp)
        
        return result_temp

    def visit_ListaIDs(self, node):
        # Não gera código, apenas retorna os IDs (não usado aqui, mas pode ser útil)
        return [child.leaf for child in node.children]
        
    def visit_ListaExpressoes(self, node):
        # Não gera código, a chamada de função lida com isso
        pass

    def visit_Empty(self, node):
        # Não gera código
        pass

# Exemplo de uso (para testes internos)
if __name__ == '__main__':
    
    print("Módulo de Geração de Código Intermediário pronto para integração.")
