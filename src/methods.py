import math
import random

def substring(string, length):
    idx = random.randrange(0, len(string) - length + 1)
    return string[idx:idx + length]

def product(s):
    res = 1
    for i in s:
        res *= i
    return res
