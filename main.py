import json

def lire_instance_json(nom_fichier):
    with open(nom_fichier, 'r') as f:
        data = json.load(f)
    return data


def arc_consistance_3(dict_variables, dict_contraintes):
    dict_variables["x_1"] = [0,1]
    a_tester = []


# Exemple d'utilisation :
if __name__ == "__main__":
    
    # Lecture des données
    fichier_contraintes = "toy/toy_constraints.json"
    fichier_variables = "toy/toy_variables.json"
    contraintes = lire_instance_json(fichier_contraintes)
    variables = lire_instance_json(fichier_variables)

    # Algorithme d'arc consistsance AC3
    arc_consistance_3(variables, contraintes)
