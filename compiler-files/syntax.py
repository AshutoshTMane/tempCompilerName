class ProgramNode:
    def __init__(self, functions):
        self.functions = functions

    def __repr__(self):
        return f"ProgramNode(functions={repr(self.functions)})"


class FunctionDefNode:
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"FunctionDefNode(name={repr(self.name)}, parameters={repr(self.parameters)}, body={repr(self.body)})"


class PrintNode:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"PrintNode(expression={repr(self.expression)})"


class AssignmentNode:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"AssignmentNode(identifier={repr(self.identifier)}, expression={repr(self.expression)})"


class IfNode:
    def __init__(self, condition, block, else_block=None):
        self.condition = condition
        self.block = block
        self.else_block = else_block

    def __repr__(self):
        return f"IfNode(condition={repr(self.condition)}, block={repr(self.block)}, else_block={repr(self.else_block)})"


class WhileNode:
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def __repr__(self):
        return f"WhileNode(condition={repr(self.condition)}, block={repr(self.block)})"


class BinaryOpNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryOpNode(left={repr(self.left)}, operator={repr(self.operator)}, right={repr(self.right)})"


class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberNode(value={repr(self.value)})"


class IdentifierNode:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"IdentifierNode(name={repr(self.name)})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def skip_ignorable_tokens(self):
        while self.current_token() and self.current_token()[0] in {'NEWLINE', 'WHITESPACE', 'COMMENT'}:
            self.pos += 1

    def eat(self, token_type):
        self.skip_ignorable_tokens()
        if self.current_token() and self.current_token()[0] == token_type:
            print(f"DEBUG: Consuming token: {self.current_token()}")
            self.pos += 1
        else:
            raise SyntaxError(
                f"Expected {token_type}, got {self.current_token()} at position {self.pos}"
            )

    def parse(self):
        self.skip_ignorable_tokens()
        functions = []

        while self.current_token() is not None:
            print(f"DEBUG: Parsing function at token: {self.current_token()}")
            functions.append(self.parse_function_def())
            self.skip_ignorable_tokens()

        print(f"DEBUG: Final AST: {functions}")
        return functions

    def parse_function_def(self):
        self.eat('DEF')
        func_name = self.current_token()[1]
        print(f"DEBUG: Function name: {func_name}")
        self.eat('IDENTIFIER')
        self.eat('LPAREN')
        parameters = self.parse_parameters()
        self.eat('RPAREN')
        self.eat('COLON')
        body = self.parse_block()
        node = FunctionDefNode(func_name, parameters, body)
        print(f"DEBUG: FunctionDefNode created: {node}")
        return node

    def parse_parameters(self):
        params = []
        while self.current_token() and self.current_token()[0] == 'IDENTIFIER':
            params.append(self.current_token()[1])
            self.eat('IDENTIFIER')
            if self.current_token() and self.current_token()[0] == 'COMMA':
                self.eat('COMMA')
        print(f"DEBUG: Parsed parameters: {params}")
        return params

    def parse_block(self):
        statements = []
        self.eat('INDENT')  # Consume the INDENT token

        while self.current_token() and self.current_token()[0] != 'DEDENT':
            self.skip_ignorable_tokens()
            if self.current_token() and self.current_token()[0] != 'DEDENT':
                print(f"DEBUG: Parsing statement at token: {self.current_token()}")
                statements.append(self.parse_statement())

        self.eat('DEDENT')  # Consume the DEDENT token
        print(f"DEBUG: Parsed block: {statements}")
        return statements

    def parse_statement(self):
        token_type = self.current_token()[0]
        print(f"DEBUG: Parsing statement of type: {token_type}")
        if token_type == 'PRINT':
            return self.parse_print()
        elif token_type == 'IF':
            return self.parse_if()
        elif token_type == 'WHILE':
            return self.parse_while()
        elif token_type == 'IDENTIFIER':
            return self.parse_assignment()
        else:
            raise SyntaxError(f"Unexpected token: {token_type}")

    def parse_print(self):
        self.eat('PRINT')
        self.eat('LPAREN')
        expression = self.parse_expression()
        self.eat('RPAREN')
        node = PrintNode(expression)
        print(f"DEBUG: PrintNode created: {node}")
        return node

    def parse_if(self):
        self.eat('IF')
        condition = self.parse_expression()
        print(f"DEBUG: If condition: {condition}")
        self.eat('COLON')
        block = self.parse_block()
        else_block = None
        if self.current_token() and self.current_token()[0] == 'ELSE':
            self.eat('ELSE')
            self.eat('COLON')
            else_block = self.parse_block()
        node = IfNode(condition, block, else_block)
        print(f"DEBUG: IfNode created: {node}")
        return node

    def parse_assignment(self):
        identifier = self.current_token()[1]
        self.eat('IDENTIFIER')
        self.eat('ASSIGN')
        expression = self.parse_expression()
        node = AssignmentNode(IdentifierNode(identifier), expression)
        print(f"DEBUG: AssignmentNode created: {node}")
        return node

    def parse_expression(self):
        left = self.parse_term()
        while self.current_token() and self.current_token()[0] in {'PLUS', 'MINUS', 'GT', 'LT', 'EQ'}:
            operator = self.current_token()[1]
            self.eat(self.current_token()[0])
            right = self.parse_term()
            left = BinaryOpNode(left, operator, right)
            print(f"DEBUG: BinaryOpNode created: {left}")
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token() and self.current_token()[0] in {'MULT', 'DIV', 'MOD'}:
            operator = self.current_token()[1]
            self.eat(self.current_token()[0])
            right = self.parse_factor()
            left = BinaryOpNode(left, operator, right)
            print(f"DEBUG: BinaryOpNode created: {left}")
        return left

    def parse_factor(self):
        token_type, token_value = self.current_token()
        if token_type == 'NUMBER':
            self.eat('NUMBER')
            node = NumberNode(token_value)
            print(f"DEBUG: NumberNode created: {node}")
            return node
        elif token_type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            node = IdentifierNode(token_value)
            print(f"DEBUG: IdentifierNode created: {node}")
            return node
        elif token_type == 'LPAREN':
            self.eat('LPAREN')
            expression = self.parse_expression()
            self.eat('RPAREN')
            print(f"DEBUG: Parsed parenthesized expression: {expression}")
            return expression
        else:
            raise SyntaxError(f"Unexpected token: {token_value}")
        

def print_ast_readable(functions, indent=0):
    for function in functions:
        print_function(function, indent)

def print_function(function, indent=0):
    prefix = "  " * indent
    print(f"{prefix}Function: {function.name}")
    print(f"{prefix}Parameters: {', '.join(function.parameters)}")
    print(f"{prefix}Body:")
    for statement in function.body:
        print_statement(statement, indent + 1)

def print_statement(statement, indent):
    prefix = "  " * indent
    if isinstance(statement, PrintNode):
        print(f"{prefix}Print:")
        print_expression(statement.expression, indent + 1)
    elif isinstance(statement, IfNode):
        print(f"{prefix}If:")
        print(f"{prefix}  Condition:")
        print_expression(statement.condition, indent + 2)
        print(f"{prefix}  Then:")
        for stmt in statement.block:
            print_statement(stmt, indent + 2)
        if statement.else_block:
            print(f"{prefix}  Else:")
            for stmt in statement.else_block:
                print_statement(stmt, indent + 2)
    elif isinstance(statement, AssignmentNode):
        print(f"{prefix}Assign:")
        print(f"{prefix}  Variable: {statement.identifier.name}")
        print(f"{prefix}  Value:")
        print_expression(statement.expression, indent + 2)

def print_expression(expression, indent):
    prefix = "  " * indent
    if isinstance(expression, BinaryOpNode):
        print(f"{prefix}Operation: {expression.operator}")
        print(f"{prefix}Left:")
        print_expression(expression.left, indent + 1)
        print(f"{prefix}Right:")
        print_expression(expression.right, indent + 1)
    elif isinstance(expression, NumberNode):
        print(f"{prefix}Number: {expression.value}")
    elif isinstance(expression, IdentifierNode):
        print(f"{prefix}Variable: {expression.name}")
