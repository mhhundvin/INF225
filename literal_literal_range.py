from symbol import Symbol
from in_dict import in_dict
import exrex


class Literal(Symbol):
    def __init__(self, args, rules, tokens, imports):
        self.args = args[0]
        self.rules = rules
        self.tokens = tokens
        self.imports = imports
        
    
    def generate(self, depth):
        if depth > 10:
            return ''
        depth += 1
        arg = self.args
        arg = in_dict(arg, self.rules, self.tokens, self.imports)
        if (isinstance(arg, Symbol)):
            return arg.generate(depth)
        return f'{arg}'

class Literal_range(Symbol):
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def generate(self, depth):
        if depth > 10:
            return ''
        depth += 1
        arg = f'[{self.start}-{self.stop}]'
        return f'{exrex.getone(arg)}'