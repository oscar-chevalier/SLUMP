from sly import Parser
from ..Syntaxic_tree.syntaxic_tree import *
from ..parser.lexer import SlumpLexer


class SlumpParser(Parser):
    debugfile = 'parser.out'
    tokens = SlumpLexer.tokens

    @_('INT', 'FLOAT', 'BOOL', 'STR')
    def primary_expression(self, p):
        return ConstantExpression(p[0])

    @_('"(" expr ")"')
    def primary_expression(self, p):
        return p.expr

    @_('ID')
    def function_path(self, p):
        return [p.ID]

    @_('function_path "." ID')
    def function_path(self, p):
        return p.function_path + [p.ID]

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
        return CallExpression(p.function_path, p.expression_list)

    @_('primary_expression')
    def unary_expression(self, p):
        return p.primary_expression

    @_('"-"',
       '"+"',
       '"!"',
       '"~"')
    def unary_operator(self, p):
        return UnaryOperator(p[0])

    @_('unary_operator unary_expression')
    def unary_expression(self, p):
        return UnaryExpression(p.unary_operator, p.multiplicative_expression)

    @_('unary_expression')
    def multiplicative_expression(self, p):
        return p.unary_expression

    @_('multiplicative_expression "*" unary_expression',
       'multiplicative_expression DIV unary_expression',
       'multiplicative_expression DIVINT unary_expression',
       'multiplicative_expression "%" unary_expression')
    def multiplicative_expression(self, p):
        return BinaryExpression(p.multiplicative_expression, BinaryOperator(p[1]), p.unary_expression)

    @_('multiplicative_expression')
    def additive_expression(self, p):
        return p.multiplicative_expression

    @_('additive_expression "+" multiplicative_expression',
       'additive_expression "-" multiplicative_expression')
    def additive_expression(self, p):
        return BinaryExpression(p.additive_expression, BinaryOperator(p[1]), p.multiplicative_expression)

    @_('additive_expression')
    def shift_expression(self, p):
        return p.additive_expression

    @_('shift_expression GTGT additive_expression',
       'shift_expression LTLT additive_expression')
    def shift_expression(self, p):
        return BinaryExpression(p.shift_expression, BinaryOperator(p[1]), p.additive_expression)

    @_('shift_expression')
    def relational_expression(self, p):
        return p.shift_expression

    @_('relational_expression LT shift_expression',
       'relational_expression GT shift_expression',
       'relational_expression LE shift_expression',
       'relational_expression GE shift_expression')
    def relational_expression(self, p):
        return BinaryExpression(p.relational_expression, BinaryOperator(p[1]), p.shift_expression)

    @_('relational_expression')
    def equality_expression(self, p):
        return p.relational_expression

    @_('equality_expression EQEQ relational_expression',
       'equality_expression NE relational_expression')
    def equality_expression(self, p):
        return BinaryExpression(p.equality_expression, BinaryOperator(p[1]), p.relational_expression)

    @_('equality_expression')
    def band_expression(self, p):
        return p.equality_expression

    @_('band_expression AMP equality_expression')
    def band_expression(self, p):
        return BinaryExpression(p.band_expression, BinaryOperator(p[1]), p.equality_expression)

    @_('band_expression')
    def bxor_expression(self, p):
        return p.band_expression

    @_('bxor_expression "^" band_expression')
    def bxor_expression(self, p):
        return BinaryExpression(p.bxor_expression, BinaryOperator(p[1]), p.band_expression)

    @_('bxor_expression')
    def bor_expression(self, p):
        return p.bxor_expression

    @_('bor_expression PIPE bxor_expression')
    def bor_expression(self, p):
        return BinaryExpression(p.bor_expression, BinaryOperator(p[1]), p.bxor_expression)

    @_('bor_expression')
    def land_expression(self, p):
        return p.bar_expression

    @_('land_expression AMPAMP bor_expression')
    def land_expression(self, p):
        return BinaryExpression(p.land_expression, BinaryOperator(p[1]), p.bor_expression)

    @_('land_expression')
    def lor_expression(self, p):
        return p.land_expression

    @_('lor_expression PIPEPIPE land_expression')
    def lor_expression(self, p):
        return BinaryExpression(p.lor_expression, BinaryOperator(p[1]), p.land_expression)

    @_('lor_expression')
    def expr(self, p):
        return p.lor_expression
