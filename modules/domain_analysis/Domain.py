from modules.domain_analysis.Symbol import Symbol
from modules.domain_analysis.SymbolTable import SymbolTable
from modules.domain_analysis.Type.CLS import CLS
from modules.domain_analysis.Type.MEM import MEM
from modules.domain_analysis.Type.TypeBase import TypeBase
from modules.domain_analysis.Type.Type import Type
from modules.lexical_analyzer.Tokens import Tokens


class Domain(object):
    def __init__(self, tokens):
        self._tokens = list(tokens)
        self._size = len(self._tokens)
        self._currentIndex = 0
        self._consumedToken = self._tokens[0]

        self._table = SymbolTable()
        self._depth = 0
        self._type = Type()

        self._current_struct = None
        self._current_func = None

    def start(self):
        self.reset()
        return self._unit()

    def reset(self):
        if not self._tokens:
            raise ValueError("Tokens list is empty, no need to parse!")

        self._currentIndex = 0
        self._consumedToken = self._tokens[0]
        self._depth = 0
        self._type = Type()
        self._table = SymbolTable()

        self._current_struct = None
        self._current_func = None

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

            print('unit')
            self._table.print()

        if not self.consume(Tokens.END):
            self.error(Tokens.END)

        return True

    def _declare_structure(self):
        # print(inspect.currentframe().f_code.co_name)
        start = self._currentIndex
        token_name = None
        if not self.consume(Tokens.STRUCT):
            return False

        if not self.consume(Tokens.ID):
            self.error(Tokens.ID)
        else:
            token_name = self._get_prv_crt_token().value

        if not self.consume(Tokens.LACC):
            self._currentIndex = start
            return False

        if self._find_symbol(self._table, token_name) is not None:
            self.error(custom="symbol redefinition:" + token_name)

        print('adding symbol from declare_structure')
        self._current_struct = self._add_symbol(self._table, token_name, CLS.CLS_STRUCT)
        self._init_symbols(self._current_struct)

        while True:
            if not self._declare_var():
                break

        if not self.consume(Tokens.RACC):
            self.error(Tokens.RACC)

        if not self.consume(Tokens.SEMICOLON):
            self.error(Tokens.SEMICOLON)
        else:
            self._current_struct = None  # we are no longer processing a structure

        return True

    def _declare_var(self):
        # print(inspect.currentframe().f_code.co_name)
        start = self._currentIndex
        token_name = None

        if not self._type_base():
            return False
        else:
            t = self._get_type_base()

        if not self.consume(Tokens.ID):
            self._currentIndex = start
            return False

        token_name = self._get_prv_crt_token().value
        print(t.type_base, token_name)

        if self._array_decl():
            t.number_of_elements = 0  # do not compute the real array size for now
        else:
            t.number_of_elements = -1

        self._add_var(token_name, t)

        while True:
            if not self.consume(Tokens.COMMA):
                break

            if not self.consume(Tokens.ID):
                self.error(custom="Expected Tokens.ID after ,")

            token_name = self._get_prv_crt_token().value
            if self._array_decl():
                t.number_of_elements = 0
            else:
                t.number_of_elements = -1
            self._add_var(token_name, t)

        if not self.consume(Tokens.SEMICOLON):
            self._currentIndex = start
            return False

        return True

    def _declare_function(self):
        # print(inspect.currentframe().f_code.co_name)

        t = None
        token_name = None

        if self._type_base():
            t = self._get_type_base()
            if self.consume(Tokens.MUL):
                t.no_of_elements = 0  # array no size
            else:
                t.no_of_elements = -1  # non-array
        elif self.consume(Tokens.VOID):
            t = Type()
            t.type_base = TypeBase.TB_VOID
        else:
            return False

        if not self.consume(Tokens.ID):
            self.error(Tokens.ID)
        else:
            token_name = self._get_prv_crt_token().value

        if not self.consume(Tokens.LPAR):
            self.error(Tokens.LPAR)

        #####
        if self._find_symbol(self._table, token_name) is not None:
            self.error(custom='symbol redefinition ' + token_name)
        self._current_func = self._add_symbol(self._table, token_name, CLS.CLS_FUNC)
        self._init_symbols(self._current_func)
        self._current_func.type = t
        self._increase_depth()
        #####

        self._declare_function_optional_part()

        if not self.consume(Tokens.RPAR):
            self.error(Tokens.RPAR)
        else:
            self._decrease_depth()

        if not self._stm_compound():
            self.error("Invalid statement")
        else:
            self._delete_symbol_after(self._table, self._current_func)

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
        else:
            self._type = self._get_type_base()

        if self._array_decl():
            pass
        else:
            self._type.number_of_elements = -1

        return True

    def _array_decl(self):
        # print(inspect.currentframe().f_code.co_name)
        if not self.consume(Tokens.LBRACKET):
            return False

        self._expr()

        self._type.number_of_elements = 0

        if not self.consume(Tokens.RBRACKET):
            self.error(Tokens.RBRACKET)

        return True

    def _func_arg(self):
        # print(inspect.currentframe().f_code.co_name)
        if not self._type_base():
            return False

        t = self._get_type_base()

        if not self.consume(Tokens.ID):
            self.error(Tokens.ID)

        token_name = self._get_prv_crt_token().value

        if self._array_decl():
            t.number_of_elements = 0
        else:
            t.number_of_elements = -1

        symbol = self._add_symbol(self._table, token_name, CLS.CLS_VAR)
        symbol.mem = MEM.MEM_ARG
        symbol.type = t

        symbol = self._add_symbol(self._current_func.getSymbolTable('args'), token_name, CLS.CLS_VAR)
        symbol.mem = MEM.MEM_ARG
        symbol.type = t

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
        start_symbol = self._table.get_last()

        if not self.consume(Tokens.LACC):
            return False
        else:
            self._increase_depth()

        while True:
            if self._declare_var() or self._stm():
                pass
            else:
                break

        if not self.consume(Tokens.RACC):
            self.error(Tokens.RACC)

        # restore level in the table and remove nested context
        self._decrease_depth()
        self._delete_symbol_after(self._table, start_symbol)

        return True

    def _find_symbol(self, table, token_name):
        return table.find(token_name)

    def _add_symbol(self, table, name, cls):
        symbol = Symbol(name, cls)
        symbol.depth = self._depth

        table.add(symbol)
        return symbol

    def _delete_symbol_after(self, table, symbol):
        table.delete_after(symbol)

    def _get_type_base(self):
        token = self._get_prv_crt_token()
        ret = Type()

        # special case if it is a structure
        token_struct = self._get_prv_crt_token(1)

        if token.code == Tokens.INT:
            ret.type_base = TypeBase.TB_INT
        elif token.code == Tokens.DOUBLE:
            ret.type_base = TypeBase.TB_DOUBLE
        elif token.code == Tokens.CHAR:
            ret.type_base = TypeBase.TB_CHAR
        elif token_struct.code == Tokens.STRUCT:
            token = self._tokens[self._currentIndex - 1]
            token_name = token.value

            symbol = self._find_symbol(self._table, token_name)
            if symbol is None:
                self.error(custom='Undefined symbol ' + token_name)

            if symbol.cls != CLS.CLS_STRUCT:
                self.error(custom=token_name + 'is not a structure')

            ret.type_base = TypeBase.TB_STRUCT
            ret.symbol = symbol

        return ret

    def _add_var(self, token_name, t):
        if self._current_struct is not None:
            print('add var struct')
            current_struct = self._current_struct
            members = current_struct.getSymbolTable('members')
            if self._find_symbol(members, token_name) is not None:
                self.error(custom='Symbol redefinition' + token_name)

            print('adding symbol from add_var#1')
            symbol = self._add_symbol(self._table, token_name, CLS.CLS_VAR)
            symbol.mem = MEM.MEM_LOCAL
        elif self._current_func is not None:
            symbol = self._find_symbol(self._table, token_name)
            print('add var function')
            if symbol is not None:
                print('found symbol at depth ' + str(symbol.depth))

                if symbol.depth == self._depth:
                    self.error(custom='symbol redefinition:' + token_name)

            print('adding symbol from add_var#2')
            symbol = self._add_symbol(self._table, token_name, CLS.CLS_VAR)
            symbol.mem = MEM.MEM_LOCAL
        else:
            symbol = self._find_symbol(self._table, token_name)
            print('add var simple', symbol)
            if symbol is not None:
                self.error(custom='symbol redefinition:' + token_name)
            print('adding symbol from add_var#3')
            symbol = self._add_symbol(self._table, token_name, CLS.CLS_VAR)
            symbol.mem = MEM.MEM_GLOBAL

        symbol.type = t

    def _init_symbols(self, symbol):
        t = None
        if symbol.cls == CLS.CLS_STRUCT:
            t = 'members'
        elif symbol.cls == CLS.CLS_FUNC:
            t = 'args'

        symbol.initSymbolTable(t)

    def _get_prv_crt_token(self, offset=0):
        index = self._tokens.index(self._consumedToken)

        if index >= offset:
            return self._tokens[index - offset]
        else:
            return self._consumedToken

    def _increase_depth(self):
        self._depth += 1
        print('Depth increased ' + str(self._depth))

    def _decrease_depth(self):
        self._depth -= 1
        print('Depth decreased ' + str(self._depth))