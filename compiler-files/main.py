from lexer import LexicalAnalyzer 
from syntax import Parser, print_ast_readable

def main():
    code = """def func():
        print(10 + 20)
        if x > 5:
            x = x - 1
    """

    # Instantiate the lexical analyzer
    analyzer = LexicalAnalyzer()
    # Tokenize the provided code
    tokens = analyzer.tokenize(code)

    # Print the list of tokens
    print("Tokens:")
    for token in tokens:
        print(token)

    # Instantiate the parser with the list of tokens
    parser = Parser(tokens)
    
    # Parse the tokens to create an AST
    ast = parser.parse()

    # Print the AST
    print("\nAST:")

# Call the function to pretty-print the AST
    print_ast_readable(ast)

if __name__ == "__main__":
    main()
