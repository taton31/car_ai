
import math
import random
import arcade
import numpy as np 
from read_map import track, read_track
from read_candy import read_candy
from variable import line_intersection, line_intersection_car
from ai_np import AI
import os
import re
from read_par import read_par
TMP_MAX=0
TMP_MIN=10000
# Imports
TMP = 0
RAND_RAN_NUM = 0

READ_PAR = False

TYPE_CROSS = 'arifm'

ALPHA_mutation = 1/2
ALpha_ = 10
# Constants
# Speed limit
MAX_SPEED = 12.0
MAX_SPEED_ROT = 3.0

ALPHA = 1
# How fast we accelerate
ACCELERATION_RATE_START = 0.4
ACCELERATION_RATE_STOP = 0.4
ACCELERATION_RATE_ROT = 1.6

# How fast to slow down after we let off the key
FRICTION = 0.02
FRICTION_ROT = 0.1

BEST_SCORE_REPEAT_COUNT = 0
BEST_SCORE_NUMBER = 0

ENGINEFORCE = 1600000
BRAKINGFORCE = ENGINEFORCE / 10
C_DRAG = 0.7
C_RR = 3000
MASS = 900
WHEEL_ROT_PER_SEC = 0.5 * 60
WHEEL_ROT_MAX = 5

COUNT_CARS = 32
CAR_START_X = 250
CAR_START_Y = 830.

MAX_TIME = 30
SUM_TIME = 0

GEN = 1
BEST_SCORE = 0
BEST_SCORE_JJJ = 0

CAR_STOP_GEN = 0
CAR_STOP_TIME = 0

FRICTION_MAX = 100000

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
SCREEN_TITLE = "CAR_AI"
RADIUS = 150


class Car (arcade.Sprite):
    def __init__(self, x, y, scale) -> None:
        super().__init__("images/car.png", scale, hit_box_algorithm='None', )
        self.AI = AI()
        self.alpha = 100
        self.Candy = Candy()
        self.Candy_score = 1
        self.center_y = y
        self.center_x = x
        self.angle = 0

        self.stop_time = 0
        self.left_time = 0
        self.right_time = 0
        
        self.remove_flag = False

        self.L = math.sqrt( self.width**2 + self.height**2)
        self.wheel_rot = 0

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.F_a = np.array([0, 0]) 
        
        self.F_traction = np.array([1, 0]) 
        self.F_drag = np.array([1, 0]) 
        self.F_rr = np.array([1, 0]) 
        self.F_long = np.array([1, 0]) 
        
        self.direct = np.array([1, 0]) 
        self.acc = np.array([0., 0.]) 
        self.vel = np.array([0., 0.]) 
        self.pos = np.array([x, y]) 
        self.F_res_a = np.array([0., 0.])

        # self.vision_vec =  [self.direct, self.rotate_Vec(self.direct, 45), self.rotate_Vec(self.direct, 90), self.rotate_Vec(self.direct, 135), self.rotate_Vec(self.direct, 180), self.rotate_Vec(self.direct, 225), self.rotate_Vec(self.direct, 270), self.rotate_Vec(self.direct, 315)]
        self.vision_vec =  [self.rotate_Vec(self.direct, 90), self.rotate_Vec(self.direct, 45), self.direct, self.rotate_Vec(self.direct, 315), self.rotate_Vec(self.direct, 270)]
        # self.vision_vec =  [self.direct, self.rotate_Vec(self.direct, 45), self.rotate_Vec(self.direct, 315)]
        
        self.vision_points = []
        self.vision_points_distance = []
        self.vision_points_distance_standart = []
        self.vision_points_OLD = []

        


    def draw (self):
        super().draw()

        # for j in self.vision_points:
        #     if j:
        #         arcade.draw_circle_filled(j[0], j[1], 10, arcade.color.WHITE)
        
        # self.Candy.draw()

    def __del__(self):
        del self.Candy

    def rotate_Vec(self, vec, angle):
        angle = math.pi * angle / 180
        rotatedX = vec[0] * math.cos(angle) - vec[1] * math.sin(angle)
        rotatedY = vec[0] * math.sin(angle) + vec[1] * math.cos(angle)
        return np.array([rotatedX, rotatedY]) 

    def ang_to_Vec(self, angle):
        angle = math.pi * angle / 180
        rotatedX = math.cos(angle)
        rotatedY = math.sin(angle)
        return np.array([rotatedX, rotatedY]) 

    def rotate_90(self, vec):
        vel_len = self.len_vec(vec)
        rotatedX = vec[1] / vel_len
        rotatedY = - vec[0] / vel_len
        return np.array([rotatedX, rotatedY]) 

    def len_vec(self, vec):
        return math.sqrt(vec.dot(vec))


    def update(self, delta_time):        

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
            self.direct = self.ang_to_Vec(self.angle)
        else: 
            self.R = math.inf
            self.F_a = np.array([0., 0.]) 
            self.F_res_a = np.array([0., 0.]) 

        

        self.F_drag = - C_DRAG * self.len_vec(self.vel) * self.vel
        self.F_rr = - C_RR * self.vel

        self.F_long = self.F_traction + self.F_drag + self.F_rr

        self.acc = self.F_long / MASS
        self.vel += self.acc * delta_time
        if self.vel.dot(self.direct)<0 : self.vel = self.vel.dot(self.rotate_Vec(self.direct, 90)) * self.rotate_Vec(self.direct, 90) / self.len_vec(self.direct)
        self.pos += self.vel * delta_time

        self.center_x = self.pos[0]
        self.center_y = self.pos[1]

        
        # self.vision_vec =  [self.direct, self.rotate_Vec(self.direct, 45), self.rotate_Vec(self.direct, 90), self.rotate_Vec(self.direct, 135), self.rotate_Vec(self.direct, 180), self.rotate_Vec(self.direct, 225), self.rotate_Vec(self.direct, 270), self.rotate_Vec(self.direct, 315)]
        self.vision_vec =  [self.rotate_Vec(self.direct, 90), self.rotate_Vec(self.direct, 45), self.direct, self.rotate_Vec(self.direct, 315), self.rotate_Vec(self.direct, 270)]
        # self.vision_vec =  [self.direct, self.rotate_Vec(self.direct, 45), self.rotate_Vec(self.direct, 315)]
        
 
        if line_intersection_car(self.get_adjusted_hit_box(), self.Candy.Candy[0]):
            
            self.Candy_score += 1
            tmp = self.Candy.Candy[0]
            self.Candy.Candy_back.append(tmp)
            self.Candy.Candy.pop(0)
            global SUM_TIME
            if len(self.Candy.Candy) == 0:
                self.Candy_score += 5 * 60. / SUM_TIME
                self.Candy.refresh()

            
            if len(self.Candy.Candy_back) > 4:
                self.Candy.Candy_back.pop(0)
        if len(self.Candy.Candy_back) > 1 and line_intersection_car(self.get_adjusted_hit_box(), self.Candy.Candy_back[0]):
            self.Candy_score -= 10
            self.remove_flag = True
            
        
        self.check_motion(delta_time)
        self.AI_update()
        
    def check_motion(self, delta_time):
        if not (self.up_pressed and not self.down_pressed): # and not self.left_pressed and not self.right_pressed: 
            self.stop_time += delta_time
        else: 
            self.stop_time = 0
        
        if self.stop_time > 1:
            self.Candy_score -= 5
            self.remove_flag = True

        if  (self.right_pressed and not self.left_pressed): # and not self.left_pressed and not self.right_pressed: 
            self.right_time += delta_time
        else: 
            self.right_time = 0
        
        if self.right_time > 0.5:
            self.remove_flag = True
            self.Candy_score -= 5

        if  (self.left_pressed and not self.right_pressed): # and not self.left_pressed and not self.right_pressed: 
            self.left_time += delta_time
        else: 
            self.left_time = 0
        
        if self.left_time > 0.5:
            self.remove_flag = True
            self.Candy_score -= 5


    def AI_update(self):
        self.AI.set_x(self.vision_points_distance_standart)
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


        # if not self.down_pressed:
        #     self.Candy_score -= 2/30
        
        
         

class Track ():
    def __init__(self):
        self.track = read_track()

    def draw(self):
        arcade.draw_line_strip(track[0], arcade.color.BLACK)
        arcade.draw_line_strip(track[1], arcade.color.BLACK)


class Candy ():
    def __init__(self):
        self.Candy = read_candy()
        self.Candy_back = []

    def draw(self):
        global TMP
        for i in range (TMP, len(self.Candy)):
            arcade.draw_line_strip(self.Candy[i], arcade.color.GREEN)

        # for i in range (len(self.Candy_back)):
        #     arcade.draw_line_strip(self.Candy_back[i], arcade.color.GREEN)

    def refresh(self):
        self.Candy = read_candy()

    def __del__(self):
        del self.Candy


        






# Classes
class Welcome(arcade.Window):
    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        global RAND_RAN_NUM
        RAND_RAN_NUM = max(list(map(lambda x: int(x[:x.find('.')]), os.listdir('par')))) + 1
        arcade.set_background_color(arcade.color.GRAY)
        self.Cars = []
        for i in range(COUNT_CARS):
            self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))
            
        if READ_PAR:
            w1, w2, b = read_par()
            for i in self.Cars:
                i.AI.set_w1(w1)
                i.AI.set_w2(w2)
                i.AI.set_b(b)

            
        self.Track = Track()

        self.latest_ = dict()

        

        


    def on_draw(self):
        self.clear()
        for i in range(len(self.Cars)):
            if not self.Cars[i].remove_flag:
                self.Cars[i].draw()    
        
        self.Track.draw()
        arcade.draw_text(f"GEN: {GEN}", 10, 50, arcade.color.BLACK)
        arcade.draw_text(f"BEST SCORE: {round(BEST_SCORE,1)}, {round(BEST_SCORE_JJJ,1)}", 10, 70, arcade.color.BLACK)
        arcade.draw_text(f"TIME CUR GEN: {round(SUM_TIME, 1)}", 10, 90, arcade.color.BLACK)
        arcade.draw_text(f"MAX TIME: {MAX_TIME}", 10, 110, arcade.color.BLACK)
        
        arcade.draw_text(f"BEST SCORE CUR: {round(self.best_score_cur(), 1)}", 10, SCREEN_HEIGHT - 30, arcade.color.BLACK)


    def on_update(self, delta_time: float = 1 / 60):
        for i in self.Cars:
            if not i.remove_flag:
                self.car_vision(i)
                i.update(delta_time)

        for i in self.Cars:
            if not i.remove_flag:
                if line_intersection_car(i.get_adjusted_hit_box(), self.Track.track[0]) or line_intersection_car(i.get_adjusted_hit_box(), self.Track.track[1]):
                    i.remove_flag = True

        global SUM_TIME
        global MAX_TIME
        global GEN, BEST_SCORE_JJJ, BEST_SCORE
        SUM_TIME += delta_time

        if not self.is_Cars_dead() or SUM_TIME > MAX_TIME:
            self.save_par_2()
            self.car_mix_8()
            BEST_SCORE_JJJ = BEST_SCORE
                    

    def best_score_cur(self):
        iii, jjj = self.get_best_car()
        return self.Cars[iii].Candy_score
            
    def save_par(self):    
        global RAND_RAN_NUM 
        global GEN
        if GEN % 50 == 0:
            latest_sort = sorted(self.latest_)
            goal_sort = latest_sort[-1]
            w1=self.latest_[goal_sort][0]
            w2=self.latest_[goal_sort][1]
            b=self.latest_[goal_sort][2]
            with open(f"par/{RAND_RAN_NUM}.txt", "a") as file:
                file.write(f"GEN: {GEN}\n")
                file.write(f"BEST SCORE: {goal_sort}\n")
                file.write(np.array2string(w1) + '\n')
                file.write(np.array2string(w2) + '\n')
                file.write(np.array2string(b) + '\n\n')

    def save_par_2(self):    
        global RAND_RAN_NUM
        global GEN
        if GEN % 50 == 0:
            goal_sort, jjj = self.get_best_car()
            w1=self.Cars[goal_sort].AI.get_w1()
            w2=self.Cars[goal_sort].AI.get_w2()
            b=self.Cars[goal_sort].AI.get_b()
            with open(f"par/{RAND_RAN_NUM}.txt", "a") as file:
                file.write(f"GEN: {GEN}\n")
                file.write(f"BEST SCORE: {goal_sort}\n")
                file.write(np.array2string(w1) + '\n')
                file.write(np.array2string(w2) + '\n')
                file.write(np.array2string(b) + '\n\n')
        
    def car_mix_1(self):
        iii, jjj = self.get_best_car()
        w1_iii = self.Cars[iii].AI.get_w1() 
        w2_iii = self.Cars[iii].AI.get_w2() 
        b_iii = self.Cars[iii].AI.get_b() 
        
        self.latest_.append([self.Cars[iii].Candy_score,[w1_iii,w2_iii,b_iii]])
        max = 0
        w1_kkk=0
        w2_kkk=0
        b_kkk=0
        for i in self.latest_:
            if i[0]>max:
                max = i[0]
                w1_kkk=i[1][0]
                w2_kkk=i[1][1]
                b_kkk=i[1][2]

        if len(self.latest_) > 5: self.latest_.pop(0)
        
        w1_jjj = self.Cars[jjj].AI.get_w1() 
        w2_jjj = self.Cars[jjj].AI.get_w2() 
        b_jjj = self.Cars[jjj].AI.get_b() 
        if len(self.latest_) == 0: 
            w1_kkk=w1_jjj
            w2_kkk=w2_jjj
            b_kkk=b_jjj
        if GEN > 3 and self.Cars[iii].Candy_score < 6:
            self.Cars.clear()
            for i in range(COUNT_CARS):
                self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))
                self.Cars[i].AI.refresh()
        else:
            self.Cars.clear()
            for i in range(COUNT_CARS):
                self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))
            for i in range(0, COUNT_CARS, 5):
                self.Cars[i].AI.set_w1(w1_iii)
                self.Cars[i].AI.set_w2(w2_iii)
                self.Cars[i].AI.set_b(b_iii)

                self.Cars[i].AI.mix_w1()
                self.Cars[i].AI.mix_w2()
                self.Cars[i].AI.mix_b()
            for i in range(1, COUNT_CARS, 5):
                self.Cars[i].AI.set_w1(w1_kkk)
                self.Cars[i].AI.set_w2(w2_kkk)
                self.Cars[i].AI.set_b(b_kkk)

                self.Cars[i].AI.mix_w1()
                self.Cars[i].AI.mix_w2()
                self.Cars[i].AI.mix_b()
            for i in range(2, COUNT_CARS, 5):
                self.Cars[i].AI.set_mix_w1(w1_iii, w1_kkk)
                self.Cars[i].AI.set_mix_w2(w2_iii, w2_kkk)
                self.Cars[i].AI.set_mix_b(b_iii, b_kkk)

                # self.Cars[i].AI.mix_lit_w1()
                # self.Cars[i].AI.mix_lit_w2()
                # self.Cars[i].AI.mix_lit_b()
                # self.Cars[i].AI.mix_w1()
                # self.Cars[i].AI.mix_w2()
                # self.Cars[i].AI.mix_b()
            for i in range(3, COUNT_CARS, 5):
                self.Cars[i].AI.set_mix_w1(w1_iii, w1_kkk)
                self.Cars[i].AI.set_mix_w2(w2_iii, w2_kkk)
                self.Cars[i].AI.set_mix_b(b_iii, b_kkk)

                self.Cars[i].AI.mix_lit_w1()
                self.Cars[i].AI.mix_lit_w2()
                self.Cars[i].AI.mix_lit_b()
            for i in range(4, COUNT_CARS, 5):
                self.Cars[i].AI.set_w1(w1_jjj)
                self.Cars[i].AI.set_w2(w2_jjj)
                self.Cars[i].AI.set_b(b_jjj)

                self.Cars[i].AI.mix_w1()
                self.Cars[i].AI.mix_w2()
                self.Cars[i].AI.mix_b()


    def car_mix_2(self):
        global SUM_TIME
        global GEN
        SUM_TIME = 0
        GEN += 1
        iii, jjj = self.get_best_car()
        w1_iii = self.Cars[iii].AI.get_w1() 
        w2_iii = self.Cars[iii].AI.get_w2() 
        b_iii = self.Cars[iii].AI.get_b() 
        self.latest_[self.Cars[iii].Candy_score] = [w1_iii,w2_iii,b_iii]
        latest_sort = sorted(self.latest_)
        
        global BEST_SCORE_JJJ
        if (len(latest_sort)) > 1:
            if latest_sort[-1] == iii:
                goal_sort = latest_sort[-2]
            else:
                goal_sort = latest_sort[-1]
            BEST_SCORE_JJJ = goal_sort
            w1_kkk=self.latest_[goal_sort][0]
            w2_kkk=self.latest_[goal_sort][1]
            b_kkk=self.latest_[goal_sort][2]
        else:
            BEST_SCORE_JJJ = 0
            w1_kkk = self.Cars[jjj].AI.get_w1() 
            w2_kkk = self.Cars[jjj].AI.get_w2() 
            b_kkk = self.Cars[jjj].AI.get_b() 

        if len(latest_sort) > 5: self.latest_.pop(list(self.latest_)[0])
        
        if GEN > 3 and self.Cars[iii].Candy_score < 9:
            self.Cars.clear()
            for i in range(COUNT_CARS):
                self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))
                self.Cars[i].AI.refresh()
        else:
            self.Cars.clear()
            for i in range(COUNT_CARS):
                self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))
            for i in range(0, COUNT_CARS, 5):
                self.Cars[i].AI.set_w1(w1_kkk)
                self.Cars[i].AI.set_w2(w2_kkk)
                self.Cars[i].AI.set_b(b_kkk)

                self.Cars[i].AI.mix_w1_AL(ALpha_)
                self.Cars[i].AI.mix_w2_AL(ALpha_)
                self.Cars[i].AI.mix_b_AL(ALpha_)
            for i in range(1, COUNT_CARS, 5):
                self.Cars[i].AI.set_w1(w1_kkk)
                self.Cars[i].AI.set_w2(w2_kkk)
                self.Cars[i].AI.set_b(b_kkk)

                self.Cars[i].AI.mix_w1_AL(ALpha_ * 1.5)
                self.Cars[i].AI.mix_w2_AL(ALpha_ * 1.5)
                self.Cars[i].AI.mix_b_AL(ALpha_ * 1.5)
            for i in range(2, COUNT_CARS, 5):
                self.Cars[i].AI.set_w1(w1_kkk)
                self.Cars[i].AI.set_w2(w2_kkk)
                self.Cars[i].AI.set_b(b_kkk)

                self.Cars[i].AI.mix_w1_AL(ALpha_ / 1.5)
                self.Cars[i].AI.mix_w2_AL(ALpha_ / 1.5)
                self.Cars[i].AI.mix_b_AL(ALpha_ / 1.5)
            for i in range(3, COUNT_CARS, 5):
                self.Cars[i].AI.set_mix_w1(w1_iii, w1_kkk)
                self.Cars[i].AI.set_mix_w2(w2_iii, w2_kkk)
                self.Cars[i].AI.set_mix_b(b_iii, b_kkk)

                self.Cars[i].AI.mix_w1_AL(ALpha_ * 1.5)
                self.Cars[i].AI.mix_w2_AL(ALpha_ * 1.5)
                self.Cars[i].AI.mix_b_AL(ALpha_ * 1.5)
            for i in range(4, COUNT_CARS, 5):
                self.Cars[i].AI.set_mix_w1(w1_iii, w1_kkk)
                self.Cars[i].AI.set_mix_w2(w2_iii, w2_kkk)
                self.Cars[i].AI.set_mix_b(b_iii, b_kkk)

    def car_mix_3(self, alpha):
        global SUM_TIME
        global GEN
        SUM_TIME = 0
        GEN += 1
        iii, jjj = self.get_best_car()
        w1_iii = self.Cars[iii].AI.get_w1() 
        w2_iii = self.Cars[iii].AI.get_w2() 
        b_iii = self.Cars[iii].AI.get_b() 
        self.latest_[self.Cars[iii].Candy_score] = [w1_iii,w2_iii,b_iii]
        if GEN > 3 and self.Cars[iii].Candy_score < 9:
            self.Cars.clear()
            for i in range(COUNT_CARS):
                self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))
                self.Cars[i].AI.refresh()
        else:
            self.Cars.clear()
            for i in range(COUNT_CARS):
                self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))
            for i in range(0, COUNT_CARS):
                self.Cars[i].AI.set_w1(w1_iii)
                self.Cars[i].AI.set_w2(w2_iii)
                self.Cars[i].AI.set_b(b_iii)
                self.Cars[i].AI.mix_w1_AL(alpha)
                self.Cars[i].AI.mix_w2_AL(alpha)
                self.Cars[i].AI.mix_b_AL(alpha)

    def car_mix_4(self):
        global SUM_TIME, GEN, BEST_SCORE_REPEAT_COUNT, BEST_SCORE_NUMBER
        SUM_TIME = 0
        GEN += 1
        iii, jjj = self.get_best_car()
        w1_iii = self.Cars[iii].AI.get_w1() 
        w2_iii = self.Cars[iii].AI.get_w2() 
        b_iii = self.Cars[iii].AI.get_b() 
        if BEST_SCORE_NUMBER == iii:
            BEST_SCORE_REPEAT_COUNT += 1
        else: 
            BEST_SCORE_NUMBER = iii
            BEST_SCORE_REPEAT_COUNT = 0

        correct_ALPHA(iii)
        
        self.latest_[self.Cars[iii].Candy_score] = [w1_iii,w2_iii,b_iii]
        latest_sort = sorted(self.latest_)
        
        global BEST_SCORE_JJJ
        if (len(latest_sort)) > 1:
            if latest_sort[-1] == iii:
                goal_sort = latest_sort[-2]
            else:
                goal_sort = latest_sort[-1]
            BEST_SCORE_JJJ = goal_sort
            w1_kkk=self.latest_[goal_sort][0]
            w2_kkk=self.latest_[goal_sort][1]
            b_kkk=self.latest_[goal_sort][2]
        else:
            BEST_SCORE_JJJ = 0
            w1_kkk = self.Cars[jjj].AI.get_w1() 
            w2_kkk = self.Cars[jjj].AI.get_w2() 
            b_kkk = self.Cars[jjj].AI.get_b() 

        if len(latest_sort) > 3: self.latest_.pop(list(self.latest_)[0])
        
        if self.Cars[iii].Candy_score < 9 or BEST_SCORE_REPEAT_COUNT > 10:
            self.Cars.clear()
            for i in range(COUNT_CARS):
                self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))
                self.Cars[i].AI.refresh()
        else:
            self.Cars.clear()
            for i in range(COUNT_CARS):
                self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))
            count = 8
            for i in range(0, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w2_kkk, b_kkk], ALpha_)
            for i in range(1, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w2_kkk, b_kkk], ALpha_ * 2)
            for i in range(2, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w2_kkk, b_kkk], ALpha_ / 2)
            for i in range(3, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w1_iii, w2_kkk, w2_iii, b_kkk, b_iii], ALpha_)
            for i in range(4, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w1_iii, w2_kkk, w2_iii, b_kkk, b_iii], 0)
            for i in range(5, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_iii, w2_iii, b_iii], ALpha_)
            for i in range(6, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_iii, w2_iii, b_iii], ALpha_ / 2)
            for i in range(7, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w2_kkk, b_kkk], ALpha_ / 8)

    def car_mix_5(self):
        global SUM_TIME, GEN, BEST_SCORE_REPEAT_COUNT, BEST_SCORE_NUMBER
        SUM_TIME = 0
        GEN += 1
        iii, jjj = self.get_best_car()
        w1_iii = self.Cars[iii].AI.get_w1() 
        w2_iii = self.Cars[iii].AI.get_w2() 
        b_iii = self.Cars[iii].AI.get_b() 
        if BEST_SCORE_NUMBER == iii:
            BEST_SCORE_REPEAT_COUNT += 1
        else: 
            BEST_SCORE_NUMBER = iii
            BEST_SCORE_REPEAT_COUNT = 0

        correct_ALPHA(iii)
        
        self.latest_[self.Cars[iii].Candy_score] = [w1_iii,w2_iii,b_iii]
        latest_sort = sorted(self.latest_)
        
        global BEST_SCORE_JJJ
        if (len(latest_sort)) > 1:
            if latest_sort[-1] == iii:
                goal_sort = latest_sort[-2]
            else:
                goal_sort = latest_sort[-1]
            BEST_SCORE_JJJ = goal_sort
            w1_kkk=self.latest_[goal_sort][0]
            w2_kkk=self.latest_[goal_sort][1]
            b_kkk=self.latest_[goal_sort][2]
        else:
            BEST_SCORE_JJJ = 0
            w1_kkk = self.Cars[jjj].AI.get_w1() 
            w2_kkk = self.Cars[jjj].AI.get_w2() 
            b_kkk = self.Cars[jjj].AI.get_b() 

        if len(latest_sort) > 4: self.latest_.pop(list(self.latest_)[0])
        
        if self.Cars[iii].Candy_score < 9 or BEST_SCORE_REPEAT_COUNT > 10:
            self.Cars.clear()
            for i in range(COUNT_CARS):
                self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))
                self.Cars[i].AI.refresh()
        else:
            self.Cars.clear()
            for i in range(COUNT_CARS):
                self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))
            count = 8
            for i in range(0, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w2_kkk, b_kkk], ALpha_)
            for i in range(1, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w2_kkk, b_kkk], ALpha_ * 4)
            for i in range(2, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w2_kkk, b_kkk], ALpha_ / 2)
            for i in range(3, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w1_iii, w2_kkk, w2_iii, b_kkk, b_iii], ALpha_)
            for i in range(4, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w1_iii, w2_kkk, w2_iii, b_kkk, b_iii], ALpha_ * 4)
            for i in range(5, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_iii, w2_iii, b_iii], ALpha_)
            for i in range(6, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_iii, w2_iii, b_iii], ALpha_ * 4)
            for i in range(7, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w2_kkk, b_kkk], ALpha_ / 4)

    def car_mix_6(self):
        global SUM_TIME, GEN, BEST_SCORE_REPEAT_COUNT, BEST_SCORE_NUMBER
        SUM_TIME = 0
        GEN += 1
        iii, jjj = self.get_best_car()
        w1_iii = self.Cars[iii].AI.get_w1() 
        w2_iii = self.Cars[iii].AI.get_w2() 
        b_iii = self.Cars[iii].AI.get_b() 
        if BEST_SCORE_NUMBER == iii:
            BEST_SCORE_REPEAT_COUNT += 1
        else: 
            BEST_SCORE_NUMBER = iii
            BEST_SCORE_REPEAT_COUNT = 0

        correct_ALPHA(iii)
        
        self.latest_[self.Cars[iii].Candy_score] = [w1_iii,w2_iii,b_iii]
        latest_sort = sorted(self.latest_)
        
        global BEST_SCORE_JJJ
        if (len(latest_sort)) > 1:
            goal_sort = latest_sort[-1]
            BEST_SCORE_JJJ = goal_sort
            w1_kkk=self.latest_[goal_sort][0]
            w2_kkk=self.latest_[goal_sort][1]
            b_kkk=self.latest_[goal_sort][2]

            goal_sort = latest_sort[-2]
            w1_iii=self.latest_[goal_sort][0]
            w2_iii=self.latest_[goal_sort][1]
            b_iii=self.latest_[goal_sort][2]
        else:
            BEST_SCORE_JJJ = 0
            w1_kkk = self.Cars[jjj].AI.get_w1() 
            w2_kkk = self.Cars[jjj].AI.get_w2() 
            b_kkk = self.Cars[jjj].AI.get_b() 

        if len(latest_sort) > 4: self.latest_.pop(list(self.latest_)[0])
        
        if self.Cars[iii].Candy_score < 9 or BEST_SCORE_REPEAT_COUNT > 10:
            self.Cars.clear()
            for i in range(COUNT_CARS):
                self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))
                self.Cars[i].AI.refresh()
        else:
            self.Cars.clear()
            for i in range(COUNT_CARS):
                self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))
            count = 8
            for i in range(0, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w2_kkk, b_kkk], ALpha_)
            for i in range(1, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w2_kkk, b_kkk], ALpha_ * 5)
            for i in range(2, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w2_kkk, b_kkk], ALpha_ * 2)
            for i in range(3, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w1_iii, w2_kkk, w2_iii, b_kkk, b_iii], ALpha_)
            for i in range(4, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w1_iii, w2_kkk, w2_iii, b_kkk, b_iii], ALpha_ * 5)
            for i in range(5, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_iii, w2_iii, b_iii], ALpha_)
            for i in range(6, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_iii, w2_iii, b_iii], ALpha_ * 5)
            for i in range(7, COUNT_CARS, count):
                self.new_gen_car(self.Cars[i], [w1_kkk, w2_kkk, b_kkk], ALpha_ / 2)

    def car_mix_7(self):
        global SUM_TIME, GEN, BEST_SCORE_REPEAT_COUNT, BEST_SCORE_NUMBER
        SUM_TIME = 0
        GEN += 1
        selection_cars_par = self.get_best_car_tournament()
        # selection_cars_par = self.get_best_car_roulette()
        # selection_cars_par = self.get_best_car_mix()
        
        iii, jjj = self.get_best_car()
        
        w1_i = self.Cars[iii].AI.get_w1() 
        w2_i = self.Cars[iii].AI.get_w2() 
        b_i = self.Cars[iii].AI.get_b() 

        w1_j = self.Cars[jjj].AI.get_w1() 
        w2_j = self.Cars[jjj].AI.get_w2() 
        b_j = self.Cars[jjj].AI.get_b() 

        self.Cars.clear()
        for i in range(COUNT_CARS):
            self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))

        
        count = 9
        for i in range(0, COUNT_CARS, count):
            self.new_gen_car_cross(self.Cars[i], [selection_cars_par[2*i], selection_cars_par[2*i + 1]], type_cross= 'arifm', mutation= 1)
        for i in range(1, COUNT_CARS, count):
            self.new_gen_car_cross(self.Cars[i], [selection_cars_par[2*i], selection_cars_par[2*i + 1]], type_cross= 'blx', mutation= 1)
        for i in range(2, COUNT_CARS, count):
            self.new_gen_car_cross(self.Cars[i], [selection_cars_par[2*i], selection_cars_par[2*i + 1]], type_cross= 'arifm', mutation= 1)
        for i in range(3, COUNT_CARS, count):
            self.new_gen_car_cross(self.Cars[i], [selection_cars_par[2*i], selection_cars_par[2*i + 1]], type_cross= 'blx', mutation= 1)
        for i in range(4, COUNT_CARS, count):
            self.new_gen_car_cross(self.Cars[i], [selection_cars_par[2*i], selection_cars_par[2*i + 1]], type_cross= 'arifm', mutation= 1)
        for i in range(5, COUNT_CARS, count):
            self.new_gen_car_cross(self.Cars[i], [selection_cars_par[2*i], selection_cars_par[2*i + 1]], type_cross= 'blx', mutation= 1)
        for i in range(6, COUNT_CARS, count):
            self.new_gen_car_cross(self.Cars[i], [selection_cars_par[2*i], selection_cars_par[2*i + 1]], type_cross= 'arifm', mutation= 1)
        for i in range(7, COUNT_CARS, count):
            self.new_gen_car_cross(self.Cars[i], [selection_cars_par[2*i], selection_cars_par[2*i + 1]], type_cross= 'blx', mutation= 1)
        for i in range(8, COUNT_CARS, count):
            self.new_gen_car_cross(self.Cars[i], [selection_cars_par[2*i], selection_cars_par[2*i + 1]], type_cross= 'arifm', mutation= 1)

        self.new_gen_car_cross(self.Cars[-1], [[w1_i,w2_i,b_i], [w1_i,w2_i,b_i]], type_cross= 'mix', mutation= 0)
        self.new_gen_car_cross(self.Cars[-2], [[w1_j,w2_j,b_j], [w1_j,w2_j,b_j]], type_cross= 'mix', mutation= 0)

    def car_mix_8(self):
        global SUM_TIME, GEN, BEST_SCORE_REPEAT_COUNT, BEST_SCORE_NUMBER
        SUM_TIME = 0
        GEN += 1
        selection_cars_par = self.get_best_car_tournament()
        # selection_cars_par = self.get_best_car_roulette()
        # selection_cars_par = self.get_best_car_mix()
        
        iii, jjj = self.get_best_car()
        
        w1_i = self.Cars[iii].AI.get_w1() 
        w2_i = self.Cars[iii].AI.get_w2() 
        b_i = self.Cars[iii].AI.get_b() 

        w1_j = self.Cars[jjj].AI.get_w1() 
        w2_j = self.Cars[jjj].AI.get_w2() 
        b_j = self.Cars[jjj].AI.get_b() 

        self.Cars.clear()
        for i in range(COUNT_CARS):
            self.Cars.append (Car(CAR_START_X, CAR_START_Y, 0.08))

        
        for i in range(COUNT_CARS):
            sum = 0
            flag_while = True
            while flag_while:
                tmp = i % 10
                tmp = tmp % 5
                mut = 1 if tmp == 0 else 1/4 if tmp == 1 else 1/10 if tmp == 2 else 1/15 if tmp == 3 else 1/20 ##################################################################
                # mut = 4
                self.new_gen_car_cross(self.Cars[i], [selection_cars_par[2*i], selection_cars_par[2*i + 1]], type_cross= 'arifm' if i % 2 == 0 else 'blx', mutation = mut)
                
                if i==0: break

                w1_iii = self.Cars[i].AI.get_w1() 
                w2_iii = self.Cars[i].AI.get_w2() 
                b_iii = self.Cars[i].AI.get_b() 
                flag_while = False
                for j in range(i):
                    w1_jjj = self.Cars[j].AI.get_w1() 
                    w2_jjj = self.Cars[j].AI.get_w2() 
                    b_jjj = self.Cars[j].AI.get_b() 
                    w1_k = w1_iii - w1_jjj
                    w2_k = w2_iii - w2_jjj
                    b_k = b_iii - b_jjj
                    sum = w1_k.sum() / w1_k.size + w2_k.sum() / w2_k.size + b_k.sum() / b_k.size
                    if math.fabs(sum) < 0.001:
                        flag_while = True
                        break 


        self.new_gen_car_cross(self.Cars[-1], [[w1_i,w2_i,b_i], [w1_i,w2_i,b_i]], type_cross= 'mix', mutation= 0)
        self.new_gen_car_cross(self.Cars[-2], [[w1_j,w2_j,b_j], [w1_j,w2_j,b_j]], type_cross= 'mix', mutation= 0)


    def add_best_car(self):
        iii, jjj = self.get_best_car()
        w1 = self.Cars[iii].AI.get_w1() 
        w2 = self.Cars[iii].AI.get_w2() 
        b = self.Cars[iii].AI.get_b() 
        self.new_gen_car_cross(self.Cars[-1], [[w1,w2,b], [w1,w2,b]], type_cross= 'mix', mutation= 0)
        w1 = self.Cars[jjj].AI.get_w1() 
        w2 = self.Cars[jjj].AI.get_w2() 
        b = self.Cars[jjj].AI.get_b() 
        self.new_gen_car_cross(self.Cars[-1], [[w1,w2,b], [w1,w2,b]], type_cross= 'mix', mutation= 0)

    def new_gen_car(self, car: Car, w12b, AL):
        if len(w12b) == 3:
            car.AI.set_w1(w12b[0])
            car.AI.set_w2(w12b[1])
            car.AI.set_b(w12b[2])
        elif len(w12b) == 6:
            car.AI.set_mix_w1(w12b[0], w12b[1])
            car.AI.set_mix_w2(w12b[2], w12b[3])
            car.AI.set_mix_b(w12b[4], w12b[5])
        if AL != 0:
            car.AI.mix_w1_AL(AL)
            car.AI.mix_w2_AL(AL)
            car.AI.mix_b_AL(AL)

    def new_gen_car_cross(self, car: Car, w12b, type_cross = 'cross', mutation = 0):
        if type_cross == 'mix':
            car.AI.set_mix_w1(w12b[0][0], w12b[1][0])
            car.AI.set_mix_w2(w12b[0][1], w12b[1][1])
            car.AI.set_mix_b(w12b[0][2], w12b[1][2])
        else:
            car.AI.set_cross_w1(w12b[0][0], w12b[1][0], type=type_cross)
            car.AI.set_cross_w2(w12b[0][1], w12b[1][1], type=type_cross)
            car.AI.set_cross_b(w12b[0][2], w12b[1][2], type=type_cross)
    
        if not mutation:
            car.AI.mutation_w1(ALPHA_mutation)
            car.AI.mutation_w2(ALPHA_mutation)
            car.AI.mutation_b(ALPHA_mutation)
        else:
            car.AI.mutation_w1(mutation)
            car.AI.mutation_w2(mutation)
            car.AI.mutation_b(mutation)

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
        
        # if not CAR.vision_points_OLD : CAR.vision_points_OLD = CAR.vision_points
        for i in range(len(CAR.vision_points)):
            if CAR.vision_points[i] == False : CAR.vision_points[i] = CAR.vision_points_OLD[i]

            CAR.vision_points_distance.append(math.sqrt ((CAR.center_x - CAR.vision_points[i][0])**2 + (CAR.center_y - CAR.vision_points[i][1])**2))

        # CAR.vision_points_distance = list(map(lambda x: x - 15, CAR.vision_points_distance))
        # CAR.vision_points_distance = list(map(lambda x: 1 if x < 1 else 400 if x > 400 else x, CAR.vision_points_distance))
        # CAR.vision_points_distance = list(map(lambda x: math.sqrt(x), CAR.vision_points_distance))
        minim = 20 #
        maxim = 1000 #
        # global TMP_MAX, TMP_MIN

        CAR.vision_points_distance_standart = list(map(lambda x: (x - minim) / (maxim - minim),CAR.vision_points_distance))
        # if TMP_MIN>min(CAR.vision_points_distance_standart): TMP_MIN = min(CAR.vision_points_distance_standart)
        # if TMP_MAX<max(CAR.vision_points_distance_standart): TMP_MAX = max(CAR.vision_points_distance_standart)
        # print(TMP_MAX, TMP_MIN)
        CAR.vision_points_OLD = CAR.vision_points.copy()

    def on_key_press(self, symbol, modifiers):

        global MAX_TIME
        global TMP
        

        if symbol == arcade.key.O:
            # global FRICTION_ROT
            MAX_TIME += 1
            TMP += 1


        if symbol == arcade.key.P:
            # global FRICTION_ROT
            MAX_TIME -= 1
            TMP -= 1

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
        j=0
        for i in self.Cars:
            if not i.remove_flag:
                j+=1
        for i in self.Cars:
            if not i.remove_flag:
                return True
        return False

    def get_best_car(self):
        global BEST_SCORE
        max = 0
        iii = 0
        
        for i in range(len(self.Cars)):
            if self.Cars[i].Candy_score > max:
                max = self.Cars[i].Candy_score
                iii = i
        BEST_SCORE = max

        max = 0
        jjj = 0
        
        for j in range(len(self.Cars)):
            if j != iii and self.Cars[j].Candy_score > max:
                max = self.Cars[j].Candy_score
                jjj = j
        return iii, jjj

    def get_best_car_tournament(self):
        selection_cars = []
        for i in range(2 * len(self.Cars)):
            tournament_list = random.sample(self.Cars, 3)
            max = -10
            for j in range(len(tournament_list)):
                if tournament_list[j].Candy_score > max:
                    max = tournament_list[j].Candy_score
                    iii = j
            selection_cars.append([tournament_list[iii].AI.get_w1(), tournament_list[iii].AI.get_w2(), tournament_list[iii].AI.get_b()])
        return selection_cars

    def get_best_car_roulette(self):
        selection_cars = []
        SUM_candy_score = 0 
        SUM_find = 0
        for i in self.Cars:
            SUM_candy_score += i.Candy_score
        
        if SUM_candy_score < COUNT_CARS * 2: return self.get_best_car_tournament()

        for k in range(2):
            for j in self.Cars:
                P = random.random()
                for i in self.Cars:
                    if SUM_find < P and SUM_find + i.Candy_score / SUM_candy_score > P:
                        selection_cars.append([j.AI.get_w1(), j.AI.get_w2(), j.AI.get_b()])
                        break
                    else: 
                        SUM_find += i.Candy_score / SUM_candy_score
                SUM_find = 0
        return selection_cars

    def get_best_car_mix(self):
        selection_cars = []
        SUM_candy_score = 0 
        SUM_find = 0
        for i in self.Cars:
            SUM_candy_score += i.Candy_score
        
        for j in self.Cars:
            P = random.random()
            for i in self.Cars:
                if SUM_find < P and SUM_find + i.Candy_score / SUM_candy_score > P:
                    selection_cars.append([j.AI.get_w1(), j.AI.get_w2(), j.AI.get_b()])
                    break
                else: 
                    SUM_find += i.Candy_score / SUM_candy_score
            SUM_find = 0

        for i in range(len(self.Cars)):
            tournament_list = random.sample(self.Cars, 5)
            max = -10
            for j in range(len(tournament_list)):
                if tournament_list[j].Candy_score > max:
                    max = tournament_list[j].Candy_score
                    iii = j
            selection_cars.append([tournament_list[iii].AI.get_w1(), tournament_list[iii].AI.get_w2(), tournament_list[iii].AI.get_b()])
        
        return selection_cars


    def death(self):
        return Car(CAR_START_X, CAR_START_Y, 0.08)


def correct_ALPHA(a):
    global ALpha_
    if a < 100:
        ALpha_ = 10
    elif a < 200:
        ALpha_ = 15
    elif a < 300:
        ALpha_ = 20
    elif a < 400:
        ALpha_ = 35
    elif a < 500:
        ALpha_ = 50
    elif a < 600:
        ALpha_ = 75
    elif a < 700:
        ALpha_ = 90
    elif a < 800:
        ALpha_ = 110
    elif a < 900:
        ALpha_ = 130
    elif a < 1000:
        ALpha_ = 150
    elif a < 1200:
        ALpha_ = 200
    elif a < 1400:
        ALpha_ = 300


# Main code entry point
if __name__ == "__main__":
    app = Welcome()
    arcade.run()

