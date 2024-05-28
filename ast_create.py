import json
from antlr4 import *
from MyLanguageLexer import MyLanguageLexer
from MyLanguageParser import MyLanguageParser
from antlr4.error.ErrorListener import ErrorListener

class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception(f"Ошибка на строке {line}:{column} {msg}")

class ASTNode:
    def __init__(self, node_type, children=None, value=None):
        self.node_type = node_type
        self.children = children if children is not None else []
        self.value = value

    def to_dict(self):
        node_dict = {"node_type": self.node_type}
        if self.value is not None:
            node_dict["value"] = self.value
        if self.children:
            node_dict["children"] = [child.to_dict() for child in self.children if child]
        return node_dict

def default_ast_node(obj):
    if isinstance(obj, ASTNode):
        return obj.to_dict()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


class ASTVisitor(ParseTreeVisitor):
    def visitProgram(self, ctx: MyLanguageParser.ProgramContext):
        statements = []
        has_return = False  # Переменная для отслеживания наличия узла return
        for statement_ctx in ctx.statement():
            statement = self.visit(statement_ctx)
            statements.append(statement)
            # Проверяем, есть ли утверждение return
            if isinstance(statement_ctx, MyLanguageParser.ReturnContext):
                has_return = True
        # Если есть утверждение return, добавляем его в список утверждений программы
        if has_return:
            statements.append(self.visitReturn(ctx.return_()))
        return ASTNode("program", children=statements)

    def visitAssignmentStatement(self, ctx: MyLanguageParser.AssignmentStatementContext):
        id_node = ASTNode("ID", value=ctx.ID().getText())
        expr_node = self.visit(ctx.expr())
        return ASTNode("assignment", children=[id_node, expr_node])

    def visitIfStatement(self, ctx: MyLanguageParser.IfStatementContext):
        equation_node = self.visit(ctx.equation())
        body_node = self.visit(ctx.ifBody())
        return ASTNode("if", children=[equation_node, body_node])

    def visitIfElseStatement(self, ctx: MyLanguageParser.IfElseStatementContext):
        equation_node = self.visit(ctx.equation())
        if_body_node = self.visit(ctx.ifBody())
        else_body_node = self.visit(ctx.elseBody())
        return ASTNode("ifElse", children=[equation_node, if_body_node, else_body_node])

    def visitForStatement(self, ctx: MyLanguageParser.ForStatementContext):
        init_node = self.visit(ctx.forInit())
        equation_node = self.visit(ctx.equation())
        modify_node = self.visit(ctx.forModify())
        body_node = self.visit(ctx.forBody())
        return ASTNode("for", children=[init_node, equation_node, modify_node, body_node])

    def visitWhileStatement(self, ctx: MyLanguageParser.WhileStatementContext):
        equation_node = self.visit(ctx.equation())
        body_node = self.visit(ctx.whileBody())
        return ASTNode("while", children=[equation_node, body_node])

    def visitPrintState(self, ctx: MyLanguageParser.PrintStateContext):
        print_body_node = self.visit(ctx.printBody())
        return ASTNode("print", children=[print_body_node])

    def visitFunctionStatement(self, ctx: MyLanguageParser.FunctionStatementContext):
        func_type = ctx.funcType().getText()
        func_name = ctx.functionName().getText()
        args_node = self.visit(ctx.functionArgs()) if ctx.functionArgs() else None
        body_node = self.visit(ctx.functionBody())
        return ASTNode("function", children=[ASTNode("type", value=func_type), ASTNode("name", value=func_name), args_node, body_node])

    def visitFunctionCall(self, ctx: MyLanguageParser.FunctionCallContext):
        func_name = ctx.functionName().getText()
        params = [self.visit(expr_ctx) for expr_ctx in ctx.functionParams().expr()] if ctx.functionParams() else []
        return ASTNode("functionCall", children=[ASTNode("name", value=func_name), *params])

    def visitReturn(self, ctx: MyLanguageParser.ReturnContext):
        if ctx.functionExpr():
            return_expr = self.visit(ctx.functionExpr())
            return ASTNode("return", children=[return_expr])
        else:
            return ASTNode("return")

    def visitExpr(self, ctx: MyLanguageParser.ExprContext):
        if ctx.INT():
            return ASTNode("int", value=int(ctx.INT().getText()))
        elif ctx.FLOAT():
            return ASTNode("float", value=float(ctx.FLOAT().getText()))
        elif ctx.ID():
            return ASTNode("ID", value=ctx.ID().getText())
        elif ctx.expr():
            left_expr = self.visit(ctx.expr(0))
            right_expr = self.visit(ctx.expr(1))
            operator = ctx.getChild(1).getText()
            return ASTNode(operator, children=[left_expr, right_expr])
        elif ctx.functionCall():
            return self.visit(ctx.functionCall())
        else:
            raise ValueError("Invalid expression")

    def visitFunctionExpr(self, ctx: MyLanguageParser.FunctionExprContext):
        if ctx.ID():
            return ASTNode("ID", value=ctx.ID().getText())
        elif ctx.INT():
            return ASTNode("int", value=int(ctx.INT().getText()))
        elif ctx.FLOAT():
            return ASTNode("float", value=float(ctx.FLOAT().getText()))
        elif ctx.functionCall():
            return self.visit(ctx.functionCall())
        else:
            raise ValueError("Invalid function expression")

    def visitEquation(self, ctx: MyLanguageParser.EquationContext):
        left_expr = self.visit(ctx.expr(0))
        right_expr = self.visit(ctx.expr(1))
        operator = ctx.comparison().getText()
        return ASTNode(operator, children=[left_expr, right_expr])

    def visitFunctionArgs(self, ctx: MyLanguageParser.FunctionArgsContext):
        args = [ASTNode("arg", value=arg.getText()) for arg in ctx.ID()]
        return ASTNode("args", children=args)

    def visitFunctionBody(self, ctx: MyLanguageParser.FunctionBodyContext):
        statements = [self.visit(statement_ctx) for statement_ctx in ctx.statement()]
        return ASTNode("functionBody", children=statements)



    def visitPrintBody(self, ctx: MyLanguageParser.PrintBodyContext):
        if ctx.ID():
            return ASTNode("ID", value=ctx.ID().getText())
        elif ctx.INT():
            return ASTNode("int", value=int(ctx.INT().getText()))
        elif ctx.FLOAT():
            return ASTNode("float", value=float(ctx.FLOAT().getText()))
        else:
            raise ValueError("Invalid print body")

    def visitForInit(self, ctx: MyLanguageParser.ForInitContext):
        var_type = ctx.children[0].getText()
        var_id = ctx.ID().getText()
        expr_node = self.visit(ctx.expr())
        return ASTNode("forInit", children=[ASTNode("type", value=var_type), ASTNode("ID", value=var_id), expr_node])

    def visitForModify(self, ctx: MyLanguageParser.ForModifyContext):
        var_id = ctx.ID().getText()
        op = ctx.getChild(1).getText()
        return ASTNode("forModify", children=[ASTNode("ID", value=var_id), ASTNode("op", value=op)])

    def visitIfBody(self, ctx: MyLanguageParser.IfBodyContext):
        statements = [self.visit(statement_ctx) for statement_ctx in ctx.statement()]
        return ASTNode("ifBody", children=statements)

    def visitElseBody(self, ctx: MyLanguageParser.ElseBodyContext):
        statements = [self.visit(statement_ctx) for statement_ctx in ctx.statement()]
        return ASTNode("elseBody", children=statements)

    def visitForBody(self, ctx: MyLanguageParser.ForBodyContext):
        statements = [self.visit(statement_ctx) for statement_ctx in ctx.statement()]
        return ASTNode("forBody", children=statements)

    def visitWhileBody(self, ctx: MyLanguageParser.WhileBodyContext):
        statements = [self.visit(statement_ctx) for statement_ctx in ctx.statement()]
        return ASTNode("whileBody", children=statements)


def create_ast(input_file, output_file):
    with open(input_file, "r") as file:
        input_text = file.read()

    lexer = MyLanguageLexer(InputStream(input_text))
    stream = CommonTokenStream(lexer)
    parser = MyLanguageParser(stream)

    parser.removeErrorListeners()
    parser.addErrorListener(MyErrorListener())

    try:
        tree = parser.program()
    except Exception as e:
        raise Exception(str(e))

    ast_visitor = ASTVisitor()
    ast = ast_visitor.visit(tree)

    with open(output_file, "w") as file:
        ast_dict = ast.to_dict()
        file.write(json.dumps(ast_dict, indent=2))

    print("AST построено")


