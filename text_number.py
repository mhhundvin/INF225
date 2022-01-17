from symbol import Generatable
from random import choice, randint

class Text(Generatable):
    def generate(self, depth):
        words = ["apple", "banana", "cherry", "apple", "cherry"]
        return f'{choice(words)}'

class Number(Generatable):
    def generate(self, depth):
        num = str(randint(1,9))
        for i in range(randint(1,4)):
            num += str(randint(0,9))
        return f'{int(num)}'