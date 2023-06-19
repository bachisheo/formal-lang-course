from project.Lagraph.Semantic import *
from project.Lagraph.Types import *
from project.antlr_out.Lagraph.LagraphParser import LagraphParser
from ..antlr_out.Lagraph.LagraphParser import LagraphParser
from ..antlr_out.Lagraph.LagraphVisitor import LagraphVisitor


class StackMemory:
    def __init__(self):
        self.stack = []
        self.cur_mem = {}

    def start_func(self):
        self.stack.append(self.cur_mem)
        self.cur_mem = {}

    def return_from(self):
        self.cur_mem = self.stack.pop()

    def add_var(self, name: str, value):
        self.cur_mem[name] = value

    def get_val_by_name(self, name: str):
        x = self.cur_mem[name]
        if x is None:
            return "ЧИНИ ПОИСК ЗНАЧЕНИЙ РЕКУРСИВНО (:"
        return x


class InterpretingVisitor(LagraphVisitor):
    """This class defines a visitor for a parse tree produced by LagraphParser."""

    def print(self, msg: str):
        print(str(msg))

    # Visit a parse tree produced by LagraphParser#prog.
    def visitProg(self, ctx: LagraphParser.ProgContext):
        self.mem = StackMemory()

    # Visit a parse tree produced by LagraphParser#st_bind.
    def visitSt_bind(self, ctx: LagraphParser.St_bindContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LagraphParser#st_print.
    def visitSt_print(self, ctx: LagraphParser.St_printContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LagraphParser#bind.
    def visitBind(self, ctx: LagraphParser.BindContext):
        var_name = (ctx.name).accept(self)
        val = (ctx.value).accept(self)
        self.mem.add_var(var_name, val)

    # Visit a parse tree produced by LagraphParser#print.
    def visitPrint(self, ctx: LagraphParser.PrintContext):
        expr = (ctx.exp).accept(self)
        self.print(expr)
        return None

    # Visit a parse tree produced by LagraphParser#lambda.
    def visitLambda(self, ctx: LagraphParser.LambdaContext):
        var = (ctx.var()).accept(self)
        expr = (ctx.expr()).accept(self)
        return Lambda(var, expr)

    # Visit a parse tree produced by LagraphParser#var_list.
    def visitVar_list(self, ctx: LagraphParser.Var_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LagraphParser#var.
    def visitVar(self, ctx: LagraphParser.VarContext):
        var_name = (ctx.value).accept(self)
        return self.mem.get_val_by_name(var_name)

    # Visit a parse tree produced by LagraphParser#int_literal.
    def visitInt_literal(self, ctx: LagraphParser.Int_literalContext):
        val = (ctx.value).accept(self)
        # ctx.value.text
        return Int(val)

    # Visit a parse tree produced by LagraphParser#string_literal.
    def visitString_literal(self, ctx: LagraphParser.String_literalContext):
        val = ctx.value.text
        return String(val)

    # Visit a parse tree produced by LagraphParser#set_literal.
    def visitSet_literal(self, ctx: LagraphParser.Set_literalContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LagraphParser#set.
    def visitSet(self, ctx: LagraphParser.SetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LagraphParser#expr_val.
    def visitExpr_val(self, ctx: LagraphParser.Expr_valContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LagraphParser#expr_star.
    def visitExpr_star(self, ctx: LagraphParser.Expr_starContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LagraphParser#expr_filter.
    def visitExpr_filter(self, ctx: LagraphParser.Expr_filterContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LagraphParser#expr_binop.
    def visitExpr_binop(self, ctx: LagraphParser.Expr_binopContext):
        operator = ctx.op.accept(self)
        expr1 = (ctx.e1).accept(self)
        expr2 = (ctx.e2).accept(self)
        return binary_operation(expr1, expr2, operator)

    # Visit a parse tree produced by LagraphParser#expr_map.
    def visitExpr_map(self, ctx: LagraphParser.Expr_mapContext):
        lambd = (ctx.l).accept(self)
        graph = (ctx.e).accept(self)
        return map_expression(lambd, graph)

    # Visit a parse tree produced by LagraphParser#expr_brace.
    def visitExpr_brace(self, ctx: LagraphParser.Expr_braceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LagraphParser#expr_one_step.
    def visitExpr_one_step(self, ctx: LagraphParser.Expr_one_stepContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LagraphParser#expr_in_set.
    def visitExpr_in_set(self, ctx: LagraphParser.Expr_in_setContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LagraphParser#expr_get.
    def visitExpr_get(self, ctx: LagraphParser.Expr_getContext):
        operator = ctx.op.accept(self)
        graph = (ctx.g).accept(self)
        return get_expression(graph, operator)

    # Visit a parse tree produced by LagraphParser#expr_var.
    def visitExpr_var(self, ctx: LagraphParser.Expr_varContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LagraphParser#expr_set.
    def visitExpr_set(self, ctx: LagraphParser.Expr_setContext):
        operator = ctx.op.accept(self)
        verts = (ctx.v).accept(self)
        graph = (ctx.g).accept(self)
        return set_expression(verts, graph, operator)

    # Visit a parse tree produced by LagraphParser#expr_load.
    def visitExpr_load(self, ctx: LagraphParser.Expr_loadContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LagraphParser#set_operator.
    def visitSet_operator(self, ctx: LagraphParser.Set_operatorContext):
        return ctx.getText()

    # Visit a parse tree produced by LagraphParser#get_operator.
    def visitGet_operator(self, ctx: LagraphParser.Get_operatorContext):
        return ctx.getText()

    # Visit a parse tree produced by LagraphParser#binary_operator.
    def visitBinary_operator(self, ctx: LagraphParser.Binary_operatorContext):
        return ctx.getText()
