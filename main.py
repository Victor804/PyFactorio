import numpy as np
import matplotlib.pyplot as plt
import random


MAP_SIZE = 1000

map = np.zeros((MAP_SIZE, MAP_SIZE))

def generate_ore_deposits(map, num_deposits=20, deposit_size=100, seed=0):
    random.seed(seed)
    for _ in range(num_deposits):
        start_x = random.randint(0, MAP_SIZE - 1)
        start_y = random.randint(0, MAP_SIZE - 1)
        
        for _ in range(deposit_size):
            map[start_y][start_x] = 1

            start_x = max(0, min(MAP_SIZE - 1, start_x + random.choice([-1, 0, 1])))
            start_y = max(0, min(MAP_SIZE - 1, start_y + random.choice([-1, 0, 1])))

# Generate map
generate_ore_deposits(map, num_deposits=100, deposit_size=500, seed=42)


plt.figure(figsize=(10, 10))
plt.imshow(map, cmap='terrain', interpolation='nearest')
plt.colorbar()
plt.title("Map with ore")
plt.show()
