import christofides.data_processor as dp
from christofides.tsp_solver import ChristofidesVisualizer

CITIES_FILE = 'data/villes_france_lat_long.csv'

def run_christofides():
  
    print("Chargement des données et calcul de la matrice de distances...")
    
    cities_data, dist_matrix, city_names = dp.create_distance_matrix(CITIES_FILE)

    if cities_data is None:
        print("Arrêt du programme suite à une erreur de chargement des données.")
        return

    print("Démarrage de la visualisation interactive de l'algorithme de Christofides.")
    print("Fermez la fenêtre graphique pour terminer le programme.")
    
    visualizer = ChristofidesVisualizer(cities_data, dist_matrix, city_names)
    visualizer.run()
    
    final_step = visualizer.graphs[-1]
    title, _, tsp_path_indices, distance = final_step
    
    tsp_path_names = [city_names[i] for i in tsp_path_indices]
    
    print("\n" + "="*50)
    print("## RÉSULTAT FINAL DE L'ALGORITHME DE CHRISTOFIDES")
    print("="*50)
    print(f"**Itinéraire Final (Cycle):** {' -> '.join(tsp_path_names)}")
    print(f"**Distance Totale (Approximation):** {distance:.2f} km")
    print("Le chemin est affiché dans le terminal et a été visualisé étape par étape.")
    print("="*50)