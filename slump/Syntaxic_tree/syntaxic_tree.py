from typing import List, Union


class UnaryOperator:
    def __init__(self, operator: str):
        self.operator = operator


class BinaryOperator:
    def __init__(self, operator: str):
        self.operator = operator


class Expression:
    pass


class CallExpression(Expression):
    def __init__(self, function: List[str], parametres: List[Expression]):
        self.function = function
        self.parametres = parametres


class ConstantExpression(Expression):
    def __init__(self, constant: Union[float, int, bool]):
        self.constant = constant


class VariableExpression(Expression):
    def __init__(self, name: str):
        self.name = name


class UnaryExpression(Expression):
    def __init__(self, op: UnaryOperator, arg: Expression):
        self.op = op
        self.arg = arg


class BinaryExpression(Expression):
    def __init__(self, arg1: Expression, op: BinaryOperator, arg2: Expression):
        self.arg1 = arg1
        self.op = op
        self.arg2 = arg2


class Statement:
    pass


class CompoundStatement(Statement):
    def __init__(self, staments: List[Statement]):
        self.statements = staments


class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: Statement):
        self.condition = condition
        self.body = body
