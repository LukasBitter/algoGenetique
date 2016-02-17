
#==============================================================================
#  CUSTOM LIBRARIES
#==============================================================================

from random import random

class Genetic:
    """
    This class regroup functions that simulate the genetic comportement
    that occured in reproduction, but don't care about natural selection
    (see Darwin class for that).

    the individuals are a list of caracteristics
    """

    @staticmethod
    def create(length, caracteristics, once=False):
        """
        create a new individual from a list of caracteristics picked randomly

        If once parameter is set to True, the caracteristics from the list
        are only taken once
        """
        if not (0 <=  length <= len(caracteristics)):
            raise AttributeError('length is not in range')

        c = list(caracteristics)
        individual = []
        for i in range(0, length):
            randomIndex = random() * len(c)
            if once:
                individual.append(c.pop(int(randomIndex)))
            else:
                individual.append(c[int(randomIndex)])

        return individual

    @staticmethod
    def renovation(individual, caracteristics, chance = 0.2, once=False):
        """
        for each caracteristics of individual, there is a small chance to mute
        in a new one picked randomly in a list of caracteristics.

        The chance can be specify passing a ratio balence between [0,1] like this:
            [0 ; chance] -> a mutation occured
            ]chance ; 1] -> no mutation

        If once parameter is set to True, the caracteristics from the list
        are only taken once
        """
        if not (0 <= chance <= 1):
            raise AttributeError('chance is not in range')
        if len(caracteristics) < len(individual) and once:
            raise AttributeError('not enough caracteristics for a once parameter')

        c = list(caracteristics)
        hybrid = []
        for i in range(0, len(individual)):
            if(random() > chance):
                hybrid.append(individual[i])
            else:
                randomIndex = random() * len(c)
                if once:
                    hybrid.append(c.pop(int(randomIndex)))
                else:
                    hybrid.append(c[int(randomIndex)])

        return hybrid

    @staticmethod
    def cross(individual1, individual2, pivo=0.5):
        """
        create a new individual from 2 parents (individual2 & individual2) with
        one part of the first parent and one part of the second.

        the pivo is the parameter that set the percent taken from the first
        and the second like this:
            [0 ; pivo] -> from parent 1 (individual1)
            ]pivo ; 1] -> from parent 2 (individual2)

        the parents must have the same length
        """
        if len(individual1) != len(individual2):
            raise AttributeError('parents lengths are not the same')
        if not (0 <= pivo <= 1):
            raise AttributeError('pivo is  not in range')

        hybrid = []
        hybrid.extend(individual1[:int(pivo*len(individual1))])
        hybrid.extend(individual2[int(pivo*len(individual1)):])

        return hybrid

    @staticmethod
    def hybridation_chance(individual1, individual2, balance = 0.5):
        """
        create a new individual from 2 parents (individual2 & individual2) with
        a random pick from them.

        the balance is the ratio from which parents the carateristic will be picked
        The rate can be specify passing a ratio balence between [0,1] like this:
            [0 ; balance] -> from parent 1 (parent1)
            ]balance ; 1] -> from parent 2 (parent2)

        the parents must have the same length
        """
        if len(individual1) != len(individual2):
            raise AttributeError('parent lengths are not the same')
        if not (0 <= balance <= 1):
            raise AttributeError('balance is  not in range')

        hybrid = []
        for i in range(0, len(individual1)):
            if(random() > balance):
                hybrid.append(individual1[i])
            else:
                hybrid.append(individual2[i])

        return hybrid

    @staticmethod
    def mutation(individual, percent = 0.2):
        """
        from a given individual create a new individual with some caracteristic
        swaped. The percent parameter define how swap mutation will occure.

        The percent can be specify passing a ratio between [0,1]
        """
        if not (0 <= percent <= 1):
            raise AttributeError('percent is  not in range')

        mutation_count = int(percent * len(individual))
        hybrid = list(individual)
        for i in range(0, mutation_count):
            randomIndex1 = int(random() * len(hybrid))
            randomIndex2 = int(random() * len(hybrid))
            tmp1 = hybrid[randomIndex1]
            tmp2 = hybrid[randomIndex2]
            hybrid[randomIndex1] = tmp2
            hybrid[randomIndex2] = tmp1

        return hybrid

#==============================================================================
#  ALGORITHMIQUE
#==============================================================================

from math import sqrt

class Darwin(object):
    """
    This class simulate the natural selection process.

    First the population are generated
    Second the individuals are confronted and ranked
    Third the best individual are determinate
    """

    def  __init__(self, **kwargs):
        self.caracteristics = kwargs.get('caracteristics', [])
        self.max_time_s = kwargs.get('max_time_s', 10)
        self.max_population =  kwargs.get('max_population', 10)

    def populate(self):
        """Prototype, please override"""
        raise Exception("This method is not override !")

    def ranking(self, individual):
        """Prototype, please override"""
        raise Exception("This method is not override !")

    def evaluate(self):
        """Prototype, please override"""
        raise Exception("This method is not override !")


class DarwinForCities1(Darwin):
    """
    Try to find the shortest path to reatch all cities

    Algorithm number 1, other will follows :-)
    """

    def  __init__(self, **kwargs):
        Darwin.__init__(self, **kwargs)
        self.elit = []

    def populate(self):
        """
        Population of several path of all cities matched
        (always pass by all the towns)
        """
        self.individuals = []
        c = self.caracteristics
        initialRank = 0
        for i in range(self.max_population):
            self.individuals.append(Genetic.create(len(c), c, True))

    def ranking(self, path):
        """
        Sum of the distance between all the town of the path

        path[0] contains the town list in visit order
        path[1] contains the rank of this path
        """
        dist = 0
        previous_town = None
        for town in path:
            if previous_town == None:
                previous_town = town
            else:
                dist += sqrt(town[1]**2 + town[2]**2)

        path[1] = dist
        return dist

    def evaluate(self):
        """
        TODO make some mutation and try again
        """
        self.rank = []
        for i in self.individuals:
            self.rank.append(self.ranking(i))

        print "PATH LENGTH : "
        print self.rank

#==============================================================================
#  READ FILE
#==============================================================================

class CitiesLoader:

    @staticmethod
    def getCitiesFromFile(fileName):
        cities = []

        with open(fileName, 'r') as f:
            for line in f:
                word = line.split(' ')
                city = (word[0], int(word[1]), int(word[2]))
                cities.append(city)

        return cities


#==============================================================================
#  GUI
#==============================================================================

import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys

class GUI:

    @staticmethod
    def showGui(cities):
        screen_x = 500
        screen_y = 500

        city_color = [10,10,200] # blue
        city_radius = 3

        font_color = [255,255,255] # white

        pygame.init()
        window = pygame.display.set_mode((screen_x, screen_y))
        pygame.display.set_caption('Exemple')
        screen = pygame.display.get_surface()
        font = pygame.font.Font(None,30)

        screen.fill(0)
        citiesCoor = [x[1:] for x in cities]
        pygame.draw.lines(screen,city_color,True,citiesCoor)
        text = font.render("Un chemin, SURREMENT le meilleur!", True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()

        while True:
        	event = pygame.event.wait()
        	if event.type == KEYDOWN: break

#==============================================================================
#  MAIN
#==============================================================================

if __name__ == "__main__":
    import sys
    #prog = open(sys.argv[1]).read()
    #print(prog)
    fileName = sys.argv[1]
    listCities = CitiesLoader.getCitiesFromFile(fileName)
    #listCities = CitiesLoader.getCitiesFromFile("Ressources12/data/pb005.txt")

    d = DarwinForCities1(caracteristics = listCities)
    d.populate()
    d.evaluate()

    GUI.showGui(listCities)
