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
    code: str = None, *, path: str = None, encoding: str = "utf-8"
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


def to_graph(cs_tree: ParserRuleContext, path: str = None) -> MultiDiGraph:
    visitor = GraphVisitor()
    cs_tree.accept(visitor)
    return visitor.graph


class Node:
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.name + str(self.id))


class GraphVisitor(LagraphVisitor):
    def __init__(self):
        self.graph = MultiDiGraph()
        self.idx = 0

    def next_id(self) -> int:
        self.idx += 1
        return self.idx

    def visitProg(self, ctx: LagraphParser.ProgContext):
        node = Node("program", self.next_id())
        self.graph.add_node(node)

        for i, s in enumerate(ctx.s):
            child = s.accept(self)
            self.graph.add_edge(node, child, str(i))
        return node

    def visitBind(self, ctx: LagraphParser.BindContext):
        node = Node("let", self.next_id())
        self.graph.add_node(node)
        var_name = (ctx.name).accept(self)
        self.graph.add_edge(node, var_name, "name")
        val = (ctx.value).accept(self)
        self.graph.add_edge(node, val, "value")
        return node

    def visitInt_literal(self, ctx: LagraphParser.Int_literalContext):
        node = Node(ctx.value.text, self.next_id())
        self.graph.add_node(node)
        return node

    def visitVar_node(self, ctx: LagraphParser.Var_nodeContext):
        node = Node(ctx.value.text, self.next_id())
        self.graph.add_node(node)
        return node

    def visitString_literal(self, ctx: LagraphParser.String_literalContext):
        node = Node(ctx.value.text, self.next_id())
        self.graph.add_node(node)
        return node

    # def visitVal(self, ctx: LagraphParser.ValContext):
    #     node = None
    #     if ctx.intGenerator() is not None:
    #         node = f"int gen {self.next_id()}"
    #     elif ctx.INT() is not None:
    #         node = f"INT {self.next_id()}: {ctx.INT()}"
    #     elif ctx.STRING() is not None:
    #         node = f"STRING {self.next_id()}: {ctx.STRING()}"

    #     self.graph.add_node(node)
    #     return node

    # def visitVar_list(self, ctx: LagraphParser.Var_listContext):
    #     node = Node(self.next_id(), label="var list")
    #     self.graph.add_node(node)

    #     for i, s in enumerate(ctx.var_list):
    #         child = s.accept(self)

    #         self.graph.add_edge(Edge(node, child, label=str(i)))

    #     return node
