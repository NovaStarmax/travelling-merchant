import math
import random

from genetic.config import CROSS_PART, MUTATION_FREQUENCY, CITIES, MARSEILLE

class TSPSolver:
    def __init__(self, cities, path=None):  # Changer path=[] en path=None
        if path is None:  # Changer len(path) == 0 en path is None
            self.create_path(cities)
        else:
            self.path = path.copy()  # Ajouter .copy() pour éviter les références partagées
        self.compute_path()

    def __str__(self):
        return f"Distance = {round(self.distance, 2)}, Path = {self.path}"

    def create_path(self, cities):
        self.path = random.sample(cities, len(cities))

    def compute_segment(self, pointA, pointD):
        # Rayon de la Terre en kilomètres
        R = 6371.0
        
        # Conversion des degrés en radians
        lat1, lon1 = math.radians(pointA[0]), math.radians(pointA[1])
        lat2, lon2 = math.radians(pointD[0]), math.radians(pointD[1])
        
        # Différences de coordonnées
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        # Formule de Haversine
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Distance en kilomètres
        return R * c

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
        # Augmenter la diversité avec différents types de mutations
        if random.random() < 0.5:
            # Swap mutation
            nb_path_mutate = max(1, int(len(self.path) * MUTATION_FREQUENCY))
            for _ in range(nb_path_mutate):
                a, b = random.sample(range(len(self.path)), 2)
                self.path[a], self.path[b] = self.path[b], self.path[a]
        else:
            # Reverse mutation - inverse une sous-séquence
            start = random.randint(0, len(self.path) - 2)
            end = random.randint(start + 1, len(self.path) - 1)
            self.path[start:end] = reversed(self.path[start:end])
        
        self.compute_path()

    def cross(self, tsp_2):
        # Ordered Crossover (OX)
        size = len(self.path)
        start, end = sorted(random.sample(range(size), 2))
        
        # Prendre une section du premier parent
        child_path = [None] * size
        child_path[start:end] = self.path[start:end]
        
        # Remplir le reste avec les villes du deuxième parent dans l'ordre
        remaining = [city for city in tsp_2.path if city not in child_path[start:end]]
        j = 0
        for i in range(size):
            if child_path[i] is None:
                child_path[i] = remaining[j]
                j += 1
                
        return TSPSolver(CITIES, path=child_path)
