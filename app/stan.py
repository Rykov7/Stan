""" Stan quote generator. """
import random

stan = [i.rstrip() for i in open('Stan.txt', 'r', encoding='utf8')]


def speak(chance):
    chance = random.randint(0, chance)
    if chance == 0:
        return random.choice(stan)
