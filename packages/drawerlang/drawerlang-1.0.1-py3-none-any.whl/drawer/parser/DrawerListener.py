# Generated from Drawer.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .DrawerParser import DrawerParser
else:
    from DrawerParser import DrawerParser

# This class defines a complete listener for a parse tree produced by DrawerParser.
class DrawerListener(ParseTreeListener):

    # Enter a parse tree produced by DrawerParser#prog.
    def enterProg(self, ctx:DrawerParser.ProgContext):
        pass

    # Exit a parse tree produced by DrawerParser#prog.
    def exitProg(self, ctx:DrawerParser.ProgContext):
        pass


    # Enter a parse tree produced by DrawerParser#stat.
    def enterStat(self, ctx:DrawerParser.StatContext):
        pass

    # Exit a parse tree produced by DrawerParser#stat.
    def exitStat(self, ctx:DrawerParser.StatContext):
        pass


    # Enter a parse tree produced by DrawerParser#originStat.
    def enterOriginStat(self, ctx:DrawerParser.OriginStatContext):
        pass

    # Exit a parse tree produced by DrawerParser#originStat.
    def exitOriginStat(self, ctx:DrawerParser.OriginStatContext):
        pass


    # Enter a parse tree produced by DrawerParser#rotStat.
    def enterRotStat(self, ctx:DrawerParser.RotStatContext):
        pass

    # Exit a parse tree produced by DrawerParser#rotStat.
    def exitRotStat(self, ctx:DrawerParser.RotStatContext):
        pass


    # Enter a parse tree produced by DrawerParser#scaleStat.
    def enterScaleStat(self, ctx:DrawerParser.ScaleStatContext):
        pass

    # Exit a parse tree produced by DrawerParser#scaleStat.
    def exitScaleStat(self, ctx:DrawerParser.ScaleStatContext):
        pass


    # Enter a parse tree produced by DrawerParser#colorStat.
    def enterColorStat(self, ctx:DrawerParser.ColorStatContext):
        pass

    # Exit a parse tree produced by DrawerParser#colorStat.
    def exitColorStat(self, ctx:DrawerParser.ColorStatContext):
        pass


    # Enter a parse tree produced by DrawerParser#pixsizeStat.
    def enterPixsizeStat(self, ctx:DrawerParser.PixsizeStatContext):
        pass

    # Exit a parse tree produced by DrawerParser#pixsizeStat.
    def exitPixsizeStat(self, ctx:DrawerParser.PixsizeStatContext):
        pass


    # Enter a parse tree produced by DrawerParser#forStat.
    def enterForStat(self, ctx:DrawerParser.ForStatContext):
        pass

    # Exit a parse tree produced by DrawerParser#forStat.
    def exitForStat(self, ctx:DrawerParser.ForStatContext):
        pass


    # Enter a parse tree produced by DrawerParser#drawStat.
    def enterDrawStat(self, ctx:DrawerParser.DrawStatContext):
        pass

    # Exit a parse tree produced by DrawerParser#drawStat.
    def exitDrawStat(self, ctx:DrawerParser.DrawStatContext):
        pass


    # Enter a parse tree produced by DrawerParser#colorLit.
    def enterColorLit(self, ctx:DrawerParser.ColorLitContext):
        pass

    # Exit a parse tree produced by DrawerParser#colorLit.
    def exitColorLit(self, ctx:DrawerParser.ColorLitContext):
        pass


    # Enter a parse tree produced by DrawerParser#value.
    def enterValue(self, ctx:DrawerParser.ValueContext):
        pass

    # Exit a parse tree produced by DrawerParser#value.
    def exitValue(self, ctx:DrawerParser.ValueContext):
        pass


    # Enter a parse tree produced by DrawerParser#expr.
    def enterExpr(self, ctx:DrawerParser.ExprContext):
        pass

    # Exit a parse tree produced by DrawerParser#expr.
    def exitExpr(self, ctx:DrawerParser.ExprContext):
        pass


    # Enter a parse tree produced by DrawerParser#valueExpr.
    def enterValueExpr(self, ctx:DrawerParser.ValueExprContext):
        pass

    # Exit a parse tree produced by DrawerParser#valueExpr.
    def exitValueExpr(self, ctx:DrawerParser.ValueExprContext):
        pass


    # Enter a parse tree produced by DrawerParser#wrappedExpr.
    def enterWrappedExpr(self, ctx:DrawerParser.WrappedExprContext):
        pass

    # Exit a parse tree produced by DrawerParser#wrappedExpr.
    def exitWrappedExpr(self, ctx:DrawerParser.WrappedExprContext):
        pass


    # Enter a parse tree produced by DrawerParser#funcCallExpr.
    def enterFuncCallExpr(self, ctx:DrawerParser.FuncCallExprContext):
        pass

    # Exit a parse tree produced by DrawerParser#funcCallExpr.
    def exitFuncCallExpr(self, ctx:DrawerParser.FuncCallExprContext):
        pass


    # Enter a parse tree produced by DrawerParser#sigExpr.
    def enterSigExpr(self, ctx:DrawerParser.SigExprContext):
        pass

    # Exit a parse tree produced by DrawerParser#sigExpr.
    def exitSigExpr(self, ctx:DrawerParser.SigExprContext):
        pass



del DrawerParser