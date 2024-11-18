import re

class LexicalAnalyzer:
    def __init__(self):
        self.token_rules = [
            # Reserved keywords
            ('DEF', r'\bdef\b'),
            ('MAIN', r'\bmain\b'),
            ('IF', r'\bif\b'),
            ('ELSE', r'\belse\b'),
            ('WHILE', r'\bwhile\b'),
            ('PRINT', r'\bprint\b'),
            ('NONE', r'\bNone\b'),
            ('TRUE', r'\bTrue\b'),
            ('FALSE', r'\bFalse\b'),

            # Comments
            ('COMMENT', r'#.*'),  # Single-line comment
            ('MULTILINE_COMMENT', r'"""(?:.|\n)*?"""|\'\'\'(?:.|\n)*?\''),  # Multi-line comments

            # Strings
            ('STRING', r'(\'[^\']*\'|\"[^\"]*\")'),

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

            # Parentheses, brackets, and colon
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('COLON', r':'),
                
            # Identifiers and numbers
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'), # Since identifiers can be anything, we have rules saying the identifier can be a-z or A-Z with underscores. Note that the first character can not be a digit, which is why we have two brackets, the second one using * to denote that we can have 'zero or more' occurrences
            ('NUMBER', r'\d+'),  # \d in regex means "string contains digits", so this means one or more occurrences of a digit
            ('FLOAT', r'\d+\.\d+'),    
                
            # Whitespace (skip these characters)
            ('NEWLINE', r'\n'),
            ('WHITESPACE', r'\s+'),
        ]

        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_rules)
    
    def tokenize(self, code):
    
        tokens = []
        indent_levels = [0]
        line_start = True

        # The regex 'finditer' function essentially finds a substring from our token_list and then turns them as an "iterator". This means we get a special object that gives us the group name and matched test in a "one at a time" fashion.
        for token in re.finditer(self.token_regex, code): 
            token_type = token.lastgroup  # The name of group that matched 
            token_value = token.group()  # The actual text matched
            if token_type == 'WHITESPACE' and line_start:
                # Handle indentation (count spaces/tabs at the start of lines)
                current_indent = len(token_value)
                if current_indent > indent_levels[-1]:
                    indent_levels.append(current_indent)
                    tokens.append(('INDENT', token_value))
                while current_indent < indent_levels[-1]:
                    indent_levels.pop()
                    tokens.append(('DEDENT', ''))

            elif token_type == 'NEWLINE':
                tokens.append(('NEWLINE', token_value))
                line_start = True

            elif token_type not in {'WHITESPACE', 'COMMENT', 'MULTILINE_COMMENT'}:
                tokens.append((token_type, token_value))
                line_start = False

        # Add DEDENT tokens for remaining indentation levels
        while len(indent_levels) > 1:
            indent_levels.pop()
            tokens.append(('DEDENT', ''))
        return tokens
        
        

