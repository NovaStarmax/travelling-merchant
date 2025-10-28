import math
import random

from config import CROSS_PART, MUTATION_FREQUENCY, CITIES, MARSEILLE

class TSPSolver:
    def __init__(self, cities, path=[]):
        if len(path) == 0:
            self.create_path(cities)
        else:
            self.path = path
        self.compute_path()

    def __str__(self):
        return f"Distance = {round(self.distance, 2)}, Path = {self.path}"

    def create_path(self, cities):
        self.path = random.sample(cities, len(cities))

    def compute_segment(self, pointA, pointD): # Changer la formule (vol d’oiseau)
        dx = pointA[0] - pointD[0]
        dy = pointA[1] - pointD[1]
        return math.sqrt(dx**2 + dy**2)

    def compute_path(self):
        self.distance = self.compute_segment(MARSEILLE, self.path[0])
        for i in range(len(self.path) - 1):
            city_1 = self.path[i]
            city_2 = self.path[i + 1]
            self.distance += self.compute_segment(city_1, city_2)
        self.distance += self.compute_segment(self.path[-1], MARSEILLE)

    def get_distance(self):
        return self.distance

    def mutate(self):  # changement
        nb_path_mutate = int(len(self.path) * MUTATION_FREQUENCY)
        for _ in range(nb_path_mutate):
            a, b = random.sample(range(len(self.path)), 2)
            self.path[a], self.path[b] = self.path[b], self.path[a]
        self.compute_path()

    def cross(self, tsp_2):
        segment_size = int(len(self.path) * CROSS_PART)
        child_path = self.path[:segment_size]
        for f in tsp_2.path:
            if f not in child_path:
                child_path.append(f)
        return TSPSolver(CITIES, path=child_path)
    