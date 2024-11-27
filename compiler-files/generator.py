from syntax import *

class CodeGenerator:
    def __init__(self):
        self.registers = ["eax", "ebx", "ecx", "edx"]
        self.in_use = []
        self.label_counter = 0

    def allocate(self):
        for register in self.registers:
            if register not in self.in_use:
                self.in_use.append(register)
                return register
        raise RuntimeError("No available registers")
    
    def deallocate(self, remove_reg):
        if remove_reg in self.in_use:
            self.in_use.remove(remove_reg)


    def print_assembly(self, assembly_code):
        for line in assembly_code:
            print(line)

    def new_label(self):
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label

    def generate_assembly(self, ast):
        assembly_code = []
        
        for function in ast:
            self.generate_function(function, assembly_code)

        return assembly_code
    
    def generate_function(self, function, assembly_code):
        assembly_code.append(f"{function.name}:")
        for statement in function.body:
            self.generate_statement(statement, assembly_code)
        assembly_code.append("RET")

    def generate_statement(self, statement, assembly_code):
        if statement is None:
            return
        if isinstance(statement, PrintNode):
            reg = self.generate_expression(statement.expression, assembly_code)
            assembly_code.append(f"MOV eax, {reg}") 
            assembly_code.append("ecall") 
            self.deallocate(reg)
        elif isinstance(statement, AssignmentNode):
            reg = self.generate_expression(statement.expression, assembly_code)
            assembly_code.append(f"MOV [{statement.identifier.name}], {reg}")  
            self.deallocate(reg)
        elif isinstance(statement, IfNode):
            else_label = self.new_label()
            end_label = self.new_label()

            reg = self.generate_expression(statement.condition, assembly_code)
            assembly_code.append(f"CMP {reg}, 0")
            assembly_code.append(f"JE {else_label}")  
            self.deallocate(reg)

            for stmt in statement.block:
                self.generate_statement(stmt, assembly_code)
            assembly_code.append(f"JMP {end_label}") 

            assembly_code.append(f"{else_label}:")
            if statement.else_block:
                for stmt in statement.else_block:
                    self.generate_statement(stmt, assembly_code)

            assembly_code.append(f"{end_label}:")
        else:
            raise ValueError(f"Unknown statement type: {type(statement)}")

    def generate_expression(self, expression, assembly_code):
        if isinstance(expression, BinaryOpNode):
            left_reg = self.generate_expression(expression.left, assembly_code)
            right_reg = self.generate_expression(expression.right, assembly_code)

            if expression.operator == "+":
                assembly_code.append(f"ADD {left_reg}, {right_reg}")
            elif expression.operator == "-":
                assembly_code.append(f"SUB {left_reg}, {right_reg}")
            elif expression.operator == "*":
                assembly_code.append(f"MOV eax, {left_reg}")  
                assembly_code.append(f"MUL {right_reg}")     
                assembly_code.append(f"MOV {left_reg}, eax")  
            elif expression.operator == "/":
                
                assembly_code.append(f"MOV eax, {left_reg}")  
                assembly_code.append(f"XOR edx, edx")        
                assembly_code.append(f"DIV {right_reg}")     
                assembly_code.append(f"MOV {left_reg}, eax")  

            self.deallocate(right_reg) 
            return left_reg  

        elif isinstance(expression, NumberNode):
            reg = self.allocate()
            assembly_code.append(f"MOV {reg}, {expression.value}")
            return reg

        elif isinstance(expression, IdentifierNode):
            reg = self.allocate()
            assembly_code.append(f"MOV {reg}, [{expression.name}]")  
            return reg

        else:
            raise ValueError(f"Unknown expression type: {type(expression)}")
