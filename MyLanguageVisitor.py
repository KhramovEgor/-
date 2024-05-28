# Generated from MyLanguage.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .MyLanguageParser import MyLanguageParser
else:
    from MyLanguageParser import MyLanguageParser

# This class defines a complete generic visitor for a parse tree produced by MyLanguageParser.

class MyLanguageVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MyLanguageParser#program.
    def visitProgram(self, ctx:MyLanguageParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#statement.
    def visitStatement(self, ctx:MyLanguageParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:MyLanguageParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#ifStatement.
    def visitIfStatement(self, ctx:MyLanguageParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#ifElseStatement.
    def visitIfElseStatement(self, ctx:MyLanguageParser.IfElseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#ifBody.
    def visitIfBody(self, ctx:MyLanguageParser.IfBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#elseBody.
    def visitElseBody(self, ctx:MyLanguageParser.ElseBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#forStatement.
    def visitForStatement(self, ctx:MyLanguageParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#forInit.
    def visitForInit(self, ctx:MyLanguageParser.ForInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#forModify.
    def visitForModify(self, ctx:MyLanguageParser.ForModifyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#forBody.
    def visitForBody(self, ctx:MyLanguageParser.ForBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#whileStatement.
    def visitWhileStatement(self, ctx:MyLanguageParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#whileBody.
    def visitWhileBody(self, ctx:MyLanguageParser.WhileBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#functionStatement.
    def visitFunctionStatement(self, ctx:MyLanguageParser.FunctionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#return.
    def visitReturn(self, ctx:MyLanguageParser.ReturnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#functionArgs.
    def visitFunctionArgs(self, ctx:MyLanguageParser.FunctionArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#functionBody.
    def visitFunctionBody(self, ctx:MyLanguageParser.FunctionBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#functionName.
    def visitFunctionName(self, ctx:MyLanguageParser.FunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#funcType.
    def visitFuncType(self, ctx:MyLanguageParser.FuncTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#functionExpr.
    def visitFunctionExpr(self, ctx:MyLanguageParser.FunctionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#functionParams.
    def visitFunctionParams(self, ctx:MyLanguageParser.FunctionParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#functionCall.
    def visitFunctionCall(self, ctx:MyLanguageParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#printState.
    def visitPrintState(self, ctx:MyLanguageParser.PrintStateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#printBody.
    def visitPrintBody(self, ctx:MyLanguageParser.PrintBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#equation.
    def visitEquation(self, ctx:MyLanguageParser.EquationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#comparison.
    def visitComparison(self, ctx:MyLanguageParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MyLanguageParser#expr.
    def visitExpr(self, ctx:MyLanguageParser.ExprContext):
        return self.visitChildren(ctx)



del MyLanguageParser