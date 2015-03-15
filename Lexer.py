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
        marker = -1

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

                    # 2 character operators
                    elif self.character == '<':
                        self.state = 13
                        self._consume_char(f)
                    elif self.character == '>':
                        self.state = 16
                        self._consume_char(f)
                    elif self.character == '=':
                        self.state = 19
                        self._consume_char(f)
                    elif self.character == '!':
                        self.state = 22
                        self._consume_char(f)
                    elif self.character == '|':
                        self.state = 25
                        self._consume_char(f)
                    elif self.character == '&':
                        self.state = 27
                        self._consume_char(f)
                    elif self.character == '/':
                        self.state = 31
                        self._consume_char(f)
                    elif self.character == '\'':
                        self.state = 34
                        marker = f.tell()
                        self._consume_char(f)
                    elif self.character == '"':
                        self.state = 38
                        marker = f.tell()
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
                elif self.state == 13:
                    if self.character == '=':
                        self.state = 15
                        self._consume_char(f)
                    else:
                        self.state = 14
                elif self.state == 14:
                    self._create_token(Tokens.LESS)
                elif self.state == 15:
                    self._create_token(Tokens.LESSEQ)

                elif self.state == 16:
                    if self.character == '=':
                        self.state = 18
                        self._consume_char(f)
                    else:
                        self.state = 17
                elif self.state == 17:
                    self._create_token(Tokens.GREATER)
                elif self.state == 18:
                    self._create_token(Tokens.GREATEREQ)

                elif self.state == 19:
                    if self.character == '=':
                        self.state = 21
                        self._consume_char(f)
                    else:
                        self.state = 20
                elif self.state == 20:
                    self._create_token(Tokens.ASSIGN)
                elif self.state == 21:
                    self._create_token(Tokens.EQUAL)

                elif self.state == 22:
                    if self.character == '=':
                        self.state = 24
                        self._consume_char(f)
                    else:
                        self.state = 23
                elif self.state == 23:
                    self._create_token(Tokens.NOT)
                elif self.state == 24:
                    self._create_token(Tokens.NOTEQ)

                elif self.state == 25:
                    if self.character == '|':
                        self.state = 26
                        self._consume_char(f)
                    else:
                        self._token_error(Tokens.OR, expected_chars='|', got=self.character)
                elif self.state == 26:
                    self._create_token(Tokens.OR)

                elif self.state == 27:
                    if self.character == '&':
                        self.state = 28
                        self._consume_char(f)
                    else:
                        self._token_error(Tokens.AND, expected_chars='&', got=self.character)
                elif self.state == 28:
                    self._create_token(Tokens.AND)

                # Comments and DIV token
                elif self.state == 29:
                    if self.character not in "*/":
                        self.state = 30
                        self._consume_char(f)
                    elif self.character == '*':
                        self.state = 29
                        self._consume_char(f)
                    elif self.character == '/':
                        self.state = 0
                        self._consume_char(f)
                elif self.state == 30:
                    if self.character not in '*':
                        if self.character in "\n\r":
                            self.line += 1
                            self.column = -1
                        self.state = 30
                        self._consume_char(f)
                    elif self.character == '*':
                        self.state = 29
                        self._consume_char(f)
                elif self.state == 31:
                    if self.character == '*':
                        self.state = 30
                        self._consume_char(f)
                    elif self.character == '/':
                        self.state = 32
                        self._consume_char(f)
                    else:
                        self.state = 33
                elif self.state == 32:
                    if self.character not in "\n\r\0":
                        self.state = 32
                        self._consume_char(f)
                    else:
                        self.state = 0
                elif self.state == 33:
                    self._create_token(Tokens.DIV)


                elif self.state == 34:
                    if self.character == '\\':
                        self.state = 35
                        self._consume_char(f)
                    elif self.character not in "'\\":
                        self.state = 36
                        self._consume_char(f)
                    else:
                        self._token_error(Tokens.CT_CHAR)
                elif self.state == 35:
                    if self.character in 'abfnrtv\'?"0\\':
                        self.state = 36
                        self._consume_char(f)
                    else:
                        self._token_error(Tokens.CT_CHAR, custom="Expected escape sequence")
                elif self.state == 36:
                    if self.character == '\'':
                        self.state = 37
                        self._consume_char(f)
                    else:
                        self._token_error(Tokens.CT_CHAR, expected_chars='\'', got=self.character)
                elif self.state == 37:
                    value = self._getString(f, marker, f.tell(), -2)
                    self._create_token(Tokens.CT_CHAR, value=value)
                elif self.state == 38:
                    if self.character == '"':
                        self.state = 41
                        self._consume_char(f)
                    elif self.character == '\\':
                        self.state = 39
                        self._consume_char(f)
                    elif self.character not in "\"\\":
                        self.state = 40
                        self._consume_char(f)
                    else:
                        self._token_error(Tokens.CT_STRING)
                elif self.state == 39:
                    if self.character in 'abfnrtv\'?"0\\':
                        self.state = 40
                        self._consume_char(f)
                    else:
                        self._token_error(Tokens.CT_STRING, custom="Expected escape sequence")
                elif self.state == 40:
                    if self.character == '"':
                        self.state = 41
                        self._consume_char(f)
                    else:
                        self.state = 38
                elif self.state == 41:
                    value = self._getString(f, marker, f.tell(), -2)
                    self._create_token(Tokens.CT_STRING, value=value)


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
        self.character = None

    def _consume_char(self, file):
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
            got = 'but got "' + got + '" instead'

        # to be removed only for debugging
        self.show_tokens()

        if not custom:
            token.error(expected_chars, got)
        else:
            token.error(custom)

        exit(1)

    def _getString(self, file, marker, current, offset=0):
        file.seek(marker)
        value = file.read(current - marker + offset)
        file.seek(current)

        return value