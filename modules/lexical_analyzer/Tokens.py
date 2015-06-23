from modules.helpers.AutoNumber import AutoNumber


class Tokens(AutoNumber):

    # Identifiers
    ID = ()

    # Constants
    CT_INT = ()
    CT_REAL = ()
    CT_STRING = ()
    CT_CHAR = ()

    # Operations
    DIV = ()
    ADD = ()
    SUB = ()
    MUL = ()
    DOT = ()
    AND = ()
    OR = ()
    NOT = ()
    NOTEQ = ()
    ASSIGN = ()
    EQUAL = ()
    GREATEREQ = ()
    GREATER = ()
    LESSEQ = ()
    LESS = ()
    COMMA = ()
    SEMICOLON = ()
    LPAR = ()
    RPAR = ()
    LBRACKET = ()
    RBRACKET = ()
    RACC = ()
    LACC = ()

    # Keywords
    BREAK = ()
    CHAR = ()
    DOUBLE = ()
    ELSE = ()
    FOR = ()
    IF = ()
    INT = ()
    RETURN = ()
    STRUCT = ()
    VOID = ()
    WHILE = ()

    END = ()

    # def __str__(self):
    #    return str(self.value)