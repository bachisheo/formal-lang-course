from antlr4 import (
    CommonTokenStream,
    InputStream,
    FileStream,
    StdinStream,
    ParserRuleContext,
)

from project.antlr_out.Lagraph.LagraphParser import LagraphParser
from ..antlr_out.Lagraph.LagraphParser import LagraphParser
from ..antlr_out.Lagraph.LagraphLexer import LagraphLexer
from ..antlr_out.Lagraph.LagraphVisitor import LagraphVisitor
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import RecognitionException
from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import to_pydot


class ExceptionListener(ErrorListener):
    def __init__(self):
        super(ExceptionListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxException(
            f'Syntax error "{offendingSymbol}" at line: {line}, column: {column}, msg:{msg}, e:{str(e)}'
        )


class SyntaxException(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __repr__(self):
        return self.msg


def parse(source: InputStream) -> LagraphParser.ProgContext:
    """
    Checks the syntax of the program
    code in the `Lagraph` language.
    """
    lexer = LagraphLexer(source)
    lexer.removeErrorListeners()
    lexer.addErrorListener(ExceptionListener())
    parser = LagraphParser(CommonTokenStream(lexer))
    parser.removeErrorListeners()
    parser.addErrorListener(ExceptionListener())
    cs_tree = parser.prog()
    return cs_tree


def parse_from(
    *, code: str = None, path: str = None, encoding: str = "utf-8"
) -> LagraphParser.ProgContext:
    if code is not None:
        stream = InputStream(code)

    elif path is not None:
        stream = FileStream(path, encoding=encoding)

    else:
        stream = StdinStream(encoding=encoding)

    return parse(stream)


def is_valid_syntax(
    code: str = None, *, path: str = None, encoding: str = "utf-8"
) -> LagraphParser.ProgContext:
    try:
        parse_from(code=code, path=path, encoding=encoding)

    except SyntaxException as e:
        return False

    return True


def to_dot(cs_tree: ParserRuleContext, path: str = None) -> str:
    dot_visitor = GraphVisitor()
    cs_tree.accept(dot_visitor)
    return to_pydot(dot_visitor.graph)


class Node:
    def __init__(self, label: str):
        self.label = label


class GraphVisitor(LagraphVisitor):
    def __init__(self):
        self.graph = MultiDiGraph()
        self.graph.name = "ast builded by ANTLR4"
        self.idx = 0

    def next_id(self) -> str:
        self.idx += 1
        return str(self.idx)

    def visitProg(self, ctx: LagraphParser.ProgContext):
        node = Node(self.next_id() + "program")
        self.graph.add_node(node)

        for i, s in enumerate(ctx.statement):
            child = s.accept(self)
            self.graph.add_edge(node, child, str(i))
        return node

    # def visitVar_list(self, ctx: LagraphParser.Var_listContext):
    #     node = Node(self.next_id(), label="var list")
    #     self.graph.add_node(node)

    #     for i, s in enumerate(ctx.var_list):
    #         child = s.accept(self)

    #         self.graph.add_edge(Edge(node, child, label=str(i)))

    #     return node
