from modules.domain_analysis.SymbolTable import SymbolTable
from modules.domain_analysis.Type.CLS import CLS
from modules.domain_analysis.Type.MEM import MEM


class Symbol(object):
    def __init__(self, name, cls):
        self.name = name
        self.cls = cls
        self.mem = MEM.MEM_GLOBAL
        self.type = None
        self.depth = 0  # 0=global, 1=function, 2=nested etc

        self.args = None  # only used by functions
        self.members = None  # only used by structs

        if cls == CLS.CLS_STRUCT:
            members = SymbolTable()
        elif cls == CLS.CLS_FUNC or cls == CLS.CLS_EXTFUNC:
            args = SymbolTable()

    def getSymbolTable(self, t):
        if t == 'args':
            return self.args
        elif t == 'members':
            return self.members
        else:
            return None

    def initSymbolTable(self, t):
        if t == 'args':
            self.args = None
        elif t == 'members':
            self.members = None

    def __str__(self):
        cls = "None"
        mem = "None"
        nbr = "-1"
        type_base = "None"
        depth = str(self.depth)
        name = self.name

        if self.type is not None:
            type_base = self.type.type_base
            nbr = self.type.no_of_elements
        if self.cls is not None:
            cls = self.cls
        if self.mem is not None:
            mem = self.mem

        return 'Name: {name}, Type: {type_base}, NO: {nbr}, CLS: {cls}, MEM: {mem}, Depth: {depth}'.format(name=name,
                                                                                                           type_base=type_base,
                                                                                                           nbr=nbr,
                                                                                                           cls=cls,
                                                                                                           depth=depth,
                                                                                                           mem=mem)

    def __eq__(self, other):
        return other.name == self.name