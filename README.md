# INF225
Genererer kode eksempler fra lark grammatikk

It is generator.py file you need to run to get the code examples.
This file imports the parse tree from lark_parser.py and use the Compiler().transform() on it.

The parser for lark grammer is in the lark_parser.py file. And uses it to parse a lark grammar.

In in_dict.py I have a function that checks if the rule is in one of the dictionarys for rules, tokens or imports. If the rule is in one of this dictionarys the function will retrives the "actual rule" (not just tha name) so it can be used. 

text-number.py have the class for generating text, just a fruit for now, and the class for generating a number, an integer.

or_sequence_repeat.py have the Or, Sequence and Repeat classes in it. Similarly literal_literal_range have the Literal and Literal_range classes.


