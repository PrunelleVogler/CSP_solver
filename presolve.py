import json

def lire_instance_json(nom_fichier):
    with open(nom_fichier, 'r') as f:
        data = json.load(f)
    return data

def ajouter_valeurs_inverses(dict_contraintes, indice1, indice2):
    for i in range(len(dict_contraintes[indice1]["valeurs"])):
        dict_contraintes[indice2]["valeurs"].append([dict_contraintes[indice1]["valeurs"][i][1], dict_contraintes[indice1]["valeurs"][i][0]])
    for i in range(len(dict_contraintes[indice2]["valeurs"])):
        dict_contraintes[indice1]["valeurs"].append([dict_contraintes[indice2]["valeurs"][i][1], dict_contraintes[indice2]["valeurs"][i][0]])


def pretraitement(dict_contraintes):
    
    # 1 - s'il y a deux contraintes pour la même paire : les concaténer
    nb_contraintes = len(dict_contraintes)
    indice_a_supprimer = []
    for i in range(nb_contraintes):
        for j in range(i):
            if dict_contraintes[i]["variable1"] == dict_contraintes[j]["variable1"] and dict_contraintes[i]["variable2"] == dict_contraintes[j]["variable2"] and j not in indice_a_supprimer:
                dict_contraintes[i]["valeurs"]= dict_contraintes[i]["valeurs"] + dict_contraintes[j]["valeurs"]
                indice_a_supprimer.append(j)
    for indice in indice_a_supprimer:
        del dict_contraintes[indice]
    
    # 2 - vérifier qu'il y a les mêmes contraintes dans les deux sens
    nb_contraintes = len(dict_contraintes)
    for i in range(nb_contraintes):
        contrainte_inverse_existe = False
        for j in range(nb_contraintes):
            if dict_contraintes[i]["variable1"] == dict_contraintes[j]["variable2"] and dict_contraintes[i]["variable2"] == dict_contraintes[j]["variable1"]:
                contrainte_inverse_existe = True
                ajouter_valeurs_inverses(dict_contraintes, i, j)
        if contrainte_inverse_existe == False:
            valeurs_a_inverser = dict_contraintes[i]["valeurs"]
            new_dic = {
                "variable1": dict_contraintes[i]["variable2"],
                "variable2": dict_contraintes[i]["variable1"],
                "valeurs": [[valeurs_a_inverser[k][1], valeurs_a_inverser[k][0]] for k in range(len(valeurs_a_inverser))]
            }
            dict_contraintes.append(new_dic)
    
    # 3 - enlever les doublons dans les valeurs des contraintes
    nb_contraintes = len(dict_contraintes)
    for i in range(nb_contraintes):
        ensembles_sans_doublons = set(tuple(liste) for liste in dict_contraintes[i]["valeurs"])
        dict_contraintes[i]["valeurs"] = [list(t) for t in ensembles_sans_doublons]

