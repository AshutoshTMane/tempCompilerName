from lexer import LexicalAnalyzer 
from syntax import Parser
from generator import CodeGenerator

def main():
    file_path = '../test-files/basicTestOne.txt'  # Replace with your file path
    with open(file_path, 'r') as file:
        code = file.read()

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
    print(ast)

    generator = CodeGenerator()
    
    assembly_code = generator.generate_assembly(ast)
    generator.print_assembly()

if __name__ == "__main__":
    main()
