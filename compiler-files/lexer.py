import re

class LexicalAnalyzer:
    def __init__(self):
        self.token_rules = [
            # Reserved keywords
            ('MAIN', r'main'),
            ('IF', r'if'), 
            ('ELSE', r'else'),
            ('WHILE', r'while'),
            ('PRINT', r'print'),

            # Arithmetic operators
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('EXP', r'\*\*'),
            ('MULT', r'\*'),
            ('DIV', r'\/'),
            ('MOD', r'%'),

            # Comparison operators
            ('EQ', r'=='),
            ('NEQ', r'!='),
            ('LT', r'<'),
            ('GT', r'>'),
            ('LTE', r'<='),
            ('GTE', r'>='),

            # Assignment
            ('ASSIGN', r'='),

            # Parentheses and braces
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
                
            # Identifiers and numbers
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'), # since identifiers can be anything, we have rules saying the identifier can be a-z or A-Z with underscores. Note that the first character can not be a digit, which is why we have two brackets, the second one using * to denote that we can have 'zero or more' occurrences
            ('NUMBER', r'\d+'),  # \d in regex means "string contains digits", so this means one or more occurrences of a digit
                
            # Comments (skip comments)
            ('COMMENT', r'\/\/[^\n]*'), 
                
            # Whitespace (skip these characters)
            ('WHITESPACE', r'\s+'),
        ]

        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_rules)
    
    def tokenize(self, code):
    
        tokens = []

        # The regex 'finditer' function essentially finds a substring from our token_list and then turns them as an "iterator". This means we get a special object that gives us the group name and matched test in a "one at a time" fashion.
        for token in re.finditer(self.token_regex, code): 
            token_type = token.lastgroup  # The name of group that matched 
            token_value = token.group()  # The actual text matched
            if token_type not in {'WHITESPACE', 'COMMENT'}:  # Skip ignored tokens
                tokens.append((token_type, token_value))
        return tokens
        
        

