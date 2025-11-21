# Projeto de Mini Compilador para Linguagem de Expressões Funcionais

## Requisitos do Projeto

O objetivo é desenvolver um mini compilador para uma linguagem de expressões matemáticas com suporte a funções definidas pelo usuário, variáveis, operadores aritméticos e escopo simples.

### Linguagem-alvo (Sintaxe e Semântica)

A linguagem deve suportar:
1.  **Declaração de Funções**: `função nome(parâmetros) = expressão`
2.  **Atribuições**: `variável = expressão`
3.  **Operadores Aritméticos**: `+`, `-`, `*`, `/`, e `^` (potência)
4.  **Tipos de Dados**: Inteiros e Ponto Flutuante.

### Fases do Compilador

O projeto será dividido nas seguintes fases:

1.  **Análise Léxica**: Identificação dos tokens da linguagem.
2.  **Análise Sintática (Parser)**: Construção de uma Árvore de Sintaxe Abstrata (AST) a partir da gramática (sugerido LL(1) ou LR).
3.  **Análise Semântica**: Verificação de tipos, escopo e chamadas de função.
4.  **Geração de Código Intermediário**: Geração de código em formato de três endereços ou bytecode simples.

## Arquitetura Proposta

A implementação será feita em **Python** devido à sua clareza e facilidade de prototipagem, utilizando a biblioteca `ply` (Python Lex-Yacc) para as fases de análise léxica e sintática, o que simplifica a construção do parser LL(1) ou LR.

### Estrutura de Diretórios

```
compilador_projeto/
├── src/
│   ├── lexer.py          # Analisador Léxico (PLY/Lex)
│   ├── parser.py         # Analisador Sintático (PLY/Yacc) e AST
│   ├── semantic_analyzer.py # Análise Semântica e Tabela de Símbolos
│   ├── intermediate_code_gen.py # Geração de Código Intermediário
│   └── main.py           # Ponto de entrada do compilador
├── tests/
│   ├── test_valid.txt    # Casos de teste válidos
│   └── test_invalid.txt  # Casos de teste inválidos
└── README.md             # Documentação do projeto
```

### Detalhamento da Implementação

| Fase | Componente | Tecnologia/Abordagem |
| :--- | :--- | :--- |
| **Léxica** | `lexer.py` | `ply.lex` |
| **Sintática** | `parser.py` | `ply.yacc` (Gramática LR) |
| **Semântica** | `semantic_analyzer.py` | Tabela de Símbolos e Verificação de Tipos |
| **Geração de Código** | `intermediate_code_gen.py` | Código de Três Endereços (Quadruplas) |

## Como Executar o Programa

### 1. Abra a pasta "compilador_projeto" no **Prompt de Comando** ou **PowerShell** do Windows

### 2. Configurar o Ambiente Virtual

   #### 2.1. Criar o ambiente virtual:

         python -m venv venv

   #### 2.2. Ativar o ambiente virtual:

         .\venv\Scripts\Activate

   É comum a política de execução estar bloqueando scripts, então o Windows não deixa ativar o ambiente virtual.
   Neste caso, executar este script, e repetir o processo: 

         Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

### 3.  Instalar a Dependência

         pip install ply

### 4. Executar o Projeto

         python src/main.py






