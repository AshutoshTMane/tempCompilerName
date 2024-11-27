import re

class LexicalAnalyzer:
    def __init__(self):
        self.token_rules = [
            # Reserved keywords
            ('DEF', r'\bdef\b'),
            ('MAIN', r'\bmain\b'),
            ('IF', r'\bif\b'),
            ('FOR', r'\bfor\b'),
            ('ELSE', r'\belse\b'),
            ('ELIF', r'\belif\b'),
            ('WHILE', r'\bwhile\b'),
            ('PRINT', r'\bprint\b'),
            ('NONE', r'\bNone\b'),
            ('TRUE', r'\bTrue\b'),
            ('FALSE', r'\bFalse\b'),
            ('IN', r'\bin\b'),
            ('RANGE', r'\brange\b'),
            ('RETURN', r'\breturn\b'),

            # Comments
            ('COMMENT', r'#.*'),  # Single-line comment
            #('MULTILINE_COMMENT', r'("""(?:.|\n)*?"""|\'\'\'(?:.|\n)*?\'\'\')'),  # Multi-line comments

            # Strings
            ('STRING', r'(\'[^\']*\'|\"[^\"]*\")'),
            ('FSTRING', r'f"[^"]*"'),
            ('COMMA', r'\,'),

            # Augmented operators
            ('PLUS_ASSIGN', r'\+='),
            ('MINUS_ASSIGN', r'-='),
            ('TIMES_ASSIGN', r'\*='),
            ('DIVIDE_ASSIGN', r'/='),

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
            ('LBRACK', r'\['),
            ('RBRACK', r'\]'),
                
            # Identifiers and numbers
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'), # Since identifiers can be anything, we have rules saying the identifier can be a-z or A-Z with underscores. Note that the first character can not be a digit, which is why we have two brackets, the second one using * to denote that we can have 'zero or more' occurrences
            ('NUMBER', r'\d+'),  # \d in regex means "string contains digits", so this means one or more occurrences of a digit
            ('FLOAT', r'\d+\.\d+'),    
                
            # Whitespace (skip these characters)
            ('INDENT', r'   '),
            ('NEWLINE', r'\n'),
            ('WHITESPACE', r'\s+'),
        ]

        self.token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_rules)
    
    def tokenize(self, code):
        tokens = []
        line_number = 1
        prev_level = 0
        current_indent = 0

        for token in re.finditer(self.token_regex, code):
            token_type = token.lastgroup
            token_value = token.group()

            if token_type in {'WHITESPACE'}:
                continue

            if token_type in {'INDENT'}:
                current_indent += 1
                tokens.append((token_type, token_value, line_number))
            elif token_type in {'NEWLINE'}:
                tokens.append((token_type, token_value, line_number))
                print(line_number)
                print(f"Previous indent level: {prev_level}")
                print(f"Current indent level: {current_indent}")
                

                if current_indent < prev_level:
                    tokens_copy = tokens[:]
                    newline_seen = False   

                    for i in range(len(tokens_copy) - 1, -1, -1):
                        if tokens_copy[i][0] == 'NEWLINE':
                            if not newline_seen:
                                newline_seen = True
                                continue
                            tokens.insert(i + 1, ('DEDENT', '', tokens_copy[i][2]+1))
                            break

                prev_level = current_indent
                current_indent = 0
                line_number += 1 

            else:
                tokens.append((token_type, token_value, line_number))

        while prev_level > 0:
            prev_level -= 1

        return tokens
