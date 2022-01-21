import enum
from re import T
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

    def generate_shortest(self, rule):
        examples = []
        args = list(set(self.args))
        print(f'OR: args: {args}')
        for arg in args:
            print(f'OR: {arg}')
            if rule == arg:
                print(f'\t--> RETURN OR')
                continue
            else:
                arg = in_dict(arg, self.rules, self.tokens, self.imports)
                if isinstance(arg, Generatable):
                    eks = arg.generate_shortest(rule)
                    if eks != '':
                        examples.append(eks)
                        return eks
                        
                else:
                    examples.append(arg)
                    # return arg

        return examples

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
                
        return text
    
    def generate_shortest(self, rule):
        text = ''
        for arg in self.args:
            print(f'SEQUENCE: {arg}')
            if arg == rule:
                print(f'\t--> SEQUENCE RETURN')
                return ''
            arg = in_dict(arg, self.rules, self.tokens, self.imports)
            if isinstance(arg, Generatable):
                eks = arg.generate_shortest(rule)
                if isinstance(eks, list):
                    eks = choice(eks)
                text += eks
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

    def generate_shortest(self, rule):
        print(f'REPEAT: {self.args}')
        if self.args == rule:
            print(f'\t--> SEGUENCE RETURN')
            return ''
        arg = in_dict(self.args, self.rules, self.tokens, self.imports)
        if isinstance(arg, Generatable):
            return arg.generate_shortest(rule)
        return ''




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

