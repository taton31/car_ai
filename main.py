
import math
import arcade
import numpy as np 
        
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


ENGINEFORCE = 1500000
BRAKINGFORCE = ENGINEFORCE * 5
C_DRAG = 2
C_RR = 30 * C_DRAG
MASS = 900
WHEEL_ROT_PER_SEC = 0.32
WHEEL_ROT_MAX = 3

FRICTION_MAX = 100000

SCREEN_WIDTH = 1850
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "CAR_AI"
RADIUS = 150

class Car (arcade.Sprite):
    def __init__(self, x, y, scale) -> None:
        super().__init__("images/car.png", scale)
        self.center_y = y
        self.center_x = x

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
        


    def set_accel(self):
        pass

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
        elif self.down_pressed and not self.up_pressed:
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

        self.F_long = self.F_traction + self.F_drag + self.F_rr + self.F_a + self.F_res_a

        self.acc = self.F_long / MASS
        self.vel += self.acc * delta_time
        self.pos += self.vel * delta_time
        self.center_x = self.pos[0]
        self.center_y = self.pos[1]
         


        






# Classes
class Welcome(arcade.Window):
    def __init__(self):

        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the background window
        arcade.set_background_color(arcade.color.GRAY)
        self.Car = Car(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 0.2)
        


    def on_draw(self):
        self.clear()

        self.Car.draw()
        arcade.draw_text(f"FA: {self.Car.len_vec(self.Car.F_a)}", 10, 50, arcade.color.BLACK)
        arcade.draw_text(f"FRESA: {self.Car.len_vec(self.Car.F_res_a)}", 10, 70, arcade.color.BLACK)
        arcade.draw_text(f"FRICTION_MAX: {C_DRAG}", 10, 90, arcade.color.BLACK)
        # arcade.draw_text(f"FR: {FRICTION_ROT}", 10, 110, arcade.color.BLACK)
        

    def on_update(self, delta_time: float = 1 / 60):
        self.Car.update(delta_time)

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



# Main code entry point
if __name__ == "__main__":
    app = Welcome()
    arcade.run()