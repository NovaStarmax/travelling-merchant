import pandas as pd
MARSEILLE = (43.2965, 5.3698)

def get_cities(path):
    df = pd.read_csv(path)
    position_cities = list(zip(df["Latitude"], df["Longitude"]))
    position_cities.remove(MARSEILLE) # Retire Marseille des villes à visiter
    return position_cities


PATH = 'data/villes_france_lat_long.csv'
CITIES = get_cities(PATH)
SELECTION_RATE = 0.3      # Augmenter pour plus de diversité
MUTATION_RATE = 0.3       # Augmenter pour plus d'exploration
MUTATION_FREQUENCY = 0.1   # Augmenter la fréquence des mutations
NB_TSP_SOLVER = 200       # Plus grande population
NB_GEN = 2000  # Très bien à partir de 1000
CROSS_PART = 0.5
