
import math
import random
import arcade
import numpy as np 
from read_map import track, read_track
from read_candy import read_candy
from intersection import line_intersection, line_intersection_car, shape_intersection_car_AI, GPT_line_intersection_car
import os
from read_par import read_par
from constans import *
from linalg import *
from neuralnetwork import NNetwork


class Car (arcade.Sprite):
    def __init__(self, x, y, scale) -> None:
        super().__init__("images/car.png", scale, hit_box_algorithm='None', )
        # self.model = NNetwork(AI_INPUT_SHAPE, AI_MIDDLE_SHAPE, AI_MIDDLE_SHAPE, AI_OUTPUT_SHAPE)
        self.model = NNetwork(AI_INPUT_SHAPE, AI_MIDDLE_SHAPE, AI_OUTPUT_SHAPE)
        global LENGTH_CHROM
        LENGTH_CHROM = NNetwork.getTotalWeights(AI_INPUT_SHAPE, AI_MIDDLE_SHAPE, AI_OUTPUT_SHAPE)
        # LENGTH_CHROM = NNetwork.getTotalWeights(AI_INPUT_SHAPE, AI_MIDDLE_SHAPE, AI_MIDDLE_SHAPE, AI_OUTPUT_SHAPE)
        # print (LENGTH_CHROM)
        self.stop_time = 0
        self.left_time = 0
        self.right_time = 0
        self.Candy_score = 0

        self.life_time = 1
        self.set_W = False

        self.alpha = 100
        
        self.Candy = Candy()
        self.Track = Track()
        
        self.center_y = y
        self.center_x = x
        self.angle = START_ANGLE
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
        self.state = []
        self.action = []
        
        self.F_traction = np.array([1, 0]) 
        self.F_drag = np.array([1, 0]) 
        self.F_rr = np.array([1, 0]) 
        self.F_long = np.array([1, 0]) 
        
        self.direct = np.array(START_DIRECT) 
        self.acc = np.array([0., 0.]) 
        self.vel = np.array([0., 0.]) 
        self.pos = np.array([x, y]) 

        self.start_x = self.center_x
        self.start_y = self.center_y
        self.start_angle = self.angle
        self.start_direct = self.direct

        self.vision_vec =  [self.direct, rotate_Vec(self.direct, 30), rotate_Vec(self.direct, 90), rotate_Vec(self.direct, -30), rotate_Vec(self.direct, -90)]
        self.vision_vec_correct =  [self.width / 2, 0.5 * (self.height ** 2 + self.width ** 2) ** 0.5 , self.height / 2, 0.5 * (self.height ** 2 + self.width ** 2) ** 0.5, self.height / 2]
        # self.vision_vec =  [rotate_Vec(self.direct, 90), rotate_Vec(self.direct, 45), self.direct, rotate_Vec(self.direct, 315), rotate_Vec(self.direct, 270)]
        # self.vision_vec =  [self.direct, rotate_Vec(self.direct, 45), rotate_Vec(self.direct, 315)]
        

    def draw (self):
        super().draw()
        self.draw_hit_box()

        for j in self.vision_points:
            if j:
                arcade.draw_circle_filled(j[0], j[1], 10, arcade.color.WHITE)

        arcade.draw_line(self.center_x, self.center_y, self.center_x + self.vel[0], self.center_y + self.vel[1], arcade.color.BLACK, 2)
        vec_right_drift = self.vel.dot(rotate_Vec(self.direct, 90)) * rotate_Vec(self.direct, 90) / len_vec (self.direct)
        arcade.draw_line(self.center_x, self.center_y, self.center_x + vec_right_drift[0], self.center_y + vec_right_drift[1], arcade.color.BLACK, 2)
        vec_left_drift = self.vel.dot(rotate_Vec(self.direct, -90)) * rotate_Vec(self.direct, -90) / len_vec (self.direct)
        arcade.draw_line(self.center_x, self.center_y, self.center_x + vec_left_drift[0], self.center_y + vec_left_drift[1], arcade.color.BLACK, 2)

        next_candy_center = np.array([self.Candy.Candy[0][0][0] + (self.Candy.Candy[0][1][0] - self.Candy.Candy[0][0][0]) / 2 , self.Candy.Candy[0][0][1] + (self.Candy.Candy[0][1][1] - self.Candy.Candy[0][0][1]) / 2] )
        next_candy_center[0] -= self.center_x
        next_candy_center[1] -= self.center_y
        vec_NextGate = - self.direct + next_candy_center

        arcade.draw_line(self.center_x, self.center_y, self.center_x + vec_NextGate[0], self.center_y + vec_NextGate[1], arcade.color.BLACK, 2)
        
        self.Candy.draw()


    # def update(self, delta_time):     
    #     self.state = self.car_vision()
    #     self.AI_update(2)
    #     self.car_phys(delta_time)

        
    #     self.vision_vec =  [self.direct, rotate_Vec(self.direct, 30), rotate_Vec(self.direct, 90), rotate_Vec(self.direct, 150), rotate_Vec(self.direct, 180), rotate_Vec(self.direct, -30), rotate_Vec(self.direct, -90), rotate_Vec(self.direct, -150)]
    #     # self.vision_vec =  [self.direct, rotate_Vec(self.direct, 45), rotate_Vec(self.direct, 90), rotate_Vec(self.direct, 135), rotate_Vec(self.direct, 180), rotate_Vec(self.direct, 225), rotate_Vec(self.direct, 270), rotate_Vec(self.direct, 315)]
    #     # self.vision_vec =  [rotate_Vec(self.direct, 90), rotate_Vec(self.direct, 45), self.direct, rotate_Vec(self.direct, 315), rotate_Vec(self.direct, 270)]
    #     # self.vision_vec =  [self.direct, rotate_Vec(self.direct, 45), rotate_Vec(self.direct, 315)]
        
 
    #     if line_intersection_car(self.get_adjusted_hit_box(), self.Candy.Candy[0]):
            
    #         self.Candy_score += 1######################################################################################################
    #         self.Candy.Candy.pop(0)
    #         global SUM_TIME
    #         if len(self.Candy.Candy) == 0:
    #             self.Candy.refresh()
        
    def check_crush(self):
        if not self.remove_flag:
            # if GPT_line_intersection_car(self.get_adjusted_hit_box(), self.Track.track[0]) or GPT_line_intersection_car(self.get_adjusted_hit_box(), self.Track.track[1]):
            if line_intersection_car(self.get_adjusted_hit_box(), self.Track.track[0]) or line_intersection_car(self.get_adjusted_hit_box(), self.Track.track[1]):
                self.remove_flag = True
                # self.Candy_score -= 100
        

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
            # self.R = self.L / math.sin(self.wheel_rot) 
            self.angle += self.wheel_rot
            self.direct = ang_to_Vec(self.angle)
        else: 
            pass
            # self.R = math.inf
        self.direct = ang_to_Vec(self.angle)
        self.F_drag = - C_DRAG * len_vec(self.vel) * self.vel
        self.F_rr = - C_RR * self.vel
        self.F_long = self.F_traction + self.F_drag + self.F_rr

        self.acc = self.F_long / MASS
        self.vel += self.acc * delta_time
        if self.vel.dot(self.direct)<0 : self.vel = self.vel.dot(rotate_Vec(self.direct, 90)) * rotate_Vec(self.direct, 90) / len_vec(self.direct)
        if len_vec(self.vel) > MAX_SPEED : self.vel = MAX_SPEED * self.vel / len_vec(self.vel)
        self.pos += self.vel * delta_time
        self.center_x = self.pos[0]
        self.center_y = self.pos[1]

    def AI_update(self, actionNo):
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        
        if actionNo == 0:
            self.left_pressed = True
        elif actionNo == 1:
            self.right_pressed = True
        elif actionNo == 2:
            self.up_pressed = True
        elif actionNo == 3:
            self.up_pressed = True
            self.left_pressed = True
        elif actionNo == 4:
            self.up_pressed = True
            self.right_pressed = True
        elif actionNo == 5:
            pass

        if actionNo == 2 or actionNo == 3 or actionNo == 4:
            self.stop_time = 0
        else:
            self.stop_time += 1

        if self.stop_time > 50:
            self.remove_flag = True
            self.Candy_score -= 100

        if actionNo == 0 or actionNo == 1:
            self.left_time += 1
        else:
            self.left_time = 0

        if self.left_time > 50:
            self.remove_flag = True
            self.Candy_score -= 100            



    def car_vision(self):
        self.vision_points.clear()
        self.vision_points_distance.clear()
        for i in self.vision_vec:
            segment = [[self.center_x, self.center_y], [self.center_x + 3000 * i[0], self.center_y + 3000 * i[1]]]
            point_1 = line_intersection(segment, self.Track.track[0])
            # point_1 = GPT_line_intersection_car(segment, self.Track.track[0])
            point_2 = line_intersection(segment, self.Track.track[1])
            # point_2 = GPT_line_intersection_car(segment, self.Track.track[1])
            if not point_1 or not point_2:
                self.vision_points.append(point_1 or point_2) 
            elif (self.center_x - point_1[0])**2 + (self.center_y - point_1[1])**2 <= (self.center_x - point_2[0])**2 + (self.center_y - point_2[1])**2: self.vision_points.append(point_1)
            elif (self.center_x - point_1[0])**2 + (self.center_y - point_1[1])**2 > (self.center_x - point_2[0])**2 + (self.center_y - point_2[1])**2: self.vision_points.append(point_2)
            
        if not self.vision_points_OLD : self.vision_points_OLD = self.vision_points
        for i in range(len(self.vision_points)):
            if self.vision_points[i] == False : self.vision_points_distance.append(300)
            else: self.vision_points_distance.append(math.sqrt ((self.center_x - self.vision_points[i][0])**2 + (self.center_y - self.vision_points[i][1])**2))
        
        self.correct_vision_distance()
        self.vision_points_distance_standart = [(min(300, line) / 300) for line in self.vision_points_distance]

        normalizedForwardVelocity = len_vec(self.vel) / MAX_SPEED
        
        if self.vel.dot(rotate_Vec(self.direct, 90)) > 0:
            normalizedPosDrift = min(self.vel.dot(rotate_Vec(self.direct, 90)), 300) / 300
            normalizedNegDrift = 0
        elif self.vel.dot(rotate_Vec(self.direct, 90)) < 0:
            normalizedPosDrift = 0
            normalizedNegDrift = -min(self.vel.dot(rotate_Vec(self.direct, 90)), 300) / 300
        else:
            normalizedPosDrift = 0
            normalizedNegDrift = 0


        # next_candy_center = np.array([self.Candy.Candy[0][0][0] + (self.Candy.Candy[0][1][0] - self.Candy.Candy[0][0][0]) / 2 , self.Candy.Candy[0][0][1] + (self.Candy.Candy[0][1][1] - self.Candy.Candy[0][0][1]) / 2] )
        # next_candy_center[0] -= self.center_x
        # next_candy_center[1] -= self.center_y
        # normalizedAngleOfNextGate = math.fabs(180 + Vec_to_ang(self.direct) - Vec_to_ang(next_candy_center)) % 360

        # normalizedAngleOfNextGate /= 360
        # print(self.vision_points_distance_standart[4])
        normalizedState = [*self.vision_points_distance_standart, normalizedForwardVelocity,
                           normalizedPosDrift, normalizedNegDrift]#, normalizedAngleOfNextGate]
        return np.reshape(np.array(normalizedState), (1, AI_INPUT_SHAPE))

    def correct_vision_distance(self):
        for i in range(len(self.vision_vec_correct)):
            self.vision_points_distance[i] -= self.vision_vec_correct[i]

    def set_zero_point(self):
        self.center_x = self.start_x
        self.center_y = self.start_y
        self.angle = self.start_angle
        self.direct = self.start_direct
        self.Candy_score = 0
        self.Candy = Candy()
        self.set_W = False
        self.life_time = 1
        self.wheel_rot = 0
        self.state = []
        self.remove_flag = False
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.acc = np.array([0., 0.]) 
        self.vel = np.array([0., 0.])
        self.pos = np.array([self.center_x, self.center_y]) 
        self.vision_vec =  [self.direct, rotate_Vec(self.direct, 30), rotate_Vec(self.direct, 90), rotate_Vec(self.direct, -30), rotate_Vec(self.direct, -90)]

        # self.vision_vec =  [self.direct, rotate_Vec(self.direct, 30), rotate_Vec(self.direct, 90), rotate_Vec(self.direct, 150), rotate_Vec(self.direct, 180), rotate_Vec(self.direct, -30), rotate_Vec(self.direct, -90), rotate_Vec(self.direct, -150)]





class Candy ():
    def __init__(self):
        self.Candy = read_candy()

    def draw(self):
        global TMP
        for i in range (0, len(self.Candy)):
            arcade.draw_line_strip(self.Candy[i], arcade.color.GREEN)

    def refresh(self):
        self.Candy = read_candy()

    def __del__(self):
        del self.Candy


class Track ():
    def __init__(self):
        self.track = read_track()

    def draw(self):
        arcade.draw_line_strip(track[0], arcade.color.BLACK)
        arcade.draw_line_strip(track[1], arcade.color.BLACK)

