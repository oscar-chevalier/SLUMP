from abc import ABCMeta, abstractmethod
from typing import List, Union, Tuple

from slump.Syntaxic_tree.extents import Extent


class UnaryOperator:
    def __init__(self, operator: str, extent: Extent):
        self.operator = operator
        self.extent: Extent = extent

    def __eq__(self, other):
        if not isinstance(other, UnaryOperator):
            return False
        return self.operator == other.operator and self.extent == other.extent

    def __repr__(self):
        return f'UnaryOperator({self.operator!r}, {self.extent!r})'


class BinaryOperator:
    def __init__(self, operator: str, extent: Extent):
        self.operator = operator
        self.extent: Extent = extent

    def __eq__(self, other):
        if not isinstance(other, BinaryOperator):
            return False
        return self.operator == other.operator and self.extent == other.extent

    def __repr__(self):
        return f'BinaryOperator({self.operator!r}, {self.extent!r})'


class Expression:
    def __init__(self, extent: Extent):
        self.extent: Extent = extent

    def __eq__(self, other):
        if not isinstance(other, Expression):
            return False
        return self.extent == other.extent


class CallExpression(Expression):
    def __init__(self, function: List[str], parameters: List[Expression], extent: Extent):
        super().__init__(extent)
        self.function = function
        self.parameters = parameters

    def __eq__(self, other):
        if not isinstance(other, CallExpression):
            return False
        return self.function == other.function and self.parameters == other.parameters and super(CallExpression, self).__eq__(other)

    def __repr__(self):
        return f'CallExpression({self.function!r}, {self.parameters!r}, {self.extent!r})'


class ConstantExpression(Expression):
    def __init__(self, constant: Union[float, int, bool], extent: Extent):
        super().__init__(extent)
        self.constant = constant

    def __eq__(self, other):
        if not isinstance(other, ConstantExpression):
            return False
        return self.constant == other.constant and super(ConstantExpression, self).__eq__(other)

    def __repr__(self):
        return f'ConstantExpression({self.constant!r}, {self.extent!r})'


class VariableExpression(Expression):
    def __init__(self, name: str, extent: Extent):
        super().__init__(extent)
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, VariableExpression):
            return False
        return self.name == other.name and super(VariableExpression, self).__eq__(other)

    def __repr__(self):
        return f'VariableExpression({self.name!r}, {self.extent!r})'


class UnaryExpression(Expression):
    def __init__(self, op: UnaryOperator, arg: Expression, extent: Extent):
        super().__init__(extent)
        self.op = op
        self.arg = arg

    def __eq__(self, other):
        if not isinstance(other, UnaryExpression):
            return False
        return self.op == other.op and self.arg == other.arg and super(UnaryExpression, self).__eq__(other)

    def __repr__(self):
        return f'UnaryExpression({self.op!r}, {self.arg!r}, {self.extent!r})'


class BinaryExpression(Expression):
    def __init__(self, arg1: Expression, op: BinaryOperator, arg2: Expression, extent: Extent):
        super().__init__(extent)
        self.arg1 = arg1
        self.op = op
        self.arg2 = arg2

    def __eq__(self, other):
        if not isinstance(other, BinaryExpression):
            return False
        return self.arg1 == other.arg1 and self.op == other.op and self.arg2 == other.arg2 and super(BinaryExpression, self).__eq__(other)

    def __repr__(self):
        return f'BinaryExpression({self.arg1!r}, {self.op!r}, {self.arg2!r}, {self.extent!r})'


class ParentheseExpression(Expression):
    def __init__(self, arg: Expression, extent: Extent):
        super().__init__(extent)
        self.arg = arg

    def __eq__(self, other):
        if not isinstance(other, ParentheseExpression):
            return False
        return self.arg == other.arg and super(ParentheseExpression, self).__eq__(other)

    def __repr__(self):
        return f'ParentheseExpression({self.arg!r}, {self.extent!r})'


class Statement(metaclass=ABCMeta):
    def __init__(self, extent: Extent):
        self.extent: Extent = extent

    def __eq__(self, other):
        if not isinstance(other, Statement):
            return False
        return self.extent == other.extent

    @abstractmethod
    def __repr__(self):
        pass


class CompoundStatement(Statement):
    def __init__(self, staments: List[Statement], extent: Extent):
        super().__init__(extent)
        self.statements = staments

    def __eq__(self, other):
        if not isinstance(other, CompoundStatement):
            return False
        return self.statements == other.statements and super(CompoundStatement, self).__eq__(other)

    def __repr__(self):
        return f'CompoundStatement({self.statements!r}, {self.extent!r})'


class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: Statement, extent: Extent):
        super().__init__(extent)
        self.condition = condition
        self.body = body

    def __eq__(self, other):
        if not isinstance(other, WhileStatement):
            return False
        return self.condition == other.condition and self.body == other.body and super(WhileStatement, self).__eq__(other)

    def __repr__(self):
        return f'WhileStatement({self.condition!r}, {self.body!r}, {self.extent!r})'


class IfStatement(Statement):
    def __init__(self, condition_body: List[Tuple[Expression, Statement]], body_false: Statement, extent: Extent):
        super().__init__(extent)
        self.condition_body = condition_body
        self.body_false = body_false

    def __eq__(self, other):
        if not isinstance(other, IfStatement):
            return False
        return other.condition_body == self.condition_body and self.body_false == other.body_false and super(IfStatement, self).__eq__(other)

    def __repr__(self):
        return f'IfStatement({self.condition_body!r}, {self.body_false!r}, {self.extent!r})'


class AssignmentStatement(Statement):
    def __init__(self, lhs: str, rhs: Expression, extent: Extent):
        super().__init__(extent)
        self.lhs = lhs
        self.rhs = rhs

    def __eq__(self, other):
        if not isinstance(other, AssignmentStatement):
            return False
        return other.lhs == self.lhs and other.rhs == self.rhs and super(AssignmentStatement, self).__eq__(other)

    def __repr__(self):
        return f'AssigmentStatement({self.lhs!r}, {self.rhs!r}, {self.extent!r})'


class ExpressionStatement(Statement):
    def __init__(self, expr: Expression, extent: Extent):
        super().__init__(extent)
        self.expr = expr

    def __eq__(self, other):
        if not isinstance(other, ExpressionStatement):
            return False
        return self.expr == other.expr and super(ExpressionStatement, self).__eq__(other)

    def __repr__(self):
        return f'ExpressionStatement({self.expr!r}, {self.extent!r})'


class ReturnStatement(Statement):
    def __init__(self, expr: Expression, extent: Extent):
        super().__init__(extent)
        self.expr = expr

    def __eq__(self, other):
        if not isinstance(other, ReturnStatement):
            return False
        return self.expr == other.expr and super(ReturnStatement, self).__eq__(other)

    def __repr__(self):
        return f'ReturnStatement({self.expr!r}, {self.extent!r})'


class FunctionDefinition:
    def __init__(self, name: str, argument_list: List[str], body: List[Statement]):
        self.name = name
        self.argument_list = argument_list
        self.body = body

    def __eq__(self, other):
        if not isinstance(other, FunctionDefinition):
            return False
        return self.name == other.name and self.argument_list == other.argument_list and self.body == other.body

    def __repr__(self):
        return f'FunctionDefinition({self.name!r}, {self.argument_list!r}, {self.body!r})'


class Toplevel:
    def __init__(self, statements: List[Statement], definition_func: List[FunctionDefinition]):
        self.statements = statements
        self.definition_func = definition_func

    def __eq__(self, other):
        if not isinstance(other, Toplevel):
            return False
        return self.statements == other.statements and self.definition_func == other.definition_func

    def __repr__(self):
        return f'Toplevel({self.statements!r}, {self.definition_func!r})'
