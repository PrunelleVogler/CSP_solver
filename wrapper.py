# Fonctions qui permettent de créer des contraintes

def alldiff(dict_variables):
    nom_variables = list(dict_variables.keys())
    nb_variables = len(dict_variables)
    contraintes_binaires = []
    for i in range(nb_variables):
        for j in range(i):
            nouvelle_contrainte = {}
            nouvelle_contrainte["variable1"] = nom_variables[i]
            nouvelle_contrainte["variable2"] = nom_variables[j]
            valeurs = []
            for val1 in dict_variables[nom_variables[i]]:
                for val2 in dict_variables[nom_variables[j]]:
                    if val1 != val2:
                        valeurs.append([val1, val2])
            nouvelle_contrainte["valeurs"] = valeurs
            contraintes_binaires.append(nouvelle_contrainte)
    return contraintes_binaires
