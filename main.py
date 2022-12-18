
import math
import arcade
import numpy as np 
        
# Imports


# Constants
# Speed limit
MAX_SPEED = 12.0
MAX_SPEED_ROT = 3.0

ALPHA = 0.01
# How fast we accelerate
ACCELERATION_RATE_START = 0.4
ACCELERATION_RATE_STOP = 0.4
ACCELERATION_RATE_ROT = 1.6

# How fast to slow down after we let off the key
FRICTION = 0.02
FRICTION_ROT = 0.1



SCREEN_WIDTH = 1850
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "CAR_AI"
RADIUS = 150

class Car (arcade.Sprite):
    def __init__(self, x, y, scale) -> None:
        super().__init__("images/car.png", scale)
        self.center_y = y
        self.center_x = x

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.F_traction = np.array([1, 0]) 
        self.F_drag = np.array([1, 0]) 
        self.F_rr = np.array([1, 0]) 
        self.F_long = np.array([1, 0]) 
        
        self.direct = np.array([1, 0]) 
        self.acc_module = 0
        self.acc_module_rot = 0

        self.vel_vector = np.array([1, 0]) 
        self.vel_module = 0
        self.vel_module_rot = 0


    def set_accel(self):
        pass

    def rotate_Vec(self, angle):
        rotatedX = self.direct[0] * math.cos(math.pi * angle/180) - self.direct[1] * math.sin(math.pi * angle/180)
        rotatedY = self.direct[0] * math.sin(math.pi * angle/180) + self.direct[1] * math.cos(math.pi * angle/180)
        self.direct = np.array([rotatedX, rotatedY]) 


    def update(self, delta_time):        

        # if self.velocity_module > FRICTION:
        #     self.velocity_module -= FRICTION
        # elif self.velocity_module < -FRICTION:
        #     self.velocity_module += FRICTION
        # else:
        #     self.velocity_module = 0

        # if self.up_pressed and not self.down_pressed:
        #     self.velocity_module += ACCELERATION_RATE
        # elif self.down_pressed and not self.up_pressed:
        #     self.velocity_module += -ACCELERATION_RATE
        # if self.left_pressed and not self.right_pressed:
        #     self.velocity_direction += ACCELERATION_RATE_ROT
        # elif self.right_pressed and not self.left_pressed:
        #     self.velocity_direction += -ACCELERATION_RATE_ROT


        # if self.velocity_direction > FRICTION_ROT:
        #     self.velocity_direction -= FRICTION_ROT
        # elif self.velocity_direction < -FRICTION_ROT:
        #     self.velocity_direction += FRICTION_ROT
        # else:
        #     self.velocity_direction = 0

        # # Apply acceleration based on the keys pressed
        

        # if self.velocity_module > MAX_SPEED:
        #     self.velocity_module = MAX_SPEED
        # elif self.velocity_module < -MAX_SPEED:
        #     self.velocity_module = -MAX_SPEED
        # if self.velocity_direction > MAX_SPEED_ROT:
        #     self.velocity_direction = MAX_SPEED_ROT
        # elif self.velocity_direction < -MAX_SPEED_ROT:
        #     self.velocity_direction = -MAX_SPEED_ROT

        # self.change_angle = self.velocity_direction
        # self.angle += self.change_angle

        # self.change_x = math.cos(math.pi * self.angle/180) * self.velocity_module
        # self.change_y = math.sin(math.pi * self.angle/180) * self.velocity_module
        
        # self.center_x += self.change_x
        # self.center_y += self.change_y


        if self.up_pressed and not self.down_pressed:
            self.acc_module = ACCELERATION_RATE_START
        elif self.down_pressed and not self.up_pressed:
            self.acc_module = -ACCELERATION_RATE_STOP

        if self.left_pressed and not self.right_pressed:
            self.vel_module_rot = ACCELERATION_RATE_ROT
        elif self.right_pressed and not self.left_pressed:
            self.vel_module_rot = -ACCELERATION_RATE_ROT


        self.rotate_Vec(self.vel_module_rot * delta_time)



        if self.velocity_direction > FRICTION_ROT:
            self.velocity_direction -= FRICTION_ROT
        elif self.velocity_direction < -FRICTION_ROT:
            self.velocity_direction += FRICTION_ROT
        else:
            self.velocity_direction = 0

            
        if self.velocity_module > FRICTION:
            self.velocity_module -= FRICTION
        elif self.velocity_module < -FRICTION:
            self.velocity_module += FRICTION
        else:
            self.velocity_module = 0


        # Apply acceleration based on the keys pressed
        

        if self.velocity_module > MAX_SPEED:
            self.velocity_module = MAX_SPEED
        elif self.velocity_module < -MAX_SPEED:
            self.velocity_module = -MAX_SPEED
        if self.velocity_direction > MAX_SPEED_ROT:
            self.velocity_direction = MAX_SPEED_ROT
        elif self.velocity_direction < -MAX_SPEED_ROT:
            self.velocity_direction = -MAX_SPEED_ROT

        self.change_angle = self.velocity_direction
        self.angle += self.change_angle

        self.change_x = math.cos(math.pi * self.angle/180) * self.velocity_module
        self.change_y = math.sin(math.pi * self.angle/180) * self.velocity_module
        
        self.center_x += self.change_x
        self.center_y += self.change_y
        


        






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
        arcade.draw_text(f"vel_der: {self.Car.velocity_direction}", 10, 50, arcade.color.BLACK)
        arcade.draw_text(f"vel_mod: {self.Car.velocity_module}", 10, 70, arcade.color.BLACK)
        arcade.draw_text(f"ang: {self.Car.angle}", 10, 90, arcade.color.BLACK)
        arcade.draw_text(f"FR: {FRICTION_ROT}", 10, 110, arcade.color.BLACK)
        

    def on_update(self, delta_time: float = 1 / 60):
        self.Car.update(delta_time)

    def on_key_press(self, symbol, modifiers):

        global FRICTION_ROT
        global ALPHA

        if symbol == arcade.key.O:
            # global FRICTION_ROT
            FRICTION_ROT += ALPHA

        if symbol == arcade.key.P:
            # global FRICTION_ROT
            FRICTION_ROT -= ALPHA

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