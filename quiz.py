import asyncio
import math
import random


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
            a = random.randint(1, difficulty)
            b = random.randint(1, difficulty)
            self.text = "{} ÷ {}".format(a, b)
            self.answer = a / b


class Quiz:
    def __init__(self,
                 questions,
                 name):

        self.questions = questions
        self.name = name
