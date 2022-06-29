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

def merge(a, b):
    a_slug_len = math.floor(len(a)/2)+1 if len(a) == 1 else math.floor(len(a)/2)
    b_slug_len = math.floor(len(b)/2)
    return a[:a_slug_len] + b[b_slug_len:]

def shipValue(a, b): 
    """return abs(math.ceil(100 * math.sin(product([ord(x) for x in a]) * product([ord(x) for x in b]))))"""
    
    """random.seed(product([ord(x) for x in a]) * product([ord(x) for x in b]))
    x = math.ceil(random.random()*100)
    random.seed(None)
    return x"""

    proda = product([ord(x) for x in a])
    prodb = product([ord(x) for x in b])
    return abs(math.ceil(100 * math.sin(proda * prodb)))

def round_to_5(s):
    return round(s/5) * 5