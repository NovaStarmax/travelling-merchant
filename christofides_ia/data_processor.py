import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calcule la distance de Haversine entre deux points (lat, lon) en kilomètres.
    """
    R = 6371  # Rayon moyen de la Terre en kilomètres

    lat1_rad, lon1_rad = radians(lat1), radians(lon1)
    lat2_rad, lon2_rad = radians(lat2), radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

def create_distance_matrix(file_path):
    """
    Charge les données des villes et crée la matrice de distances complète.

    Retourne:
        DataFrame: Les données des villes.
        numpy.array: La matrice de distances.
        list: La liste des noms de  .
    """
    try:
        cities_df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Erreur: Le fichier {file_path} est introuvable.")
        return None, None, None

    city_names = cities_df['Ville'].tolist()
    n = len(city_names)
    distance_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(i + 1, n):
            lat1, lon1 = cities_df.iloc[i]['Latitude'], cities_df.iloc[i]['Longitude']
            lat2, lon2 = cities_df.iloc[j]['Latitude'], cities_df.iloc[j]['Longitude']
            dist = haversine_distance(lat1, lon1, lat2, lon2)
            distance_matrix[i, j] = dist
            distance_matrix[j, i] = dist 

    return cities_df, distance_matrix, city_names

def calculate_path_distance(distance_matrix, path_indices):
    """Calcule la distance totale pour un chemin d'indices donné."""
    total_distance = 0
    # Le chemin est un cycle, il revient au point de départ
    for i in range(len(path_indices) - 1):
        u = path_indices[i]
        v = path_indices[i+1]
        total_distance += distance_matrix[u, v]
    return total_distance