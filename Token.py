from sys import stderr


class Token(object):
    def __init__(self, code, value=None, line=0, column=0):
        self.code = code
        self.line = line
        self.column = column
        self.value = value

    def error(self, *args):
        print("Error at (%d:%d):" % (self.line, self.column), *args, file=stderr)

    def __str__(self):
        value = ''
        if self.value:
            value = ':' + str(self.value)

        return str(self.code) + value + ('(%d, %d)' % (self.line, self.column))