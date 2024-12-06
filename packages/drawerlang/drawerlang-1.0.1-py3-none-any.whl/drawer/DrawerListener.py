from antlr4 import Token
from .SymbolTable import SymbolTable
from .parser.DrawerListener import DrawerListener as DrawerBaseListener
import webcolors
import math

class DrawerListener(DrawerBaseListener):
    def __init__(self):
        super().__init__()
        self.commands = []

    def enterProg(self, ctx):
        ctx.table = SymbolTable({
            'pi': math.pi,
            'cos': math.cos,
            'sin': math.sin,
            'abs': abs,
            'log': math.log,
            'exp': math.exp,
            'sqrt': math.sqrt,
            'tan': math.tan,
        })

    def enterEveryRule(self, ctx):
        if ctx.parentCtx:
            ctx.table = ctx.parentCtx.table

    def enterForStat(self, ctx):
        ctx.table = ctx.parentCtx.table.push()

    def exitExpr(self, ctx):
        if ctx.op1:
            match ctx.op1.text:
                case '+':
                    ctx.getValue = lambda: ctx.expr(0).getValue() + ctx.expr(1).getValue()
                case '-':
                    ctx.getValue = lambda: ctx.expr(0).getValue() - ctx.expr(1).getValue()
        elif ctx.op2:
            match ctx.op2.text:
                case '*':
                    ctx.getValue = lambda: ctx.expr(0).getValue() * ctx.expr(1).getValue()
                case '/':
                    ctx.getValue = lambda: ctx.expr(0).getValue() / ctx.expr(1).getValue()
        else:
            ctx.getValue = lambda: ctx.getChild(0).getValue()

    def exitValueExpr(self, ctx):
        ctx.getValue = lambda: ctx.value().getValue()

    def exitWrappedExpr(self, ctx):
        ctx.getValue = lambda: ctx.expr().getValue()

    def exitFuncCallExpr(self, ctx):
        ctx.getValue = lambda: ctx.table[ctx.ID().getText().lower()](ctx.expr().getValue())

    def exitSigExpr(self, ctx):
        ctx.getValue = (lambda: ctx.expr().getValue()) if ctx.sig.text == '+' else (lambda: -ctx.expr().getValue())


    def exitForStat(self, ctx):
        initValue = ctx.expr(0).getValue()
        endValue = ctx.expr(1).getValue()
        step = ctx.expr(2).getValue()
        hasVariable = ctx.ID() is not None
        if hasVariable:
            # 这里的 ctx.table 能直接访问到 enterProg 中的 ctx.table
            ctx.table[ctx.ID().getText().lower()] = initValue
        while initValue <= endValue:
            xValue = ctx.expr(3).getValue()
            yValue = ctx.expr(4).getValue()
            self.draw(xValue, yValue)
            ctx.table[ctx.ID().getText().lower()] = initValue
            initValue += step
            ctx.table.pop()

    def exitValue(self, ctx):
        ctx.getValue = lambda: (float(ctx.NUM().getText()) if ctx.NUM() else ctx.table[ctx.ID().getText().lower()])

    def exitColorStat(self, ctx):
        self.color(ctx.colorLit().getColor())

    def exitColorLit(self, ctx):
        if ctx.name:
            ctx.getColor = lambda: tuple(v for v in webcolors.name_to_rgb(ctx.name.text))
        elif ctx.red:
            ctx.getColor = lambda: (ctx.red.getValue(), ctx.green.getValue(), ctx.blue.getValue(), ctx.alpha.getValue() if ctx.alpha else 255)
        elif ctx.hue:
            ctx.getColor = lambda: (webcolors.hsv_to_rgb(ctx.hue.getValue(), ctx.saturation.getValue(), ctx.lightness.getValue(), ctx.alpha.getValue() if ctx.alpha else 255))
        elif ctx.HEX():
            ctx.getColor = lambda: tuple(v for v in webcolors.hex_to_rgb(ctx.HEX().getText()))

    def exitScaleStat(self, ctx):
        self.scale(ctx.expr(0).getValue(), float(ctx.expr(1).getValue()))

    def exitDrawStat(self, ctx):
        self.draw(float(ctx.expr(0).getValue(), ctx.expr(1).getValue()))

    def exitOriginStat(self, ctx):
        self.origin(ctx.expr(0).getValue(), float(ctx.expr(1).getValue()))

    def exitRotStat(self, ctx):
        self.rotate(ctx.expr().getValue())

    def exitPixsizeStat(self, ctx):
        self.pixsize(ctx.expr().getValue())

    def exitProg(self, ctx):
        ctx.commands = self.commands

    def draw(self, x, y):
        self.commands.append(('draw', x, y))

    def color(self, color: tuple[int, int, int, int]):
        self.commands.append(('color', color))

    def scale(self, x, y):
        self.commands.append(('scale', x, y))

    def origin(self, x, y):
        self.commands.append(('origin', x, y))

    def rotate(self, angle):
        self.commands.append(('rotate', angle))

    def pixsize(self, size):
        self.commands.append(('pixsize', size))

__all__ = ['DrawerListener']
