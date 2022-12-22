
import math
import random
import arcade
import numpy as np 
from read_map import track, read_track
from read_candy import read_candy
from variable import line_intersection, line_intersection_car
from ai_np import AI
import os
from read_par import read_par
from constans import *
from linalg import *


class Car (arcade.Sprite):
    def __init__(self, x, y, scale) -> None:
        super().__init__("images/car.png", scale, hit_box_algorithm='None', )
        self.AI = AI()
        self.stop_time = 0
        self.left_time = 0
        self.right_time = 0
        self.Candy_score = 1

        self.alpha = 100
        
        self.Candy = Candy()
        self.center_y = y
        self.center_x = x
        self.angle = 0
        self.L = math.sqrt( self.width**2 + self.height**2)
        self.wheel_rot = 0

        self.remove_flag = False
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        
        self.vision_points = []
        self.vision_points_distance = []
        self.vision_points_distance_standart = []
        self.vision_points_OLD = []

        self.F_traction = np.array([1, 0]) 
        self.F_drag = np.array([1, 0]) 
        self.F_rr = np.array([1, 0]) 
        self.F_long = np.array([1, 0]) 
        
        self.direct = np.array([1, 0]) 
        self.acc = np.array([0., 0.]) 
        self.vel = np.array([0., 0.]) 
        self.pos = np.array([x, y]) 

        # self.vision_vec =  [self.direct, rotate_Vec(self.direct, 45), rotate_Vec(self.direct, 90), rotate_Vec(self.direct, 135), rotate_Vec(self.direct, 180), rotate_Vec(self.direct, 225), rotate_Vec(self.direct, 270), rotate_Vec(self.direct, 315)]
        self.vision_vec =  [rotate_Vec(self.direct, 90), rotate_Vec(self.direct, 45), self.direct, rotate_Vec(self.direct, 315), rotate_Vec(self.direct, 270)]
        # self.vision_vec =  [self.direct, rotate_Vec(self.direct, 45), rotate_Vec(self.direct, 315)]
        

    def draw (self):
        super().draw()
        self.draw_hit_box()

        # for j in self.vision_points:
        #     if j:
        #         arcade.draw_circle_filled(j[0], j[1], 10, arcade.color.WHITE)
        
        # self.Candy.draw()


    def update(self, delta_time):        

        self.car_phys(delta_time)

        
        # self.vision_vec =  [self.direct, rotate_Vec(self.direct, 45), rotate_Vec(self.direct, 90), rotate_Vec(self.direct, 135), rotate_Vec(self.direct, 180), rotate_Vec(self.direct, 225), rotate_Vec(self.direct, 270), rotate_Vec(self.direct, 315)]
        self.vision_vec =  [rotate_Vec(self.direct, 90), rotate_Vec(self.direct, 45), self.direct, rotate_Vec(self.direct, 315), rotate_Vec(self.direct, 270)]
        # self.vision_vec =  [self.direct, rotate_Vec(self.direct, 45), rotate_Vec(self.direct, 315)]
        
 
        if line_intersection_car(self.get_adjusted_hit_box(), self.Candy.Candy[0]):
            
            self.Candy_score += 1######################################################################################################
            self.Candy.Candy.pop(0)
            global SUM_TIME
            if len(self.Candy.Candy) == 0:
                self.Candy.refresh()
        
        self.AI_update()
        

    def car_phys(self, delta_time):
        if self.up_pressed and not self.down_pressed:
            self.F_traction = self.direct * ENGINEFORCE
        elif not self.up_pressed and self.down_pressed:
            self.F_traction = - self.direct * BRAKINGFORCE
        else:
            self.F_traction = 0

        if self.left_pressed and not self.right_pressed:
            self.wheel_rot += WHEEL_ROT_PER_SEC * delta_time
            if WHEEL_ROT_MAX < self.wheel_rot: self.wheel_rot = WHEEL_ROT_MAX
        elif self.right_pressed and not self.left_pressed:
            self.wheel_rot -= WHEEL_ROT_PER_SEC * delta_time
            if -WHEEL_ROT_MAX > self.wheel_rot: self.wheel_rot = -WHEEL_ROT_MAX
        else:
            if math.fabs(self.wheel_rot) < WHEEL_ROT_PER_SEC:
                self.wheel_rot = 0
                pass
            else:
                self.wheel_rot += math.copysign(WHEEL_ROT_PER_SEC, -self.wheel_rot)

        if self.wheel_rot != 0 and self.vel.dot(self.vel) != 0:
            self.R = self.L / math.sin(self.wheel_rot) 
            self.angle += self.wheel_rot
            self.direct = ang_to_Vec(self.angle)
        else: 
            self.R = math.inf

        self.F_drag = - C_DRAG * len_vec(self.vel) * self.vel
        self.F_rr = - C_RR * self.vel
        self.F_long = self.F_traction + self.F_drag + self.F_rr

        self.acc = self.F_long / MASS
        self.vel += self.acc * delta_time
        if self.vel.dot(self.direct)<0 : self.vel = self.vel.dot(rotate_Vec(self.direct, 90)) * rotate_Vec(self.direct, 90) / len_vec(self.direct)
        self.pos += self.vel * delta_time

        self.center_x = self.pos[0]
        self.center_y = self.pos[1]

    def AI_update(self):
        return
        z = self.AI.calc()
        if z[0]:
            self.up_pressed = True
        else:  
            self.up_pressed = False

        # if z[1]:
        #     self.down_pressed = True
        # else:  
        #     self.down_pressed = False
        
        if z[1]:
            self.right_pressed = True
        else:  
            self.right_pressed = False

        if z[2]:
            self.left_pressed = True
        else:  
            self.left_pressed = False



class Track ():
    def __init__(self):
        self.track = read_track()

    def draw(self):
        arcade.draw_line_strip(track[0], arcade.color.BLACK)
        arcade.draw_line_strip(track[1], arcade.color.BLACK)


class Candy ():
    def __init__(self):
        self.Candy = read_candy()

    def draw(self):
        global TMP
        for i in range (TMP, len(self.Candy)):
            arcade.draw_line_strip(self.Candy[i], arcade.color.GREEN)

    def refresh(self):
        self.Candy = read_candy()

    def __del__(self):
        del self.Candy


class Welcome(arcade.Window):
    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.GRAY)

        self.car_refresh()
        self.scan_par(READ_PAR)
        
        self.Track = Track()

        self.latest_ = dict()########################################################

    def car_refresh(self):
        self.Cars = []
        for i in range(COUNT_CARS):
            self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))

    def scan_par(self, flag):
        if flag:
            pass
            # w1, w2, b = read_par()
            # for i in self.Cars:
            #     i.AI.set_w1(w1)
            #     i.AI.set_w2(w2)
            #     i.AI.set_b(b)


    def on_draw(self):
        self.clear()

        for i in self.Cars:
            if not i.remove_flag:
                i.draw()    
        
        self.Track.draw()
        arcade.draw_text(f"GEN: {GEN}", 10, 50, arcade.color.BLACK)
        # arcade.draw_text(f"BEST SCORE: {round(BEST_SCORE,1)}, {round(BEST_SCORE_JJJ,1)}", 10, 70, arcade.color.BLACK)
        # arcade.draw_text(f"TIME CUR GEN: {round(SUM_TIME, 1)}", 10, 90, arcade.color.BLACK)
        arcade.draw_text(f"BEST SCORE CUR: {round(self.best_score_cur(), 1)}", 10, SCREEN_HEIGHT - 30, arcade.color.BLACK)


    def on_update(self, delta_time: float = 1 / 60):
        for i in self.Cars:
            if not i.remove_flag:
                self.car_vision(i)
                i.update(delta_time)
                if line_intersection_car(i.get_adjusted_hit_box(), self.Track.track[0]) or line_intersection_car(i.get_adjusted_hit_box(), self.Track.track[1]):
                    i.remove_flag = True
                    pass

        global TICK_SUM, TICK_MAX
        TICK_SUM += 1

        if not self.is_Cars_dead() or TICK_SUM > TICK_MAX:
            #SAVE PAR
            #NEW GEN
            self.car_refresh()
                    

    def best_score_cur(self):
        iii = self.get_best_car()
        return self.Cars[iii].Candy_score
        
      
    def car_vision(self, CAR : Car):
        CAR.vision_points.clear()
        CAR.vision_points_distance.clear()
        for i in CAR.vision_vec:
            segment = [[CAR.center_x, CAR.center_y], [CAR.center_x + 1000 * i[0], CAR.center_y + 1000 * i[1]]]
            point_1 = line_intersection(segment, self.Track.track[0])
            point_2 = line_intersection(segment, self.Track.track[1])
            if not point_1 or not point_2:
                CAR.vision_points.append(point_1 or point_2) 
            elif (CAR.center_x - point_1[0])**2 + (CAR.center_y - point_1[1])**2 < (CAR.center_x - point_2[0])**2 + (CAR.center_y - point_2[1])**2: CAR.vision_points.append(point_1)
            elif (CAR.center_x - point_1[0])**2 + (CAR.center_y - point_1[1])**2 > (CAR.center_x - point_2[0])**2 + (CAR.center_y - point_2[1])**2: CAR.vision_points.append(point_2)
        
        if not CAR.vision_points_OLD : CAR.vision_points_OLD = CAR.vision_points
        for i in range(len(CAR.vision_points)):
            if CAR.vision_points[i] == False : CAR.vision_points[i] = CAR.vision_points_OLD[i]

            CAR.vision_points_distance.append(math.sqrt ((CAR.center_x - CAR.vision_points[i][0])**2 + (CAR.center_y - CAR.vision_points[i][1])**2))

        minim = 20 
        maxim = 1000 

        CAR.vision_points_distance_standart = list(map(lambda x: (x - minim) / (maxim - minim),CAR.vision_points_distance))
        CAR.vision_points_OLD = CAR.vision_points.copy()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.O:
            pass

        if symbol == arcade.key.P:
            pass

        if symbol == arcade.key.UP:
            for i in self.Cars:
                if not i.remove_flag:
                    i.up_pressed = True

        if symbol == arcade.key.DOWN:
            for i in self.Cars:
                if not i.remove_flag:
                    i.down_pressed = True

        if symbol == arcade.key.LEFT:
            for i in self.Cars:
                if not i.remove_flag:
                    i.left_pressed = True

        if symbol == arcade.key.RIGHT:
            for i in self.Cars:
                if not i.remove_flag:
                    i.right_pressed = True
            

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            for i in self.Cars:
                if not i.remove_flag:
                    i.up_pressed = False

        if symbol == arcade.key.DOWN:
            for i in self.Cars:
                if not i.remove_flag:
                    i.down_pressed = False

        if symbol == arcade.key.LEFT:
            for i in self.Cars:
                if not i.remove_flag:
                    i.left_pressed = False

        if symbol == arcade.key.RIGHT:
            for i in self.Cars:
                if not i.remove_flag:
                    i.right_pressed = False
    

    def is_Cars_dead(self):
        for i in self.Cars:
            if not i.remove_flag:
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

