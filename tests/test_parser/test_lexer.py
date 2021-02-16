from unittest import TestCase
from slump.parser.lexer import SlumpLexer


class TestLexer(TestCase):
    def test1(self):
        list_test = [
            ('3 + 2',  [
                ('INT', (3, 1), 1, 0),
                ('+', '+', 1, 2),
                ('INT', (2, 1), 1, 4)]),
            ('silicium = sensor(foundation1, @metaglass);\nif(silicium < 4000){\ncontrol.enabled(conveyor1, true);\n}\n'
             'else{\ncontrol.enabled(conveyor1, false);\n}', [
                ('ID', 'silicium', 1, 0), ('EQ', '=', 1, 9), ('ID', 'sensor', 1, 11), ('(', '(', 1, 17),
                ('ID', 'foundation1', 1, 18), (',', ',', 1, 29), ('ID', '@metaglass', 1, 31), (')', ')', 1, 41),
                (';', ';', 1, 42), ('IF', 'if', 2, 44), ('(', '(', 2, 46), ('ID', 'silicium', 2, 47),
                ('LT', '<', 2, 56), ('INT', (4000, 4), 2, 58), (')', ')', 2, 62), ('{', '{', 2, 63),
                ('ID', 'control', 3, 65), ('.', '.', 3, 72), ('ID', 'enabled', 3, 73), ('(', '(', 3, 80),
                ('ID', 'conveyor1', 3, 81), (',', ',', 3, 90), ('BOOL', (True, 4), 3, 92), (')', ')', 3, 96),
                (';', ';', 3, 97), ('}', '}', 4, 99), ('ELSE', 'else', 5, 101), ('{', '{', 5, 105),
                ('ID', 'control', 6, 107), ('.', '.', 6, 114), ('ID', 'enabled', 6, 115), ('(', '(', 6, 122),
                ('ID', 'conveyor1', 6, 123), (',', ',', 6, 132), ('BOOL', (False, 5), 6, 134), (')', ')', 6, 139),
                (';', ';', 6, 140), ('}', '}', 7, 142)]),
            ('3 +\nwhile 1.54 && 5.54', [
                ('INT', (3, 1), 1, 0), ('+', '+', 1, 2), ('WHILE', 'while', 2, 4), ('FLOAT', (1.54, 4), 2, 10),
                ('AMPAMP', '&&', 2, 15), ('FLOAT', (5.54, 4), 2, 18)
            ])
        ]
        lexer = SlumpLexer()
        for text, expected_toks in list_test:
            actual_toks = list(lexer.tokenize(text))
            self.assertEqual(len(expected_toks), len(actual_toks), repr(actual_toks))
            for expected_token, actual_token in zip(expected_toks, actual_toks):
                self.assertEqual(expected_token[0], actual_token.type, repr(expected_token)+repr(actual_token))
                self.assertEqual(expected_token[1], actual_token.value)
                self.assertEqual(expected_token[2], actual_token.lineno)
                self.assertEqual(expected_token[3], actual_token.index, repr(expected_token)+repr(actual_token))
