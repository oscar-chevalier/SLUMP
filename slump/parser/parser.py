from sly import Parser
from ..Syntaxic_tree.syntaxic_tree import *
from ..parser.lexer import SlumpLexer


class SlumpParser(Parser):
    debugfile = 'parser.out'
    tokens = SlumpLexer.tokens
    start = 'toplevel'

    def __init__(self):
        self.text = ''
        self.filename = ''
        self.lexer = SlumpLexer()

    @_('ID')
    def primary_expression(self, p):
        return VariableExpression(p.ID, self.create_extent(p, 0, len(p.ID)))

    @_('INT', 'FLOAT', 'BOOL', 'STR')
    def primary_expression(self, p):
        return ConstantExpression(p[0][0], self.create_extent(p, 0, p[0][1]))

    @_('"(" expr ")"')
    def primary_expression(self, p):
        left_extent = self.create_extent(p, 0, 1)
        right_extent = self.create_extent(p, 2, 1)
        extent = Extent.fromto(left_extent, right_extent)
        return ParentheseExpression(p.expr, extent)

    @_('ID')
    def function_path(self, p):
        return [p.ID], self.create_extent(p, 0, len(p.ID))

    @_('function_path "." ID')
    def function_path(self, p):
        return p.function_path[0] + [p.ID], p.function_path[1]

    @_('')
    def expression_list(self, p):
        return []

    @_('expr')
    def not_empty_expression_list(self, p):
        return [p.expr]

    @_('not_empty_expression_list "," expr')
    def not_empty_expression_list(self, p):
        return p.not_empty_expression_list + [p.expr]

    @_('not_empty_expression_list')
    def expression_list(self, p):
        return p.not_empty_expression_list

    @_('function_path "(" expression_list ")"')
    def primary_expression(self, p):
        left_extent = p.function_path[1]
        right_extent = self.create_extent(p, 3, 1)
        extent = Extent.fromto(left_extent, right_extent)
        return CallExpression(p.function_path[0], p.expression_list, extent)

    @_('primary_expression')
    def unary_expression(self, p):
        return p.primary_expression

    @_('"-"',
       '"+"',
       '"!"',
       '"~"')
    def unary_operator(self, p):
        return UnaryOperator(p[0], self.create_extent(p, 0, 1))

    @_('unary_operator unary_expression')
    def unary_expression(self, p):
        return UnaryExpression(p.unary_operator, p.unary_expression, Extent.fromto(p.unary_operator.extent, p.unary_expression))

    @_('unary_expression')
    def multiplicative_expression(self, p):
        return p.unary_expression

    @_('multiplicative_expression "*" unary_expression',
       'multiplicative_expression DIV unary_expression',
       'multiplicative_expression DIVINT unary_expression',
       'multiplicative_expression "%" unary_expression')
    def multiplicative_expression(self, p):
        op_extent = self.create_extent(p, 1, len(p[1]))
        ex_extent = Extent.fromto(p.multiplicative_expression.extent, p.unary_expression.extent)
        return BinaryExpression(p.multiplicative_expression, BinaryOperator(p[1], op_extent), p.unary_expression, ex_extent)

    @_('multiplicative_expression')
    def additive_expression(self, p):
        return p.multiplicative_expression

    @_('additive_expression "+" multiplicative_expression',
       'additive_expression "-" multiplicative_expression')
    def additive_expression(self, p):
        op_extent = self.create_extent(p, 1, 1)
        ex_extent = Extent(p.additive_expression.extent, p.multiplicative_expression.extent)
        return BinaryExpression(p.additive_expression, BinaryOperator(p[1], op_extent), p.multiplicative_expression, ex_extent)

    @_('additive_expression')
    def shift_expression(self, p):
        return p.additive_expression

    @_('shift_expression GTGT additive_expression',
       'shift_expression LTLT additive_expression')
    def shift_expression(self, p):
        op_extent = self.create_extent(p, 1, 2)
        ex_extent = Extent(p.shift_expression.extent, p.additive_expression.extent)
        return BinaryExpression(p.shift_expression, BinaryOperator(p[1], op_extent), p.additive_expression, ex_extent)

    @_('shift_expression')
    def relational_expression(self, p):
        return p.shift_expression

    @_('relational_expression LT shift_expression',
       'relational_expression GT shift_expression',
       'relational_expression LE shift_expression',
       'relational_expression GE shift_expression')
    def relational_expression(self, p):
        op_extent = self.create_extent(p, 1, 1)
        ex_extent = Extent(p.relational_expression.extent, p.shift_expression.extent)
        return BinaryExpression(p.relational_expression, BinaryOperator(p[1], op_extent), p.shift_expression, ex_extent)

    @_('relational_expression')
    def equality_expression(self, p):
        return p.relational_expression

    @_('equality_expression EQEQ relational_expression',
       'equality_expression NE relational_expression')
    def equality_expression(self, p):
        op_extent = self.create_extent(p, 1, 2)
        ex_extent = Extent(p.equality_expression.extent, p.relational_expression.extent)
        return BinaryExpression(p.equality_expression, BinaryOperator(p[1], op_extent), p.relational_expression, ex_extent)

    @_('equality_expression')
    def band_expression(self, p):
        return p.equality_expression

    @_('band_expression AMP equality_expression')
    def band_expression(self, p):
        op_extent = self.create_extent(p, 1, 1)
        ex_extent = Extent(p.band_expression.extent, p.equality_expression.extent)
        return BinaryExpression(p.band_expression, BinaryOperator(p[1], op_extent), p.equality_expression, ex_extent)

    @_('band_expression')
    def bxor_expression(self, p):
        return p.band_expression

    @_('bxor_expression "^" band_expression')
    def bxor_expression(self, p):
        op_extent = self.create_extent(p, 1, 1)
        ex_extent = Extent(p.bxor_expression.extent, p.band_expression.extent)
        return BinaryExpression(p.bxor_expression, BinaryOperator(p[1], op_extent), p.band_expression, ex_extent)

    @_('bxor_expression')
    def bor_expression(self, p):
        return p.bxor_expression

    @_('bor_expression PIPE bxor_expression')
    def bor_expression(self, p):
        op_extent = self.create_extent(p, 1, 1)
        ex_extent = Extent(p.bor_expression.extent, p.bxor_expression.extent)
        return BinaryExpression(p.bor_expression, BinaryOperator(p[1], op_extent), p.bxor_expression, ex_extent)

    @_('bor_expression')
    def land_expression(self, p):
        return p.bor_expression

    @_('land_expression AMPAMP bor_expression')
    def land_expression(self, p):
        op_extent = self.create_extent(p, 1, 2)
        ex_extent = Extent(p.land_expression.extent, p.bor_expression.extent)
        return BinaryExpression(p.land_expression, BinaryOperator(p[1], op_extent), p.bor_expression, ex_extent)

    @_('land_expression')
    def lor_expression(self, p):
        return p.land_expression

    @_('lor_expression PIPEPIPE land_expression')
    def lor_expression(self, p):
        op_extent = self.create_extent(p, 1, 2)
        ex_extent = Extent(p.lor_expression.extent, p.land_expression.extent)
        return BinaryExpression(p.lor_expression, BinaryOperator(p[1], op_extent), p.land_expression, ex_extent)

    @_('lor_expression')
    def expr(self, p):
        return p.lor_expression

    @_('statement')
    def compound_statement(self, p):
        return [p.statement]

    @_('compound_statement statement')
    def compound_statement(self, p):
        return p.compound_statement + [p.statement]

    @_('')
    def compound_statement_opt(self, p):
        return []

    @_('compound_statement')
    def compound_statement_opt(self, p):
        return p.compound_statement

    @_('WHILE "(" expr ")" "{" compound_statement_opt "}"')
    def statement(self, p):
        lbrace_extent = self.create_extent(p, 4, 1)
        rbrace_extent = self.create_extent(p, 6, 1)
        compound_extent = Extent.fromto(lbrace_extent, rbrace_extent)
        while_kw_extent = self.create_extent(p, 0, 5)
        while_extent = Extent.fromto(while_kw_extent, rbrace_extent)
        return WhileStatement(p.expr, CompoundStatement(p.compound_statement_opt, compound_extent), while_extent)

    @_('')
    def else_opt(self, p):
        return CompoundStatement([], Extent.create(self.filename, -1, -1, 0))

    @_('ELSE "{" compound_statement "}"')
    def else_opt(self, p):
        lbrace_extent = self.create_extent(p, 1, 1)
        rbrace_extent = self.create_extent(p, 3, 1)
        compound_extent = Extent.fromto(lbrace_extent, rbrace_extent)
        return CompoundStatement(p.compound_statement, compound_extent)

    @_('')
    def else_if_list(self, p):
        return []

    @_('else_if_list ELSE IF "(" expr ")" "{" compound_statement "}"')
    def else_if_list(self, p):
        lbrace_extent = self.create_extent(p, 6, 1)
        rbrace_extent = self.create_extent(p, 8, 1)
        compound_extent = Extent.fromto(lbrace_extent, rbrace_extent)
        return p.else_if_list + [(p.expr, CompoundStatement(p.compound_statement, compound_extent))]

    @_('IF "(" expr ")" "{" compound_statement_opt "}" else_if_list else_opt')
    def statement(self, p):
        if p.else_opt.extent.begin.line == -1:
            if len(p.else_if_list) == 0:
                end_extent = self.create_extent(p, 6, 1)
            else:
                end_extent = p.else_if_list[-1][1].extent
            p.else_opt.extent.begin = end_extent.end
            p.else_opt.extent.end = end_extent.end
        else:
            end_extent = p.else_opt.extent
        begin_extent = self.create_extent(p, 0, 2)
        if_extent = Extent.fromto(begin_extent, end_extent)
        return IfStatement([(p.expr, p.compound_statement_opt)] + p.else_if_list, p.else_opt, if_extent)

    @_('ID EQ expr ";"')
    def statement(self, p):
        begin_extent = self.create_extent(p, 0, len(p.ID))
        end_extent = self.create_extent(p, 3, 1)
        assignement_extent = Extent.fromto(begin_extent, end_extent)
        return AssignmentStatement(p.ID, p.expr, assignement_extent)

    @_('expr ";"')
    def statement(self, p):
        begin_extent = p.expr.extent
        end_extent = self.create_extent(p, 1, 1)
        expression_extent = Extent.fromto(begin_extent, end_extent)
        return ExpressionStatement(p.expr, expression_extent)

    @_('statement')
    def toplevel_element(self, p):
        return p.statement, False

    @_('')
    def list_id(self, p):
        return []

    @_('non_empty_list_id')
    def list_id(self, p):
        return p.non_empty_list_id

    @_('ID')
    def non_empty_list_id(self, p):
        return [p.ID]

    @_('non_empty_list_id "," ID')
    def non_empty_list_id(self, p):
        return p.non_empty_list_id + [p.ID]

    @_('')
    def function_body(self, p):
        return []

    @_('statement')
    def statement_or_return(self, p):
        return p.statement

    @_('RETURN expr ";"')
    def statement_or_return(self, p):
        begin_extent = self.create_extent(p, 0, 6)
        end_extent = self.create_extent(p, 2, 1)
        return_extent = Extent.fromto(begin_extent, end_extent)
        return ReturnStatement(p.expr, return_extent)

    @_('function_body statement_or_return')
    def function_body(self, p):
        return p.function_body + [p.statement_or_return]

    @_('FUN ID "(" list_id ")" "{" function_body "}"')
    def function_def(self, p):
        return FunctionDefinition(p.ID, p.list_id, p.function_body)

    @_('function_def')
    def toplevel_element(self, p):
        return p.function_def, True

    @_('')
    def toplevel_element_list(self, p):
        return [], []

    @_('toplevel_element_list toplevel_element')
    def toplevel_element_list(self, p):
        statements, function_def = p.toplevel_element_list
        s, is_function_def = p.toplevel_element
        if is_function_def:
            return statements, function_def + [s]
        return statements + [s], function_def

    @_('toplevel_element_list')
    def toplevel(self, p):
        return Toplevel(*p.toplevel_element_list)

    def parse_from_text(self, text, filename='[NONE]'):
        self.text = text
        self.filename = filename
        return self.parse(self.lexer.tokenize(self.text))

    def find_column(self, token):
        last_cr = self.text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = -1
        column = token.index - last_cr
        return column

    def create_extent(self, p, index: int, length: int):
        return Extent.create(self.filename, p.lineno, self.find_column(p._slice[index]), length)
