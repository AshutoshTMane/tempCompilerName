from syntax import *

class CodeGenerator:


    def generate_assembly(self, ast):
        assembly_code = []
        
        for function in ast:
            self.generate_function(function, assembly_code)

        return assembly_code
    
    def generate_function(self, function, assembly_code):
        assembly_code.append("{function.name}:")
        for statement in function.body:
            self.generate_statement(statement, assembly_code)
        assembly_code.append("RET")

