from lark_parser import tree
from lark.visitors import Transformer
from random import choice
import exrex
import regex as re
from text_number import Text, Number
from in_dict import in_dict
from or_sequence_repeat import Or, Sequence, Repeat, Group
from literal_literal_range import Literal, Literal_range, Regular_expression
from symbol import NonTerminal, Terminal, Token


rules = {}
tokens = {}
imports = {}
# aliases = {}


class Compiler(Transformer):
    def start(self, args):
        return Sequence(args, rules, tokens, imports)

    def rule(self, args):
        print(f'rule {args[0]}: {args[-1]}\n')
        rules[args[0]] = args[-1] 
    
    def token(self, args):
        print(f'token {args[0]}: {args[-1]}\n')
        tokens[args[0]] = args[-1]
    
    def import_statement(self, args):
        return args
    def import_path(self, args):
        arg = str(args[-1])
        print(f'\t\t-->import_statment: {arg}')
        if 'STRING' in arg:
            imports[arg] = Text()
        elif 'INT' in arg or 'NUMBER' in arg:
            imports[arg] = Number()

    def expansions(selv, args):
        print(f'expansions: {args}\n')
        return Or(args, rules, tokens, imports)

    def alias(self, args):
        # if len(args) > 1:
        #     imports[args[-1]] = args[0]
        # aliases[args[-1]] = args[0]
        return args[0]

    def expansion(self, args):
        print(f'expansion: {args}\n')
        return Sequence(args, rules, tokens, imports)
    
    def expr(self, args):
        print(f'exper: {args}')
        return args
    
    def opexper(self, args):
        print(f'\nopexpr: {args}')
        arg = args[0]
        op = args[1]
        if op == '?':
            return Or([arg, arg, ''], rules, tokens, imports)
        elif op == '*':
            # print(f'opexper: *')
            x = Or([Repeat(arg, 0, 4, rules, tokens, imports), Repeat(arg, 0, 4, rules, tokens, imports), ''], rules, tokens, imports)
            # print(f'\t-------> x: {x}')
            return x
        elif op == '+':
            return Repeat(arg, 0, 4, rules, tokens, imports)
    
    def repeat(self, args):
        print(f'REPEAT {args}')
        return Repeat(args[0], 0, args[1], rules, tokens, imports)

    def expr_range(self, args):
        print(f'expr_range {args}')
        return Repeat(args[0], args[1], args[2], rules, tokens, imports)


    def atom(self, args):
        print(f'atom: {args}')
        return args
        # group og maybe: returner args?
    
    def group(self, args):
        print(f'group: {args[0]}')
        return Group(args, rules, tokens, imports)

    def maybe(self, args):
        print(f'maybe: {args[0]}')
        return Or([args[0], args[0], ''], rules, tokens, imports)

    def value(self, args):
        return args

    def literal_range(self, args):
        print(f'literal_range: {args}')
        return Literal_range(args[0], args[-1])
    
    def literal(self, args):
        return Literal(args)    # , rules, tokens, imports)

    def name(self, args):
        return args[0]

    def _VBAR(self, args):
        return f'{args}'
    def OP(self, args):
        return f'{args}'
    def RULE(self, args):
        if args[0] == '?' or args[0] == '!':
            return NonTerminal(f'{args[1:]}')
        return NonTerminal(f'{args}')
    def TOKEN(self, args):
        return Token(f'{args}')
    def STRING(self, args):
        return Terminal(args[1:-1])
    def REGEXP(self, args):
        # print(f'\n-----------------REGEXP--------------------\n')
        print(f'\REGEXP args: {args}')
        reg = f'{args[1:-1]}'
        # print(f'\t\tREG: {reg}')
        # new = re.sub('\\\p{Lu}', 'A-Z', reg)
        # new = re.sub('\\\p{Ll}', 'a-z', new)
        # new = re.sub('\\\p{..}', '', new)
        # print(f'\targs: {new}')
        # x = exrex.getone(new)
        # print(f'\tgen: {x}')
        # return f'{x}'
        return Regular_expression(reg)

    def _NL(self, args):
        return f'{args}'    

    
    
    

    





Compiler().transform(tree)
print('\n\n------------------------------------------------------------------')
print('-------------------EXAMPLES---------------------------------------')
print('------------------------------------------------------------------\n')

for (name,arg) in rules.items():
    print(f'Example for {name}:')
    
    arg = in_dict(arg, rules, tokens, imports)
    
    eks = arg.generate(0)

    # eks = re.sub(' +', ' ', eks)
    print(f'\t{eks}')
    print('\n---------------------------------------\n')
    
# for (k,v) in rules.items():
#     print(f'{k} : {v}')
#     print(f'\t{k in rules.keys()}')    

# print(f'echo: {rules["echo"]}')
# arg = in_dict('echo', rules, tokens, imports)
# # print(f'arg after in_dict: {arg}')
# print(arg.generate(0))

# print(f"{tokens['_ECHO']}: {tokens['_ECHO'].generate(0)}")


# print('\n\n---------------------------------------')
# print('Example for list (' , rules['list'] ,'):\n')
# print(rules['list'].generate(0))
# print()

# for k,v in aliases.items():
#     print(f'{k}: {v}') 