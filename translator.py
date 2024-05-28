import json
from llvmlite import ir

class LLVMTranslator:
    def __init__(self):
        self.module = ir.Module(name="my_module")
        self.builder = None
        self.func_symtab = {}

    def translate_program(self, ast):
        main_type = ir.FunctionType(ir.IntType(32), [])
        main_func = ir.Function(self.module, main_type, name="main")
        block = main_func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        self.create_global_fmt_str()
        self.func_symtab = {}

        for child in ast['children']:
            if child['node_type'] == "functionCall":
                self.main_func_call = child
            else:
                self.translate_statement(child)

        if not self.builder.block.is_terminated:
            if hasattr(self, 'main_func_call'):
                self.translate_function_call(self.main_func_call)
            self.builder.ret(ir.Constant(ir.IntType(32), 0))

    def create_global_fmt_str(self):
        int_fmt_str = ir.GlobalVariable(self.module, ir.ArrayType(ir.IntType(8), len("%d\n") + 1), name="int_fmt_str")
        int_fmt_str.initializer = ir.Constant(ir.ArrayType(ir.IntType(8), len("%d\n") + 1), bytearray(b"%d\n\00"))
        self.int_fmt_str_ptr = self.builder.bitcast(int_fmt_str, ir.IntType(8).as_pointer())

        float_fmt_str = ir.GlobalVariable(self.module, ir.ArrayType(ir.IntType(8), len("%.6f\n") + 1),
                                          name="float_fmt_str")
        float_fmt_str.initializer = ir.Constant(ir.ArrayType(ir.IntType(8), len("%.6f\n") + 1), bytearray(b"%.6f\n\00"))
        self.float_fmt_str_ptr = self.builder.bitcast(float_fmt_str, ir.IntType(8).as_pointer())

    def translate_statement(self, node):
        node_type = node['node_type']
        if node_type == "for":
            self.translate_for(node)
        elif node_type == "while":
            self.translate_while(node)
        elif node_type == "ifElse":
            self.translate_if_else(node)
        elif node_type == "print":
            self.translate_print(node)
        elif node_type == "assignment":
            self.translate_assignment(node)
        elif node_type == "function":
            self.translate_function(node)
        elif node_type == "return":
            self.translate_return(node)
        elif node_type == "functionCall":
            # We'll handle the main function call separately
            pass
        else:
            raise ValueError(f"Unknown node type: {node_type}")

    def translate_function(self, node):
        func_name = node['children'][1]['value']
        func_args = node['children'][2]['children']
        func_body = node['children'][3]

        arg_types = [ir.IntType(32) for _ in func_args]  # Assuming all arguments are integers for simplicity
        func_type = ir.FunctionType(ir.IntType(32), arg_types)
        function = ir.Function(self.module, func_type, name=func_name)
        block = function.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)

        for i, arg in enumerate(function.args):
            arg_name = func_args[i]['value']
            arg.name = arg_name
            ptr = self.builder.alloca(arg.type, name=arg_name)
            self.builder.store(arg, ptr)
            self.func_symtab[arg_name] = ptr

        self.translate_statements(func_body['children'])

    def translate_return(self, node):
        return_value = self.translate_expression(node['children'][0])
        self.builder.ret(return_value)

    def translate_function_call(self, node):
        function_name = node['children'][0]['value']
        function_args = [self.translate_expression(arg) for arg in node['children'][1:]]
        function = self.module.get_global(function_name)
        if not function:
            raise ValueError(f"Function '{function_name}' is not defined")
        return self.builder.call(function, function_args)

    def translate_for(self, node):
        init_node = node['children'][0]
        condition_node = node['children'][1]
        modify_node = node['children'][2]
        body_node = node['children'][3]

        self.translate_for_init(init_node)

        loop_condition_block = self.builder.append_basic_block(name="loop_condition")
        loop_body_block = self.builder.append_basic_block(name="loop_body")
        loop_modify_block = self.builder.append_basic_block(name="loop_modify")
        after_loop_block = self.builder.append_basic_block(name="after_loop")

        self.builder.branch(loop_condition_block)

        self.builder.position_at_end(loop_condition_block)
        cond_value = self.translate_expression(condition_node)
        self.builder.cbranch(cond_value, loop_body_block, after_loop_block)

        self.builder.position_at_end(loop_body_block)
        self.translate_statements(body_node['children'])
        self.builder.branch(loop_modify_block)

        self.builder.position_at_end(loop_modify_block)
        self.translate_for_modify(modify_node)
        self.builder.branch(loop_condition_block)

        self.builder.position_at_end(after_loop_block)

    def translate_for_init(self, node):
        var_name = node['children'][1]['value']
        initial_value = self.translate_expression(node['children'][2])
        ptr = self.builder.alloca(initial_value.type, name=var_name)
        self.func_symtab[var_name] = ptr
        self.builder.store(initial_value, ptr)

    def translate_for_modify(self, node):
        if node['children'][1]['value'] == "++":
            var_name = node['children'][0]['value']
            var_ptr = self.func_symtab.get(var_name)
            if not var_ptr:
                raise ValueError(f"Variable '{var_name}' is not defined")
            var_value = self.builder.load(var_ptr)
            new_value = self.builder.add(var_value, ir.Constant(ir.IntType(32), 1))
            self.builder.store(new_value, var_ptr)
        elif node['children'][1]['value'] == "--":
            var_name = node['children'][0]['value']
            var_ptr = self.func_symtab.get(var_name)
            if not var_ptr:
                raise ValueError(f"Variable '{var_name}' is not defined")
            var_value = self.builder.load(var_ptr)
            new_value = self.builder.sub(var_value, ir.Constant(ir.IntType(32), 1))
            self.builder.store(new_value, var_ptr)
        else:
            raise ValueError(f"Unknown operation in forModify: {node['children'][1]['value']}")

    def translate_while(self, node):
        condition_node = node['children'][0]
        body_node = node['children'][1]

        loop_condition_block = self.builder.append_basic_block(name="loop_condition")
        loop_body_block = self.builder.append_basic_block(name="loop_body")
        after_loop_block = self.builder.append_basic_block(name="after_loop")

        self.builder.branch(loop_condition_block)

        self.builder.position_at_end(loop_condition_block)
        cond_value = self.translate_expression(condition_node)
        self.builder.cbranch(cond_value, loop_body_block, after_loop_block)

        self.builder.position_at_end(loop_body_block)
        self.translate_statements(body_node['children'])
        self.builder.branch(loop_condition_block)

        self.builder.position_at_end(after_loop_block)

    def translate_if_else(self, node):
        condition_node = node['children'][0]
        if_body_node = node['children'][1]
        else_body_node = node['children'][2]

        if_block = self.builder.append_basic_block(name="if_block")
        else_block = self.builder.append_basic_block(name="else_block")
        merge_block = self.builder.append_basic_block(name="merge_block")

        cond_value = self.translate_expression(condition_node)
        self.builder.cbranch(cond_value, if_block, else_block)

        self.builder.position_at_end(if_block)
        self.translate_statements(if_body_node['children'])
        self.builder.branch(merge_block)

        self.builder.position_at_end(else_block)
        self.translate_statements(else_body_node['children'])
        self.builder.branch(merge_block)

        self.builder.position_at_end(merge_block)

    def translate_print(self, node):
        value = self.translate_expression(node['children'][0])
        print_func = self.module.globals.get("printf")
        if not print_func:
            voidptr_ty = ir.IntType(8).as_pointer()
            print_func_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
            print_func = ir.Function(self.module, print_func_ty, name="printf")

        if isinstance(value.type, ir.IntType):
            self.builder.call(print_func, [self.int_fmt_str_ptr, value])
        elif isinstance(value.type, ir.DoubleType):
            self.builder.call(print_func, [self.float_fmt_str_ptr, value])
        else:
            raise ValueError(f"Unsupported type for print: {value.type}")

    def translate_assignment(self, node):
        var_name = node['children'][0]['value']
        value = self.translate_expression(node['children'][1])
        if var_name not in self.func_symtab:
            ptr = self.builder.alloca(value.type, name=var_name)
            self.func_symtab[var_name] = ptr
        else:
            ptr = self.func_symtab[var_name]
        self.builder.store(value, ptr)

    def translate_expression(self, node):
        if node['node_type'] == "int":
            return ir.Constant(ir.IntType(32), node['value'])
        elif node['node_type'] == "float":
            return ir.Constant(ir.DoubleType(), node['value'])
        elif node['node_type'] == "ID":
            ptr = self.func_symtab.get(node['value'])
            if not ptr:
                raise ValueError(f"Variable '{node['value']}' is not defined")
            return self.builder.load(ptr)
        elif node['node_type'] == '<':
            left = self.translate_expression(node['children'][0])
            right = self.translate_expression(node['children'][1])
            if isinstance(left.type, ir.DoubleType) or isinstance(right.type, ir.DoubleType):
                if isinstance(left.type, ir.IntType) and left.type.width == 32:
                    left = self.builder.sitofp(left, ir.DoubleType())
                if isinstance(right.type, ir.IntType) and right.type.width == 32:
                    right = self.builder.sitofp(right, ir.DoubleType())
                return self.builder.fcmp_ordered('<', left, right)
            else:
                return self.builder.icmp_signed('<', left, right)
        elif node['node_type'] == '>':
            left = self.translate_expression(node['children'][0])
            right = self.translate_expression(node['children'][1])
            if isinstance(left.type, ir.DoubleType) or isinstance(right.type, ir.DoubleType):
                if isinstance(left.type, ir.IntType) and left.type.width == 32:
                    left = self.builder.sitofp(left, ir.DoubleType())
                if isinstance(right.type, ir.IntType) and right.type.width == 32:
                    right = self.builder.sitofp(right, ir.DoubleType())
                return self.builder.fcmp_ordered('>', left, right)
            else:
                return self.builder.icmp_signed('>', left, right)
        elif node['node_type'] == '==':
            left = self.translate_expression(node['children'][0])
            right = self.translate_expression(node['children'][1])
            if isinstance(left.type, ir.DoubleType) or isinstance(right.type, ir.DoubleType):
                if isinstance(left.type, ir.IntType) and left.type.width == 32:
                    left = self.builder.sitofp(left, ir.DoubleType())
                if isinstance(right.type, ir.IntType) and right.type.width == 32:
                    right = self.builder.sitofp(right, ir.DoubleType())
                return self.builder.fcmp_ordered('==', left, right)
            else:
                return self.builder.icmp_signed('==', left, right)
        elif node['node_type'] == '!=':
            left = self.translate_expression(node['children'][0])
            right = self.translate_expression(node['children'][1])
            if isinstance(left.type, ir.DoubleType) or isinstance(right.type, ir.DoubleType):
                if isinstance(left.type, ir.IntType) and left.type.width == 32:
                    left = self.builder.sitofp(left, ir.DoubleType())
                if isinstance(right.type, ir.IntType) and right.type.width == 32:
                    right = self.builder.sitofp(right, ir.DoubleType())
                return self.builder.fcmp_ordered('!=', left, right)
            else:
                return self.builder.icmp_signed('!=', left, right)
        elif node['node_type'] == '+':
            left = self.translate_expression(node['children'][0])
            right = self.translate_expression(node['children'][1])
            if isinstance(left.type, ir.DoubleType) or isinstance(right.type, ir.DoubleType):
                if isinstance(left.type, ir.IntType) and left.type.width == 32:
                    left = self.builder.sitofp(left, ir.DoubleType())
                if isinstance(right.type, ir.IntType) and right.type.width == 32:
                    right = self.builder.sitofp(right, ir.DoubleType())
                return self.builder.fadd(left, right)
            else:
                return self.builder.add(left, right)
        elif node['node_type'] == '-':
            left = self.translate_expression(node['children'][0])
            right = self.translate_expression(node['children'][1])
            if isinstance(left.type, ir.DoubleType) or isinstance(right.type, ir.DoubleType):
                if isinstance(left.type, ir.IntType) and left.type.width == 32:
                    left = self.builder.sitofp(left, ir.DoubleType())
                if isinstance(right.type, ir.IntType) and right.type.width == 32:
                    right = self.builder.sitofp(right, ir.DoubleType())
                return self.builder.fsub(left, right)
            else:
                return self.builder.sub(left, right)
        elif node['node_type'] == '*':
            left = self.translate_expression(node['children'][0])
            right = self.translate_expression(node['children'][1])
            if isinstance(left.type, ir.DoubleType) or isinstance(right.type, ir.DoubleType):
                if isinstance(left.type, ir.IntType) and left.type.width == 32:
                    left = self.builder.sitofp(left, ir.DoubleType())
                if isinstance(right.type, ir.IntType) and right.type.width == 32:
                    right = self.builder.sitofp(right, ir.DoubleType())
                return self.builder.fmul(left, right)
            else:
                return self.builder.mul(left, right)



        elif node['node_type'] == '/':
            left = self.translate_expression(node['children'][0])
            right = self.translate_expression(node['children'][1])
            if isinstance(left.type, ir.DoubleType) or isinstance(right.type, ir.DoubleType):
                if isinstance(left.type, ir.IntType) and left.type.width == 32:
                    left = self.builder.sitofp(left, ir.DoubleType())
                if isinstance(right.type, ir.IntType) and right.type.width == 32:
                    right = self.builder.sitofp(right, ir.DoubleType())
                return self.builder.fdiv(left, right)
            else:
                return self.builder.sdiv(left, right)
        else:
            raise ValueError(f"Unknown node type: {node['node_type']}")

    def translate_statements(self, statements):
        for statement in statements:
            self.translate_statement(statement)

    def generate_code(self):
        return str(self.module)

def load_ast_from_file(filename):
    with open(filename, "r") as file:
        print("Переведено в LLVM")
        return json.load(file)



