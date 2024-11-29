class ProgramNode:
    def __init__(self, functions, statements):
        self.functions = functions  # List of function definitions
        self.statements = statements  # List of top-level statements

    def __repr__(self):
        # Start with a header
        output = ["AST:"]
        
        # Create an index to track the order of appearance
        index = 0
        
        # Iterate over both functions and statements
        for node in self.functions + self.statements:
            if isinstance(node, FunctionDefNode):
                output.append(f"[{index}] {repr(node)}")
            else:
                output.append(f"[{index}] {repr(node)}")
            index += 1
        
        return "\n".join(output)
    
class Error:
    def __init__(self, message, line_number):
        self.message = message
        self.line_number = line_number

    def __str__(self):
        return f"Line {self.line_number}: {self.message}"


class FunctionDefNode:
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"FunctionDefNode(name={repr(self.name)}, parameters={repr(self.parameters)}, body={repr(self.body)})"
    
class ReturnNode:
    def __init__(self, value=None):
        self.value = value 

    def __repr__(self):
        return f"ReturnNode(value={self.value})"

class FunctionCallNode:
    def __init__(self, function_name, arguments):
        self.function_name = function_name
        self.arguments = arguments
    def __repr__(self):
        return f"FunctionCallNode(function_name={self.function_name}, arguments={self.arguments})"


class PrintNode:
    def __init__(self, parameters):
        self.parameters = parameters

    def __repr__(self):
        return f"PrintNode(expression={repr(self.parameters)})"


class AssignmentNode:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"AssignmentNode(identifier={repr(self.identifier)}, expression={repr(self.expression)})"
    
class AugmentedAssignmentNode:
    def __init__(self, identifier, operator, expression):
        self.identifier = identifier
        self.operator = operator
        self.expression = expression
    
    def __repr__(self):
        return f"AssignmentNode(identifier={repr(self.identifier)}, operator={repr(self.operator)} expression={repr(self.expression)})"
    
class ListNode:
    def __init__(self, elements):
        self.elements = elements
    
    def __repr__(self):
        return f"ListNode({self.elements})"


class IfNode:
    def __init__(self, condition, block, elif_condition=None, elif_block=None, else_block=None):
        self.condition = condition
        self.block = block
        self.elif_condition = elif_condition
        self.elif_block = elif_block
        self.else_block = else_block

    def __repr__(self):
        return (f"IfNode(condition={repr(self.condition)}, block={repr(self.block)}, "
                f"elif_condition={repr(self.elif_condition)}, elif_block={repr(self.elif_block)}, "
                f"else_block={repr(self.else_block)})")

class ForNode:
    def __init__(self, variable, collection, block):
        self.variable = variable  
        self.collection = collection 
        self.block = block 

    def __repr__(self):
        return f"ForNode(variable={repr(self.variable)}, collection={repr(self.collection)}, block={repr(self.block)})"

class RangeNode:
    def __init__(self, start, stop, step):
        self.start = start
        self.stop = stop
        self.step = step

    def __repr__(self):
        return f"RangeNode(start={self.start}, stop={self.stop}, step={self.step})"


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
    
class FloatNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"FloatNode(value={repr(self.value)})"

class StringNode:
    def __init__(self, value):
        self.value = value 
    
    def __repr__(self):
        return f"StringNode({self.value})"
    
class FStringNode:
    def __init__(self, parts):
        self.parts = parts  

    def __repr__(self):
        return f"FStringNode(parts={repr(self.parts)})"

    
class BooleanNode:
    def __init__(self, value):
        self.value = value  
    
    def __repr__(self):
        return f"BooleanNode({self.value})"


class IdentifierNode:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"IdentifierNode(name={repr(self.name)})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []
        self.success = True

    def add_error(self, message):
        line_number = self.current_token()[2] if self.current_token() else "Unknown"
        self.errors.append(Error(message, line_number))
        self.success = False

    def print_errors(self):
        if self.errors:
            print("Syntax Errors:")
            for error in self.errors:
                print(str(error))
        else:
            print("No syntax errors found.")

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
            self.add_error(f"Expected {token_type}, got {self.current_token()[0]}")


    def parse(self):
        self.skip_ignorable_tokens()
        functions = []
        statements = []

        while self.current_token() is not None:
            self.skip_ignorable_tokens()
            if self.current_token()[0] == "DEF":
                is_main = self.current_token()[1] == "main"
                functions.append(self.parse_function_def(is_main))
            else:
                statements.append(self.parse_statement())
            self.skip_ignorable_tokens()

        return ProgramNode(functions, statements), self.success


    def parse_function_def(self, main = False): # Add parameter to check if function is 'main' or not
        self.eat('DEF')
        func_name = 'main' if main else self.current_token()[1]
        print(f"DEBUG: Function name: {func_name}")
        self.eat('MAIN' if main else 'IDENTIFIER') # Eat main if main
        self.eat('LPAREN')
        parameters = self.parse_parameters()
        self.eat('RPAREN')
        self.eat('COLON')
        body = self.parse_block(in_function = True)
        node = FunctionDefNode(func_name, parameters, body)
        print(f"DEBUG: FunctionDefNode created: {node}")
        return node
    
    def parse_function_call(self):
        token = self.current_token()
        if token[0] != 'IDENTIFIER':
            self.add_error(f"Expected function name, found {token}")

        function_name = token[1]  # Save the function name
        self.eat('IDENTIFIER')  # Consume the identifier

        # Ensure the next token is an opening parenthesis
        if self.current_token()[0] != 'LPAREN':
            self.add_error(f"Expected '(' after function name, found {self.current_token()}")

        self.eat('LPAREN')  # Consume '('
        arguments = []

        # Parse arguments if present
        if self.current_token()[0] != 'RPAREN':  # Not an empty argument list
            while True:
                arguments.append(self.parse_expression())  # Parse an argument expression
                if self.current_token()[0] == 'COMMA':  # Handle comma-separated arguments
                    self.eat('COMMA')
                else:
                    break

        # Ensure the closing parenthesis is present
        if self.current_token()[0] != 'RPAREN':
            self.add_error(f"Expected ')' after arguments, found {self.current_token()}")

        self.eat('RPAREN')  # Consume ')'

        # Create and return the function call node
        node = FunctionCallNode(function_name=function_name, arguments=arguments)
        print(f"DEBUG: FunctionCallNode created: {node}")
        return node

    
    def parse_return(self):
        # Ensure the current token is 'RETURN'
        if self.current_token()[0] != 'RETURN':
            self.add_error("Expected 'RETURN'")

        self.eat('RETURN')  # Consume the 'RETURN' token

        if self.current_token() and self.current_token()[0] not in {'SEMICOLON', 'NEWLINE'}:
            # Parse the expression being returned
            return_value = self.parse_expression()
        else:
            # Handle `return;` with no value
            return_value = None

        # Create a ReturnNode
        node = ReturnNode(value=return_value)
        print(f"DEBUG: ReturnNode created: {node}")
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
    
    def parse_parameter(self):
        expression = self.parse_expression()
        print(f"DEBUG: Parsed expression: {expression}")
        return expression
    

    def parse_block(self, in_function=False):
        statements = []
        self.eat('INDENT')  # Consume the INDENT token
        print("in block")

        while self.current_token() and self.current_token()[0] != 'DEDENT':
            self.skip_ignorable_tokens()

            # Handle `RETURN` statement
            if self.current_token() and self.current_token()[0] == 'RETURN':
                if in_function:
                    statements.append(self.parse_return())
                else:
                    self.add_error("Return statement found outside of a function")

            # Handle `ELIF` or `ELSE` tokens
            elif self.current_token() and self.current_token()[0] in ['ELIF', 'ELSE']:
                return statements

            # Parse other statements
            elif self.current_token() and self.current_token()[0] != 'DEDENT':
                print(f"DEBUG: Parsing statement at token: {self.current_token()}")
                statements.append(self.parse_statement())

        # Consume `DEDENT` token to close the block
        if self.current_token() is not None:
            self.eat('DEDENT')
            print("Ate Dedent")

        print(f"DEBUG: Parsed block: {statements}")
        print("out of block")
        return statements


    def parse_statement(self):
        self.skip_ignorable_tokens()
        token_type = self.current_token()[0]

        print(f"DEBUG: Parsing statement of type: {token_type}")
        if token_type == 'PRINT':
            return self.parse_print()
        elif token_type == 'IF':
            return self.parse_if()
        elif token_type == 'FOR':  
            return self.parse_for()
        elif token_type == 'WHILE':
            return self.parse_while()
        elif token_type == 'IDENTIFIER':
            return self.parse_assignment()
        elif token_type == 'INDENT':
            self.eat('INDENT')
        else:
            self.add_error(f"Unexpected token: {token_type}")
        
        self.skip_ignorable_tokens()

    def parse_print(self):
        self.eat('PRINT')
        self.eat('LPAREN')

        parameters = []

        parameters.append(self.parse_parameter())

        while self.current_token() and self.current_token()[0] == 'COMMA':
            self.eat('COMMA')
            parameters.append(self.parse_parameter())
        
        self.eat('RPAREN')
        node = PrintNode(parameters)
        print(f"DEBUG: PrintNode created: {node}")
        return node


    def parse_if(self):
        if self.current_token()[0] not in {'IF', 'ELIF', 'ELSE'}:
            self.add_error(f"Expected 'IF', 'ELIF', or 'ELSE' but found {self.current_token()}")
        
        if self.current_token()[0] == 'IF':
            self.eat('IF')
        elif self.current_token()[0] == 'ELIF':
            self.eat('ELIF')

        condition = self.parse_expression()
        print(f"DEBUG: If/Elif condition: {condition}")

        if self.current_token()[0] != 'COLON':
            self.add_error("Expected ':' after if/elif condition")
        self.eat('COLON')

        print("hi)")
        block = self.parse_block()
        

        else_block = None
        elif_condition = None
        elif_block = None

        while self.current_token() and (self.current_token()[0] == 'ELIF' or self.current_token()[0] == 'ELSE'):
            if self.current_token()[0] == 'ELIF':
                self.eat('ELIF')
                elif_condition = self.parse_expression()
                print(f"DEBUG: Elif condition: {elif_condition}")

                if self.current_token()[0] != 'COLON':
                    self.add_error("Expected ':' after elif condition")
                self.eat('COLON')

                elif_block = self.parse_block()
            else: 
                self.eat('ELSE')

                if self.current_token()[0] != 'COLON':
                    self.add_error("Expected ':' after else")
                self.eat('COLON')
                else_block = self.parse_block()
                break 

        node = IfNode(condition, block, elif_condition, elif_block, else_block)
        print(f"DEBUG: IfNode created: {node}")
        return node

    def parse_for(self):
        self.eat('FOR')  
        variable = IdentifierNode(self.current_token()[1])
        self.eat('IDENTIFIER') 
        self.eat('IN')  

        if self.current_token()[0]  == 'RANGE': 
            collection = self.parse_range()
        else:   
            collection = self.parse_expression()  
        self.eat('COLON') 

        block = self.parse_block()  

        node = ForNode(variable, collection, block)
        print(f"DEBUG: ForNode created: {node}")
        return node

    def parse_while(self):
        self.eat('WHILE')
        condition = self.parse_expression()

        self.eat('COLON') 

        block = self.parse_block()

        node = WhileNode(condition, block)
        print(f"DEBUG: WhileNode created: {node}")

        return node

    
    def parse_range(self):
        self.eat('RANGE')
        self.eat('LPAREN') 

        list_expr = self.parse_expression()  
        
        self.eat('RPAREN')  

        node = ListNode(list_expr)  
        print(f"DEBUG: ListNode created: {node}")
        return node
    
    def parse_list(self):
        self.eat('LBRACK') 
        
        elements = [] 
        
        while self.current_token()[0] != 'RBRACK': 
            print(self.current_token())
            element = self.parse_expression()  
            elements.append(element) 
            
            if self.current_token()[0] == 'COMMA': 
                self.eat('COMMA')
            elif self.current_token()[0] != 'RBRACK':
                self.add_error(f"Unexpected token: {self.current_token()}")
        
        self.eat('RBRACK')  
        

        node = ListNode(elements)
        print(f"DEBUG: ListNode created: {node}")
        return node


    def parse_assignment(self):
        identifier = self.current_token()[1]
        self.eat('IDENTIFIER')

        operator = None
        if self.current_token()[0] in {'PLUS_ASSIGN', 'MINUS_ASSIGN', 'TIMES_ASSIGN', 'DIVIDE_ASSIGN'}:
            operator = self.current_token()[0]
            self.eat(operator)

        if operator is None:
            self.eat('ASSIGN')

        expression = self.parse_expression()

        if operator:
            node = AugmentedAssignmentNode(IdentifierNode(identifier), operator, expression)
            print(f"DEBUG: AugmentedAssignmentNode created: {node}")
        else:
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
        left = self.parse_element()
        while self.current_token() and self.current_token()[0] in {'EXP'}:
            operator = self.current_token()[1]
            self.eat(self.current_token()[0])
            right = self.parse_factor()
            left = BinaryOpNode(left, operator, right)
            print(f"DEBUG: BinaryOpNode created: {left}")
        return left
    
    def parse_element(self):
        if self.current_token()[0] == 'IDENTIFIER':
            token = self.current_token()
            
            # Check if the next token is LPAREN, indicating a function call
            if self.peek_next_token() and self.peek_next_token()[0] == 'LPAREN':
                return self.parse_function_call()
            else:
                # Plain identifier
                self.eat('IDENTIFIER')
                node = IdentifierNode(token[1])
                print(f"DEBUG: IdentifierNode created: {node}")
                return node
        
        elif self.current_token()[0] == 'LBRACK':
            print(f"DEBUG: Detected LBRACK, attempting to parse list at token: {self.current_token()}")
            node = self.parse_list()
            print(f"DEBUG: ListNode created: {node}")
            return node

        elif self.current_token()[0] == 'NUMBER':
            token = self.current_token()
            self.eat('NUMBER')
            node = NumberNode(token[1])
            print(f"DEBUG: NumberNode created: {node}")
            return node

        elif self.current_token()[0] == 'FLOAT':
            token = self.current_token()
            self.eat('FLOAT')
            node = FloatNode(token[1])
            print(f"DEBUG: FloatNode created: {node}")
            return node

        elif self.current_token()[0] == 'STRING': 
            token = self.current_token()
            self.eat('STRING')
            node = StringNode(token[1])  
            print(f"DEBUG: StringNode created: {node}")
            return node

        elif self.current_token()[0] == 'TRUE':  
            token = self.current_token()
            self.eat('TRUE')
            node = BooleanNode(True) 
            print(f"DEBUG: BooleanNode created: {node}")
            return node

        elif self.current_token()[0] == 'FALSE':  
            token = self.current_token()
            self.eat('FALSE')
            node = BooleanNode(False)  
            print(f"DEBUG: BooleanNode created: {node}")
            return node

        elif self.current_token()[0] == 'LPAREN':
            self.eat('LPAREN')
            node = self.parse_expression()  
            self.eat('RPAREN') 
            print(f"DEBUG: Parenthesized expression node: {node}")
            return node

        else:
            rself.add_error("Expected ELEMENT but found " + str(self.current_token()))

    def peek_next_token(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return None




### ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""
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
"""