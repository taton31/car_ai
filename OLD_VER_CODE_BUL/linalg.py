import math
import numpy as np
def rotate_Vec(vec, angle):
        angle = math.pi * angle / 180
        rotatedX = vec[0] * math.cos(angle) - vec[1] * math.sin(angle)
        rotatedY = vec[0] * math.sin(angle) + vec[1] * math.cos(angle)
        return np.array([rotatedX, rotatedY]) 

def ang_to_Vec(angle):
    angle = math.pi * angle / 180
    rotatedX = math.cos(angle)
    rotatedY = math.sin(angle)
    return np.array([rotatedX, rotatedY]) 

def Vec_to_ang(vec):
    rotatedX = 180 * math.acos(vec[0] / len_vec(vec)) / math.pi
    if vec.dot(np.array([0,-1])) > 0: rotatedX *= -1
    return rotatedX

def rotate_90(vec):
    vel_len = len_vec(vec)
    rotatedX = vec[1] / vel_len
    rotatedY = - vec[0] / vel_len
    return np.array([rotatedX, rotatedY]) 

def len_vec(vec):
    return math.sqrt(vec.dot(vec))



if __name__ == "__main__":
    print( Vec_to_ang(np.array([1,-1])))
