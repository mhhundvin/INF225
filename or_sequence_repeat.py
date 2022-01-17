import enum
from symbol import Generatable
from random import choice
from in_dict import in_dict, new_depth, max_depth


class Or(Generatable):
    def __init__(self, args, rules, tokens, imports):
        self.args = args
        self.rules = rules
        self.tokens = tokens
        self.imports = imports

    def generate(self, depth):
        if depth > max_depth:
            return ''
        arg = choice(self.args)
        # print(f'Or.generate arg: {arg}')
        arg = in_dict(arg, self.rules, self.tokens, self.imports)
        
        if isinstance(arg, Generatable):
            depth = new_depth(arg, depth)
            x = arg.generate(depth)
            # print(f'\t\tOR if: x: {x} - arg {arg}')
            return x
        return ''

class Sequence(Generatable):
    def __init__(self, args, rules, tokens, imports):
        self.args = args
        self.rules = rules
        self.tokens = tokens
        self.imports = imports

    def generate(self, depth):
        if depth > max_depth:
            return ''
        # depth += 1
        # print(f'Sequence args: {self.args}')
        text = ''
        for idx, arg in enumerate(self.args):
            # print(f'\t{idx} --> Sequence arg: {arg} --> {type(arg)}')
            arg = in_dict(arg, self.rules, self.tokens, self.imports)
            # print(f'\t-->Sequence in_dict: {arg}')
            
            
            if isinstance(arg, Generatable):
                # print(f'\t\t-->isinstance: true\t arg: {arg}')
                depth = new_depth(arg, depth)
                x = arg.generate(depth)
                # print(f'\t\t\tSeq --> x {x}\targ: {arg}')
                # if x == '':
                #     return ''
                # else:
                text += x
                # print(f'\t\t--> text: {text}')
            else:
                print(f'\t\tSequence ELSE --> arg: {arg} --> {type(arg)}')
                # text += arg
                
        return text

class Repeat(Generatable):
    def __init__(self, args, start, stop, rules, tokens, imports):
        self.args = args
        self.start = start
        self.stop = stop
        self.rules = rules
        self.tokens = tokens
        self.imports = imports
    
    def generate(self, depth):
        if depth > max_depth:
            return ''
        arg = self.args
        arg = in_dict(arg, self.rules, self.tokens, self.imports)

        # print(f'REPEAT: {self.args} -> {arg}')
        # print(f'isinstance(arg, Generatable): {isinstance(arg, Generatable)}')
        text = ''
        if isinstance(arg, Generatable):
            for i in range(int(self.start), int(self.stop)):
                # print(f'\ti = {i}')
                depth = new_depth(arg, depth)
                x = arg.generate(depth)
                # if x == '':
                #     return ''
                # else:
                text += x
        return text

class Group(Generatable):
    def __init__(self, args, rules, tokens, imports):
        self.args = args
        self.rules = rules
        self.tokens = tokens
        self.imports = imports

    def generate(self, depth):
        if depth > max_depth:
            return ''
        text = ''
        for idx, arg in enumerate(self.args):
            arg = in_dict(arg, self.rules, self.tokens, self.imports)
            # print(f'\t-->Group in_dict: {arg}')

            if isinstance(arg, Generatable):
                # print(f'\t\t-->isinstance: true\t arg: {arg}')
                depth = new_depth(arg, depth)
                x = arg.generate(depth)
                # print(f'\t\t\tSeq --> x {x}\targ: {arg}')
                if x == '':
                    return ''
                text += x
                # print(f'\t\t--> text: {text}')
            else:
                print(f'\tGROUP ELSE --> arg: {arg}')
                # text += arg
                
        return text

