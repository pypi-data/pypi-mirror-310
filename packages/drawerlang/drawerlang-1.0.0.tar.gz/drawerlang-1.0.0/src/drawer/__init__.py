from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker
from .DrawerListener import DrawerListener
from .parser.DrawerLexer import DrawerLexer
from .parser.DrawerParser import DrawerParser

def drawer_parse(src: str) -> list[tuple]:
    # 创建词法分析器
    lexer = DrawerLexer(InputStream(src))

    # 创建词标记流
    stream = CommonTokenStream(lexer)

    # 创建语法解析器
    parser = DrawerParser(stream)

    # 创建解析树
    tree = parser.prog()

    walker = ParseTreeWalker()

    walker.walk(DrawerListener(), tree)

    return tree.commands

del CommonTokenStream, InputStream, ParseTreeWalker, DrawerListener, DrawerLexer, DrawerParser

__all__ = ['drawer_parse']
