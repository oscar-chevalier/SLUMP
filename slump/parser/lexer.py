from sly import Lexer


class SlumpLexer(Lexer):
    tokens = {INT, FLOAT, ID, STR, WHILE, IF, ELSE, BOOL, EQ, EQEQ, LE, LT, GE, GT, NE, AMP, AMPAMP, PIPE,
              PIPEPIPE, DIV, DIVINT, LTLT, GTGT, FUN, RETURN}
    literals = {'+', '-', '*', '%', '(', ')', '{', '}',  '^', '.', ';', ',', '!'}

    ignore = ' \t'
    ignore_comment = r'\#.*'

    EQ = r'='
    EQEQ = r'=='
    LTLT = r'<<'
    GTGT = r'>>'
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='
    AMPAMP = r'&&'
    AMP = r'&'
    PIPEPIPE = r'\|\|'
    PIPE = r'\|'
    DIVINT = r'//'
    DIV = r'/'

    @_(r'\d+\.\d+')
    def FLOAT(self, t):
        t.value = float(t.value), len(t.value)
        return t

    @_(r'\d+')
    def INT(self, t):
        t.value = int(t.value), len(t.value)
        return t

    @_('"[^"]*"')
    def STR(self, t):
        t.value = t.strip('"'), len(t.value)
        return t

    @_('true|false')
    def BOOL(self, t):
        t.value = t.value == 'true', len(t.value)
        return t

    ID = r'[a-zA-Z_@][a-zA-Z0-9_]*'
    ID['while'] = WHILE
    ID['if'] = IF
    ID['else'] = ELSE
    ID['fun'] = FUN
    ID['return'] = RETURN

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

