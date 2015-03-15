from enum import Enum


class AutoNumber(Enum):
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        
        return obj


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