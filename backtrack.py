import json
import random
from main import *
import time
import copy
from copy import deepcopy

########### fonction test si une contrainte est violée par l'instantiation

def test(instantiation,constraints): 
    if len(instantiation) == 0: 
        return True
    for c in constraints:
        var1 = c['variable1']
        var2 = c['variable2']
        if var1 in instantiation and var2 in instantiation:
            answer = False
            for val in c['valeurs']:
                if instantiation[var1] == val[0] and instantiation[var2] == val[1]:
                    answer = True
            if not(answer):
                return False 
    
    for var in instantiation.keys():
        val = instantiation[var]
        for c1 in constraints:
            if c1['variable1'] == var:
                answer = False
                for val1 in c1['valeurs']:
                    if val1[0] == val:
                        answer = True
                if not(answer):
                    return False
    return True

###### Fonction backtrack avec choix aléatoire des variables pour le branchement

def backtrack_random_choice_variables(constraints, variables):
    instantiation = {} 
    nb_calls = 0
    def aux_backtrack(constraints, variables):
        nonlocal instantiation
        nonlocal nb_calls
        nb_calls +=1
        if not(test(instantiation,constraints)):
            return False, nb_calls
        if len(variables) == len(instantiation):
            ##print(instantiation)
            return True, nb_calls
        names = [name for name in variables if name not in instantiation]
        random.shuffle(names)
        var = names[0]
        dom = variables[var]
        for x in dom:
            instantiation[var] = x
            if test(instantiation,constraints):
                if aux_backtrack(constraints, variables):
                    #print(instantiation)
                    return True, nb_calls
            del instantiation[var]
        return False, nb_calls
    return aux_backtrack(constraints, variables)


def backtrack_AC3_random_choice_variables(constraints, variables):
    instantiation = {} 
    nb_calls = 0
    variables1 = deepcopy(variables)
    arc_consistance_3(variables1, constraints)
    constraints2 = constraints
    variables2 = deepcopy(variables1)
    def aux_backtrack():
        nonlocal instantiation
        nonlocal variables1
        nonlocal variables2
        nonlocal constraints2
        nonlocal nb_calls
        nb_calls +=1
        if not(test(instantiation,constraints2)):
            return False, nb_calls
        if len(variables2) == len(instantiation):
            #print(instantiation)
            return True, nb_calls
        names = [name for name in variables2 if name not in instantiation]
        random.shuffle(names)
        var = names[0] 
        variables1 = deepcopy(variables2)
        for x in variables2[var]:
            instantiation[var] = x
            variables2[var] = [x]
            arc_consistance_3(variables2,constraints2)
            a = 0
            for name1 in variables2:
                if len(variables2[name1]) == 0:
                    a=1
            if a == 0:
                if test(instantiation,constraints2):
                    if aux_backtrack():
                        #print(instantiation)
                        return True, nb_calls
            del instantiation[var]
            variables2 = deepcopy(variables1)
        return False, nb_calls
    return aux_backtrack() 


def backtrack_Forward_checking_random_choice_variables(constraints, variables):
    instantiation = {} 
    nb_calls = 0
    variables1 = deepcopy(variables)
    arc_consistance_3(variables1, constraints)
    constraints2 = constraints
    variables2 = deepcopy(variables1)
    def aux_backtrack():
        nonlocal instantiation
        nonlocal variables1
        nonlocal variables2
        nonlocal constraints2
        nonlocal nb_calls
        nb_calls +=1
        if not(test(instantiation,constraints2)):
            return False, nb_calls
        if len(variables2) == len(instantiation):
            #print(instantiation)
            return True, nb_calls
        names = [name for name in variables2 if name not in instantiation]
        random.shuffle(names)
        var = names[0] 
        variables1 = deepcopy(variables2)
        for x in variables2[var]:
            instantiation[var] = x
            variables2[var] = [x]
            forward_checking(variables2, constraints2, var, x, instantiation)
            a = 0
            for name1 in variables2:
                if len(variables2[name1]) == 0:
                    a=1
            if a == 0:
                if test(instantiation,constraints2):
                    if aux_backtrack():
                        #print(instantiation)
                        return True, nb_calls
            del instantiation[var]
            variables2 = deepcopy(variables1)
        return False, nb_calls
    return aux_backtrack()


def backtrack_var_min_dom(constraints, variables):
    instantiation = {} 
    nb_calls = 0
    def aux_backtrack(constraints, variables):
        nonlocal instantiation
        nonlocal nb_calls
        nb_calls +=1
        if not(test(instantiation,constraints)):
            return False, nb_calls
        if len(variables) == len(instantiation):
            #print(instantiation)
            return True, nb_calls
        var = variables_min_dom(variables,instantiation)
        dom = variables[var]
        for x in dom:
            instantiation[var] = x
            if test(instantiation,constraints):
                if aux_backtrack(constraints, variables):
                    #print(instantiation)
                    return True, nb_calls
            del instantiation[var]
        return False, nb_calls
    return aux_backtrack(constraints, variables)


def backtrack_var_most_constraints(constraints, variables):
    instantiation = {} 
    nb_calls = 0
    variables1 = sort_variables_most_constraints(variables,constraints)
    def aux_backtrack(constraints, variables):
        nonlocal instantiation
        nonlocal nb_calls
        nb_calls +=1
        if not(test(instantiation,constraints)):
            return False, nb_calls
        if len(variables) == len(instantiation):
            #print(instantiation)
            return True, nb_calls
        names = [name for name in variables if name not in instantiation]
        var = names[0] 
        dom = variables[var]
        for x in dom:
            instantiation[var] = x
            if test(instantiation,constraints):
                if aux_backtrack(constraints, variables):
                    #print(instantiation)
                    return True, nb_calls
            del instantiation[var]
        return False, nb_calls
    return aux_backtrack(constraints, variables1)


def backtrack_most_supported_val_random_choice_variables(constraints, variables):
    instantiation = {} 
    nb_calls = 0
    variables1 = sort_dom_variables_most_suported(variables,constraints)
    def aux_backtrack(constraints, variables):
        nonlocal instantiation
        nonlocal nb_calls
        nb_calls +=1
        if not(test(instantiation,constraints)):
            return False, nb_calls
        if len(variables) == len(instantiation):
            #print(instantiation)
            return True, nb_calls
        names = [name for name in variables if name not in instantiation]
        random.shuffle(names)
        var = names[0]
        dom = variables[var]
        for x in dom:
            instantiation[var] = x
            if test(instantiation,constraints):
                if aux_backtrack(constraints, variables):
                    #print(instantiation)
                    return True, nb_calls
            del instantiation[var]
        return False, nb_calls
    return aux_backtrack(constraints, variables1)


def backtrack_fusion_FC_var_min_dom_val_most_supported(constraints, variables):
    instantiation = {} 
    nb_calls = 0
    variables1 = deepcopy(sort_dom_variables_most_suported(variables,constraints))
    constraints2 = constraints
    variables2 = deepcopy(variables1)
    def aux_backtrack():
        nonlocal instantiation
        nonlocal variables1
        nonlocal variables2
        nonlocal constraints2
        nonlocal nb_calls
        nb_calls +=1
        if not(test(instantiation,constraints2)):
            return False, nb_calls
        if len(variables2) == len(instantiation):
            ##print(instantiation)
            return True, nb_calls
        var = variables_min_dom(variables,instantiation)
        variables1 = deepcopy(variables2)
        for x in variables2[var]:
            instantiation[var] = x
            variables2[var] = [x]
            forward_checking(variables2, constraints2, var, x, instantiation)
            a = 0
            for name1 in variables2:
                if len(variables2[name1]) == 0:
                    a=1
            if a == 0:
                if test(instantiation,constraints2):
                    if aux_backtrack():
                        ##print(instantiation)
                        return True, nb_calls
            del instantiation[var]
            variables2 = deepcopy(variables1)
        return False, nb_calls
    return aux_backtrack()

############

n = 20
with open('n_reines/reines_variables_'+str(n)+'.json') as file:
    variables_ = json.load(file)

with open('n_reines/reines_constraints_'+str(n)+'.json') as file1:
    constraints_ = json.load(file1)


#############


### test
    
pretraitement(constraints_)
""" 
t = time.time()
print(backtrack_random_choice_variables(constraints_, variables_))
print("Time Bc0 = ",time.time()-t)
 """""" 
t=time.time()
print(backtrack_most_supported_val_random_choice_variables(constraints_, variables_))
print("Time val most supported = ",time.time()-t)
 """
 
t=time.time()
print(backtrack_fusion_FC_var_min_dom_val_most_supported(constraints_, variables_))
print("Time fusion = ",time.time()-t)

""" 
t=time.time()
print(backtrack_Forward_checking_random_choice_variables(constraints_, variables_))
print("Time FC = ",time.time()-t)

 """

""" 
t=time.time()
print(backtrack_var_min_dom(constraints_, variables_))
print("Time var min dom = ",time.time()-t)

t=time.time()
print(backtrack_var_most_constraints(constraints_, variables_))
print("Time var most constraints = ",time.time()-t)
 """
""" 
t=time.time()
print(backtrack_AC3_random_choice_variables(constraints_, variables_))
print("Time = ",time.time()-t)


t=time.time()
print(backtrack_Forward_checking_random_choice_variables(constraints_, variables_))
print("Time = ",time.time()-t)


t=time.time()
print(backtrack_var_min_dom(constraints_, variables_))
print("Time = ",time.time()-t)


t=time.time()
print(backtrack_var_most_constraints(constraints_, variables_))
print("Time = ",time.time()-t)


t=time.time()
print(backtrack_most_supported_val_random_choice_variables(constraints_, variables_))
print("Time = ",time.time()-t)


t=time.time()
print(backtrack_AC3_var_min_dom(constraints_, variables_))
print("Time = ",time.time()-t)

 """