import random
from tsp_solver import TSPSolver
from config import NB_TSP_SOLVER, SELECTION_RATE, MUTATION_RATE

class TravelingSalesmanProblem:
    def __init__(self, tsp_solver):
        self.tsp_solver = tsp_solver
        self.create_tsp_solver(tsp_solver)

    def create_tsp_solver(self, tsp_solver):
        self.tsp_solver = []
        for _ in range(NB_TSP_SOLVER):
            b = TSPSolver(tsp_solver)
            self.tsp_solver.append(b)

    def sort_tsp_solvers(self):
        self.tsp_solver.sort(key=lambda tsp: tsp.get_distance())

    def select_tsp_solvers(self):
        nb_selected = max(2, int(len(self.tsp_solver) * SELECTION_RATE))  # Au moins 2 sélectionnés
        self.sort_tsp_solvers()  # Trier d'abord
        return self.tsp_solver[:nb_selected]  # Garder les meilleurs

    def cross_tsp_solvers(self):
        selected_tsp_solvers = self.select_tsp_solvers()
        new_population = selected_tsp_solvers.copy()  # Garder les meilleurs

        while len(new_population) < NB_TSP_SOLVER:
            tsp_1 = random.choice(selected_tsp_solvers)
            tsp_2 = random.choice(selected_tsp_solvers)
            while tsp_1 == tsp_2:
                tsp_2 = random.choice(selected_tsp_solvers)
            child = tsp_1.cross(tsp_2)
            new_population.append(child)

        self.tsp_solver = new_population

    def mutate_tsp_solvers(self):
        nb_tsp_solvers_to_mutate = int(NB_TSP_SOLVER * MUTATION_RATE)
        tsp_solvers_to_mutate = random.sample(self.tsp_solver, nb_tsp_solvers_to_mutate)
        for tsp in tsp_solvers_to_mutate:
            tsp.mutate()

    def average_tsp_solvers(self):
        total = sum(tsp.get_distance() for tsp in self.tsp_solver)
        average = total / NB_TSP_SOLVER
        return average

    def print_generation(self, gen):
        current_avg = self.average_tsp_solvers()
        print(f"Generation {gen}:")
        print(f"Average distance: {current_avg:.2f}")
        print(f"Best distance: {get_best_tsp.get_distance():.2f}")
        print(f"Population diversity: {len(set(tuple(tsp.path) for tsp in tsp.tsp_solver))}")
        print("-" * 50)
