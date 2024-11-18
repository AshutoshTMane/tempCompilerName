class GrammarRules:
    def __init__(self):
        # Define grammar rules as a dictionary
        self.rules = {
            # Program structure
            "program": ["main_block"],
            
            # Main block
            "main_block": ["MAIN LBRACE statements RBRACE"],
            
            # Statements
            "statements": ["statement statements", ""],
            
            # Single statement
            "statement": ["print_statement", "if_statement", "assignment_statement"],
            
            # Print statement
            "print_statement": ["PRINT LPAREN expression RPAREN"],
            
            # If statement
            "if_statement": ["IF LPAREN expression RPAREN LBRACE statements RBRACE"],
            
            # Assignment statement
            "assignment_statement": ["IDENTIFIER ASSIGN expression"],
            
            # Expression (arithmetic or boolean)
            "expression": [
                "arithmetic_expression",
                "arithmetic_expression comparison_operator arithmetic_expression"
            ],
            
            # Arithmetic expression
            "arithmetic_expression": [
                "term",
                "arithmetic_expression PLUS term",
                "arithmetic_expression MINUS term"
            ],
            
            # Term (factors combined by *, /, %)
            "term": ["factor", "term MULT factor", "term DIV factor", "term MOD factor"],
            
            # Factor (individual numbers, variables, or grouped expressions)
            "factor": ["NUMBER", "IDENTIFIER", "LPAREN expression RPAREN"],
            
            # Comparison operators
            "comparison_operator": ["EQ", "NEQ", "LT", "GT", "LTE", "GTE"],
        }

    def get_rule(self, non_terminal):
        """Retrieve rules for a given non-terminal."""
        return self.rules.get(non_terminal, [])

    def print_grammar(self):
        """Print the grammar rules."""
        for non_terminal, productions in self.rules.items():
            print(f"{non_terminal} -> {' | '.join(productions)}")
