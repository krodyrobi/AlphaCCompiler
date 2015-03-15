import string
from Token import Token
from sys import exit
from Tokens import Tokens


class Lexer(object):
    def __init__(self):
        self.__prepare_scan()

    def scan(self, file_path):
        self.__prepare_scan()
        end_hit = False

        with open(file_path, 'r') as f:
            self._consume_char(f)

            while True:
                if self.state == 0:
                    if self.character in " \t\r":
                        self._consume_char(f)
                    elif self.character == "\n":
                        self.line += 1
                        self.column = -1
                        self._consume_char(f)
                    elif self.character == '+':
                        self.state = 1
                        self._consume_char(f)
                    elif self.character == '-':
                        self.state = 2
                        self._consume_char(f)
                    elif self.character == '*':
                        self.state = 3
                        self._consume_char(f)
                    elif self.character == '.':
                        self.state = 4
                        self._consume_char(f)
                    elif self.character == '{':
                        self.state = 5
                        self._consume_char(f)
                    elif self.character == '}':
                        self.state = 6
                        self._consume_char(f)
                    elif self.character == ']':
                        self.state = 7
                        self._consume_char(f)
                    elif self.character == '[':
                        self.state = 8
                        self._consume_char(f)
                    elif self.character == ')':
                        self.state = 9
                        self._consume_char(f)
                    elif self.character == '(':
                        self.state = 10
                        self._consume_char(f)
                    elif self.character == ';':
                        self.state = 11
                        self._consume_char(f)
                    elif self.character == ',':
                        self.state = 12
                        self._consume_char(f)


                elif self.state == 1:
                    self._create_token(Tokens.ADD)
                elif self.state == 2:
                    self._create_token(Tokens.SUB)
                elif self.state == 3:
                    self._create_token(Tokens.MUL)
                elif self.state == 4:
                    self._create_token(Tokens.DOT)
                elif self.state == 5:
                    self._create_token(Tokens.LACC)
                elif self.state == 6:
                    self._create_token(Tokens.RACC)
                elif self.state == 7:
                    self._create_token(Tokens.RBRACKET)
                elif self.state == 8:
                    self._create_token(Tokens.LBRACKET)
                elif self.state == 9:
                    self._create_token(Tokens.RPAR)
                elif self.state == 10:
                    self._create_token(Tokens.LPAR)
                elif self.state == 11:
                    self._create_token(Tokens.SEMICOLON)
                elif self.state == 12:
                    self._create_token(Tokens.COMMA)

                # Check end of file
                # check it last so the previous consumed char
                # won't mess things up and make sure we gave the loop
                # one more run before we trigger the END event
                if end_hit:
                    self.column += 1
                    if self.state != 0:
                        self._token_error(Tokens.END, custom='Unexpected end of file')
                    else:
                        self._create_token(Tokens.END)
                        break

                if not self.character:
                    end_hit = True

    def show_tokens(self):
        print([str(token) for token in self.tokens])

    def __prepare_scan(self):
        self.tokens = []
        self.line = 1
        self.column = -1
        self.state = 0
        self.cur_pos = -1
        self.character = None

    def _consume_char(self, file):
        self.cur_pos += 1
        self.column += 1
        self.character = file.read(1)

    def _create_token(self, code, value=None):
        token = Token(code, value, self.line, self.column)
        self.state = 0

        self.tokens.append(token)

    def _token_error(self, code, expected_chars='', got='', custom=''):
        token = Token(code=code, line=self.line, column=self.column)

        if expected_chars and got:
            expected_chars = 'Expected ' + expected_chars
            got = 'but got ' + got + 'instead'

        # to be removed only for debugging
        self.show_tokens()

        if not custom:
            token.error(expected_chars, got)
        else:
            token.error(custom)

        exit(1)