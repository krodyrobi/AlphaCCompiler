

class Syntax(object):
    def __init__(self, tokens):
        self.currentIndex = 9
        self.tokens = tokens
        self.consumedToken = None
        self.size = len(tokens)

    def consume(self, token):
        if self.currentIndex >= self.size:
            return False

        tok = self.tokens[self.currentIndex]
        if token == tok:
            self.consumedToken = tok
            self.currentIndex += 1
            return True

        return False