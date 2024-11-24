from syntax import *

class CodeGenerator:
    def generate_assembly(self, ast):
        assembly_code = []
        
        for function in ast:
            code += self.generate_function(function)

        return assembly_code
