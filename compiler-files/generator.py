from syntax import *

class CodeGenerator:
    def __init__(self):
        self.registers = ["eax", "ebx", "ecx", "edx", "r5", "r6", "r7", "r8", "r9", "r10", "r11"]
        self.in_use = []
        self.label_counter = 0
        self.assembly_code = []

    def allocate(self):
        for register in self.registers:
            if register not in self.in_use:
                self.in_use.append(register)
                return register
        raise RuntimeError("No available registers")
    
    def deallocate(self, remove_reg):
        if remove_reg in self.in_use:
            self.in_use.remove(remove_reg)

    def generate_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def generate_assembly(self, node):
        if isinstance(node, ProgramNode):
            for function in node.functions:
                self.generate_assembly(function)
            for statement in node.statements:
                self.generate_assembly(statement)
        elif isinstance(node, FunctionDefNode):
            self.assembly_code.append(f"{node.name}:")
            self.assembly_code.append("push ebp")
            self.assembly_code.append("mov ebp, esp")
            for statement in node.body:
                self.generate_assembly(statement)
            self.assembly_code.append("pop ebp")
            self.assembly_code.append("ret")
        elif isinstance(node, AssignmentNode):
            # Handle assignments like count = count + 1
            if isinstance(node.expression, BinaryOpNode) and node.expression.operator == '+':
                left_reg = self.generate_assembly(node.expression.left)
                right_reg = self.generate_assembly(node.expression.right)
                self.assembly_code.append(f"add {left_reg}, {right_reg}")
                self.assembly_code.append(f"mov DWORD PTR [{node.identifier.name}], {left_reg}")
                self.deallocate(left_reg)
                self.deallocate(right_reg)
            else:
                reg = self.generate_assembly(node.expression)
                self.assembly_code.append(f"mov DWORD PTR [{node.identifier.name}], {reg}")
                self.deallocate(reg)
        elif isinstance(node, BinaryOpNode):
            # Handle binary operations like x + 2
            left_reg = self.generate_assembly(node.left)
            right_reg = self.generate_assembly(node.right)
            if node.operator == '+':
                self.assembly_code.append(f"add {left_reg}, {right_reg}")
            elif node.operator == '-':
                self.assembly_code.append(f"sub {left_reg}, {right_reg}")
            elif node.operator == '*':
                self.assembly_code.append(f"imul {left_reg}, {right_reg}")
            elif node.operator == '/':
                self.assembly_code.append("cdq")  # Sign-extend for division
                self.assembly_code.append(f"idiv {right_reg}")
            self.deallocate(right_reg)
            return left_reg

        elif isinstance(node, NumberNode):
            reg = self.allocate()
            self.assembly_code.append(f"mov {reg}, {node.value}")
            return reg
        elif isinstance(node, IdentifierNode):
            reg = self.allocate()
            self.assembly_code.append(f"mov {reg}, [{node.name}]")
            return reg
        elif isinstance(node, PrintNode):
            for param in node.parameters:
                reg = self.generate_assembly(param)
                self.assembly_code.append(f"push {reg}")
                self.assembly_code.append("call print")
                self.assembly_code.append("add esp, 4")
                self.deallocate(reg)
        elif isinstance(node, IfNode):
            # If-elif-else handling
            else_label = self.generate_label()
            elif_label = None
            end_label = self.generate_label()

            # If condition
            condition_reg = self.generate_assembly(node.condition)
            self.assembly_code.append(f"cmp DWORD PTR [{node.condition.left.name}], DWORD PTR [{node.condition.right.name}]")
            self.assembly_code.append(f"jle {else_label}")  # Jump to elif/else if x <= y
            for statement in node.block:
                self.generate_assembly(statement)
            self.assembly_code.append(f"jmp {end_label}")  # Skip elif/else

            # Elif condition
            if node.elif_condition:
                elif_label = self.generate_label()
                self.assembly_code.append(f"{elif_label}:")
                self.assembly_code.append(f"cmp DWORD PTR [{node.elif_condition.left.name}], DWORD PTR [{node.elif_condition.right.name}]")
                self.assembly_code.append(f"jne {else_label}")  # Jump to else if x != y
                for statement in node.elif_block:
                    self.generate_assembly(statement)
                self.assembly_code.append(f"jmp {end_label}")

            # Else block
            self.assembly_code.append(f"{else_label}:")
            if node.else_block:
                for statement in node.else_block:
                    self.generate_assembly(statement)

            # End of if-elif-else
            self.assembly_code.append(f"{end_label}:")
            self.deallocate(condition_reg)
        elif isinstance(node, WhileNode):
            start_label = self.generate_label()
            end_label = self.generate_label()

            # Start of the loop
            self.assembly_code.append(f"{start_label}:")

            # Evaluate the loop condition
            condition_reg = self.generate_assembly(node.condition.left)
            compare_value = self.generate_assembly(node.condition.right)
            self.assembly_code.append(f"cmp {condition_reg}, {compare_value}")
            self.assembly_code.append(f"jge {end_label}")  # Exit loop if count >= 3
            self.deallocate(compare_value)

            # Loop body
            for statement in node.block:
                self.generate_assembly(statement)

            # Jump back to the start of the loop
            self.assembly_code.append(f"jmp {start_label}")

            # End of loop
            self.assembly_code.append(f"{end_label}:")
            self.deallocate(condition_reg)
        elif isinstance(node, ForNode):
            start_label = self.generate_label()
            end_label = self.generate_label()
            counter_reg = self.allocate()
            collection_reg = self.allocate()

            # Generate code to get the collection
            self.generate_assembly(node.collection)
            self.assembly_code.append(f"mov {collection_reg}, eax")

            # Initialize counter
            self.assembly_code.append(f"mov {counter_reg}, 0")

            # Start of loop
            self.assembly_code.append(f"{start_label}:")

            # Compare counter with collection length
            self.assembly_code.append(f"cmp {counter_reg}, [len_{collection_reg}]")
            self.assembly_code.append(f"jge {end_label}")

            # Get current element
            self.assembly_code.append(f"mov eax, [{collection_reg} + {counter_reg} * 4]")
            self.assembly_code.append(f"mov [{node.variable.name}], eax")

            # Generate code for loop body
            for statement in node.block:
                self.generate_assembly(statement)

            # Increment counter
            self.assembly_code.append(f"inc {counter_reg}")
            self.assembly_code.append(f"jmp {start_label}")

            # End of loop
            self.assembly_code.append(f"{end_label}:")

            self.deallocate(counter_reg)
            self.deallocate(collection_reg)


    def print_assembly(self):
        for line in self.assembly_code:
            print(line)
