import json
from wrapper import *

n = 4
nom_variables = "n_reines/reines_variables_" + str(n) + ".json"
nom_constraints = "n_reines/reines_constraints_" + str(n) + ".json"

# Création du dictionnaire de variables
variables = {}
for i in range(n):
    variables["c" + str(i)] = [k for k in range(n)]

with open(nom_variables, "w") as fichier:
    json.dump(variables, fichier, indent=4)

# Création du dictionnaire de contraintes
contraintes = []

for i in range(n):
    for j in range(i):
        nouvelle_contrainte = {}
        nouvelle_contrainte["variable1"] = "c"+str(i)
        nouvelle_contrainte["variable2"] = "c"+str(j)
        valeurs = []
        for val1 in variables["c"+str(i)]:
            for val2 in variables["c"+str(j)]:
                if (val1 - val2 != j - i) and (val2 - val1 != j - i) and val1 != val2:
                    valeurs.append([val1, val2])
        nouvelle_contrainte["valeurs"] = valeurs
        contraintes.append(nouvelle_contrainte)

with open(nom_constraints, "w") as fichier:
    json.dump(contraintes, fichier, indent=4)
