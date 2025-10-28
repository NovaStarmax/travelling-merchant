import pandas as pd
MARSEILLE = (43.2965, 5.3698)

def get_cities(path):
    df = pd.read_csv(path)
    position_cities = list(zip(df["Latitude"], df["Longitude"]))
    position_cities.remove(MARSEILLE) # Retire Marseille des villes à visiter
    return position_cities


PATH = 'data/villes_france_lat_long.csv'
CITIES = get_cities(PATH)
SELECTION_RATE = 0.1  # Meilleur à 0,1   # 1er impact sur le résultat
MUTATION_RATE = 0.1  # Meilleur à 0,1
MUTATION_FREQUENCY = 0.02  # Meilleur à 0,02
NB_TSP_SOLVER = 100
NB_GEN = 1000  # Très bien à partir de 1000
CROSS_PART = 0.5
