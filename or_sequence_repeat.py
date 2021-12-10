import enum
from symbol import Symbol
from random import choice
from in_dict import in_dict

class Or(Symbol):
    def __init__(self, args, rules, tokens, imports):
        self.args = args
        self.rules = rules
        self.tokens = tokens
        self.imports = imports

    def generate(self, depth):
        if depth > 10:
            return ''
        depth += 1
        arg = choice(self.args)
        # print(f'Or.generate arg: {arg}')
        arg = in_dict(arg, self.rules, self.tokens, self.imports)
            
        if isinstance(arg, Symbol):
            x = arg.generate(depth)
            # print(f'\t\tOR if: x: {x} - arg {arg}')
            return x
        # else:
            # print(f'\t-->OR: "{arg}" Type: {type(arg)}')
        return ''

class Sequence(Symbol):
    def __init__(self, args, rules, tokens, imports):
        self.args = args
        self.rules = rules
        self.tokens = tokens
        self.imports = imports

    def generate(self, depth):
        if depth > 10:
            return ''
        depth += 1
        # print(f'Sequence args: {self.args}')
        text = ''
        for idx, arg in enumerate(self.args):
            # print(f'\t{idx} --> Sequence arg: {arg}')
            arg = in_dict(arg, self.rules, self.tokens, self.imports)
            # print(f'\t-->Sequence in_dict: {arg}')

            if isinstance(arg, Symbol):
                # print(f'\t\t-->isinstance: true\t arg: {arg}')
                x = arg.generate(depth)
                # print(f'\t\t\tSeq --> x {x}\targ: {arg}')
                text += x
                # print(f'\t\t--> text: {text}')
            else:
                print(f'\tELSE --> arg: {arg}')
                # text += arg
                
        return text

class Repeat(Symbol):
    def __init__(self, args, start, stop, rules, tokens, imports):
        self.args = args
        self.start = start
        self.stop = stop
        self.rules = rules
        self.tokens = tokens
        self.imports = imports
    
    def generate(self, depth):
        if depth > 10:
            return ''
        depth += 1
        arg = self.args
        arg = in_dict(arg, self.rules, self.tokens, self.imports)

        # print(f'REPEAT: {self.args} -> {arg}')
        # print(f'isinstance(arg, Symbol): {isinstance(arg, Symbol)}')
        text = ''
        if isinstance(arg, Symbol):
            for i in range(int(self.start), int(self.stop)):
                # print(f'\ti = {i}')
                text += arg.generate(depth)
        return text