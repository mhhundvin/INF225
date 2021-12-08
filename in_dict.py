#from myGenerator import rules, tokens, imports

def in_dict(arg, rules, tokens, imports):
    while arg in rules.keys() or arg in tokens.keys() or arg in imports.keys():
        if arg in rules.keys():
            arg = rules[arg]
        if arg in tokens.keys():
            arg = tokens[arg]
        if arg in imports.keys():
            arg = imports[arg]
    return arg