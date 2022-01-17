class Generatable():
    pass


class NonTerminal():
    def __init__(self, args):
        self.args = args

    def __repr__(self):
        return self.args
    
    def __eq__(self, other):
        if isinstance(other, NonTerminal):
            return self.args == other.args
    def __hash__(self):
        return hash(self.args)

class Terminal():
    def __init__(self, args):
        self.args = args

    def __repr__(self):
        return self.args
    
    def __eq__(self, other):
        if isinstance(other, Terminal):
            return self.args == other.args
    def __hash__(self):
        return hash(self.args)

class Token():
    def __init__(self, args):
        self.args = args

    def __repr__(self):
        return self.args
    
    def __eq__(self, other):
        if isinstance(other, Token):
            return self.args == other.args
    def __hash__(self):
        return hash(self.args)
