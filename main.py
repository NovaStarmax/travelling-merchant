from genetic.run_tsp_genetic import run_tsp_genetic_algorithm
from christofides.run_christofides import run_christofides

def main():

    print("***** SÉLECTION DE L'ALGORITHME ****")
    print("1. Algorithme Génétique")
    print("2. Algorithme de Christofides")
    
    choix = input("Entrez le numéro de votre choix (1 ou 2) : ")

    if choix == "1":
        print("\nLancement de l'Algorithme Génétique :")
        run_tsp_genetic_algorithm()
        
    elif choix == "2":
        print("\nl'Algorithme de Christofides :")
        run_christofides()
        
    else:
        print(f"\nErreur : '{choix}' n'est pas une option valide. Veuillez relancer et taper 1 ou 2.")

if __name__ == "__main__":
    main()
