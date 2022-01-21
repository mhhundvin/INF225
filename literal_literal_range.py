from symbol import Generatable
from in_dict import in_dict, max_depth, new_depth
import exrex
import re


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
    
    def generate_shortest(self, rule):
        arg = self.args
        if (isinstance(arg, Generatable)):
            return arg.generate(rule)
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
    
    def generate_shortest(self, rule):
        arg = f'[{self.start}-{self.stop}]'
        return f'{exrex.getone(arg)}'

class Regular_expression(Generatable):
    def __init__(self, arg):
        self.arg = arg
    
    def generate(self, depth):
        new = re.sub('\\\p{Lu}', 'A-Z', self.arg)
        new = re.sub('\\\p{Ll}', 'a-z', new)
        new = re.sub('\\\p{..}', '', new)
        new = re.sub('\\\w', '[A-Za-Z0-9_]', new)
        new = re.sub('\\\W', '[^A-Za-Z0-9_]', new)
        new = re.sub('\\\D', '[^0-9]', new)
        # new = re.sub('\\\S', '[???]', new)
        return f'{exrex.getone(self.arg)}'

    def generate_shortest(self, rule):
        return f'{exrex.getone(self.arg)}'