import numpy as np
import random
from ant_colony import AntColony
a = [[0 for i in range(150)] for j in range(150)]

for i in range(150):
    for j in range(150):
        if i == j:
            a[i][j] = np.inf
        else:
            a[i][j] = random.randint(5, 50)

dist = np.array(a)
ant_colony = AntColony(dist, 35, 100, 0.4, alpha=2, beta=3)
shortest_path = ant_colony.run()
print("L min: {}".format(ant_colony.lmin))
print("Shortest path: {}".format(shortest_path[0]))
print("Shortest dist: {}".format(shortest_path[1]))
ant_colony.ploting()