

class SymbolTable(object):
    def __init__(self):
        self.table = []

    def add(self, symbol):
        print('Adding ' + str(symbol))
        self.table.append(symbol)

    def find(self, name):
        print('find ' + name)
        for item in reversed(self.table):
            if item.name == name:
                return item

        return None

    def delete_after(self, symbol):
        print('delete after')
        try:
            index = self.table.index(symbol)
            print('Removing indexes:' + str(index) + ' ' + str(len(self.table)))

            self.table = self.table[:index]
        except ValueError:
            print('Not in the table')

    def get_last(self):
        try:
            return self.table[-1]
        except IndexError:
            return None

    def get_beginning(self):
        try:
            return self.table[0]
        except IndexError:
            return None

    def get_index(self, index):
        try:
            return self.table[index]
        except IndexError:
            return None

    def clear(self):
        self.table = []

    def print(self):
        for symbol in self.table:
            print(symbol)

            table = symbol.getSymbolTable('args')
            if table is not None:
                if len(table) == 0:
                    print("No args")
                else:
                    print("Function args:")
                    table.print()

            table = symbol.getSymbolTable('members')
            if table is not None:
                if len(table) == 0:
                    print("No members")
                else:
                    print("Members:")
                    table.print()

    def size(self):
        return len(self.table)