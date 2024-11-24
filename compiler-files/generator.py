from syntax import *

class CodeGenerator:


    def generate_assembly(self, ast):
        assembly_code = []
        
        for function in ast:
            code += self.generate_function(function)

        return assembly_code
    
    def generate_function(self, function):
        for statement in function.body:
            code += self.generate_statement(statement)
