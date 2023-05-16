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
) -> LagraphParser.ProgContext:
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

    def visitPrint(self, ctx: LagraphParser.PrintContext):
        node = Node("print", self.next_id())
        self.graph.add_node(node)
        expr = (ctx.exp).accept(self)
        self.graph.add_edge(node, expr)
        return node

    #
    # set/add statements
    #

    def visitExpr_set_start(self, ctx: LagraphParser.Expr_set_startContext):
        node = Node("set_start", self.next_id())
        self.graph.add_node(node)
        verts = (ctx.v).accept(self)
        self.graph.add_edge(node, verts, 0)
        graph = (ctx.g).accept(self)
        self.graph.add_edge(node, graph, 1)
        return node

    def visitExpr_set_final(self, ctx: LagraphParser.Expr_set_finalContext):
        node = Node("set_final", self.next_id())
        self.graph.add_node(node)
        verts = (ctx.v).accept(self)
        self.graph.add_edge(node, verts, 0)
        graph = (ctx.g).accept(self)
        self.graph.add_edge(node, graph, 1)
        return node

    def visitExpr_add_start(self, ctx: LagraphParser.Expr_add_startContext):
        node = Node("add_start", self.next_id())
        self.graph.add_node(node)
        verts = (ctx.v).accept(self)
        self.graph.add_edge(node, verts, 0)
        graph = (ctx.g).accept(self)
        self.graph.add_edge(node, graph, 1)
        return node

    def visitExpr_add_final(self, ctx: LagraphParser.Expr_add_finalContext):
        node = Node("add_final", self.next_id())
        self.graph.add_node(node)
        verts = (ctx.v).accept(self)
        self.graph.add_edge(node, verts, 0)
        graph = (ctx.g).accept(self)
        self.graph.add_edge(node, graph, 1)
        return node

    #
    # of statements
    #
    def visitExpr_starts(self, ctx: LagraphParser.Expr_startsContext):
        """
        visit node with 'startOf' expression"
        """
        node = Node("get_starts", self.next_id())
        self.graph.add_node(node)
        graph = (ctx.g).accept(self)
        self.graph.add_edge(node, graph)
        return node

    def visitExpr_finals(self, ctx: LagraphParser.Expr_finalsContext):
        """
        visit node with 'finalOf' expression"
        """
        node = Node("get_finals", self.next_id())
        self.graph.add_node(node)
        graph = (ctx.g).accept(self)
        self.graph.add_edge(node, graph)
        return node

    def visitExpr_reach(self, ctx: LagraphParser.Expr_reachContext):
        """
        visit node with 'reachableOf' expression"
        """
        node = Node("get_reachable", self.next_id())
        self.graph.add_node(node)
        graph = (ctx.g).accept(self)
        self.graph.add_edge(node, graph)
        return node

    def visitExpr_get_vertex(self, ctx: LagraphParser.Expr_get_vertexContext):
        """
        visit node with 'verticesOf' expression"
        """
        node = Node("get_vertex", self.next_id())
        self.graph.add_node(node)
        graph = (ctx.g).accept(self)
        self.graph.add_edge(node, graph)
        return node

    def visitExpr_get_edges(self, ctx: LagraphParser.Expr_get_edgesContext):
        """
        visit node with 'edgesOf' expression"
        """
        node = Node("get_vertex", self.next_id())
        self.graph.add_node(node)
        graph = (ctx.g).accept(self)
        self.graph.add_edge(node, graph)
        return node

    def visitExpr_get_labels(self, ctx: LagraphParser.Expr_get_labelsContext):
        """
        visit node with 'labelsOf' expression"
        """
        node = Node("get_labels", self.next_id())
        self.graph.add_node(node)
        graph = (ctx.g).accept(self)
        self.graph.add_edge(node, graph)
        return node

    def visitExpr_map(self, ctx: LagraphParser.Expr_mapContext):
        """
        visit node with 'map' expression"
        """
        node = Node("map", self.next_id())
        self.graph.add_node(node)
        foo = (ctx.f).accept(self)
        self.graph.add_edge(node, foo, 0)
        graph = (ctx.e).accept(self)
        self.graph.add_edge(node, graph, 1)
        return node

    def visitLambda(self, ctx: LagraphParser.LambdaContext):
        """
        visit node with 'lambda' expression"
        """
        node = Node("lambda", self.next_id())
        self.graph.add_node(node)
        vars = (ctx.var_list()).accept(self)
        self.graph.add_edge(node, vars, 0)
        expr = (ctx.expr()).accept(self)
        self.graph.add_edge(node, expr, 1)
        return node

    def visitVar_list(self, ctx: LagraphParser.Var_listContext):
        """
        visit node with 'var_list'"
        """
        node = Node("var_list", self.next_id())
        self.graph.add_node(node)

        vars = (ctx.v1).accept(self)
        self.graph.add_edge(node, vars, 0)

        for i, s in enumerate(ctx.v):
            child = s.accept(self)
            self.graph.add_edge(node, child, i + 1)

        return node

    def visitFoo(self, ctx: LagraphParser.FooContext):
        return (ctx.lmb).accept(self)
