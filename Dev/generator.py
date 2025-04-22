import random

rangen = open('random_generations.txt', 'w')
#opens the files to write into
translate = {
    'w': 'water',
    'r': 'road',
    'g': 'grass',
    'l': 'log',
    's': 'stone'
}

for z in range(200):
    randoms = []
    if z % 3 == 0:#I want there to be more land than water or road since that makes more sense
        row_type = "water"
    elif z%3 == 1:
        row_type = "road"#goes through varable z and alternates between land, water and road
    else:
        row_type = "land"
    
    for j in range(10):
        if row_type == "water":
            randoms.append(random.choices(['w', 'l'], weights=[65, 35])[0]) #sets weights to probability of getting water and log
        elif row_type == "road":
            randoms.append(random.choices(['r'], weights=[100])[0])#sets a 100% probability of getting road since the road will always be road
        else:
            randoms.append(random.choices(['g', 's'], weights=[70, 30])[0])#sets the weitghts to probability of getting grass and stone 
    
    if row_type == "water" and 'l' not in randoms:#makes it so that the game isn't unplayable by making sure there is atleast 1 log per water strip
        random_position = random.randint(0, 9)
        randoms[random_position] = 'l'
    
    rangen.write(str(randoms))#converts the list to a string and writes it to the file
    rangen.write('\n')

print("Generated 200 rows of terrain for Frogger")
rangen.close()