from lexer import LexicalAnalyzer 

if __name__ == "__main__":
    code = """
    main {
        print(10 + 20);
        // This is a comment
        if (x > 5) {
            x = x - 1;
        }
    }
    """

    # Instantiate the lexical analyzer
    analyzer = LexicalAnalyzer()
    # Tokenize the provided code
    tokens = analyzer.tokenize(code)

    # Print the list of tokens
    for token in tokens:
        print(token)
