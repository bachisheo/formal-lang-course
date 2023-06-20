from project.Lagraph.Exceptions import InterpretingError
from project.Lagraph.Semantic import *
from project.Lagraph.Types import *
from project.antlr_out.Lagraph.LagraphParser import LagraphParser
from project.antlr_out.Lagraph.LagraphVisitor import LagraphVisitor
from antlr4.Token import CommonToken


def interpret(prog):
    vis = InterpretingVisitor()
    tree = prog()
    tree.accept(vis)
    return vis.output


def interpret(script: str):
    """
    Interprets the given code string and returns the output as a string.
    """
    visitor = InterpretingVisitor()
    tree = get_parse_tree(script)
    tree.accept(vis)


def interpret_file(file: str):
    """
    Interprets the code in the specified file and returns the output as a string.
    """
    return _interpret(lambda: get_parse_tree_from_file(file))


class StackMemory:
    """
    Object for storing and getting program variables
    """

    def __init__(self):
        self.stack = []
        self.cur_mem = {}

    def set_var(self, name: str, value):
        self.cur_mem[name] = value
        return None

    def get_val(self, name) -> LagraphType:
        if not name in self.cur_mem:
            raise InterpretingError(f'Uninitialized variable "{name}" used')
        return self.cur_mem[name]


class InterpretingVisitor(LagraphVisitor):
    """This class defines a visitor for a parse tree produced by LagraphParser."""

    def __init__(self):
        self.__log = ""

    def get_log(self) -> str:
        return self.__log

    def print(self, msg):
        print(msg)
        if len(self.__log) == 0:
            self.__log = str(msg)
        else:
            self.__log += "\n" + str(msg)

    # Visit a parse tree produced by LagraphParser#prog.
    def visitProg(self, ctx: LagraphParser.ProgContext):
        self.mem = StackMemory()
        return self.visitChildren(ctx)

    def getString(self, token):
        if isinstance(token, CommonToken):
            return token.text
        return token.value.text

    def acceptBy(self, obj):
        if hasattr(obj, "accept"):
            return obj.accept(self)

    # Visit a parse tree produced by LagraphParser#bind.
    def visitBind(self, ctx: LagraphParser.BindContext):
        var_name = self.getString(ctx.name)
        val = self.acceptBy(ctx.value)
        self.mem.set_var(var_name, val)
        return None

    # Visit a parse tree produced by LagraphParser#print.
    def visitPrint(self, ctx: LagraphParser.PrintContext):
        expr = self.acceptBy(ctx.exp)
        self.print(expr)
        return None

    # Visit a parse tree produced by LagraphParser#lambda.
    def visitLambda(self, ctx: LagraphParser.LambdaContext):
        var = self.getString(ctx.var())
        expr = ctx.expr()
        return LambdaType(var, expr)

    # Visit a parse tree produced by LagraphParser#var.
    def visitVar(self, ctx: LagraphParser.VarContext):
        var_name = self.acceptBy(ctx.value)
        return self.mem.get_val(var_name)

    # Visit a parse tree produced by LagraphParser#int_literal.
    def visitInt_literal(self, ctx: LagraphParser.Int_literalContext):
        val = self.getString(ctx.value)
        return int(val)

    # Visit a parse tree produced by LagraphParser#string_literal.
    def visitString_literal(self, ctx: LagraphParser.String_literalContext):
        val = self.getString(ctx.value)
        return val[1:-1]

    # Visit a parse tree produced by LagraphParser#set.
    def visitSet(self, ctx: LagraphParser.SetContext):
        vals = set()
        vals.add(self.acceptBy(ctx.v1))
        for v in ctx.vs:
            vals.add(self.acceptBy(v))
        return vals

    # Visit a parse tree produced by LagraphParser#tuple.
    def visitTuple(self, ctx: LagraphParser.TupleContext):
        lst = [self.acceptBy(ctx.v1)]
        for v in ctx.vs:
            lst.append(self.acceptBy(v))
        return tuple(lst)

    # Visit a parse tree produced by LagraphParser#expr_val.
    def visitExpr_val(self, ctx: LagraphParser.Expr_valContext):
        expr = self.acceptBy(ctx.e)
        return expr

    # Visit a parse tree produced by LagraphParser#expr_star.
    def visitExpr_star(self, ctx: LagraphParser.Expr_starContext):
        expr = self.acceptBy(ctx.e)
        return

    # Visit a parse tree produced by LagraphParser#expr_filter.
    def visitExpr_filter(self, ctx: LagraphParser.Expr_filterContext):
        lambda_ = self.acceptBy(ctx.l)
        graph = self.acceptBy(ctx.e)
        return filter_expression(self, lambda_, graph)

    # Visit a parse tree produced by LagraphParser#expr_binop.
    def visitExpr_binop(self, ctx: LagraphParser.Expr_binopContext):
        operator = self.acceptBy(ctx.op)
        expr1 = self.acceptBy(ctx.e1)
        expr2 = self.acceptBy(ctx.e2)
        return binary_operation(expr1, expr2, operator)

    # Visit a parse tree produced by LagraphParser#expr_map.
    def visitExpr_map(self, ctx: LagraphParser.Expr_mapContext):
        lambda_ = self.acceptBy(ctx.l)
        graph = self.acceptBy(ctx.e)
        return map_expression(self, lambda_, graph)

    # Visit a parse tree produced by LagraphParser#expr_from_regex.
    def visitExpr_from_regex(self, ctx: LagraphParser.Expr_from_regexContext):
        source = self.acceptBy(ctx.e)
        return load_graph("regex", source)

    # Visit a parse tree produced by LagraphParser#expr_in_set.
    def visitExpr_in_set(self, ctx: LagraphParser.Expr_in_setContext):
        elem = self.acceptBy(ctx.e)
        set_ = self.acceptBy(ctx.s)
        return is_in_set(elem, set_)

    # Visit a parse tree produced by LagraphParser#expr_get.
    def visitExpr_get(self, ctx: LagraphParser.Expr_getContext):
        operator = self.acceptBy(ctx.op)
        graph = self.acceptBy(ctx.graph)
        return get_expression(graph, operator)

    # Visit a parse tree produced by LagraphParser#expr_var.
    def visitExpr_var(self, ctx: LagraphParser.Expr_varContext):
        if isinstance(ctx.e, LagraphParser.VarContext):
            if isinstance(ctx.e.value, CommonToken):
                name = self.getString(ctx.e.value)
                return self.mem.get_val(name)
        expr = self.acceptBy(ctx.e)
        return expr

    # Visit a parse tree produced by LagraphParser#expr_set.
    def visitExpr_set(self, ctx: LagraphParser.Expr_setContext):
        operator = self.acceptBy(ctx.op)
        vertices = self.acceptBy(ctx.values)
        graph = self.acceptBy(ctx.graph)
        return set_expression(vertices, graph, operator)

    # Visit a parse tree produced by LagraphParser#expr_load.
    def visitExpr_load(self, ctx: LagraphParser.Expr_loadContext):
        way = self.getString(ctx.way)
        source = self.getString(ctx.source)[1:-1]
        return load_graph(way, source)

    # Visit a parse tree produced by LagraphParser#set_operator.
    def visitSet_operator(self, ctx: LagraphParser.Set_operatorContext):
        return ctx.getText()

    # Visit a parse tree produced by LagraphParser#get_operator.
    def visitGet_operator(self, ctx: LagraphParser.Get_operatorContext):
        return ctx.getText()

    # Visit a parse tree produced by LagraphParser#binary_operator.
    def visitBinary_operator(self, ctx: LagraphParser.Binary_operatorContext):
        return ctx.getText()
