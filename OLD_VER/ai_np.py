import math
import random
import numpy as np
X_SHAPE = 5
W1_SHAPE = (4, 5)
W2_SHAPE = (3, 4)
Y_SHAPE = 3
B_SHAPE = 4
# X_SHAPE = 8
# W1_SHAPE = (6, 8)
# W2_SHAPE = (4, 6)
# Y_SHAPE = 4
# B_SHAPE = 6
# ALPHA = 30
ALPHA = 20
ALPHA_MUT = 1
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!ubral BBBBBBBBBB
MUTATION_P = 8
ALPHA_BLX = 2
ALPHA_LIT = ALPHA * 2
ALPHA_BIG = ALPHA / 2

class AI():
    def __init__(self) -> None:
        # np.random.seed(1)
        
        self.w1 = np.random.random(size=W1_SHAPE) * 2 - 1
        self.w2 = np.random.random(size=W2_SHAPE) * 2 - 1
        self.b = np.random.random(size=(B_SHAPE,)) * 2 - 1
        
        # self.w1 = np.array(((1,2),(3,4),(5,6)))
        # self.w2 = np.array(((1,2,3),(4,5,6)))
        
    def act(self, x):
        return 0 if x < 0.5 else 1

    def set_w1(self, x):
        self.w1 = x

    def set_mix_w1(self, x, y):
        self.w1 = (x + y) / 2

    def set_cross_w1(self, x, y, type = 'cross'):
        if type == 'cross':
            c = np.zeros(x.shape)
            for i in range (c.shape[0]):
                for j in range (c.shape[1]):
                    c[i][j] = x[i][j] if random.randint(0,1) else y[i][j]
            self.w1 = c
        elif type == 'arifm':
            lam = random.random()
            self.w1 = x * lam + y * (1 - lam)
        elif type == 'blx':
            c = np.zeros(x.shape)
            for i in range (c.shape[0]):
                for j in range (c.shape[1]):
                    minim = min(x[i][j], y[i][j]) - ALPHA_BLX
                    maxim = max(x[i][j], y[i][j]) + ALPHA_BLX
                    c[i][j] = minim + random.random() * (maxim - minim)
            self.w1 = c

    def set_cross_w2(self, x, y, type = 'cross'):
        if type == 'cross':
            c = np.zeros(x.shape)
            for i in range (c.shape[0]):
                for j in range (c.shape[1]):
                    c[i][j] = x[i][j] if random.randint(0,1) else y[i][j]
            self.w2 = c
        elif type == 'arifm':
            lam = random.random()
            self.w2 = x * lam + y * (1 - lam)
        elif type == 'blx':
            c = np.zeros(x.shape)
            for i in range (c.shape[0]):
                for j in range (c.shape[1]):
                    minim = min(x[i][j], y[i][j]) - ALPHA_BLX
                    maxim = max(x[i][j], y[i][j]) + ALPHA_BLX
                    c[i][j] = minim + random.random() * (maxim - minim)
            self.w2 = c

    def set_cross_b(self, x, y, type = 'cross'):
        if type == 'cross':
            c = np.zeros(x.shape)
            for i in range (c.shape[0]):
                c[i] = x[i] if random.randint(0,1) else y[i]
            self.b = c
        elif type == 'arifm':
            lam = random.random()
            self.b = x * lam + y * (1 - lam)
        elif type == 'blx':
            c = np.zeros(x.shape)
            for i in range (c.shape[0]):
                    minim = min(x[i], y[i]) - ALPHA_BLX
                    maxim = max(x[i], y[i]) + ALPHA_BLX
                    c[i] = minim + random.random() * (maxim - minim)
            self.b = c
    
    def mutation_w1(self, AL):
        rand_mut = (np.random.random(size=self.w1.shape) * 2 - 1) / AL
        P = MUTATION_P / (self.w1.shape[0] * self.w1.shape[1])
        for i in range (self.w1.shape[0]):
            for j in range (self.w1.shape[1]):
                self.w1[i][j] += 0 if P > random.random() else rand_mut[i][j]

        # self.w1 = self.w1 / np.amax(np.abs(self.w1))   ###########################################################################################################3

    def mutation_w2(self, AL):
        rand_mut = (np.random.random(size=self.w2.shape) * 2 - 1) / AL
        P = MUTATION_P / (self.w2.shape[0] * self.w2.shape[1])
        for i in range (self.w2.shape[0]):
            for j in range (self.w2.shape[1]):
                self.w2[i][j] += 0 if random.random() < P else rand_mut[i][j]
        # self.w2 = self.w2 / np.amax(np.abs(self.w2))
        

    def mutation_b(self, AL):
        rand_mut = (np.random.random(size=self.b.shape) * 2 - 1) / AL
        P = 1 / self.b.shape[0]
        for i in range (self.b.shape[0]):
            self.b[i] += 0 if random.random() < P else rand_mut[i]
        # self.b = self.b / np.amax(np.abs(self.b))


    def mix_w2_AL(self, ALPHA):
        self.w2 = self.w2 + (np.random.random(size=self.w2.shape) / ALPHA) * 2 - 1. / ALPHA

    def mix_b_AL(self, ALPHA):
        self.b = self.b + (np.random.random(size=(B_SHAPE,)) / ALPHA) * 2 - 1. / ALPHA

    def set_w2(self, x):
        self.w2 = x

    def set_mix_w2(self, x, y):
        self.w2 = (x + y) / 2

    def set_b(self, x):
        self.b = x

    def set_mix_b(self, x, y):
        self.b = (x + y) / 2

    def set_x(self, x):
        self.x = x

    def mix_w1(self):
        self.w1 = self.w1 + (np.random.random(size=self.w1.shape) / ALPHA) * 2 - 1. / ALPHA

    def mix_w2(self):
        self.w2 = self.w2 + (np.random.random(size=self.w2.shape) / ALPHA) * 2 - 1. / ALPHA

    def mix_b(self):
        self.b = self.b + (np.random.random(size=(B_SHAPE,)) / ALPHA) * 2 - 1. / ALPHA

    def mix_w1_AL(self, ALPHA):
        self.w1 = self.w1 + (np.random.random(size=self.w1.shape) / ALPHA) * 2 - 1. / ALPHA

    def mix_w2_AL(self, ALPHA):
        self.w2 = self.w2 + (np.random.random(size=self.w2.shape) / ALPHA) * 2 - 1. / ALPHA

    def mix_b_AL(self, ALPHA):
        self.b = self.b + (np.random.random(size=(B_SHAPE,)) / ALPHA) * 2 - 1. / ALPHA

    def mix_lit_w1(self):
        self.w1 = self.w1 + (np.random.random(size=self.w1.shape) / ALPHA_LIT) * 2 - 1. / ALPHA_LIT

    def mix_lit_w2(self):
        self.w2 = self.w2 + (np.random.random(size=self.w2.shape) / ALPHA_LIT) * 2 - 1. / ALPHA_LIT

    def mix_lit_b(self):
        self.b = self.b + (np.random.random(size=(B_SHAPE,)) / ALPHA_LIT) * 2 - 1. / ALPHA_LIT

    def mix_big_w1(self):
        self.w1 = self.w1 + (np.random.random(size=self.w1.shape) / ALPHA_BIG) * 2 - 1. / ALPHA_BIG

    def mix_big_w2(self):
        self.w2 = self.w2 + (np.random.random(size=self.w2.shape) / ALPHA_BIG) * 2 - 1. / ALPHA_BIG

    def mix_big_b(self):
        self.b = self.b + (np.random.random(size=(B_SHAPE,)) / ALPHA_BIG) * 2 - 1. / ALPHA_BIG

    def get_w1(self):
        return self.w1

    def get_w2(self):
        return self.w2

    def get_b(self):
        return self.b

    def refresh(self):
        self.w1 = np.random.random(size=W1_SHAPE) * 2 - 1
        self.w2 = np.random.random(size=W2_SHAPE) * 2 - 1
        self.b = np.random.random(size=(B_SHAPE,)) * 2 - 1

    def calc(self):
        z = np.dot(self.w1, self.x)
        # z = np.dot(self.w1, self.x) + self.b
        z = list(map(self.act, z))
        z = np.dot(self.w2, z)
        z = list(map(self.act, z))
        return z




if __name__ == "__main__":
    a=AI()
    w1 = np.array(((1,2),(3,4),(5,6)))/2
    w2 = np.array(((3,2),(3,4),(5,6)))
    a.set_mix_w1(w1,w2)
    print (w1)
    
