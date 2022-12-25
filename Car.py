
import math
import random
import arcade
import numpy as np 
from read_map import track, read_track
from read_candy import read_candy
from intersection import line_intersection, line_intersection_car
import os
from read_par import read_par
from constans import *
from linalg import *
from neuralnetwork import NNetwork


class Car (arcade.Sprite):
    def __init__(self, x, y, scale) -> None:
        super().__init__("images/car.png", scale, hit_box_algorithm='None', )
        self.model = NNetwork(AI_INPUT_SHAPE, AI_MIDDLE_SHAPE, AI_OUTPUT_SHAPE)
        global LENGTH_CHROM
        LENGTH_CHROM = NNetwork.getTotalWeights(AI_INPUT_SHAPE, AI_MIDDLE_SHAPE, AI_OUTPUT_SHAPE)
        self.stop_time = 0
        self.left_time = 0
        self.right_time = 0
        self.Candy_score = 1

        self.alpha = 100
        
        self.Candy = Candy()
        self.Track = Track()
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
        self.state = []
        
        self.F_traction = np.array([1, 0]) 
        self.F_drag = np.array([1, 0]) 
        self.F_rr = np.array([1, 0]) 
        self.F_long = np.array([1, 0]) 
        
        self.direct = np.array([1, 0]) 
        self.acc = np.array([0., 0.]) 
        self.vel = np.array([0., 0.]) 
        self.pos = np.array([x, y]) 

        self.vision_vec =  [self.direct, rotate_Vec(self.direct, 30), rotate_Vec(self.direct, 90), rotate_Vec(self.direct, 150), rotate_Vec(self.direct, 180), rotate_Vec(self.direct, -30), rotate_Vec(self.direct, -90), rotate_Vec(self.direct, -150)]
        # self.vision_vec =  [rotate_Vec(self.direct, 90), rotate_Vec(self.direct, 45), self.direct, rotate_Vec(self.direct, 315), rotate_Vec(self.direct, 270)]
        # self.vision_vec =  [self.direct, rotate_Vec(self.direct, 45), rotate_Vec(self.direct, 315)]
        

    def draw (self):
        super().draw()
        # self.draw_hit_box()

        # for j in self.vision_points:
        #     if j:
        #         arcade.draw_circle_filled(j[0], j[1], 10, arcade.color.WHITE)
        
        # self.Candy.draw()


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
            if line_intersection_car(self.get_adjusted_hit_box(), self.Track.track[0]) or line_intersection_car(self.get_adjusted_hit_box(), self.Track.track[1]):
                self.remove_flag = True
                self.Candy_score -= 100
        

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
            self.down_pressed = True
        elif actionNo == 4:
            self.up_pressed = True
            self.left_pressed = True
        elif actionNo == 5:
            self.up_pressed = True
            self.right_pressed = True
        elif actionNo == 6:
            self.down_pressed = True
            self.left_pressed = True
        elif actionNo == 7:
            self.down_pressed = True
            self.right_pressed = True
        elif actionNo == 8:
            pass

    def car_vision(self):
        self.vision_points.clear()
        self.vision_points_distance.clear()
        for i in self.vision_vec:
            segment = [[self.center_x, self.center_y], [self.center_x + 300 * i[0], self.center_y + 300 * i[1]]]
            point_1 = line_intersection(segment, self.Track.track[0])
            point_2 = line_intersection(segment, self.Track.track[1])
            if not point_1 or not point_2:
                self.vision_points.append(point_1 or point_2) 
            elif (self.center_x - point_1[0])**2 + (self.center_y - point_1[1])**2 < (self.center_x - point_2[0])**2 + (self.center_y - point_2[1])**2: self.vision_points.append(point_1)
            elif (self.center_x - point_1[0])**2 + (self.center_y - point_1[1])**2 > (self.center_x - point_2[0])**2 + (self.center_y - point_2[1])**2: self.vision_points.append(point_2)
        
        if not self.vision_points_OLD : self.vision_points_OLD = self.vision_points
        for i in range(len(self.vision_points)):
            if self.vision_points[i] == False : self.vision_points_distance.append(300)
            else: self.vision_points_distance.append(math.sqrt ((self.center_x - self.vision_points[i][0])**2 + (self.center_y - self.vision_points[i][1])**2))

        self.vision_points_distance_standart = [1 - (max(1.0, line) / 300) for line in self.vision_points_distance]

        normalizedForwardVelocity = max(0.0, len_vec(self.vel) / MAX_SPEED)
        normalizedReverseVelocity = 0
        
        if self.vel.dot(rotate_Vec(self.direct, 90)) > 0:
            normalizedPosDrift = min(self.vel.dot(rotate_Vec(self.direct, 90)), 300) / 300
            normalizedNegDrift = 0
        else:
            normalizedPosDrift = 0
            normalizedNegDrift = min(self.vel.dot(rotate_Vec(self.direct, 90)), 300) / 300

        next_candy_center = np.array([self.Candy.Candy[0][0][0] + (self.Candy.Candy[0][1][0] - self.Candy.Candy[0][0][0]) / 2 , self.Candy.Candy[0][0][1] + (self.Candy.Candy[0][1][1] - self.Candy.Candy[0][0][1]) / 2] )
        next_candy_center[0] -= self.center_x
        next_candy_center[1] -= self.center_y
        normalizedAngleOfNextGate = (Vec_to_ang(self.direct) - Vec_to_ang(next_candy_center)) % 360

        normalizedAngleOfNextGate /= 360

        normalizedState = [*self.vision_points_distance_standart, normalizedForwardVelocity, normalizedReverseVelocity,
                           normalizedPosDrift, normalizedNegDrift, normalizedAngleOfNextGate]
        return np.reshape(np.array(normalizedState), (1, AI_INPUT_SHAPE))




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


class Track ():
    def __init__(self):
        self.track = read_track()

    def draw(self):
        arcade.draw_line_strip(track[0], arcade.color.BLACK)
        arcade.draw_line_strip(track[1], arcade.color.BLACK)


