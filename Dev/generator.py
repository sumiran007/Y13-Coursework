import pygame 
rangen = open('random_generations.txt', 'a')
import random
water = []
for i in range(10):
    water.append(['w'])
print(water)

translate = {
        'w': 'water',
        'r': 'rock',
        'g': 'grass',
        'l': 'log',
    }



for z in range (200):
    randoms = []
    for j in range(10):
        randoms.append(random.choice(['w', 'r', 'g', 'l']))
    rangen.write(str(randoms))
    rangen.write('\n')
print(randoms)
rangen.close()

    
