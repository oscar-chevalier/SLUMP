from unittest import TestCase

from slump.Syntaxic_tree.extents import Locus
from slump.parser.parser import SlumpParser
from slump.parser.lexer import SlumpLexer
from slump.Syntaxic_tree.syntaxic_tree import *


class TestParser(TestCase):
    def test1(self):
        filename = '[NONAME]'

        def e(begin: int, end: int) -> Extent:
            return Extent(Locus(filename, 1, begin), Locus(filename, 1, end))

        def one(begin: int, end: int) -> Expression:
            return ConstantExpression(1, e(begin, end))

        def two(begin: int, end: int) -> Expression:
            return ConstantExpression(2, e(begin, end))

        test_cases = [
            ('i = 1 + 2;', Toplevel([AssignmentStatement('i', BinaryExpression(one(5, 6), BinaryOperator('+', e(7, 8)), two(9, 10), e(5, 10)), e(1, 11))], [])),
            ('i = j;', Toplevel([AssignmentStatement('i', VariableExpression('j', ''), '')], [])),
            ('while(true){}',  Toplevel([WhileStatement(ConstantExpression(True, ''), CompoundStatement([], ''), '')], [])),
            ('1+2+3;', Toplevel([ExpressionStatement(BinaryExpression(BinaryExpression(ConstantExpression(1, ''), BinaryOperator('+', ''), ConstantExpression(2, ''), ''), BinaryOperator('+', ''), ConstantExpression(3, ''), ''), '')], [])),
            ('fun nom(a, b){}', Toplevel([], [FunctionDefinition('nom', ['a', 'b'], [])])),
            ('fun nom(a, b){ return a; }', Toplevel([], [FunctionDefinition('nom', ['a', 'b'], [ReturnStatement(VariableExpression('a', ''), '')])])),
            ('fun nom(){ a = 2; return 0; }', Toplevel([], [FunctionDefinition('nom', [], [AssignmentStatement('a', ConstantExpression(2, ''), ''), ReturnStatement(ConstantExpression(0, ''), '')])])),
            ('fun nom(){ a = 2; return 0; }\ni = 1 + 2;', ''),
        ]
        parser = SlumpParser()
        lexer = SlumpLexer()
        for text, expected in test_cases:
            result = parser.parse_from_text(text, filename)
            expected: Toplevel
            print(repr(expected))
            print(repr(result))
            self.assertEqual(expected, result)
