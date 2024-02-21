from presolve import *

    
def arc_consistance_3(dict_variables, dict_contraintes):
    nb_contraintes = len(dict_contraintes)
    a_tester = [i for i in range(nb_contraintes)]
    
    #Il faut aussi supprimer les contraintes
    while len(a_tester) > 0:
        contr = a_tester.pop()
        var1 = dict_contraintes[contr]["variable1"]
        var2 = dict_contraintes[contr]["variable2"]
        print(var1, " ", var2)
        valeurs_contr = dict_contraintes[contr]["valeurs"]
        domaines_var1 = dict_variables[var1]
        nb_domaines_var1 = len(domaines_var1)
        
        le_domaine_a_change = False
        valeurs_a_supprimer = []
        for i in range(nb_domaines_var1):
            val1_i = domaines_var1[i]
            valeur_supportee = False

            # On parcourt les valeurs possibles du couple (var1, var2)
            for j in range(len(valeurs_contr)):
                if valeurs_contr[j][0] == val1_i and (valeurs_contr[j][1] in dict_variables[var2]):
                    valeur_supportee = True
                    continue
            # val1_i n'est suportée par aucune valeur de var2
            if valeur_supportee == False:
                valeurs_a_supprimer.append(val1_i)
                le_domaine_a_change = True
        print(valeurs_a_supprimer)
        # Il existe val1_i qui n'est suportée par aucune valeur de var2
        if le_domaine_a_change == True:
            nouveau_domaine = domaines_var1
            for element in valeurs_a_supprimer:
                nouveau_domaine.remove(element)
            dict_variables[var1] = nouveau_domaine
            for k in range(nb_contraintes):
                if k not in a_tester and dict_contraintes[k]["variable2"] == var1 and dict_contraintes[k]["variable1"] != var2:
                    a_tester.append(k)





if __name__ == "__main__":
    
    # Lecture des données
    fichier_contraintes = "toy/toy_constraints.json"
    fichier_variables = "toy/toy_variables.json"
    contraintes = lire_instance_json(fichier_contraintes)
    variables = lire_instance_json(fichier_variables)

    # Prétraitement
    # (mettre les contraintes dans les deux sens)
    pretraitement(contraintes)
    for i in range(len(contraintes)):
        print(contraintes[i])
    # Algorithme d'arc consistsance AC3
    # (permet de réduire les domaines des variables)
    # Attention, seul le dictionnaire variables est modifié
    arc_consistance_3(variables, contraintes)
    print(variables)

