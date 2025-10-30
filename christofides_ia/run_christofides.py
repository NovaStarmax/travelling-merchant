import data_processor as dp
from tsp_solver import ChristofidesVisualizer

# Chemin vers votre fichier de données des villes
CITIES_FILE = 'data/villes_france_lat_long.csv'

def main():
    """
    Méthode principale pour lancer la résolution du TSP avec
    l'algorithme de Christofides et sa visualisation étape par étape.
    """
    print("Chargement des données et calcul de la matrice de distances...")
    
    # Étape 1: Préparation des données
    cities_data, dist_matrix, city_names = dp.create_distance_matrix(CITIES_FILE)

    if cities_data is None:
        print("Arrêt du programme suite à une erreur de chargement des données.")
        return

    # Étape 2: Lancer la visualisation de l'algorithme
    print("Démarrage de la visualisation interactive de l'algorithme de Christofides.")
    print("Fermez la fenêtre graphique pour terminer le programme.")
    
    visualizer = ChristofidesVisualizer(cities_data, dist_matrix, city_names)
    visualizer.run()
    
    # Afficher le résultat final dans la console après la fermeture de la fenêtre
    final_step = visualizer.graphs[-1]
    title, _, tsp_path_indices, distance = final_step
    
    # Convertir les indices en noms de villes
    tsp_path_names = [city_names[i] for i in tsp_path_indices]
    
    print("\n" + "="*50)
    print("## RÉSULTAT FINAL DE L'ALGORITHME DE CHRISTOFIDES")
    print("="*50)
    print(f"**Itinéraire Final (Cycle):** {' -> '.join(tsp_path_names)}")
    print(f"**Distance Totale (Approximation):** {distance:.2f} km")
    print("Le chemin est affiché dans le terminal et a été visualisé étape par étape.")
    print("="*50)


if __name__ == '__main__':
    main()