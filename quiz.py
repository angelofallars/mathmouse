import asyncio
import math
import random


def get_factors(n):
    """Return a list of the factors of a number n.
Does not include 1 or the number n in list of factors because they're used for
division questions.
"""
    factors = []

    for i in range(2, n):
        if n % i == 0:
            factors.append(i)

    return factors


class Question:
    def __init__(self,
                 text=None,
                 answer=None,
                 q_type=None,
                 difficulty=20):

        self.text = text
        self.answer = answer
        self.q_type = q_type
        self.difficulty = difficulty

        if q_type == 'addition':
            a = random.randint(1, difficulty)
            b = random.randint(1, difficulty)
            self.text = "{} + {}".format(a, b)
            self.answer = a + b

        elif q_type == 'subtraction':
            a = random.randint(1, difficulty)
            b = random.randint(1, difficulty)
            self.text = "{} - {}".format(a, b)
            self.answer = a - b

        elif q_type == 'multiplication':
            a = random.randint(1, difficulty)
            b = random.randint(1, difficulty // 3)
            self.text = "{} x {}".format(a, b)
            self.answer = a * b

        elif q_type == 'division':
            # Only whole division for now

            factors = []
            while factors == []:
                a = random.randint(1, difficulty * 1.5)
                factors = get_factors(a)

            b = random.choice(factors)

            self.text = "{} ÷ {}".format(a, b)
            self.answer = a / b


class Quiz:
    def __init__(self,
                 questions,
                 name):

        self.questions = questions
        self.name = name
