import networkx as nx
import matplotlib.pyplot as plt
import data_processor as dp
from typing import List, Tuple

class ChristofidesVisualizer:
    
    def __init__(self, cities_df, distance_matrix, city_names):
        self.cities_df = cities_df
        self.distance_matrix = distance_matrix
        self.city_names = city_names
        self.n = len(city_names)
        self.step = 0
        self.total_steps = 4

        self.city_coords = {i: (row['Longitude'], row['Latitude']) 
                            for i, row in cities_df.iterrows()}
        self.pos = self.city_coords
       
        self.graphs = self._initialize_graphs()

        self.fig, self.ax = plt.subplots(figsize=(12, 12))
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        self.plot_current_step()

    def _initialize_graphs(self) -> List[Tuple[str, nx.Graph, List[int], float]]:

        G = nx.Graph()
        for i in range(self.n):
            for j in range(i + 1, self.n):
                G.add_edge(i, j, weight=self.distance_matrix[i, j])

        MST = nx.minimum_spanning_tree(G, weight='weight')
        
        odd_degree_nodes = [v for v, degree in MST.degree() if degree % 2 != 0]
  
        subgraph = G.subgraph(odd_degree_nodes)
        
        try:
            matching_edges = nx.algorithms.matching.min_weight_matching(subgraph, max_weight=False)
        except Exception as e:
            print(f"Avertissement: Impossible de calculer le Min Weight Matching. Erreur: {e}")
            matching_edges = []
        
        H = MST.copy()
        H.add_edges_from(matching_edges) 

        tsp_path_indices = nx.approximation.christofides(G, weight='weight')
        tsp_distance = dp.calculate_path_distance(self.distance_matrix, tsp_path_indices)

        return [
            ("1. Graphe Complet Pondéré", G, [], 0.0),
            ("2. Arbre Couvrant Minimum (ACM)", MST, [], 0.0),
            (f"3. Graphe Eulérien (ACM + Couplage sur {len(odd_degree_nodes)} villes)", H, odd_degree_nodes, 0.0),
            (f"4. Circuit TSP Final ({tsp_distance:.2f} km)", G, tsp_path_indices, tsp_distance)
        ]

    def plot_current_step(self):
        
        title, graph, highlight_nodes_or_path, distance = self.graphs[self.step]
        
        self.ax.clear()
        self.ax.set_title(f"Algorithme de Christofides - Étape {self.step + 1} : {title}", fontsize=14)
        
        node_labels = {i: self.city_names[i] for i in graph.nodes()}
        
        nx.draw_networkx_nodes(graph, self.pos, node_size=300, node_color='lightgray', ax=self.ax)
        nx.draw_networkx_labels(graph, self.pos, labels=node_labels, font_size=8, ax=self.ax)
        
        margin = 0.5
        min_lon = self.cities_df['Longitude'].min() - margin
        max_lon = self.cities_df['Longitude'].max() + margin
        min_lat = self.cities_df['Latitude'].min() - margin
        max_lat = self.cities_df['Latitude'].max() + margin
        self.ax.set_xlim(min_lon, max_lon)
        self.ax.set_ylim(min_lat, max_lat)
        self.ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        self.ax.set_xlabel("Longitude")
        self.ax.set_ylabel("Latitude")

        if self.step == 0:
            nx.draw_networkx_edges(graph, self.pos, edge_color='lightgray', alpha=0.5, ax=self.ax)
            
        elif self.step == 1:
            nx.draw_networkx_edges(graph, self.pos, edge_color='darkblue', width=2, ax=self.ax)
            
        elif self.step == 2:
            nx.draw_networkx_edges(graph, self.pos, edge_color='green', width=2, alpha=0.7, ax=self.ax)
            nx.draw_networkx_nodes(graph, self.pos, nodelist=highlight_nodes_or_path, 
                                   node_size=400, node_color='red', alpha=0.9, ax=self.ax)
                                   
        elif self.step == 3:
            tsp_path_indices = highlight_nodes_or_path
            
            edges = [(tsp_path_indices[i], tsp_path_indices[i+1]) 
                     for i in range(len(tsp_path_indices) - 1)]
            
            nx.draw_networkx_edges(graph, self.pos, edgelist=edges, edge_color='red', width=3, ax=self.ax)
            
            start_node_index = tsp_path_indices[0]
            nx.draw_networkx_nodes(graph, self.pos, nodelist=[start_node_index], 
                                   node_size=500, node_color='gold', label='Départ', ax=self.ax)
            
            self.ax.text(0.5, 0.02, f"Distance Totale: {distance:.2f} km", 
                         transform=self.ax.transAxes, ha="center", fontsize=12, 
                         bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.8))
        
        plt.draw()

    def on_key_press(self, event):
        if event.key == ' ':
            self.step = (self.step + 1) % self.total_steps
            self.plot_current_step()
            
    def run(self):
        plt.show()