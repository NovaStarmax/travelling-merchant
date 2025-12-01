from genetic.traveling_salesman_problem import TravelingSalesmanProblem
from genetic.config import NB_GEN, CITIES, MARSEILLE
import matplotlib.pyplot as plt

def run_tsp_genetic_algorithm():
    tsp = TravelingSalesmanProblem(CITIES)

    average_distances = []
    best_bees_generation = []

    for gen in range(NB_GEN):
        tsp.cross_tsp_solvers()
        tsp.mutate_tsp_solvers()
        current_avg = tsp.average_tsp_solvers()
        average_distances.append(current_avg)

        get_best_tsp = min(tsp.tsp_solver, key=lambda tsp: tsp.get_distance())
        best_bees_generation.append(get_best_tsp)
        
        # Debug prints
        if gen % 100 == 0:  # Afficher tous les 100 générations
            print(f"Generation {gen}:")
            print(f"Average distance: {current_avg:.2f}")
            print(f"Best distance: {get_best_tsp.get_distance():.2f}")
            print("-" * 50)

    master_tsp = min(
        best_bees_generation, key=lambda tsp: tsp.get_distance()
    )  # min permet prendre l'objet avec la valeur la plus faible
    master_tsp_path = master_tsp.path

    master_tsp_path.append(MARSEILLE)
    master_tsp_path.insert(0, MARSEILLE)

    x, y = zip(*master_tsp_path)  # * pour décompresser la liste en deux

    best_tsp_distance = master_tsp.get_distance()

    plt.figure()

    plt.subplot(1, 2, 1)
    plt.plot(average_distances, label="Average Distance", color="red", lw=1)
    plt.title("Evolution of generation")
    plt.xlabel("Generation")
    plt.ylabel("Average distance")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(x, y, "o--", color="green", label="Best TSP Path")
    plt.title("Best TSP Path of All Generation")
    plt.text(0.5, 0.5, f"Final Distance: {best_tsp_distance:.2f}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()

    plt.show()

# run_tsp_genetic_algorithm()