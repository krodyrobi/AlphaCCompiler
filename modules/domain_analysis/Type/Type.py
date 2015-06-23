
class Type(object):
    def __init__(self, type_base=None):
        self.type_base = type_base
        self.symbol = None

        #  >0 array of given size
        #  =0 array no size
        #  <0 non-array
        self.no_of_elements = -1

    def duplicate(self):
        t = Type()

        t.type_base = self.type_base
        t.no_of_elements = self.no_of_elements
        t.symbol = self.symbol

        return t