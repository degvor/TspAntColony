import random as rn
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import choice as np_choice
# import warnings
# warnings.filterwarnings('error')


class AntColony():
    def __init__(self, distances, n_ants, n_iterations, decay, alpha=1, beta=1):
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.path_plotting = []
        self.iteration_plotting = []
        self.lmin = self.get_lmin()
        self.iterarion = 0

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            self.spread_pheronome(all_paths)
            shortest_path = min(all_paths, key=lambda x: x[1])
            self.path_plotting.append(shortest_path[1])
            self.iteration_plotting.append(i)
            if min(self.path_plotting) > shortest_path[1]:
                print("Interation: {}, shortest dist: {}".format(self.iterarion + 1, shortest_path[1]))
            else:
                print("Interation: {}, shortest dist: {}".format(self.iterarion + 1, min(self.path_plotting)))
            self.iterarion += 1
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path
        return all_time_shortest_path

    def get_lmin(self):
        dist = np.copy(self.distances)
        lmin = 0
        iter = 0
        for j in range(len(dist) - 1):
            buff = min(dist[iter])
            index = np.where(dist[iter] == buff)[0]
            index = index[0]
            lmin += buff
            for i in range(len(dist[iter])):
                dist[iter][i] = np.inf
                dist[i][iter] = np.inf
            iter = index
            if j == len(dist) - 2:
                lmin += self.distances[iter][0]
        return lmin

    def ploting(self):
        dist = []
        for i in range(len(self.path_plotting)):
            tmp = min(self.path_plotting)
            index = self.path_plotting.index(tmp)
            self.path_plotting[index] = np.inf
            dist.append(tmp)
        dist.reverse()
        x = []
        y = []
        for j in range(0, self.n_iterations + 1, 20):
            if j == self.n_iterations:
                x.append(dist[-1])
                y.append(self.iteration_plotting[-1])
            else:
                x.append(dist[j])
                y.append(self.iteration_plotting[j])
        print("Values for each 20 iter: {}".format(x))
        plt.plot(y, x)
        plt.show()

    def spread_pheronome(self, all_paths):
        sorted_paths = sorted(all_paths, key=lambda x: x[1])
        self.pheromone = self.pheromone * (1 - self.decay)
        for path, dist in sorted_paths:
            for move in path:
                self.pheromone[move] += self.lmin / dist

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(rn.randint(0, 139))
            all_paths.append((path, self.gen_path_dist(path)))
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for i in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        row = pheromone ** self.alpha * ((1.0 / dist) ** self.beta)
        # try:
        #     norm_row = row / row.sum()
        #     move = np_choice(self.all_inds, 1, p=norm_row)[0]
        # except RuntimeWarning:
        #     move = random.choice(self.all_inds)
        norm_row = row / row.sum()
        chance = rn.random()
        temp = 0
        for i in range(len(norm_row)):
            if i == 0:
                temp = norm_row[i]
                if chance <= temp:
                    move = i
                    break
            else:
                temp += norm_row[i]
                if chance <= temp:
                    move = i
                    break
        # move = np_choice(self.all_inds, 1, p=norm_row)[0]
        return move
