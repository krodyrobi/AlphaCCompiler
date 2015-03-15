import string
from Token import Token
from sys import exit
from Tokens import Tokens


class Lexer(object):
    keywords_map = {
        'if':     Tokens.IF,
        'else':   Tokens.ELSE,
        'for':    Tokens.FOR,
        'while':  Tokens.WHILE,
        'break':  Tokens.BREAK,
        'char':   Tokens.CHAR,
        'double': Tokens.DOUBLE,
        'int':    Tokens.INT,
        'return': Tokens.RETURN,
        'void':   Tokens.VOID,
        'struct': Tokens.STRUCT
    }

    def __init__(self):
        self.__prepare_scan()

    def scan(self, file_path):
        self.__prepare_scan()
        end_hit = False
        offset = 0
        integer_base = 10

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

                    # Comments + DIV
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

                    # ID
                    elif self.character in string.ascii_letters + '_':
                        self.state = 42
                        marker = f.tell() - 1
                        self._consume_char(f)

                    # CT_INT
                    elif self.character == '0':
                        self.state = 44
                        marker = f.tell() - 1
                        self._consume_char(f)
                    elif self.character in '123456789':
                        self.state = 50
                        marker = f.tell() - 1
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
                    value = self._getString(f, marker, -2)
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
                    value = self._getString(f, marker, -2)
                    self._create_token(Tokens.CT_STRING, value=value)

                # ID
                elif self.state == 42:
                    if self.character in string.ascii_letters + string.digits + '_':
                        self._consume_char(f)
                        # If file ends right after this character jump to
                        # finalize the ID
                        if not self.character:
                            self.state = 43
                            offset = 0
                        else:
                            offset = -1
                            self.state = 42
                    else:
                        self.state = 43
                elif self.state == 43:
                    value = self._getString(f, marker, offset)
                    code = self.keywords_map.get(value, Tokens.ID)

                    if code != Tokens.ID:
                        value = None
                    self._create_token(code, value)

                # CT_INT
                elif self.state == 44:
                    if self.character == 'x':
                        integer_base = 16
                        self.state = 45
                        self._consume_char(f)
                    elif self.character in '89':
                        self.state = 48
                        self._consume_char(f)
                    else:
                        self.state = 47
                elif self.state == 45:
                    if self.character in string.hexdigits:
                        self.state = 46
                        self._consume_char(f)
                    else:
                        self._token_error(Tokens.CT_INT, string.hexdigits, self.character)
                elif self.state == 46:
                    if self.character in string.hexdigits:
                        self.state = 46
                        self._consume_char(f)
                    else:
                        self.state = 51
                elif self.state == 47:
                    integer_base = 8
                    if self.character in '01234567':
                        self._consume_char(f)
                        if not self.character:
                            self.state = 51
                            offset = 0
                        else:
                            self.state = 47
                            offset = -1
                    elif self.character == '.':
                        self.state = 52
                        self._consume_char(f)
                    elif self.character in '89':
                        self._consume_char(f)
                        self.state = 49
                    elif self.character in 'eE':
                        self._consume_char(f)
                        self.state = 54
                    else:
                        self.state = 51
                elif self.state == 48:
                    if self.character in string.digits:
                        self.state = 48
                        self._consume_char(f)
                    elif self.character == '.':
                        self.state = 52
                        self._consume_char(f)
                    elif self.character in 'eE':
                        self._consume_char(f)
                        self.state = 54
                    else:
                        self._token_error(Tokens.CT_REAL, expected_chars='eE.'+string.digits, got=self.character)
                elif self.state == 49:
                    if self.character in string.digits:
                        self.state = 49
                        self._consume_char(f)
                    elif self.character == '.':
                        self.state = 52
                        self._consume_char(f)
                    elif self.character in 'eE':
                        self._consume_char(f)
                        self.state = 54
                    else:
                        self._token_error(Tokens.CT_REAL, expected_chars='eE.'+string.digits, got=self.character)
                elif self.state == 50:
                    integer_base = 10
                    if self.character in string.digits:
                        self._consume_char(f)
                        if not self.character:
                            self.state = 51
                            offset = 0
                        else:
                            self.state = 50
                            offset = -1
                    elif self.character == '.':
                        self.state = 52
                        self._consume_char(f)
                    elif self.character in 'eE':
                        self._consume_char(f)
                        self.state = 54
                    else:
                        self.state = 51
                elif self.state == 51:
                    value = int(self._getString(f, marker, offset), integer_base)
                    self._create_token(Tokens.CT_INT, value)
                elif self.state == 52:
                    if self.character in string.digits:
                        self.state = 53
                        self._consume_char(f)
                    else:
                        self._token_error(Tokens.CT_REAL, expected_chars=string.digits, got=self.character)
                elif self.state == 53:
                    if self.character in string.digits:
                        self._consume_char(f)
                        if not self.character:
                            self.state = 57
                            offset = 0
                        else:
                            self.state = 53
                            offset = -1
                    elif self.character in 'eE':
                        self.state = 54
                        self._consume_char(f)
                    else:
                        self.state = 57
                elif self.state == 54:
                    if self.character in '+-':
                        self.state = 55
                        self._consume_char(f)
                    else:
                        self.state = 55
                elif self.state == 55:
                    if self.character in string.digits:
                        self.state = 56
                        self._consume_char(f)
                    else:
                        self._token_error(Tokens.CT_REAL, expected_chars=string.digits, got=self.character)
                elif self.state == 56:
                    if self.character in string.digits:
                        self._consume_char(f)

                        if not self.character:
                            self.state = 57
                            offset = 0
                        else:
                            self.state = 56
                            offset = -1
                    else:
                        self.state = 57
                elif self.state == 57:
                    value = float(self._getString(f, marker, offset))
                    self._create_token(Tokens.CT_REAL, value)

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
        for token in self.tokens:
            print(str(token))

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
            expected_chars = 'Expected [' + expected_chars + ']'
            got = ', but got ' + repr(got) + ' instead'

        # to be removed only for debugging
        self.show_tokens()

        if not custom:
            token.error(expected_chars, got)
        else:
            token.error(custom)

        exit(1)

    def _getString(self, file, marker, offset=0):
        current = file.tell()

        file.seek(marker)
        value = file.read(current - marker + offset)

        file.seek(current)

        return value