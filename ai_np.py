import math
import numpy as np
X_SHAPE = 8
W1_SHAPE = (10, 8)
W2_SHAPE = (4, 10)
Y_SHAPE = 4
B_SHAPE = 10
ALPHA = 10
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
        z = np.dot(self.w1, self.x) + self.b
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
    


# def go(ls):
#     x = np.array(ls) #8

#     w11 = [0.3, 0.3, 0]
#     w12 = [0.4, -0.5, 1]
#     weight1 = np.array([w11, w12])  # матрица 2x3
#     weight2 = np.array([-1, 1])     # вектор 1х2

#     sum_hidden = np.dot(weight1, x)       # вычисляем сумму на входах нейронов скрытого слоя
#     print("Значения сумм на нейронах скрытого слоя: "+str(sum_hidden))

#     out_hidden = np.array([act(x) for x in sum_hidden])
#     print("Значения на выходах нейронов скрытого слоя: "+str(out_hidden))

#     sum_end = np.dot(weight2, out_hidden)
#     y = act(sum_end)
#     print("Выходное значение НС: "+str(y))

#     return y

# house = 1
# rock = 0
# attr = 1

# res = go(house, rock, attr)
# if res == 1:
#     print("Ты мне нравишься")
# else:
#     print("Созвонимся")