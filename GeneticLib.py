"""
This module regroup functions and classes that simulate the genetic comportement
that occured in reproduction, but don't care about natural selection
(see Darwin module for that).
"""

from random import random

def mutation(person, lstMutation, mutationPercent = 0.2):
    """
    the person are a list of caracteristics
    the lstMutation is list of the authorised mutation on the
    the mutationPercent is the chance to mutate a caracteristic

    return an hybrid with the same lenth but caracteristic randomly mutate
    from the list of mutation.

    The rate can be specify passing a ratio balence between [0,1] like this:
        [0 ; mutationPercent] -> a mutation occured
        ]mutationPercent ; 1] -> no mutation
    """
    #check balance range
    if not (0 <= mutationPercent <= 1):
        raise AttributeError('mutationPercent is not in range')

    hybrid = []
    for i in range(0, len(person)):
        if(random() > mutationPercent):
            hybrid.append(person[i])
        else:
            randomIndex = random() * len(lstMutation)
            hybrid.append(lstMutation[int(randomIndex)])

    return hybrid

def hybridation(parent1, parent2, balance = 0.5):
    """
    the parents are a list of caracteristics
    the balance is the ratio from which parents the carateristic will be picked

    return an hybrid with the same lenth but caracteristic randomly picked
    from  the first or second parent.

    The rate can be specify passing a ratio balence between [0,1] like this:
        [0 ; balance] -> from parent 1 (parent1)
        ]balance ; 1] -> from parent 2 (parent2)
    """
    #check on the similitud
    if len(parent1) != len(parent2):
        raise AttributeError('parent lengths are not the same')
    #check balance range
    if not (0 <= balance <= 1):
        raise AttributeError('balance is  not in range')

    hybrid = []
    for i in range(0, len(parent1)):
        if(random() > balance):
            hybrid.append(parent1[i])
        else:
            hybrid.append(parent2[i])

    return hybrid

if __name__ == "__main__":
    chemin = [1,2,3,4,5,6,7,8,9]
    listeVillePossiblePourMutation = [11,12,13,14,15,16,17,18,19]

    print mutation(chemin,listeVillePossiblePourMutation)
