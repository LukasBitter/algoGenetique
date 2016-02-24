# ==============================================================================
#  CUSTOM LIBRARIES
# ==============================================================================
import copy
import cProfile
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
        if not (0 <= length):
            if once and length <= len(cities_list):
                raise AttributeError('length is not in range')

        c = list(cities_list)
        path = []
        for i in xrange(0, length):
            randomIndex = random() * len(c)
            if once:
                path.extend([c.pop(int(randomIndex))])
            else:
                path.extend([c[int(randomIndex)]])

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
        # print("******************")
        # print("Cross: Path1 = ", path1)
        # print("Cross: Path2 = ", path2)
        hybrid.extend(path1[:int(pivo * len(path1))])
        hybrid.extend(path2[int(pivo * len(path1)):])

        # print("Cross: hybrid = ", hybrid)

        return hybrid

    @staticmethod
    def hybridation(path1, path2, balance=0.5):
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
        for i in xrange(0, len(path1)):
            if (random() > balance):
                hybrid.extend([path1[i]])
            else:
                hybrid.extend([path2[i]])

        return hybrid

    @staticmethod
    def mutation(path, percent=0.5):
        """
        from a given path create a new path with some caracteristic
        swaped. The percent parameter define how swap mutation will occure.

        The percent can be specify passing a ratio between [0,1]
        """
        if not (0 <= percent <= 1):
            raise AttributeError('percent is  not in range')

        mutation_count = int(percent * len(path))
        hybrid = list(path)
        for i in xrange(0, mutation_count):
            randomIndex1 = int(random() * len(hybrid))
            randomIndex2 = int(random() * len(hybrid))
            tmp1 = hybrid[randomIndex1]
            tmp2 = hybrid[randomIndex2]
            hybrid[randomIndex1] = tmp2
            hybrid[randomIndex2] = tmp1

        return hybrid


# ==============================================================================
#  CUSTOM CLASSES
# ==============================================================================

from math import sqrt
import time


class Darwin(object):
    """
    Execute the genetic algorithm in a given time
    """

    def __init__(self, **kwargs):
        self.max_time_s = float(kwargs.get('max_time_s', 10))
        self.cities_list = kwargs.get('cities_list', [])
        self.pop_number =  kwargs.get('pop_number', 10)

    def initialisation(self):
        """
        Create a starting pool of random path
        """
        self.paths_list = []
        for i in xrange(self.pop_number):
            # print("init pop_number: ", i)
            path = Genetic.createPath(len(self.cities_list), self.cities_list, True)
            # print("path: ", path)
            self.paths_list.extend([MyPathRanked(path)])
            # print("path_list size: ", len(self.paths_list))

        for i in self.paths_list:
            i.ranking()
            # print("Path ", i)

    def runAlgorithm(self):
        """Prototype, please override"""
        raise Exception("This method is not override !")

    def run(self):
        timeout = False

        self.initialisation()

        print "start algorithm for ~" + str(self.max_time_s) + " s"
        startTime = time.time()

        logList = []
        count = 0
        bestPath = self.runAlgorithm()

        while not timeout:
            count += 1
            # print("while counts ", count)
            newBestPath = self.runAlgorithm()
            bestPath = (bestPath, newBestPath)[newBestPath.getRank() < bestPath.getRank()]
            endTime = time.time()
            # print("paths_list len before append: ", len(self.paths_list))
            # print(self.paths_list)
            logList.extend([self.paths_list])
            # print("loglist count: ", len(logList[count-1]))

            if (endTime - startTime > self.max_time_s):# or count > 3):
                timeout = True

        with open('log.txt', 'w') as f:
            for list_path in logList:
                f.write('************************ ' + str(len(list_path)) + '\n')
                count_path = 0
                for path in list_path:
                    count_path +=1
                    f.write("Path " + str(count_path) + " / " + str(path.rank) + ": " + path.path.__repr__())
                    f.write('\n')

        print "runs count: ", count
        print "algorithm finish in " + str(endTime - startTime) + " s"
        print "the best path lenght found : " + str(bestPath.getRank())
        print bestPath.path
        return bestPath.path

    def getValidPathList(self, paths_list):
        new_path_list = []
        for rankedPath in (paths_list):
            if self.isValid(rankedPath):
                new_path_list.extend([rankedPath]);
        return new_path_list

    def isValid(self, rankedPath):
        for city in self.cities_list:
            #print city
            #print rankedPath
            if city not in rankedPath.path:
                # print("One invalid path deleted")
                return False
        return True

    def printPathList(self, msg, pathList):
        count = 0
        print(msg)
        for idx, path in enumerate(pathList):
            print idx, ")  ",
            for j in path.path:
                print j[0],
            print ": ", path.rank


class DarwinForCities1(Darwin):
    """
    Try to find the shortest path to reatch all cities
    Algorithm number 1 very trivial, other will follows :-)
    """

    def __init__(self, **kwargs):
        Darwin.__init__(self, **kwargs)
        self.percent = kwargs.get('percentKeep', 0.3)

    def runAlgorithm(self):
        pivot = int(len(self.paths_list) * self.percent)
        self.paths_list = self.paths_list[:pivot]

        for i in xrange(len(self.cities_list) - pivot):
            path = Genetic.createPath(len(self.cities_list), self.cities_list, True)
            self.paths_list.append(MyPathRanked(path))

        prev_path = None
        for i in self.paths_list:
            Genetic.mutation(i.path)
            i.ranking()

        self.paths_list = self.getValidPathList(self.paths_list)

        self.paths_list = sorted(self.paths_list, key=MyPathRanked.getRank)

        return self.paths_list[0]

class DarwinForCities2(Darwin):
    """
    Try 2 TODO algorithm descrition
    """

    def __init__(self, **kwargs):
        Darwin.__init__(self, **kwargs)
        self.percent = kwargs.get('percentKeep', 0.3)
        self.elit = []

    def runAlgorithm(self):

        # print '***********************************'
        # print '**********  RUN ALGO  *************'
        # print '***********************************'

        # if self.elit:
            # self.printPathList("Elites before double: ", self.elit)

        for i in xrange(len(self.paths_list)):
            newPath = Genetic.createPath(len(self.cities_list), self.cities_list, True)
            self.paths_list.extend([MyPathRanked(newPath)])

        # if self.elit:
            # self.printPathList("Elites after double: ", self.elit)

        prev = None
        for i in self.paths_list:
            i.path = Genetic.mutation(i.path, 0.4)
            i.ranking()
            '''if(prev != None):
                temp = i
                i.path = Genetic.crossPathWithPivot(i.path, prev.path, 0.5)
                prev.path = Genetic.crossPathWithPivot(prev.path, temp.path, 0.5)
                i.ranking()
                prev.ranking()
                prev = None
            else:
                prev = i'''
        # if self.elit:
            # self.printPathList("Elites after mutation: ", self.elit)

        # self.printPathList("Paths_list after genetic mutation: " + str(len(self.paths_list)), self.paths_list)
        self.paths_list = self.getValidPathList(self.paths_list)
        # self.printPathList("Paths_list after delete unvalid: " + str(len(self.paths_list)), self.paths_list)
        if self.elit:
            # self.printPathList("Elites: ", self.elit)
            self.paths_list.extend((self.elit[0], self.elit[1]))
            # self.printPathList("List with elites: ", self.paths_list)
        self.paths_list = sorted(self.paths_list, key=MyPathRanked.getRank)
        # self.printPathList("Paths_list after sort: " + str(len(self.paths_list)), self.paths_list)
        self.paths_list = self.paths_list[:len(self.cities_list)]
        # self.printPathList("Paths_list after keep numer pop: " + str(len(self.paths_list)), self.paths_list)
        self.elit = copy.deepcopy(self.paths_list[:2])
        # self.printPathList("New elites: ", self.elit)

        return self.paths_list[0]


class DarwinForCities3(Darwin):
    """
    Try 2 TODO algorithm descrition
    """

    def __init__(self, **kwargs):
        Darwin.__init__(self, **kwargs)
        self.percent = kwargs.get('percentKeep', 0.3)
        self.listTownSize = kwargs.get('listTownSize', 10)
        self.elit = []

    def runAlgorithm(self):

        for i in xrange(self.listTownSize):
            newPath = Genetic.createPath(len(self.cities_list), self.cities_list, True)
            self.paths_list.extend([MyPathRanked(newPath)])

        prev = None
        for i in self.paths_list:
            i.path = Genetic.mutation(i.path, 0.4)
            i.ranking()

        self.paths_list = self.getValidPathList(self.paths_list)
        if self.elit:
            self.paths_list.extend((self.elit[0], self.elit[1]))
        self.paths_list = sorted(self.paths_list, key=MyPathRanked.getRank)
        self.paths_list = self.paths_list[:self.listTownSize]
        self.elit = copy.deepcopy(self.paths_list[:2])

        return self.paths_list[0]


class MyPathRanked(object):
    def __init__(self, path):
        self.path = path
        self.rank = 0
        #self.ranking()  // si on laisse ca, il y a un 10 appels de ranking() a chaque ajout de path a path_list

    def __repr__(self):
        return "MyPathRanked : " + str(self.rank)

    def getRank(self):
        return self.rank

    def __len__(self):
        return len(self.path)

    def ranking(self):
        """
        Sum of the distance between all the town of the path
        """
        dist = 0.0
        previous_town = None

        for town in self.path:
            if previous_town != None:
                dist += sqrt((town[1] - previous_town[1]) ** 2 + (town[2] - previous_town[2]) ** 2)
                #print("previous_town != None")
            previous_town = town

        first_town = self.path[0]
        last_town = self.path[len(self.path) - 1]
        dist += sqrt((last_town[1] - first_town[1]) ** 2 + (last_town[2] - first_town[2]) ** 2)
        self.rank = dist


# ==============================================================================
#  READ FILE
# ==============================================================================

class CitiesLoader:
    @staticmethod
    def getCitiesFromFile(fileName):
        cities = []

        with open(fileName, 'r') as f:
            for line in f:
                word = line.split(' ')
                city = (word[0], int(word[1]), int(word[2]))
                cities.extend([city])

        return cities


# ==============================================================================
#  GUI
# ==============================================================================

import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys


class GUI:
    @staticmethod
    def showGui(cities):
        screen_x = 500
        screen_y = 500

        city_color = [10, 10, 200]  # blue
        city_radius = 3

        font_color = [255, 255, 255]  # white

        pygame.init()
        window = pygame.display.set_mode((screen_x, screen_y))
        pygame.display.set_caption('Exemple')
        screen = pygame.display.get_surface()
        font = pygame.font.Font(None, 30)

        screen.fill(0)
        citiesCoor = [x[1:] for x in cities]
        pygame.draw.lines(screen, city_color, True, citiesCoor)
        text = font.render("Un chemin, SURREMENT le meilleur!", True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()

        while True:
            event = pygame.event.wait()
            if event.type == KEYDOWN: break


def go_solve(file=None, gui=True, maxtime=0):
    listCities = CitiesLoader.getCitiesFromFile(file)

    d = DarwinForCities3(cities_list=listCities, max_time_s=maxtime)


    listCities = d.run()

    GUI.showGui(listCities)


# ==============================================================================
#  MAIN
# ==============================================================================

if __name__ == "__main__":
    import sys

    # prog = open(sys.argv[1]).read()
    # print(prog)
    fileName = sys.argv[1]
    gui = sys.argv[2]
    maxTime = sys.argv[3]

    go_solve(fileName, gui, maxTime)
