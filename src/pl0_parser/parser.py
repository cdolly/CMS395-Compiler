from hash_tables import OPERATOR_HASH_TABLE, KEYWORD_HASH_TABLE
from pl0_parser.constants import SKIPS


INVERSE_OPERATOR_HASH_TABLE = {v: k for k, v in OPERATOR_HASH_TABLE.items()}
INVERSE_KEYWORD_HASH_TABLE = {v: k for k, v in KEYWORD_HASH_TABLE.items()}


class Parser:

    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.i = -1
        self.token = None

    def parse(self):
        self.next()
        self.program()

    def program(self):
        self.block()
        self.match(INVERSE_OPERATOR_HASH_TABLE['.'])

    def block(self):
        if self.token == INVERSE_KEYWORD_HASH_TABLE['const']:
            self.match(INVERSE_KEYWORD_HASH_TABLE['const'])
            self.ident()
            self.match(INVERSE_OPERATOR_HASH_TABLE['='])
            self.number()
            while self.token == INVERSE_OPERATOR_HASH_TABLE[',']:
                self.match(INVERSE_OPERATOR_HASH_TABLE[','])
                self.ident()
                self.match(INVERSE_OPERATOR_HASH_TABLE['='])
                self.number()
            self.match(INVERSE_OPERATOR_HASH_TABLE[';'])
        if self.token == INVERSE_KEYWORD_HASH_TABLE['var']:
            self.match(INVERSE_KEYWORD_HASH_TABLE['var'])
            self.ident()
            while self.token == INVERSE_OPERATOR_HASH_TABLE[',']:
                self.match(INVERSE_OPERATOR_HASH_TABLE[','])
                self.ident()
            self.match(INVERSE_OPERATOR_HASH_TABLE[';'])
        while self.token == INVERSE_KEYWORD_HASH_TABLE['procedure']:
            self.match(INVERSE_KEYWORD_HASH_TABLE['procedure'])
            self.ident()
            self.match(INVERSE_OPERATOR_HASH_TABLE[';'])
            self.block()
            self.match(INVERSE_OPERATOR_HASH_TABLE[';'])
        self.statement()

    def statement(self):
        if self.token[0] == '0':
            self.ident()
            self.match(INVERSE_OPERATOR_HASH_TABLE[':='])
            self.expression()
        elif self.token == INVERSE_KEYWORD_HASH_TABLE['call']:
            self.match(INVERSE_KEYWORD_HASH_TABLE['call'])
            self.ident()
        elif self.token == INVERSE_KEYWORD_HASH_TABLE['begin']:
            self.match(INVERSE_KEYWORD_HASH_TABLE['begin'])
            self.statement()
            while self.token == INVERSE_OPERATOR_HASH_TABLE[';']:
                self.match(INVERSE_OPERATOR_HASH_TABLE[';'])
                self.statement()
            self.match(INVERSE_KEYWORD_HASH_TABLE['end'])
        elif self.token == INVERSE_KEYWORD_HASH_TABLE['if']:
            self.match(INVERSE_KEYWORD_HASH_TABLE['if'])
            self.condition()
            self.match(INVERSE_KEYWORD_HASH_TABLE['then'])
            self.statement()
        elif self.token == INVERSE_KEYWORD_HASH_TABLE['while']:
            self.match(INVERSE_KEYWORD_HASH_TABLE['while'])
            self.condition()
            self.match(INVERSE_KEYWORD_HASH_TABLE['do'])
            self.statement()
        else:
            self.err('Could not parse statement')

    def condition(self):
        if self.token == INVERSE_KEYWORD_HASH_TABLE['odd']:
            self.match(INVERSE_KEYWORD_HASH_TABLE['odd'])
            self.expression()
        else:
            self.expression()
            self.match(None, [
                INVERSE_OPERATOR_HASH_TABLE['='],
                INVERSE_OPERATOR_HASH_TABLE['#'],
                INVERSE_OPERATOR_HASH_TABLE['<'],
                INVERSE_OPERATOR_HASH_TABLE['<='],
                INVERSE_OPERATOR_HASH_TABLE['>'],
                INVERSE_OPERATOR_HASH_TABLE['>='],
            ])
            self.expression()

    def expression(self):
        if self.token == INVERSE_OPERATOR_HASH_TABLE['+'] or self.token == INVERSE_OPERATOR_HASH_TABLE['-']:
            self.match(None, [
                INVERSE_OPERATOR_HASH_TABLE['+'],
                INVERSE_OPERATOR_HASH_TABLE['-']
            ])
        self.term()
        while self.token == INVERSE_OPERATOR_HASH_TABLE['+'] or self.token == INVERSE_OPERATOR_HASH_TABLE['-']:
            self.match(None, [
                INVERSE_OPERATOR_HASH_TABLE['+'],
                INVERSE_OPERATOR_HASH_TABLE['-']
            ])
            self.term()

    def term(self):
        self.factor()
        while self.token == INVERSE_OPERATOR_HASH_TABLE['*'] or self.token == INVERSE_OPERATOR_HASH_TABLE['/']:
            self.match(None, [
                INVERSE_OPERATOR_HASH_TABLE['*'],
                INVERSE_OPERATOR_HASH_TABLE['/']
            ])
            self.factor()

    def factor(self):
        if self.token[0] == '0':
            self.ident()
        elif self.token[0] == '1':
            self.number()
        elif self.token == INVERSE_OPERATOR_HASH_TABLE['(']:
            self.match(INVERSE_OPERATOR_HASH_TABLE['('])
            self.expression()
            self.match(INVERSE_OPERATOR_HASH_TABLE[')'])
        else:
            self.err("Could not parse factor")

    def ident(self):
        if self.token[0] == '0':
            self.next()
        else:
            self.err("Expected an identifier")

    def number(self):
        if self.token[0] == '1':
            self.next()
        else:
            self.err("Expected a numeral")

    def match(self, expect, expects=[]):
        if self.token == expect or (len(expects) > 0 and self.token in expects):
            self.next()
        else:
            t = OPERATOR_HASH_TABLE[expect] if expect in OPERATOR_HASH_TABLE else KEYWORD_HASH_TABLE[expect]
            self.err(f'Expected a "{t}"')

    def next(self):
        if self.i < len(self.tokens):
            self.i += 1
            self.token = self.tokens[self.i]
        while self.token in SKIPS and self.i + 1 < len(self.tokens):
            self.i += 1
            self.token = self.tokens[self.i]

        print(f'token: {self.tokens[self.i]}')  # for debugging

    def err(self, msg):
        print(f'[Error]: {msg}')

        # error recovery here
        # loop thru keys until a valid compilation resume key is found

        quit()
