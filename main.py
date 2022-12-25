
import math
import random
import arcade
import numpy as np 
from read_map import track, read_track
from read_candy import read_candy
from intersection import line_intersection, line_intersection_car
# from ai_np import AI
import os
from read_par import read_par
from constans import *
from linalg import *
from dp import DP, getScore, update_car
from algelitism import eaSimpleElitism_START, eaSimpleElitism_CONTINUE 
from Car import Car



class Track ():
    def __init__(self):
        self.track = read_track()

    def draw(self):
        arcade.draw_line_strip(track[0], arcade.color.BLACK)
        arcade.draw_line_strip(track[1], arcade.color.BLACK)



class Welcome(arcade.Window):
    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.GRAY)

        # self.car_refresh()
        # self.scan_par(READ_PAR)
        self.dp = DP()
        self.Track = Track()
        self.draw_cars=[]

        self.dp.population, self.dp.logbook, self.dp.hof = eaSimpleElitism_START(self.dp.population, self.dp.toolbox,
                                                cxpb=P_CROSSOVER,
                                                mutpb=P_MUTATION,
                                                ngen=MAX_GENERATIONS,
                                                halloffame=self.dp.hof,
                                                stats=self.dp.stats,
                                                verbose=True)


    # def car_refresh(self):
    #     self.Cars = []
    #     for i in range(COUNT_CARS):
    #         # self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))

    # def scan_par(self, flag):
    #     if flag:
    #         pass
    #         # w1, w2, b = read_par()
    #         # for i in self.Cars:
    #         #     i.AI.set_w1(w1)
    #         #     i.AI.set_w2(w2)
    #         #     i.AI.set_b(b)

    def cars_to_draw(self, pop):
        for i in pop:
            if not i.car.remove_flag:
                x = arcade.Sprite("images/car.png", 0.08, hit_box_algorithm='None')
                x.center_y = i.car.center_y
                x.center_x = i.car.center_x
                x.angle = i.car.angle
                x.draw()

    def on_draw(self):
        self.clear()
        self.cars_to_draw(self.dp.population)

        # cars = self.dp.population.copy
        # for i in self.dp.population:
        #     if not i.car.remove_flag:
        #         i.car.draw()   
        
        self.Track.draw()

        arcade.draw_text(f"GEN: {GEN}", 10, 50, arcade.color.BLACK)
        # arcade.draw_text(f"BEST SCORE: {round(BEST_SCORE,1)}, {round(BEST_SCORE_JJJ,1)}", 10, 70, arcade.color.BLACK)
        # arcade.draw_text(f"TIME CUR GEN: {round(SUM_TIME, 1)}", 10, 90, arcade.color.BLACK)
        # arcade.draw_text(f"BEST SCORE CUR: {round(self.best_score_cur(), 1)}", 10, SCREEN_HEIGHT - 30, arcade.color.BLACK)


    def on_update(self, delta_time: float = 1 / 60):

        # вызов поколения  
        cur_tick = 0
        global GEN  
        GEN += 1
        if cur_tick < 2 and not self.is_Cars_dead():
            cur_tick += 1
            for i in self.dp.population:
                update_car(i)
        else:        
            print (f"Прожило тиков: {cur_tick}")
            self.dp.population, self.dp.logbook = eaSimpleElitism_CONTINUE(self.dp.population, self.dp.toolbox,
                                                    cxpb=P_CROSSOVER,
                                                    mutpb=P_MUTATION,
                                                    ngen=MAX_GENERATIONS,
                                                    halloffame=self.dp.hof,
                                                    stats=self.dp.stats,
                                                    verbose=True,
                                                    logbook=self.dp.logbook,
                                                    gen = GEN)
            cur_tick = 0
            GEN += 1
            if GEN % 1 == 0:
                    with open(f"par/{RAND_RAN_NUM}.txt", "a") as file:
                        file.write(f"GEN: {GEN}\n")
                        file.write(self.dp.hof.items[0].car.model.get_weights() + '\n\n')

        # for i in self.dp.population:
        #     if not i.car.remove_flag:
        #         getScore(i)
                
        
        
                   
        # global TICK_SUM, TICK_MAX
        # TICK_SUM += 1

        # if not self.is_Cars_dead() or TICK_SUM > TICK_MAX:
        #     #SAVE PAR
        #     #NEW GEN
        #     self.car_refresh()
                    
    
    # def best_score_cur(self):
    #     iii = self.get_best_car()
    #     return self.Cars[iii].Candy_score
        
      
    

    # def on_key_press(self, symbol, modifiers):
    #     if symbol == arcade.key.O:
    #         pass

    #     if symbol == arcade.key.P:
    #         pass

    #     if symbol == arcade.key.UP:
    #         for i in self.Cars:
    #             if not i.remove_flag:
    #                 i.up_pressed = True

    #     if symbol == arcade.key.DOWN:
    #         for i in self.Cars:
    #             if not i.remove_flag:
    #                 i.down_pressed = True

    #     if symbol == arcade.key.LEFT:
    #         for i in self.Cars:
    #             if not i.remove_flag:
    #                 i.left_pressed = True

    #     if symbol == arcade.key.RIGHT:
    #         for i in self.Cars:
    #             if not i.remove_flag:
    #                 i.right_pressed = True
            

    # def on_key_release(self, symbol: int, modifiers: int):
    #     if symbol == arcade.key.UP:
    #         for i in self.Cars:
    #             if not i.remove_flag:
    #                 i.up_pressed = False

    #     if symbol == arcade.key.DOWN:
    #         for i in self.Cars:
    #             if not i.remove_flag:
    #                 i.down_pressed = False

    #     if symbol == arcade.key.LEFT:
    #         for i in self.Cars:
    #             if not i.remove_flag:
    #                 i.left_pressed = False

    #     if symbol == arcade.key.RIGHT:
    #         for i in self.Cars:
    #             if not i.remove_flag:
    #                 i.right_pressed = False
    

    def is_Cars_dead(self):
        for i in self.dp.population:
            if not i.car.remove_flag:
                return True
        return False

    def get_best_car(self):
        max = 0
        iii = 0
        
        for i in range(len(self.Cars)):
            if self.Cars[i].Candy_score > max:
                max = self.Cars[i].Candy_score
                iii = i
        return iii

    

if __name__ == "__main__":
    RAND_RAN_NUM = max(list(map(lambda x: int(x[:x.find('.')]), os.listdir('par')))) + 1

    app = Welcome()

    arcade.run()

    

