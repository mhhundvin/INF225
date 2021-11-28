from os import kill
from lark import Lark
import lark
from lark.visitors import Transformer
from random import choice, randint
import exrex
import regex as re

larkGrammer = open('grammars/lark.lark', 'r').read()
json_grammar = open('grammars/jsonGrammar.lark', 'r').read()
hedy_grammar = open('grammars/hedy/level1.lark', 'r').read()
verilog_grammar = open('grammars/verilog.lark', 'r').read()  
regex_grammar = open('grammars/regex.lark', 'r').read()
yaml_grammar = open('grammars/yaml.lark', 'r').read()

rules = {}
tokens = {}
imports = {}

def inDict(arg):
    while arg in rules.keys() or arg in tokens.keys() or arg in imports.keys():
        if arg in rules.keys():
            arg = rules[arg]
        if arg in tokens.keys():
            arg = tokens[arg]
        if arg in imports.keys():
            arg = imports[arg]
    return arg


class Symbol():
    pass

# class DictObj(Symbol):
#     def __init__(self, args):
#         self.args = args
    
#     def generate(self, depth):
#         if depth > 10:
#             return ''
#         depth += 1
#         arg = self.args
#         if arg in rules.keys():
#             arg = rules[arg]
#         if arg in tokens.keys():
#             arg = tokens[arg]
#         if arg in imports.keys():
#             arg = imports[arg]

#         if isinstance(arg, Symbol):
#             x = arg.generate(depth)
#             return x
#         return ''



class Or(Symbol):
    def __init__(self, args):
        self.args = args

    def generate(self, depth):
        if depth > 10:
            return ''
        depth += 1
        arg = choice(self.args)
        # print(f'Or.generate arg: {arg}')
        arg = inDict(arg)
            
        if isinstance(arg, Symbol):
            x = arg.generate(depth)
            # print(f'\t\tOR if: x: {x} - arg {arg}')
            return x
        # else:
            # print(f'\t-->OR: "{arg}" Type: {type(arg)}')
        return ''


class Sequence(Symbol):
    def __init__(self, args):
        self.args = args

    def generate(self, depth):
        if depth > 10:
            return ''
        depth += 1
        # print(f'Sequence args: {self.args}')
        text = ''
        for arg in self.args:
            arg = inDict(arg)
            # print(f'\t-->Sequence arg: {arg}')

            if isinstance(arg, Symbol):
                # print(f'\t\t-->isinstance: true')
                x = arg.generate(depth)
                # print(f'\tSeq --> x {x}\targ: {arg}')
                text += x
                # print(f'\t\t--> text: {text}')
            else:
                print(f'\tELSE --> arg: {arg}')
                # text += arg
                
        return text

class Repeat(Symbol):
    def __init__(self, args, start, stop):
        self.args = args
        self.start = start
        self.stop = stop
    
    def generate(self, depth):
        if depth > 10:
            return ''
        depth += 1
        arg = self.args
        arg = inDict(arg)

        # print(f'REPEAT: {self.args} -> {arg}')
        # print(f'isinstance(arg, Symbol): {isinstance(arg, Symbol)}')
        text = ''
        if isinstance(arg, Symbol):
            for i in range(int(self.start), int(self.stop)):
                # print(f'\ti = {i}')
                text += arg.generate(depth)
        return text
            

class Text(Symbol):
    def generate(self, depth):
        words = ["apple", "banana", "cherry", "apple", "cherry"]
        return f'{choice(words)}'

class Number(Symbol):
    def generate(self, depth):
        num = str(randint(1,9))
        for i in range(randint(1,4)):
            num += str(randint(0,9))
        return f'{int(num)}'

class Literal(Symbol):
    def __init__(self, args):
        self.args = args[0]
    
    def generate(self, depth):
        if depth > 10:
            return ''
        depth += 1
        arg = self.args
        arg = inDict(arg)
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





class Compiler(Transformer):
    def start(self, args):
        return Sequence(args)

    def rule(self, args):
        print(f'rule {args[0]}: {args[-1]}\n')
        rules[args[0]] = args[-1] 
    
    def token(self, args):
        print(f'token {args[0]}: {args[-1]}\n')
        tokens[args[0]] = args[-1]
    
    def import_statement(self, args):
        return args
    def import_path(self, args):
        arg = args[-1]
        if 'STRING' in arg:
            imports[arg] = Text()
        elif 'INT' in arg or 'NUMBER' in arg:
            imports[arg] = Number()

    def expansions(selv, args):
        print(f'expansions: {args}\n')
        return Or(args)

    def alias(self, args):
        return args[0]

    def expansion(self, args):
        print(f'expansion: {args}\n')
        return Sequence(args)
    
    def expr(self, args):
        print(f'exper: {args}')
        return args
    
    def opexper(self, args):
        print(f'\nopexpr: {args}')
        arg = args[0]
        op = args[1]
        if op == '?':
            return Or([arg, arg, ''])
        elif op == '*':
            # print(f'opexper: *')
            x = Or([Repeat(arg, 0, 4), Repeat(arg, 0, 4), ''])
            # print(f'\t-------> x: {x}')
            return x
        elif op == '+':
            return Repeat(arg, 0, 4)
    
    def repeat(self, args):
        print(f'REPEAT {args}')
        return Repeat(args[0], 0, args[1])

    def expr_range(self, args):
        print(f'expr_range {args}')
        return Repeat(args[0], args[1], args[2])


    def atom(self, args):
        print(f'atom: {args}')
        return args
        # group og maybe: returner args?
    
    def maybe(self, args):
        print(f'maybe: {args[0]}')
        return Or([args[0], args[0], ''])

    def value(self, args):
        return args

    def literal_range(self, args):
        print(f'literal_range: {args}')
        return Literal_range(args[0], args[-1])
    
    def literal(self, args):
        return Literal(args)

    def name(self, args):
        return args[0]

    def _VBAR(self, args):
        return f'{args}'
    def OP(self, args):
        return f'{args}'
    def RULE(self, args):
        if args[0] == '?':
            return f'{args[1:]}'
        return f'{args}'
    def TOKEN(self, args):
        return f'{args}'
    def STRING(self, args):
        return args[1:-1]   # args
    def REGEXP(self, args):
        # print(f'\n-----------------REGEXP--------------------\n')
        print(f'\REGEXP args: {args}')
        reg = f'{args[1:-1]}'
        new = re.sub('\\\p{Lu}', 'A-Z', reg)
        new = re.sub('\\\p{Ll}', 'a-z', new)
        new = re.sub('\\\p{..}', '', new)
        # print(f'\targs: {new}')
        x = exrex.getone(new)
        # print(f'\tgen: {x}')
        return f'{x}'

    def _NL(self, args):
        return f'{args}'    

    
    
    

    


parser = Lark(larkGrammer)


tree = parser.parse(json_grammar)


Compiler().transform(tree)
print('\n\n------------------------------------------------------------------')
print('-------------------EXAMPLES---------------------------------------')
print('------------------------------------------------------------------\n')

for (name,arg) in rules.items():
    print(f'Example for {name}:')
    
    arg = inDict(arg)
    
    eks = arg.generate(0)

    # eks = re.sub(' +', ' ', eks)
    print(f'\t{eks}')
    print('\n---------------------------------------\n')
    


# print('\n\n---------------------------------------')
# print('Example for list (' , rules['list'] ,'):\n')
# print(rules['list'].generate(0))
# print()
