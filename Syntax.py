import inspect
from Tokens import Tokens


class Syntax(object):
    def __init__(self, tokens):
        self._tokens = list(tokens)
        self._size = len(self._tokens)
        self._currentIndex = 0
        self._consumedToken = self._tokens[0]

    def start(self):
        self.reset()
        return self._unit()

    def reset(self):
        if not self._tokens:
            raise ValueError("Tokens list is empty, no need to parse!")

        self._currentIndex = 0
        self._consumedToken = self._tokens[0]

    def error(self, expected_token=None, custom=None):
        if self._currentIndex >= self._size:
            exit(1)

        token = self._tokens[self._currentIndex]
        if custom:
            token.error(custom)
        elif expected_token:
            expected = 'Expected ' + str(expected_token)
            got = ', but got ' + str(token) + ' instead'

            token.error(expected, got)

        exit(1)

    def consume(self, token):
        if self._currentIndex >= self._size:
            return False

        tok = self._tokens[self._currentIndex]

        # print('to consume: ' + str(token) + ' got ' + str(tok))
        if tok.has_code(token):
            self._consumedToken = tok
            self._currentIndex += 1
            # print('consumed')
            return True

        return False

    def _unit(self):
        # print(inspect.currentframe().f_code.co_name)
        while True:
            if self._declare_structure():
                pass
            elif self._declare_var():
                pass
            elif self._declare_function():
                pass
            else:
                break
        if not self.consume(Tokens.END):
            self.error(Tokens.END)

        return True

    def _declare_structure(self):
        # print(inspect.currentframe().f_code.co_name)
        start = self._currentIndex
        if not self.consume(Tokens.STRUCT):
            return False

        if not self.consume(Tokens.ID):
            self.error(Tokens.ID)

        if not self.consume(Tokens.LACC):
            self._currentIndex = start
            return False

        while True:
            if not self._declare_var():
                break

        if not self.consume(Tokens.RACC):
            self.error(Tokens.RACC)

        if not self.consume(Tokens.SEMICOLON):
            self.error(Tokens.SEMICOLON)

        return True

    def _declare_var(self):
        # print(inspect.currentframe().f_code.co_name)
        start = self._currentIndex
        if not self._type_base():
            return False

        if not self.consume(Tokens.ID):
            self._currentIndex = start
            return False

        self._array_decl()

        while True:
            if not self.consume(Tokens.COMMA):
                break

            if not self.consume(Tokens.ID):
                self.error(custom="Expected Tokens.ID after ,")

            self._array_decl()

        if not self.consume(Tokens.SEMICOLON):
            self._currentIndex = start
            return False

        return True

    def _declare_function(self):
        # print(inspect.currentframe().f_code.co_name)
        if self._type_base():
            self.consume(Tokens.MUL)
        elif not self.consume(Tokens.VOID):
            return False

        if not self.consume(Tokens.ID):
            self.error(Tokens.ID)

        if not self.consume(Tokens.LPAR):
            self.error(Tokens.LPAR)

        self._declare_function_optional_part()

        if not self.consume(Tokens.RPAR):
            self.error(Tokens.RPAR)

        if not self._stm_compound():
            self.error("Invalid statement")

        return True

    def _declare_function_optional_part(self):
        # print(inspect.currentframe().f_code.co_name)
        if self._func_arg():
            while True:
                if self.consume(Tokens.COMMA):
                    if not self._func_arg():
                        self.error(custom="Expected expression after ,")
                else:
                    break
        return True

    def _type_base(self):
        # print(inspect.currentframe().f_code.co_name)
        if self.consume(Tokens.INT):
            pass
        elif self.consume(Tokens.DOUBLE):
            pass
        elif self.consume(Tokens.CHAR):
            pass
        elif self.consume(Tokens.STRUCT):
            if not self.consume(Tokens.ID):
                self.error(Tokens.ID)
        else:
            return False
        return True

    def _type_name(self):
        # print(inspect.currentframe().f_code.co_name)
        if not self._type_base():
            return False

        self._array_decl()
        return True

    def _array_decl(self):
        # print(inspect.currentframe().f_code.co_name)
        if not self.consume(Tokens.LBRACKET):
            return False

        self._expr()

        if not self.consume(Tokens.RBRACKET):
            self.error(Tokens.RBRACKET)

        return True

    def _func_arg(self):
        # print(inspect.currentframe().f_code.co_name)
        if not self._type_base():
            return False

        if not self.consume(Tokens.ID):
            self.error(Tokens.ID)

        self._array_decl()
        return True

    def _expr(self):
        # print(inspect.currentframe().f_code.co_name)
        return self._expr_assign()

    def _expr_assign(self):
        # print(inspect.currentframe().f_code.co_name)
        start = self._currentIndex
        if self._expr_unary():
            if self.consume(Tokens.ASSIGN):
                if self._expr_assign():
                    return True
                else:
                    self.error("Expected assignment expression")
            # We got here so we need to rewind the index
            self._currentIndex = start

        return self._expr_or()

    def _expr_or(self):
        # print(inspect.currentframe().f_code.co_name)
        if not self._expr_and():
            return False

        # since this will always return true due to epsilon
        # we can skip it's check
        self._expr_or_()
        return True

    def _expr_or_(self):
        # print(inspect.currentframe().f_code.co_name)
        if self.consume(Tokens.OR):
            if not self._expr_and():
                self.error(custom="Missing OR operand")
            self._expr_or_()

        return True

    def _expr_and(self):
        # print(inspect.currentframe().f_code.co_name)
        if not self._expr_eq():
            return False

        self._expr_and_()
        return True

    def _expr_and_(self):
        # print(inspect.currentframe().f_code.co_name)
        if self.consume(Tokens.AND):
            if not self._expr_eq():
                self.error(custom="Missing AND operand")
            self._expr_add_()

        return True

    def _expr_eq(self):
        # print(inspect.currentframe().f_code.co_name)
        if self._expr_rel():
            if self._expr_eq_():
                return True
        return False

    def _expr_eq_(self):
        # print(inspect.currentframe().f_code.co_name)
        if self.consume(Tokens.EQUAL) or self.consume(Tokens.NOTEQ):
            if self._expr_rel():
                if self._expr_eq_():
                    return True
            else:
                self.error(custom="Invalid expression")

        return True

    def _expr_rel(self):
        # print(inspect.currentframe().f_code.co_name)
        if not self._expr_add():
            return False

        self._expr_rel_()
        return True

    def _expr_rel_(self):
        # print(inspect.currentframe().f_code.co_name)
        if self.consume(Tokens.LESS) or self.consume(Tokens.LESSEQ) \
                or self.consume(Tokens.GREATER) or self.consume(Tokens.GREATEREQ):
            if self._expr_add():
                if self._expr_rel_():
                    return True
            else:
                self.error(custom="Invalid expression")

        return True

    def _expr_add(self):
        # print(inspect.currentframe().f_code.co_name)
        if not self._expr_mul():
            return False

        self._expr_add_()
        return True

    def _expr_add_(self):
        # print(inspect.currentframe().f_code.co_name)
        if self.consume(Tokens.ADD) or self.consume(Tokens.SUB):
            if self._expr_mul():
                if self._expr_add_():
                    return True
            else:
                self.error(custom="Invalid expression")

        return True

    def _expr_mul(self):
        # print(inspect.currentframe().f_code.co_name)
        if self._expr_cast():
            if self._expr_mul_():
                return True
        return False

    def _expr_mul_(self):
        # print(inspect.currentframe().f_code.co_name)
        if self.consume(Tokens.MUL) or self.consume(Tokens.DIV):
            if self._expr_cast():
                if self._expr_mul_():
                    return True
            else:
                self.error(custom="Invalid expression")

        return True

    def _expr_cast(self):
        # print(inspect.currentframe().f_code.co_name)
        if self.consume(Tokens.LPAR):
            if not self._type_name():
                self.error(custom="Cast type required")

            if not self.consume(Tokens.RPAR):
                self.error(Tokens.RPAR)

            if not self._expr_cast():
                self.error("Cast expression missing")
        elif self._expr_unary():
            pass
        else:
            return False
        return True

    def _expr_unary(self):
        # print(inspect.currentframe().f_code.co_name)
        if self.consume(Tokens.SUB) or self.consume(Tokens.NOT):
            if not self._expr_unary():
                self.error(custom="Missing unary expression after" + self._consumedToken.code)
        elif self._expr_postfix():
            pass
        else:
            return False
        return True

    def _expr_postfix(self):
        # print(inspect.currentframe().f_code.co_name)
        if not self._expr_primary():
            return False

        return self._expr_postfix_()

    def _expr_postfix_(self):
        # print(inspect.currentframe().f_code.co_name)
        if self.consume(Tokens.LBRACKET):
            if not self._expr():
                self.error(custom="Missing expression after [")

            if not self.consume(Tokens.RBRACKET):
                self.error(Tokens.RBRACKET)

            self._expr_postfix_()
        elif self.consume(Tokens.DOT):
            if not self.consume(Tokens.ID):
                self.error(Tokens.ID)
            self._expr_postfix_()

        return True

    def _expr_primary(self):
        # print(inspect.currentframe().f_code.co_name)
        start = self._currentIndex
        if self.consume(Tokens.ID):
            self._expr_primary_optional_part()
            return True
        elif self.consume(Tokens.CT_CHAR):
            return True
        elif self.consume(Tokens.CT_REAL):
            return True
        elif self.consume(Tokens.CT_INT):
            return True
        elif self.consume(Tokens.CT_STRING):
            return True
        elif self.consume(Tokens.LPAR):
            if not self._expr():
                self._currentIndex = start
                return False
            if not self.consume(Tokens.RPAR):
                self.error(Tokens.RPAR)
            return True
        return False

    def _expr_primary_optional_part(self):
        # print(inspect.currentframe().f_code.co_name)
        if not self.consume(Tokens.LPAR):
            return False

        if self._expr():
            while True:
                if self.consume(Tokens.COMMA):
                    if not self._expr():
                        self.error(custom="Expected expression after ,")
                else:
                    break

        if not self.consume(Tokens.RPAR):
            self.error(Tokens.RPAR)

        return True

    def _stm(self):
        # print(inspect.currentframe().f_code.co_name)
        if self._stm_compound():
            pass
        elif self.consume(Tokens.IF):
            if not self.consume(Tokens.LPAR):
                self.error(Tokens.LPAR)
            if not self._expr():
                self.error(custom="Invalid expression after (")
            if not self.consume(Tokens.RPAR):
                self.error(Tokens.RPAR)
            if not self._stm():
                self.error(custom="Missing if expression")
            if self.consume(Tokens.ELSE):
                if not self._stm():
                    self.error(custom="Missing else expression")
        elif self.consume(Tokens.WHILE):
            if not self.consume(Tokens.LPAR):
                self.error(Tokens.LPAR)
            if not self._expr():
                self.error(custom="Invalid expression after (")
            if not self.consume(Tokens.RPAR):
                self.error(Tokens.RPAR)
            if not self._stm():
                self.error(custom="Missing while expression")
        elif self.consume(Tokens.FOR):
            if not self.consume(Tokens.LPAR):
                self.error(Tokens.LPAR)

            self._expr()
            if not self.consume(Tokens.SEMICOLON):
                self.error(Tokens.SEMICOLON)
            self._expr()
            if not self.consume(Tokens.SEMICOLON):
                self.error(Tokens.SEMICOLON)
            self._expr()

            if not self.consume(Tokens.RPAR):
                self.error(Tokens.RPAR)
            if not self._stm():
                self.error(custom="Missing for expression")
        elif self.consume(Tokens.BREAK):
            if not self.consume(Tokens.SEMICOLON):
                self.error(Tokens.SEMICOLON)
        elif self.consume(Tokens.RETURN):
            self._expr()
            if not self.consume(Tokens.SEMICOLON):
                self.error(Tokens.SEMICOLON)
        elif self._expr():
            if not self.consume(Tokens.SEMICOLON):
                self.error(Tokens.SEMICOLON)
        elif self.consume(Tokens.SEMICOLON):
            pass
        else:
            return False
        return True

    def _stm_compound(self):
        # print(inspect.currentframe().f_code.co_name)
        if not self.consume(Tokens.LACC):
            return False

        while True:
            if self._declare_var() or self._stm():
                pass
            else:
                break

        if not self.consume(Tokens.RACC):
            self.error(Tokens.RACC)

        return True