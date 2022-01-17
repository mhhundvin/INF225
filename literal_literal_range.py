from symbol import Generatable
from in_dict import in_dict, max_depth, new_depth
import exrex


class Literal(Generatable):
    def __init__(self, args):    # , rules, tokens, imports):
        self.args = args[0]
        # self.rules = rules
        # self.tokens = tokens
        # self.imports = imports
        
    def generate(self, depth):
        if depth > max_depth:
            return ''
        arg = self.args
        if (isinstance(arg, Generatable)):
            # print(f'---> literal is symbol: {arg}')
            depth = new_depth(arg, depth)
            return arg.generate(depth)
        return f'{arg}'

class Literal_range(Generatable):
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def generate(self, depth):
        if depth > max_depth:
            return ''
        arg = f'[{self.start}-{self.stop}]'
        return f'{exrex.getone(arg)}'

class Regular_expression(Generatable):
    def __init__(self, arg):
        self.arg = arg
    
    def generate(self, depth):
        return f'{exrex.getone(self.arg)}'