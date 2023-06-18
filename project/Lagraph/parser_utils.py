from antlr4 import (
    CommonTokenStream,
    InputStream,
    FileStream,
    StdinStream,
    ParserRuleContext,
)
from antlr4.error.ErrorListener import ErrorListener
from networkx.drawing.nx_pydot import to_pydot
from networkx import MultiDiGraph
from project.Lagraph.Parser import GraphVisitor
from project.antlr_out.Lagraph.LagraphLexer import LagraphLexer


from project.antlr_out.Lagraph.LagraphParser import LagraphParser


class ExceptionListener(ErrorListener):
    """Listener raising syntax exception"""

    def __init__(self):
        super(ExceptionListener, self).__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise SyntaxException(
            f'Syntax error "{offendingSymbol}" at line: {line}, column: {column}, msg:{msg}, e:{str(e)}'
        )


class SyntaxException(Exception):
    """Exception using for syntax error"""

    def __init__(self, msg: str):
        self.msg = msg

    def __repr__(self):
        return self.msg


def parse(source: InputStream) -> LagraphParser.ProgContext:
    """
    Checks the syntax of the program
    code in the `Lagraph` language from InputStream
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
    code: str = None, *, path: str = None, encoding: str = "utf-8"
) -> LagraphParser.ProgContext:
    """
    Checks the syntax of the program
    code in the `Lagraph` language from different sources.
    """
    if code is not None:
        stream = InputStream(code)

    elif path is not None:
        stream = FileStream(path, encoding=encoding)

    else:
        stream = StdinStream(encoding=encoding)

    return parse(stream)


def is_valid_syntax(
    code: str = None, *, path: str = None, encoding: str = "utf-8"
) -> bool:
    """
    Check that the syntax of the program
    code is correct.
    """
    try:
        parse_from(code=code, path=path, encoding=encoding)

    except SyntaxException as e:
        return False

    return True


def to_dot(cs_tree: ParserRuleContext) -> str:
    """
    Return AST representation in DOT string
    """
    graph = to_pydot(to_graph(cs_tree)).to_string()
    return graph


def to_graph(cs_tree: ParserRuleContext) -> MultiDiGraph:
    """
    Represent ANTLR CST as MultiDiGraph of AST
    """
    visitor = GraphVisitor()
    cs_tree.accept(visitor)
    return visitor.graph
