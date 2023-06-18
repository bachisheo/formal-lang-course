from project.antlr_out.Lagraph.LagraphParser import LagraphParser
from ..antlr_out.Lagraph.LagraphParser import LagraphParser
from ..antlr_out.Lagraph.LagraphVisitor import LagraphVisitor

from networkx import MultiDiGraph


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

    def visitExpr_set(self, ctx: LagraphParser.Expr_setContext):
        """
        visit node with 'setStart' and etc. expression"
        """
        operator = ctx.op.accept(self)
        node = Node(operator, self.next_id())
        self.graph.add_node(node)
        verts = (ctx.v).accept(self)
        self.graph.add_edge(node, verts, 0)
        graph = (ctx.g).accept(self)
        self.graph.add_edge(node, graph, 1)
        return node

    def visitSet_operator(self, ctx: LagraphParser.Set_operatorContext) -> str:
        return ctx.getText()

    #
    # of statements
    #
    def visitExpr_get(self, ctx: LagraphParser.Expr_getContext):
        """
        visit node with 'startOf' and etc. expression"
        """
        operator = ctx.op.accept(self)
        node = Node(operator, self.next_id())
        self.graph.add_node(node)
        graph = (ctx.g).accept(self)
        self.graph.add_edge(node, graph)
        return node

    def visitGet_operator(self, ctx: LagraphParser.Get_operatorContext):
        return ctx.getText()

    def visitExpr_map(self, ctx: LagraphParser.Expr_mapContext):
        """
        visit node with 'map' expression"
        """
        node = Node("map", self.next_id())
        self.graph.add_node(node)
        lambd = (ctx.l).accept(self)
        self.graph.add_edge(node, lambd, 0)
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
