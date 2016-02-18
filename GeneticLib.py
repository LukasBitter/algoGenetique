
#==============================================================================
#  CUSTOM LIBRARIES
#==============================================================================

from random import random

class Genetic:
    """
    This class regroup functions that simulate the genetic comportement for
    cities creation
    """

    @staticmethod
    def createPath(length, cities_list, once=True):
        """
        create a new path between cities from a list of cities picked randomly

        If once parameter is set to True, the cities from the list only
        taken once
        """
        if not (0 <=  length):
            if once and length <= len(cities_list):
                raise AttributeError('length is not in range')

        c = list(cities_list)
        path = []
        for i in range(0, length):
            randomIndex = random() * len(c)
            if once:
                path.append(c.pop(int(randomIndex)))
            else:
                path.append(c[int(randomIndex)])

        return path

    @staticmethod
    def crossPathWithPivot(path1, path2, pivo=0.5):
        """
        create a new path from 2 parents (path1 & path2) with
        one part of the first parent and one part of the second.

        the pivo is the parameter that set the percent taken from the first
        and the second like this:
            [0 ; pivo] -> from parent 1 (path1)
            ]pivo ; 1] -> from parent 2 (path2)

        the parents must have the same length
        """
        if len(path1) != len(path2):
            raise AttributeError('parents lengths are not the same')
        if not (0 <= pivo <= 1):
            raise AttributeError('pivo is  not in range')

        hybrid = []
        hybrid.extend(path1[:int(pivo*len(path1))])
        hybrid.extend(path2[int(pivo*len(path1)):])

        return hybrid

    @staticmethod
    def hybridation(path1, path2, balance = 0.5):
        """
        create a new individual from 2 parents (path1 & path2) with
        a random pick from them.

        the balance is the ratio from which parents the carateristic will be picked
        The rate can be specify passing a ratio balence between [0,1] like this:
            [0 ; balance] -> from parent 1 (parent1)
            ]balance ; 1] -> from parent 2 (parent2)

        the parents must have the same length
        """
        if len(path1) != len(path2):
            raise AttributeError('parent lengths are not the same')
        if not (0 <= balance <= 1):
            raise AttributeError('balance is  not in range')

        hybrid = []
        for i in range(0, len(path1)):
            if(random() > balance):
                hybrid.append(path1[i])
            else:
                hybrid.append(path2[i])

        return hybrid

    @staticmethod
    def mutation(path, percent = 0.2):
        """
        from a given path create a new path with some caracteristic
        swaped. The percent parameter define how swap mutation will occure.

        The percent can be specify passing a ratio between [0,1]
        """
        if not (0 <= percent <= 1):
            raise AttributeError('percent is  not in range')

        mutation_count = int(percent * len(path))
        hybrid = list(path)
        for i in range(0, mutation_count):
            randomIndex1 = int(random() * len(hybrid))
            randomIndex2 = int(random() * len(hybrid))
            tmp1 = hybrid[randomIndex1]
            tmp2 = hybrid[randomIndex2]
            hybrid[randomIndex1] = tmp2
            hybrid[randomIndex2] = tmp1

        return hybrid

#==============================================================================
#  CUSTOM CLASSES
#==============================================================================

from math import sqrt
import time

class Darwin(object):
    """
    Execute the genetic algorithm in a given time
    """

    def  __init__(self, **kwargs):
        self.max_time_s = kwargs.get('max_time_s', 10)

    def initialisation(self):
        """Prototype, please override"""
        raise Exception("This method is not override !")

    def runAlgorithm(self):
        """Prototype, please override"""
        raise Exception("This method is not override !")

    def run(self):
        timeout = False
        bestPath = None

        self.initialisation()

        print "start algorithm for ~"+str(self.max_time_s)+" s"
        startTime = time.time()
        while not timeout:
            bestPath = self.runAlgorithm()

            endTime = time.time()

            if endTime - startTime > self.max_time_s:
                timeout = True

        print "algorithm finish in "+str(endTime - startTime)+" s"
        return bestPath


class DarwinForCities1(Darwin):
    """
    Try to find the shortest path to reatch all cities

    Algorithm number 1, other will follows :-)
    """

    def  __init__(self, **kwargs):
        Darwin.__init__(self, **kwargs)
        self.cities_list = kwargs.get('cities_list', [])
        self.elit = []

    def initialisation(self):
        """
        Create a starting pool of random path
        """
        self.paths_list = []
        for i in range(len(self.cities_list)):
            path = Genetic.createPath(len(self.cities_list), self.cities_list, True)
            self.paths_list.append(MyPathRanked(path))

    def runAlgorithm(self):
        """
        Find the best path with genetic optimisation
        """
        #TODO make some mutation and try again
        self.rank = {}
        for i in self.paths_list:
            i.ranking()

        #self.paths_list.path.sort(key=rank)



        return self.paths_list[0].path  #TODO return the best


class MyPathRanked(object):
    def __init__(self, path):
        self.path = path
        self.rank = 0
        self.ranking()

    def ranking(self):
        """
        Sum of the distance between all the town of the path
        """
        dist = 0
        previous_town = None

        for town in self.path:
            if previous_town == None:
                previous_town = town
            else:
                dist += sqrt(town[1]**2 + town[2]**2)
        self.rank = dist

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

def go_solve(file=None, gui=True, maxtime=0):

    listCities = CitiesLoader.getCitiesFromFile(file)

    d = DarwinForCities1(cities_list = listCities, max_time_s= maxtime)
    listCities = d.run()

    GUI.showGui(listCities)



#==============================================================================
#  MAIN
#==============================================================================

if __name__ == "__main__":
    import sys
    #prog = open(sys.argv[1]).read()
    #print(prog)
    fileName = sys.argv[1]
    gui = sys.argv[2]
    maxTime = sys.argv[3]

    go_solve(fileName, gui, maxTime)

    GUI.showGui(listCities)
