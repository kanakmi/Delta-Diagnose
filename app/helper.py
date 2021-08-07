import random
from string import digits

def random_str(n=7):
    return "".join([random.choice(digits) for s in range(n)])