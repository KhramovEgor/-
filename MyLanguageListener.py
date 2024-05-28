# Generated from MyLanguage.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .MyLanguageParser import MyLanguageParser
else:
    from MyLanguageParser import MyLanguageParser

# This class defines a complete listener for a parse tree produced by MyLanguageParser.
class MyLanguageListener(ParseTreeListener):

    # Enter a parse tree produced by MyLanguageParser#program.
    def enterProgram(self, ctx:MyLanguageParser.ProgramContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#program.
    def exitProgram(self, ctx:MyLanguageParser.ProgramContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#statement.
    def enterStatement(self, ctx:MyLanguageParser.StatementContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#statement.
    def exitStatement(self, ctx:MyLanguageParser.StatementContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#assignmentStatement.
    def enterAssignmentStatement(self, ctx:MyLanguageParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#assignmentStatement.
    def exitAssignmentStatement(self, ctx:MyLanguageParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#ifStatement.
    def enterIfStatement(self, ctx:MyLanguageParser.IfStatementContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#ifStatement.
    def exitIfStatement(self, ctx:MyLanguageParser.IfStatementContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#ifElseStatement.
    def enterIfElseStatement(self, ctx:MyLanguageParser.IfElseStatementContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#ifElseStatement.
    def exitIfElseStatement(self, ctx:MyLanguageParser.IfElseStatementContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#ifBody.
    def enterIfBody(self, ctx:MyLanguageParser.IfBodyContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#ifBody.
    def exitIfBody(self, ctx:MyLanguageParser.IfBodyContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#elseBody.
    def enterElseBody(self, ctx:MyLanguageParser.ElseBodyContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#elseBody.
    def exitElseBody(self, ctx:MyLanguageParser.ElseBodyContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#forStatement.
    def enterForStatement(self, ctx:MyLanguageParser.ForStatementContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#forStatement.
    def exitForStatement(self, ctx:MyLanguageParser.ForStatementContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#forInit.
    def enterForInit(self, ctx:MyLanguageParser.ForInitContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#forInit.
    def exitForInit(self, ctx:MyLanguageParser.ForInitContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#forModify.
    def enterForModify(self, ctx:MyLanguageParser.ForModifyContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#forModify.
    def exitForModify(self, ctx:MyLanguageParser.ForModifyContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#forBody.
    def enterForBody(self, ctx:MyLanguageParser.ForBodyContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#forBody.
    def exitForBody(self, ctx:MyLanguageParser.ForBodyContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#whileStatement.
    def enterWhileStatement(self, ctx:MyLanguageParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#whileStatement.
    def exitWhileStatement(self, ctx:MyLanguageParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#whileBody.
    def enterWhileBody(self, ctx:MyLanguageParser.WhileBodyContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#whileBody.
    def exitWhileBody(self, ctx:MyLanguageParser.WhileBodyContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#functionStatement.
    def enterFunctionStatement(self, ctx:MyLanguageParser.FunctionStatementContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#functionStatement.
    def exitFunctionStatement(self, ctx:MyLanguageParser.FunctionStatementContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#return.
    def enterReturn(self, ctx:MyLanguageParser.ReturnContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#return.
    def exitReturn(self, ctx:MyLanguageParser.ReturnContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#functionArgs.
    def enterFunctionArgs(self, ctx:MyLanguageParser.FunctionArgsContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#functionArgs.
    def exitFunctionArgs(self, ctx:MyLanguageParser.FunctionArgsContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#functionBody.
    def enterFunctionBody(self, ctx:MyLanguageParser.FunctionBodyContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#functionBody.
    def exitFunctionBody(self, ctx:MyLanguageParser.FunctionBodyContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#functionName.
    def enterFunctionName(self, ctx:MyLanguageParser.FunctionNameContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#functionName.
    def exitFunctionName(self, ctx:MyLanguageParser.FunctionNameContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#funcType.
    def enterFuncType(self, ctx:MyLanguageParser.FuncTypeContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#funcType.
    def exitFuncType(self, ctx:MyLanguageParser.FuncTypeContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#functionExpr.
    def enterFunctionExpr(self, ctx:MyLanguageParser.FunctionExprContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#functionExpr.
    def exitFunctionExpr(self, ctx:MyLanguageParser.FunctionExprContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#functionParams.
    def enterFunctionParams(self, ctx:MyLanguageParser.FunctionParamsContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#functionParams.
    def exitFunctionParams(self, ctx:MyLanguageParser.FunctionParamsContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#functionCall.
    def enterFunctionCall(self, ctx:MyLanguageParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#functionCall.
    def exitFunctionCall(self, ctx:MyLanguageParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#printState.
    def enterPrintState(self, ctx:MyLanguageParser.PrintStateContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#printState.
    def exitPrintState(self, ctx:MyLanguageParser.PrintStateContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#printBody.
    def enterPrintBody(self, ctx:MyLanguageParser.PrintBodyContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#printBody.
    def exitPrintBody(self, ctx:MyLanguageParser.PrintBodyContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#equation.
    def enterEquation(self, ctx:MyLanguageParser.EquationContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#equation.
    def exitEquation(self, ctx:MyLanguageParser.EquationContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#comparison.
    def enterComparison(self, ctx:MyLanguageParser.ComparisonContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#comparison.
    def exitComparison(self, ctx:MyLanguageParser.ComparisonContext):
        pass


    # Enter a parse tree produced by MyLanguageParser#expr.
    def enterExpr(self, ctx:MyLanguageParser.ExprContext):
        pass

    # Exit a parse tree produced by MyLanguageParser#expr.
    def exitExpr(self, ctx:MyLanguageParser.ExprContext):
        pass



del MyLanguageParser