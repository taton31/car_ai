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

def rotate_90(vec):
    vel_len = len_vec(vec)
    rotatedX = vec[1] / vel_len
    rotatedY = - vec[0] / vel_len
    return np.array([rotatedX, rotatedY]) 

def len_vec(vec):
    return math.sqrt(vec.dot(vec))