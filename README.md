# Code Generator
Generate code examples for languages based on there lark grammars.

You first have to run lark_parser.py to create the tree that generator.py uses. Here you also decide which language you want to generate code from.
It is generator.py file you need to run to get the code examples.
This file imports the parse tree from lark_parser.py and use the Compiler().transform() on it.

For Compiler().transform() I have created different functions for the rules in lark.lark, the grammar that we create the parser from. This functions create different instances of the classes that I have created, so that I can use there .generate() methods to get the examples.


In in_dict.py I have a function that checks if the argument is in one of the dictionarys for rules, tokens or imports. If the argument is in one of this dictionarys the function will retrive the "actual rule" (not just tha name) so it can be used.
In this file I have also a variable max_depth that I use to limit the recursion depth. I also have a function new_dept(arg, depth) that calucaltes the new depth based on the argument. If the argument is a Token or a Terminal I increase it by 1, and if it is a NonTerminal I set it to 0, otherwise it dose note change.

text-number.py have the class for generating text, just a fruit for now, and the class for generating a number, an integer.

or_sequence_repeat.py have the Or, Sequence and Repeat classes in it. Similarly literal_literal_range have the Literal and Literal_range classes.


