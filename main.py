
import math
import arcade
import numpy as np 
from read_map import track, read_track
from variable import line_intersection

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
WHEEL_ROT_PER_SEC = 0.32
WHEEL_ROT_MAX = 3

FRICTION_MAX = 100000

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
SCREEN_TITLE = "CAR_AI"
RADIUS = 150

class Car (arcade.Sprite):
    def __init__(self, x, y, scale) -> None:
        super().__init__("images/car.png", scale, hit_box_algorithm='None')
        self.center_y = y
        self.center_x = x
        self.angle = 270

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
        # self.vision_vec =  [self.direct]
        
        self.vision_points = []
        self.vision_points_distance = []
        self.vision_points_OLD = []

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
            self.wheel_rot += WHEEL_ROT_PER_SEC
            if WHEEL_ROT_MAX < self.wheel_rot: self.wheel_rot = WHEEL_ROT_MAX
        elif self.right_pressed and not self.left_pressed:
            self.wheel_rot -= WHEEL_ROT_PER_SEC
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
        # self.vision_vec =  [self.direct]

    

        

        
        
        
         

class Track ():
    def __init__(self):
        self.track = read_track()

    def draw(self):
        # self.track_sprites = arcade.SpriteList()
        # self.player = arcade.Sprite()
        # self.player.center_y = self.height / 2
        # self.player.left = 10
        # self.all_sprites.append(self.player)
        arcade.draw_line_strip(track[0], arcade.color.BLACK)
        arcade.draw_line_strip(track[1], arcade.color.BLACK)

        






# Classes
class Welcome(arcade.Window):
    def __init__(self):

        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        


        # Set the background window
        arcade.set_background_color(arcade.color.GRAY)
        self.Car = Car(120, SCREEN_HEIGHT / 2, 0.08)
        self.Track = Track()

        


    def on_draw(self):
        self.clear()

        self.Car.draw()
        for i in self.Car.vision_points:
            if i:
                arcade.draw_circle_filled(i[0], i[1], 10, arcade.color.WHITE)
        self.Track.draw()
        arcade.draw_text(f"FA: {self.Car.len_vec(self.Car.F_a)}", 10, 50, arcade.color.BLACK)
        arcade.draw_text(f"FRESA: {self.Car.len_vec(self.Car.F_res_a)}", 10, 70, arcade.color.BLACK)
        arcade.draw_text(f"FRICTION_MAX: {C_DRAG}", 10, 90, arcade.color.BLACK)
        # arcade.draw_text(f"FR: {FRICTION_ROT}", 10, 110, arcade.color.BLACK)
        

    def on_update(self, delta_time: float = 1 / 60):
        self.Car.update(delta_time)
        self.car_vision()
        
        if line_intersection(self.Car.get_adjusted_hit_box(), self.Track.track[0]) or line_intersection(self.Car.get_adjusted_hit_box(), self.Track.track[1]):
            pass
            self.death()


    def car_vision(self):
        self.Car.vision_points.clear()
        self.Car.vision_points_distance.clear()
        for i in self.Car.vision_vec:
            segment = [[self.Car.center_x, self.Car.center_y], [self.Car.center_x + 1000 * i[0], self.Car.center_y + 1000 * i[1]]]
            point_1 = line_intersection(segment, self.Track.track[0])
            point_2 = line_intersection(segment, self.Track.track[1])
            if not point_1 or not point_2:
                self.Car.vision_points.append(point_1 or point_2) 
            elif (self.Car.center_x - point_1[0])**2 + (self.Car.center_y - point_1[1])**2 < (self.Car.center_x - point_2[0])**2 + (self.Car.center_y - point_2[1])**2: self.Car.vision_points.append(point_1)
            elif (self.Car.center_x - point_1[0])**2 + (self.Car.center_y - point_1[1])**2 > (self.Car.center_x - point_2[0])**2 + (self.Car.center_y - point_2[1])**2: self.Car.vision_points.append(point_2)
        
        # if not self.Car.vision_points_OLD : self.Car.vision_points_OLD = self.Car.vision_points
        for i in range(len(self.Car.vision_points)):
            if self.Car.vision_points[i] == False : self.Car.vision_points[i] = self.Car.vision_points_OLD[i]

            self.Car.vision_points_distance.append(math.sqrt ((self.Car.center_x - self.Car.vision_points[i][0])**2 + (self.Car.center_y - self.Car.vision_points[i][1])**2))
        
        self.Car.vision_points_OLD = self.Car.vision_points.copy()

    def on_key_press(self, symbol, modifiers):

        global C_DRAG
        global ALPHA

        if symbol == arcade.key.O:
            # global FRICTION_ROT
            C_DRAG += ALPHA

        if symbol == arcade.key.P:
            # global FRICTION_ROT
            C_DRAG -= ALPHA

        if symbol == arcade.key.UP:
            self.Car.up_pressed = True

        if symbol == arcade.key.DOWN:
            self.Car.down_pressed = True

        if symbol == arcade.key.LEFT:
            self.Car.left_pressed = True

        if symbol == arcade.key.RIGHT:
            self.Car.right_pressed = True
            

    def on_key_release(self, symbol: int, modifiers: int):
        
        if symbol == arcade.key.UP:
            self.Car.up_pressed = False

        if symbol == arcade.key.DOWN:
            self.Car.down_pressed = False

        if symbol == arcade.key.LEFT:
            self.Car.left_pressed = False

        if symbol == arcade.key.RIGHT:
            self.Car.right_pressed = False
    
    def death(self):
        self.Car = Car(120, SCREEN_HEIGHT / 2, 0.08)



# Main code entry point
if __name__ == "__main__":
    app = Welcome()
    arcade.run()

