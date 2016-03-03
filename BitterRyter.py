# ==============================================================================
#  CUSTOM LIBRARIES
# ==============================================================================
import copy
from random import random

class Genetic:
    '''
    This class regroup functions that simulate the genetic comportement for
    cities creation
    '''

    @staticmethod
    def createPath(length, cities_list, once=True):
        '''
        Create a new path between cities from a list of cities picked randomly
        :param length: length f the path
        :param cities_list: list of cities
        :param once: If set to True, the cities from the list are only taken once
        :return: cities path
        '''
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
        '''
        Create a new path from 2 parents (path1 & path2) with one
        part of the first parent and one part of the second.
        the parents must have the same length
        :param path1: first parent
        :param path2: second parent
        :param pivo: set the percent taken from the first and the second like this:
            [0 ; pivo] -> from parent 1 (path1)
            ]pivo ; 1] -> from parent 2 (path2)
        :return: child1, child2
        '''
        if len(path1) != len(path2):
            raise AttributeError('parents lengths are not the same')
        if not (0 <= pivo <= 1):
            raise AttributeError('pivo is  not in range')

        l = len(path1)
        hybrid1 = []
        hybrid2 = []
        hybrid1.extend(path1[:int(pivo * l)])
        hybrid1.extend(path2[int(pivo * l):])
        hybrid2.extend(path2[:int(pivo * l)])
        hybrid2.extend(path1[int(pivo * l):])
        return hybrid1, hybrid2

    @staticmethod
    def mutation(path, percent=0.5):
        '''
        From a given path create a new path with some caracteristic swaped.
        :param path:
        :param percent: defines how swap mutation will occure (ratio between [0,1])
        :return:
        '''
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

    @staticmethod
    def swap(path, i, j):
        '''
        Swaps two cities in a path
        :param path: cities path
        :param i: index of city #1
        :param j: index of city #2
        :return: n/a
        '''
        temp = path[i]
        path[i] = path[j]
        path[j] = temp

# ==============================================================================
#  CUSTOM CLASSES
# ==============================================================================

from math import sqrt
import time


class Darwin(object):
    '''
    Execute the genetic algorithm in a given time
    '''

    def __init__(self, **kwargs):
        self.max_time_s = float(kwargs.get('max_time_s', 10))
        self.cities_list = kwargs.get('cities_list', [])
        self.pop_number =  kwargs.get('pop_number', 10)
        self.func_gui =  kwargs.get('func_gui')
        self.listElitSize = kwargs.get('listElitSize', self.pop_number/10)

    def initialisation(self):
        '''
        Create a starting pool of random path
        :return: n/a
        '''
        self.paths_list = []
        self.elit = []
        for i in xrange(self.pop_number):
            path = Genetic.createPath(len(self.cities_list), self.cities_list, True)
            self.paths_list.extend([MyPathRanked(path)])

        for i in self.paths_list:
            i.ranking()
        self.paths_list = sorted(self.paths_list, key=MyPathRanked.getRank)

    def runAlgorithm(self):
        '''
        Prototype, please override
        '''
        raise Exception("This method is not override !")

    def run(self):
        timeout = False

        self.initialisation()
        startTime = time.time()
        bestPath = self.runAlgorithm()

        while not timeout:
            newBestPath = self.runAlgorithm()
            bestPath = (bestPath, newBestPath)[newBestPath.getRank() < bestPath.getRank()]
            endTime = time.time()

            if self.func_gui != None:
                self.func_gui(bestPath.path)
            if (endTime - startTime > self.max_time_s):
                timeout = True

        return bestPath.getRank(), bestPath.path


    def dist(self,c1, c2):
        '''
        :param c1: city #1
        :param c2: city #2
        :return: distance between c1 and c2
        '''
        return sqrt((c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2)

    def getValidPathList(self, paths_list):
        '''
        :param paths_list:
        :return: paths_list containing only valid paths
        '''
        new_path_list = []
        for rankedPath in (paths_list):
            if self.isValid(rankedPath):
                new_path_list.extend([rankedPath]);
        return new_path_list

    def isValid(self, rankedPath):
        '''
        :param rankedPath:
        :return: True if path is valid, else False
        '''
        for city in self.cities_list:
            if city not in rankedPath.path:
                return False
        return True

class DarwinForCities(Darwin):
    '''
    Class for handling a genetic algorthm implementation
    '''

    def __init__(self, **kwargs):
        Darwin.__init__(self, **kwargs)

    def runAlgorithm(self):
        '''
        This function implements the genetic algorithm
        :return: the best path encountered during genetic modification
        '''

        self.selected_paths = []

        # Selection
        totalLength = 0
        for i in range(self.pop_number) :
            totalLength += i

        for n in range(self.pop_number):
            randomLen = int(random() * totalLength)
            stopLen = 0
            for i in range(len(self.paths_list)):
                stopLen += len(self.paths_list)-i
                if stopLen > randomLen:
                    self.selected_paths.extend([MyPathRanked(self.paths_list[i].path)])
                    self.selected_paths[-1].ranking()
                    break

        # mutation and cross
        new_path_list = []
        for i in range(0, len(self.selected_paths), 2):
            curr1 = self.selected_paths[i]
            curr2 = self.selected_paths[i+1]
            newPath1 = Genetic.mutation(curr1.path, random())
            newPath2 = Genetic.mutation(curr2.path, random())
            new_path_list.extend([MyPathRanked(newPath1)])
            new_path_list[-1].ranking()
            new_path_list.extend([MyPathRanked(newPath2)])
            new_path_list[-1].ranking()

            pivot = random()
            newPath1, newPath2 = Genetic.crossPathWithPivot(curr1.path, curr2.path, pivot)
            new_path_list.extend([MyPathRanked(newPath1)])
            new_path_list[-1].ranking()
            new_path_list.extend([MyPathRanked(newPath2)])
            new_path_list[-1].ranking()

        self.selected_paths.extend(new_path_list)
        self.selected_paths = self.getValidPathList(self.selected_paths)

        # 2opt
        for p in self.selected_paths:
            for i in range(len(p)-3):
                for j in range(i+2,len(p)-1):
                    d_ab = self.dist(p.path[i], p.path[i+1])
                    d_cd = self.dist(p.path[j], p.path[j+1])
                    d_ac = self.dist(p.path[i], p.path[j])
                    d_bd = self.dist(p.path[i+1], p.path[j+1])
                    if (d_ab + d_cd > d_ac + d_bd):
                        Genetic.swap(p.path,i+1,j)
                        p.ranking()

        if self.elit:
            self.selected_paths.extend((self.elit))
        self.selected_paths = sorted(self.selected_paths, key=MyPathRanked.getRank)
        self.selected_paths = self.selected_paths[:self.pop_number]
        self.elit = copy.deepcopy(self.selected_paths[:self.listElitSize])

        self.paths_list = copy.deepcopy(self.selected_paths)

        return self.selected_paths[0]


class MyPathRanked(object):
    '''
    Class for handling ranked paths
    '''
    def __init__(self, path):
        self.path = path
        self.rank = 0

    def __repr__(self):
        return "MyPathRanked : " + str(self.rank)

    def getRank(self):
        return self.rank

    def __len__(self):
        return len(self.path)

    def ranking(self):
        '''
        Sum of the distance between all the town of the path
        :return: n/a
        '''
        dist = 0.0
        previous_town = None

        for town in self.path:
            if previous_town != None:
                dist += sqrt((town[1] - previous_town[1]) ** 2 + (town[2] - previous_town[2]) ** 2)
            previous_town = town

        first_town = self.path[0]
        last_town = self.path[len(self.path) - 1]
        dist += sqrt((last_town[1] - first_town[1]) ** 2 + (last_town[2] - first_town[2]) ** 2)
        self.rank = dist


# ==============================================================================
#  READ FILE
# ==============================================================================

class CitiesLoader:
    '''
    Class used t load a cities file
    '''
    @staticmethod
    def getCitiesFromFile(fileName):
        '''
        :param fileName:
        :return: cities list
        '''
        cities = []

        with open(fileName, 'r') as f:
            for line in f:
                word = line.split(' ')
                city = (word[0], int(word[1]), int(word[2]))
                cities.extend([city])

        return cities


# ==============================================================================
#  GA_SOLVE
# ==============================================================================

def ga_solve(file=None, gui=False, maxtime=0):
    '''

    :param file: cities filename
    :param gui: gui showing or not
    :param maxtime: maxtime allowed for best path finding throught genetic modification
    :return: n/a
    '''
    import pygame
    from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
    import sys

    collecting = file==None
    listCities = []
    if file != None:
        listCities = CitiesLoader.getCitiesFromFile(file)
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

    def drawEdition(positions):
        positions = [x[1:] for x in positions]
        screen.fill(0)
        for pos in positions:
			pygame.draw.circle(screen,city_color,pos,city_radius)
        text = font.render("Nombre: %i" % len(positions), True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()

    drawEdition(listCities)

    if collecting:
        counting = 0
        while collecting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    collecting = False
                elif event.type == MOUSEBUTTONDOWN:
                    counting = counting+1
                    pos = pygame.mouse.get_pos()
                    print (str(counting), pos[0], pos[1])
                    listCities.append((str(counting), pos[0], pos[1]))
                    drawEdition(listCities)

    def drawRecherche(positions):
        positions = [x[1:] for x in positions]
        screen.fill(0)
        pygame.draw.lines(screen,city_color,True,positions)
        text = font.render("Un chemin, pas le meilleur!", True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()

    if gui:
        drawRecherche(listCities)
    else:
        drawRecherche = None

    d = DarwinForCities(cities_list=listCities, max_time_s=maxtime, func_gui=drawRecherche)
    bestlen, listCities = d.run()
    if gui:
        drawRecherche(listCities)
    return bestlen, listCities

    while True:
    	event = pygame.event.wait()
    	if event.type == KEYDOWN: break



# ==============================================================================
#  MAIN
# ==============================================================================

if __name__ == "__main__":
    import sys
    fileName = sys.argv[1]
    if fileName == 'None':
        fileName = None
    gui = sys.argv[2]
    maxTime = sys.argv[3]

    bestlenresult, pathresult = ga_solve(fileName, gui, maxTime)
    print bestlenresult
