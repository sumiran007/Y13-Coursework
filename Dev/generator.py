import pygame 
import random
water = []
for i in range(10):
    water.append(['w'])
print(water)
randoms = []
translate = {
        'w': 'water',
        'r': 'rock',
        'g': 'grass',
        'l': 'log',
    }
for j in range(10):
    randoms.append(random.choice(['w', 'r', 'g', 'l']))
print(randoms)
    
