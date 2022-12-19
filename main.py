
import math
import arcade
import numpy as np 
from read_map import track, read_track
from read_candy import read_candy
from variable import line_intersection
from ai_np import AI

# Imports


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


ENGINEFORCE = 1600000
BRAKINGFORCE = ENGINEFORCE / 10
C_DRAG = 0.7
C_RR = 3000
MASS = 900
WHEEL_ROT_PER_SEC = 0.5 * 60
WHEEL_ROT_MAX = 5

COUNT_CARS = 8

MAX_TIME = 5
SUM_TIME = 0

GEN = 0
BEST_SCORE = 0

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
        self.Candy_score = 0
        self.center_y = y
        self.center_x = x
        self.angle = 270

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
        
        self.direct = np.array([0, -1]) 
        self.acc = np.array([0., 0.]) 
        self.vel = np.array([0., 0.]) 
        self.pos = np.array([x, y]) 
        self.F_res_a = np.array([0., 0.])

        self.vision_vec =  [self.direct, self.rotate_Vec(self.direct, 45), self.rotate_Vec(self.direct, 90), self.rotate_Vec(self.direct, 135), self.rotate_Vec(self.direct, 180), self.rotate_Vec(self.direct, 225), self.rotate_Vec(self.direct, 270), self.rotate_Vec(self.direct, 315)]
        
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

        
        self.vision_vec =  [self.direct, self.rotate_Vec(self.direct, 45), self.rotate_Vec(self.direct, 90), self.rotate_Vec(self.direct, 135), self.rotate_Vec(self.direct, 180), self.rotate_Vec(self.direct, 225), self.rotate_Vec(self.direct, 270), self.rotate_Vec(self.direct, 315)]
 
 
        if line_intersection(self.get_adjusted_hit_box(), self.Candy.Candy[0]):
             
            self.Candy_score += 1
            self.Candy.Candy.pop(0)

            if len(self.Candy.Candy) == 0:
                self.Candy.refresh()

        self.AI_update()
        
    def AI_update(self):
        self.AI.set_x(self.vision_points_distance_standart)
        z = self.AI.calc()
        if z[0]:
            self.up_pressed = True
        else:  
            self.up_pressed = False
        
        if z[1]:
            self.right_pressed = True
        else:  
            self.right_pressed = False

        if z[2]:
            self.left_pressed = True
        else:  
            self.left_pressed = False

        # if not self.up_pressed:
        #     self.Candy_score -= 1/30

        # if z[3]:
        #     self.down_pressed = True
        # else:  
        #     self.down_pressed = False



        



    

        

        
        
        
         

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
        for i in self.Candy:
            arcade.draw_line_strip(i, arcade.color.GREEN)

    def refresh(self):
        self.Candy = read_candy()

    def __del__(self):
        del self.Candy


        






# Classes
class Welcome(arcade.Window):
    def __init__(self):

        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        


        # Set the background window
        arcade.set_background_color(arcade.color.GRAY)
        # self.Car = Car(120, SCREEN_HEIGHT / 2, 0.08)
        self.Cars = []
        for i in range(COUNT_CARS):
            self.Cars.append (Car(120, 580.0, 0.08))
            
        self.Track = Track()

        

        


    def on_draw(self):
        self.clear()
        for i in self.Cars:
            if not i.remove_flag:
                i.draw()    
        # self.Car.draw()
        
        
        self.Track.draw()
        arcade.draw_text(f"GEN: {GEN}", 10, 50, arcade.color.BLACK)
        arcade.draw_text(f"BEST SCORE: {BEST_SCORE}", 10, 70, arcade.color.BLACK)
        arcade.draw_text(f"TIME CUR GEN: {SUM_TIME}", 10, 90, arcade.color.BLACK)
        arcade.draw_text(f"MAX TIME: {MAX_TIME}", 10, 110, arcade.color.BLACK)
        

    def on_update(self, delta_time: float = 1 / 60):
        for i in self.Cars:
            if not i.remove_flag:
                self.car_vision(i)
                i.update(delta_time)

        for i in self.Cars:
            if not i.remove_flag:
                if line_intersection(i.get_adjusted_hit_box(), self.Track.track[0]) or line_intersection(i.get_adjusted_hit_box(), self.Track.track[1]):
                    i.remove_flag = True
                    # i.Candy_score *= 3/4
        global SUM_TIME
        global MAX_TIME
        global GEN
        SUM_TIME += delta_time

        if not self.is_Cars_dead() or SUM_TIME > MAX_TIME:
            iii, jjj = self.get_best_car()
            print (self.Cars[iii].Candy_score, self.Cars[jjj].Candy_score)
            SUM_TIME = 0
            GEN += 1
            w1_iii = self.Cars[iii].AI.get_w1() 
            w2_iii = self.Cars[iii].AI.get_w2() 
            b_iii = self.Cars[iii].AI.get_b() 
            
            w1_jjj = self.Cars[jjj].AI.get_w1() 
            w2_jjj = self.Cars[jjj].AI.get_w2() 
            b_jjj = self.Cars[jjj].AI.get_b() 
            print (w1_iii, w1_jjj)
            self.Cars = []
            for i in range(COUNT_CARS):
                self.Cars.append (Car(120, 580.0, 0.08))
            for i in range(0, COUNT_CARS, 4):
                self.Cars[i].AI.set_w1(w1_iii)
                self.Cars[i].AI.set_w2(w2_iii)
                self.Cars[i].AI.set_b(b_iii)

                self.Cars[i].AI.mix_w1()
                self.Cars[i].AI.mix_w2()
                self.Cars[i].AI.mix_b()
            for i in range(1, COUNT_CARS, 4):
                self.Cars[i].AI.set_w1(w1_jjj)
                self.Cars[i].AI.set_w2(w2_jjj)
                self.Cars[i].AI.set_b(b_jjj)

                self.Cars[i].AI.mix_w1()
                self.Cars[i].AI.mix_w2()
                self.Cars[i].AI.mix_b()
            for i in range(2, COUNT_CARS, 4):
                self.Cars[i].AI.set_mix_w1(w1_iii, w1_jjj)
                self.Cars[i].AI.set_mix_w2(w2_iii, w2_jjj)
                self.Cars[i].AI.set_mix_b(b_iii, b_jjj)

                # self.Cars[i].AI.mix_lit_w1()
                # self.Cars[i].AI.mix_lit_w2()
                # self.Cars[i].AI.mix_lit_b()
                self.Cars[i].AI.mix_w1()
                self.Cars[i].AI.mix_w2()
                self.Cars[i].AI.mix_b()
            for i in range(3, COUNT_CARS, 4):
                self.Cars[i].AI.set_mix_w1(w1_iii, w1_jjj)
                self.Cars[i].AI.set_mix_w2(w2_iii, w2_jjj)
                self.Cars[i].AI.set_mix_b(b_iii, b_jjj)
            
            # if GEN > 5 and self.Cars[iii].Candy_score < 5:
            #     for i in range(COUNT_CARS):
            #         self.Cars[i].AI.refresh()
                
        


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

        minim = min(CAR.vision_points_distance)
        maxim = max(CAR.vision_points_distance)
        CAR.vision_points_distance_standart = list(map(lambda x: (x - minim) / (maxim - minim),CAR.vision_points_distance))

        CAR.vision_points_OLD = CAR.vision_points.copy()

    def on_key_press(self, symbol, modifiers):

        global MAX_TIME
        

        if symbol == arcade.key.O:
            # global FRICTION_ROT
            MAX_TIME += 1

        if symbol == arcade.key.P:
            # global FRICTION_ROT
            MAX_TIME -= 1

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

    # def is_Cars_stop(self):
    #     for i in self.Cars:
    #         if not i.remove_flag:
    #             return True
    #     return False

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
        
        for i in range(len(self.Cars)):
            if i != iii and self.Cars[i].Candy_score > max:
                max = self.Cars[i].Candy_score
                jjj = i
        return iii, jjj

    def death(self):
        return Car(120, SCREEN_HEIGHT / 2, 0.08)



# Main code entry point
if __name__ == "__main__":
    app = Welcome()
    arcade.run()

