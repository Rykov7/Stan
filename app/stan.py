""" Stan quote generator. """
import random


def speak(chance_of):
    number = random.randint(0, chance_of)
    if number == 0:
        return random.choice([i.rstrip() for i in open('Stan.txt', 'r', encoding='utf8') if i])
