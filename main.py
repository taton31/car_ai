
import math
import random
import arcade
import numpy as np 
from read_map import track, read_track
# from read_candy import read_candy
# from intersection import line_intersection, line_intersection_car
# from ai_np import AI
import os
from read_par import read_par
from constans import *
from linalg import *
from dp import DP, getScore, update_car, update_car_2, set_car_w
from algelitism import eaSimpleElitism_START, eaSimpleElitism_CONTINUE 
# from Car import Car
from multiprocessing import Pool
from multiprocessing import Barrier, Process



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
        self.x = arcade.Sprite("images/car.png", 0.08, hit_box_algorithm='None')
        global POPULATION_SIZE, READ_PAR, TICK_MAX, SHOW_BEST
        if SHOW_BEST:
            READ_PAR = True
            TICK_MAX = 10000
            POPULATION_SIZE = 1
        
        if DEBAG_MODE:
            TICK_MAX = 1000000

          
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


    def cars_to_draw(self, pop):
        for i in pop:
            if not i.car.remove_flag:
                self.x.center_y = i.car.center_y
                self.x.center_x = i.car.center_x
                self.x.angle = i.car.angle
                self.x.alpha = 100
                self.x.draw()
                arcade.draw_text(getScore(i)[0], self.x.center_x + 10, self.x.center_y + 10, arcade.color.BLACK, bold = True)


    def car_draw_best(self):
        
        x = arcade.Sprite("images/car.png", 0.08, hit_box_algorithm='None')
        x.center_y = self.dp.get_best().car.center_y
        x.center_x = self.dp.get_best().car.center_x
        x.angle = self.dp.get_best().car.angle
        x.draw()

    def on_draw(self):
        self.clear()
        if DEBAG_MODE:
            car = self.dp.population[0]
            car.car.draw()
        else:
            self.cars_to_draw(self.dp.population)
        # self.car_draw_best()

        # car = self.dp.population[0]
        # car.car.draw()
        # car.car.Candy.draw()
        
        self.Track.draw()

        arcade.draw_text(f"GEN:  {GEN}", 10, 50, arcade.color.BLACK)
        arcade.draw_text(f"TICK: {CUR_TICK}", 10, 70, arcade.color.BLACK)
        arcade.draw_text(f"MAX SCORE: {self.dp.logbook[-1]['max']}", 10, 90, arcade.color.BLACK)
        # arcade.draw_text(f"TIME CUR GEN: {round(SUM_TIME, 1)}", 10, 90, arcade.color.BLACK)
        # arcade.draw_text(f"BEST SCORE CUR: {round(self.best_score_cur(), 1)}", 10, SCREEN_HEIGHT - 30, arcade.color.BLACK)

        pass


    def on_update(self, delta_time: float = 1/60):

        # вызов поколения  
        global GEN, CUR_TICK, TICK_MAX 

        self.check_tick()
        
        if self.is_ex_live_Car():
            CUR_TICK += 1

            for i in self.dp.population:
                update_car(i)
                # print(i.car.state)

            # for i in self.dp.population:
            #     set_car_w(i)
            # tst = []
            # for i in self.dp.population:
            #     tst.append(i.car)

            # for i in tst:
            #     update_car_2(i)
            # with Pool() as p:
            # self.p.map(update_car_2, tst)
            # self.dp.toolbox.map(update_car_2, tst)


        else:        
            if not DEBAG_MODE:
            # print (f"Прожило тиков: {CUR_TICK}")
                if GEN % 15 == 0:
                    # TICK_MAX += 100
                    # print (f"Количество тиков: {TICK_MAX}")
                    with open(f"par/{RAND_RAN_NUM}.txt", "a") as file:
                        file.write(f"GEN: {GEN}\n")
                        file.write(f"MAX SCORE: {self.dp.logbook[-1]['max']}\n")
                        file.write(np.array2string(self.dp.get_best().car.model.get_weights()) + '\n\n')
                
                sigma = 2.0
                if GEN == 1 and READ_PAR: 
                    self.dp.change_indpb(sigma * 1)
                    self.elitism(0.8)
                elif self.dp.logbook[-1]['max'] <= 22:
                    self.dp.change_indpb(sigma * 4)
                    self.elitism(0.5)
                    
                elif 22 < self.dp.logbook[-1]['max'] <= 30:
                    self.dp.change_indpb(sigma * 3)
                    self.elitism(0.5)

                elif 30 < self.dp.logbook[-1]['max'] <= 55:
                    self.dp.change_indpb(sigma * 2)
                    self.elitism(0.3)

                elif 55 < self.dp.logbook[-1]['max'] <= 70:
                    self.dp.change_indpb(sigma * 2)
                    self.elitism(0.3)

                elif 70 < self.dp.logbook[-1]['max']:
                    self.dp.change_indpb(sigma * 1)
                    self.elitism(0.4)

                else:
                    self.dp.change_indpb(sigma * 1)
                    self.elitism(0.4)
                

                for i in self.dp.population:
                    i.car.set_zero_point()
                CUR_TICK = 1
                GEN += 1

            else:
                for i in self.dp.population:
                    i.car.set_zero_point()
            
    def elitism(self, mutpb):
        self.dp.population, self.dp.logbook = eaSimpleElitism_CONTINUE(self.dp.population, self.dp.toolbox,
                                                cxpb=P_CROSSOVER,
                                                mutpb=mutpb,
                                                ngen=MAX_GENERATIONS,
                                                halloffame=None,
                                                # halloffame=self.dp.hof,
                                                stats=self.dp.stats,
                                                verbose=True,
                                                logbook=self.dp.logbook,
                                                gen = GEN)
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
        
      
    def check_tick(self):
        for i in self.dp.population:
            if not i.car.remove_flag:
                i.car.life_time = CUR_TICK
                if CUR_TICK > TICK_MAX:
                    i.car.remove_flag = True



    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.O:
            pass

        if symbol == arcade.key.P:
            pass

        if not DEBAG_MODE: return

        if symbol == arcade.key.UP:
            for i in self.dp.population:
                if not i.car.remove_flag:
                    i.car.up_pressed = True

        if symbol == arcade.key.DOWN:
            for i in self.dp.population:
                if not i.car.remove_flag:
                    i.car.down_pressed = True

        if symbol == arcade.key.LEFT:
            for i in self.dp.population:
                if not i.car.remove_flag:
                    i.car.left_pressed = True

        if symbol == arcade.key.RIGHT:
            for i in self.dp.population:
                if not i.car.remove_flag:
                    i.car.right_pressed = True
            

    def on_key_release(self, symbol: int, modifiers: int):
        if not DEBAG_MODE: return

        if symbol == arcade.key.UP:
            for i in self.dp.population:
                if not i.car.remove_flag:
                    i.car.up_pressed = False

        if symbol == arcade.key.DOWN:
            for i in self.dp.population:
                if not i.car.remove_flag:
                    i.car.down_pressed = False

        if symbol == arcade.key.LEFT:
            for i in self.dp.population:
                if not i.car.remove_flag:
                    i.car.left_pressed = False

        if symbol == arcade.key.RIGHT:
            for i in self.dp.population:
                if not i.car.remove_flag:
                    i.car.right_pressed = False

        

    def is_ex_live_Car(self):
        for i in self.dp.population:
            if not i.car.remove_flag:
                return True
        return False


if __name__ == "__main__":
    RAND_RAN_NUM = max(list(map(lambda x: int(x[:x.find('.')]), os.listdir('par')))) + 1

    app = Welcome()
    arcade.run()

    



