from unittest import TestCase

from slump.Syntaxic_tree.extent import Locus
from slump.parser.parser import SlumpParser
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
            ('i = j;', Toplevel([AssignmentStatement('i', VariableExpression('j', e(5, 6)), e(1, 7))], [])),
            ('while(true){}',  Toplevel([WhileStatement(ConstantExpression(True, e(7, 11)), CompoundStatement([], e(12, 14)), e(1, 14))], [])),
            ('1+2+3;', Toplevel([ExpressionStatement(BinaryExpression(BinaryExpression(ConstantExpression(1, e(1, 2)), BinaryOperator('+', e(2, 3)), ConstantExpression(2, e(3, 4)), e(1, 4)), BinaryOperator('+', e(4, 5)), ConstantExpression(3, e(5, 6)), e(1, 6)), e(1, 7))], [])),
            ('fun nom(a, b){}', Toplevel([], [FunctionDefinition('nom', ['a', 'b'], [], e(1, 16))])),
            ('fun nom(a, b){ return a; }', Toplevel([], [FunctionDefinition('nom', ['a', 'b'], [ReturnStatement(VariableExpression('a', e(23, 24)), e(16, 25))], e(1, 27))])),
            ('fun nom(){ a = 2; return 0; }', Toplevel([], [FunctionDefinition('nom', [], [AssignmentStatement('a', two(16, 17), e(12, 18)), ReturnStatement(ConstantExpression(0, e(26, 27)), e(19, 28))], e(1, 30))])),
            ('fun nom(){ a = 2; return 0; }\ni = 1 + 2;', Toplevel([AssignmentStatement('i', BinaryExpression(ConstantExpression(1, Extent(Locus(filename, 2, 5), Locus(filename, 2, 6))), BinaryOperator('+', Extent(Locus(filename, 2, 7), Locus(filename, 2, 8))), ConstantExpression(2, Extent(Locus(filename, 2, 9), Locus(filename, 2, 10))), Extent(Locus(filename, 2, 5), Locus(filename, 2, 10))), Extent(Locus(filename, 2, 1), Locus(filename, 2, 11)))], [FunctionDefinition('nom', [], [AssignmentStatement('a', two(16, 17), e(12, 18)), ReturnStatement(ConstantExpression(0, e(26, 27)), e(19, 28))], e(1, 30))])),
        ]
        parser = SlumpParser()
        for text, expected in test_cases:
            result = parser.parse_from_text(text, filename)
            expected: Toplevel
            self.assertEqual(expected, result)
