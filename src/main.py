# src/main.py

import sys
import os

# Adiciona o diretório src ao path para resolver imports relativos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer import lexer
from src.parser import parser, Node
from src.semantic_analyzer import SemanticAnalyzer
from src.intermediate_code_gen import IntermediateCodeGenerator

def print_ast(node, level=0):
    """Função auxiliar para imprimir a AST (apenas para debug)"""
    indent = "  " * level
    leaf_val = f"'{node.leaf}'" if isinstance(node.leaf, (int, float, str)) else str(node.leaf)
    print(f"{indent}{node.type} (Leaf: {leaf_val})")
    for child in node.children:
        print_ast(child, level + 1)

def compile_code(code):
    """Função principal para compilar o código."""
    print("--- Análise Léxica e Sintática ---")
    try:
        # 1. Análise Léxica e Sintática
        ast = parser.parse(code, lexer=lexer)
        if not ast:
            print("Análise Sintática Falhou.")
            return None
        
        print("Análise Sintática Concluída com Sucesso. AST Gerada.")
        # print_ast(ast) # Descomentar para ver a AST
        
        # 2. Análise Semântica
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(ast)
        
        # 3. Geração de Código Intermediário
        code_generator = IntermediateCodeGenerator()
        intermediate_code = code_generator.generate(ast)
        
        print("\n--- Código Intermediário Gerado ---")
        for instruction in intermediate_code:
            print(f"({instruction[0]}, {instruction[1]}, {instruction[2]}, {instruction[3]})")
            
        return intermediate_code
        
    except Exception as e:
        print(f"Erro durante a análise: {e}")
        return None
    """Função principal para compilar o código."""
    print("--- Análise Léxica e Sintática ---")
    try:
        # O parser.parse chama o lexer internamente
        ast = parser.parse(code, lexer=lexer)
        if ast:
            print("Análise Sintática Concluída com Sucesso. AST Gerada.")
            print_ast(ast)
            return ast
        else:
            print("Análise Sintática Falhou.")
            return None
    except Exception as e:
        print(f"Erro durante a análise: {e}")
        return None

def run_tests(file_path, expected_to_fail=False):
    print(f"\n--- Executando Teste: {file_path} (Esperado Falha: {expected_to_fail}) ---")
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        
        # Remove linhas de comentário e vazias para não confundir o lexer/parser
        lines = [line for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]
        code_clean = '\n'.join(lines)
        
        result = compile_code(code_clean)
        
        if expected_to_fail and result is not None:
            print("ERRO: O teste deveria falhar, mas a compilação foi bem-sucedida.")
        elif not expected_to_fail and result is None:
            print("ERRO: O teste deveria ser bem-sucedido, mas a compilação falhou.")
        elif not expected_to_fail and result is not None:
            print("SUCESSO: Compilação bem-sucedida.")
        elif expected_to_fail and result is None:
            print("SUCESSO: Compilação falhou como esperado.")
            
    except FileNotFoundError:
        print(f"Erro: Arquivo de teste não encontrado em {file_path}")
    except Exception as e:
        print(f"Erro inesperado durante a execução do teste: {e}")


def main_menu():
    import sys
    
    while True:
        print("\n" + "="*30)
        print(" MINI COMPILADOR - MENU ")
        print("="*30)
        print("1: Rodar Testes Automáticos (validos e invalidos)")
        print("2: Testar Código Manualmente (Interativo)")
        print("3: Sair")
        print("="*30)
        
        try:
            escolha = input("Escolha o modo (1, 2 ou 3): ").strip()
        except EOFError:
            print("\nEntrada cancelada. Saindo.")
            break
        except KeyboardInterrupt:
            print("\nOperação cancelada. Saindo.")
            break

        if escolha == '1':
            # Modo 1: Rodar Testes Automáticos
            run_tests('tests/test_valid.txt', expected_to_fail=False)
            run_tests('tests/test_invalid.txt', expected_to_fail=True)
            
        elif escolha == '2':
            # Modo 2: Teste Manual Interativo
            print("\n--- Modo de Teste Interativo ---")
            print("Digite seu código (tecle Enter e depois Ctrl+D ou Ctrl+Z+Enter para finalizar):")
            
            try:
                # Lê todas as linhas digitadas pelo usuário até o EOF
                codigo_interativo = sys.stdin.read()
            except EOFError:
                print("\nEntrada cancelada. Voltando ao menu.")
                continue
            except KeyboardInterrupt:
                print("\nOperação cancelada. Voltando ao menu.")
                continue
                
            if codigo_interativo.strip():
                compile_code(codigo_interativo)
            else:
                print("Nenhum código fornecido.")
                
        elif escolha == '3':
            print("Saindo do Mini Compilador. Até logo!")
            break
            
        else:
            print("Escolha inválida. Por favor, digite 1, 2 ou 3.")

if __name__ == '__main__':
    main_menu()

