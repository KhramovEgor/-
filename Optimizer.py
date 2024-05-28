import json
import math

class ASTOptimizer:
    def __init__(self, ast_file):
        with open(ast_file, 'r') as file:
            self.ast = json.load(file)

    def calculate(self, expr):
        if expr['node_type'] == 'int':
            return expr['value']
        elif expr['node_type'] == 'float':
            return expr['value']
        elif expr['node_type'] == '+':
            return self.calculate(expr['children'][0]) + self.calculate(expr['children'][1])
        elif expr['node_type'] == '-':
            return self.calculate(expr['children'][0]) - self.calculate(expr['children'][1])
        elif expr['node_type'] == '*':
            return self.calculate(expr['children'][0]) * self.calculate(expr['children'][1])
        elif expr['node_type'] == '/':
            return self.calculate(expr['children'][0]) / self.calculate(expr['children'][1])
        elif expr['node_type'] == '^':
            return math.pow(self.calculate(expr['children'][0]), self.calculate(expr['children'][1]))

    def traverse(self, node):
        if 'children' in node:
            for i, child in enumerate(node['children']):
                if isinstance(child, dict):
                    self.traverse(child)
                    if child['node_type'] in ['+', '-', '*', '/', '^']:
                        try:
                            value = self.calculate(child)
                            if isinstance(value, int):
                                node['children'][i] = {'node_type': 'int', 'value': int(value)}
                            else:
                                node['children'][i] = {'node_type': 'float', 'value': float(value)}
                        except:
                            pass
        return node

    def find_used_variables(self, node, used_vars):
        if 'children' in node:
            for child in node['children']:
                if isinstance(child, dict):
                    if child['node_type'] == 'ID':
                        used_vars.add(child['value'])
                    self.find_used_variables(child, used_vars)

    def find_all_variables(self, node, all_vars):
        if 'children' in node:
            for child in node['children']:
                if isinstance(child, dict):
                    if child['node_type'] == 'assignment':
                        var_name = child['children'][0]['value']
                        all_vars.add(var_name)
                    self.find_all_variables(child, all_vars)

    def remove_dead_code(self, node, used_vars, all_vars):
        if 'children' in node:
            new_children = []
            for child in node['children']:
                if isinstance(child, dict):
                    if child['node_type'] == 'assignment':
                        var_name = child['children'][0]['value']
                        if var_name not in used_vars and var_name in all_vars:
                            continue
                    self.remove_dead_code(child, used_vars, all_vars)
                    new_children.append(child)
            node['children'] = new_children

    def remove_redundant_operations(self, node):
        if 'children' in node:
            new_children = []
            for child in node['children']:
                if isinstance(child, dict):
                    if child['node_type'] in ['+', '-', '*', '/']:
                        left = self.calculate(child['children'][0])
                        right = self.calculate(child['children'][1])
                        # Проверяем, являются ли оба операнда константами
                        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                            # Выполняем операцию и добавляем результат в AST
                            if child['node_type'] == '+':
                                result = left + right
                            elif child['node_type'] == '-':
                                result = left - right
                            elif child['node_type'] == '*':
                                result = left * right
                            elif child['node_type'] == '/':
                                result = left / right

                            if isinstance(result, int):
                                new_children.append({'node_type': 'int', 'value': int(result)})
                            else:
                                new_children.append({'node_type': 'float', 'value': float(result)})
                            continue  # Пропускаем добавление текущего узла в дочерние узлы
                # Если необходимо, рекурсивно обрабатываем дочерние узлы
                if isinstance(child, dict):
                    child = self.remove_redundant_operations(child)
                new_children.append(child)
            node['children'] = new_children
        return node

    def optimize(self):
        self.ast = self.traverse(self.ast)

        all_vars = set()
        self.find_all_variables(self.ast, all_vars)

        used_vars = set()
        for child in self.ast['children']:
            if child['node_type'] in ['while', 'print']:
                self.find_used_variables(child, used_vars)

        self.remove_dead_code(self.ast, used_vars, all_vars)
        self.remove_redundant_operations(self.ast)

    def save_ast(self, output_file):
        with open(output_file, 'w') as file:
            json.dump(self.ast, file, indent=2)


def optimize_ast(ast_file, output_file):
    optimizer = ASTOptimizer(ast_file)
    optimizer.optimize()
    optimizer.save_ast(output_file)
