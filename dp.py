import time

from deap import base, algorithms
from deap import creator
from deap import tools
from constans import *
import algelitism
from linalg import *
from intersection import line_intersection, line_intersection_car
from neuralnetwork import NNetwork
from read_par import read_par

import random
import numpy as np
from Car import Car

class car_ind(list):
    def __init__(self, *args):
        if READ_PAR: 
            super().__init__(read_par(FILE_PAR))
        else:
            super().__init__(*args)
        self.car = Car(CAR_START_X, CAR_START_Y, 0.08)

class DP():
    def __init__(self):
        global POPULATION_SIZE, READ_PAR, TICK_MAX, SHOW_BEST
        if SHOW_BEST:
            READ_PAR = True
            TICK_MAX = 10000
            POPULATION_SIZE = 1
        self.hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", car_ind, fitness=creator.FitnessMax)
        global LENGTH_CHROM
        LENGTH_CHROM = NNetwork.getTotalWeights(AI_INPUT_SHAPE, AI_MIDDLE_SHAPE, AI_OUTPUT_SHAPE)

        self.toolbox = base.Toolbox()

        self.toolbox.register("randomWeight", random.uniform, -1.0, 1.0)
        self.toolbox.register("individualCreator", tools.initRepeat, creator.Individual, self.toolbox.randomWeight, LENGTH_CHROM)
        self.toolbox.register("populationCreator", tools.initRepeat, list, self.toolbox.individualCreator)
        # if READ_PAR: 

        #     # self.toolbox.register("create_ind", create_ind, '48')
        #     self.toolbox.register("read_par", read_par, '48')
        #     self.toolbox.register("create_ind", creator.Individual, self.toolbox.read_par)
        #     self.toolbox.register("populationCreator", tools.initRepeat, list, self.toolbox.create_ind)
        
        self.population = self.toolbox.populationCreator(n=POPULATION_SIZE)
        
        self.toolbox.register("evaluate", getScore)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        self.toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=LOW, up=UP, eta=ETA)
        self.toolbox.register("mutate", tools.mutPolynomialBounded, low=LOW, up=UP, eta=ETA, indpb= 1 * 1.0/LENGTH_CHROM)

        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("max", np.max)
        # self.stats.register("avg", np.mean)
        
        self.logbook = ''


        # algelitism.eaSimpleElitism
        # algorithms.eaSimple
        # population, logbook = algelitism.eaSimpleElitism(population, self.toolbox,
        #                                         cxpb=P_CROSSOVER,
        #                                         mutpb=P_MUTATION,
        #                                         ngen=MAX_GENERATIONS,
        #                                         halloffame=self.hof,
        #                                         stats=self.stats,
        #                                         verbose=True)

        # maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")

        # best = self.hof.items[0]
        # print(best)

    def change_indpb(self, alpha):
        self.toolbox.register("mutate", tools.mutPolynomialBounded, low=LOW, up=UP, eta=ETA, indpb=alpha * 1.0/LENGTH_CHROM)

    def get_best(self):
        return tools.selBest(self.population, 1)[0]



def create_ind(a):
    return creator.Individual(read_par(a))

def getScore(individual):
    return individual.car.Candy_score,

    
def update_car(individual):
    if individual.car.remove_flag: return
    individual.car.state = individual.car.car_vision()
    # print (max(individual.car.state))
    if not individual.car.set_W:
        individual.car.set_W = True
        individual.car.model.set_weights(individual)
    # print(len_vec(individual.car.vel))
    individual.car.AI_update(np.argmax(individual.car.model.predict(individual.car.state)))
    individual.car.car_phys(1/60)

    individual.car.check_crush()

    # individual.car.vision_vec =  [individual.car.direct, rotate_Vec(individual.car.direct, 30), rotate_Vec(individual.car.direct, 90), rotate_Vec(individual.car.direct, 150), rotate_Vec(individual.car.direct, 180), rotate_Vec(individual.car.direct, -30), rotate_Vec(individual.car.direct, -90), rotate_Vec(individual.car.direct, -150)]
    individual.car.vision_vec =  [individual.car.direct, rotate_Vec(individual.car.direct, 30), rotate_Vec(individual.car.direct, 90), rotate_Vec(individual.car.direct, -30), rotate_Vec(individual.car.direct, -90)]

    if line_intersection_car(individual.car.get_adjusted_hit_box(), individual.car.Candy.Candy[0]):
        
        individual.car.Candy_score += 1######################################################################################################
        individual.car.Candy.Candy.pop(0)
        if len(individual.car.Candy.Candy) == 0:
            individual.car.Candy.refresh()

    


def update_car_2(car):
    if car.remove_flag: return
    car.state = car.car_vision()
    car.AI_update(np.argmax(car.model.predict(car.state)))
    car.car_phys(1/60)

    car.check_crush()

    car.vision_vec =  [car.direct, rotate_Vec(car.direct, 30), rotate_Vec(car.direct, 90), rotate_Vec(car.direct, 150), rotate_Vec(car.direct, 180), rotate_Vec(car.direct, -30), rotate_Vec(car.direct, -90), rotate_Vec(car.direct, -150)]

    if line_intersection_car(car.get_adjusted_hit_box(), car.Candy.Candy[0]):
        
        car.Candy_score += 1######################################################################################################
        car.Candy.Candy.pop(0)
        if len(car.Candy.Candy) == 0:
            car.Candy.refresh()


def set_car_w(individual):
    if not individual.car.set_W:
        individual.car.set_W = True
        individual.car.model.set_weights(individual)

    



