REGALIAS_ENABLE = True
import random
try:
    import regalias
except:
    REGALIAS_ENABLE = False

def enabled():
    return REGALIAS_ENABLE

def generate_alias():
    return regalias.generate_japanese_alias_from_rng(random.Random())