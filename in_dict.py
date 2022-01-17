#from myGenerator import rules, tokens, imports
from symbol import NonTerminal, Terminal, Token

max_depth = 50

def in_dict(arg, rules, tokens, imports):
    while arg in rules.keys() or arg in tokens.keys() or str(arg) in imports.keys():
        if arg in rules.keys():
            arg = rules[arg]
        if arg in tokens.keys():
            arg = tokens[arg]
        if str(arg) in imports.keys():
            arg = imports[str(arg)]
    return arg

def new_depth(arg, depth):
    if isinstance(arg, NonTerminal):
        depth = 0
    elif isinstance(arg, Terminal):
        depth += 1
    elif isinstance(arg, Token):
        depth += 1
    return depth