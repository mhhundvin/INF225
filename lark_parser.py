from lark import Lark

larkGrammer = open('grammars/lark.lark', 'r').read()
json_grammar = open('grammars/jsonGrammar.lark', 'r').read()
hedy_grammar = open('grammars/hedy/level1.lark', 'r').read()
yaml_grammar = open('grammars/yaml.lark', 'r').read()

parser = Lark(larkGrammer)

tree = parser.parse(hedy_grammar)