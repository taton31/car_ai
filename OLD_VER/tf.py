import math
import random
import numpy as np

# a=np.array([[1,1],[1,1]], dtype=float)
b=np.array([[2,2],[2,-2],[-3,2]], dtype=float)
# print (b.size)
# c = np.zeros(a.shape)
# rand_mut = (np.random.random(size=b.shape) * 2 - 1) / 1
# for i in range (b.shape[0]):
#     b[i] = b[i] + (0 if random.randint(0,1) else rand_mut[i])
#     print(0 if random.randint(0,1) else rand_mut[i])

print(np.amax(np.abs(b)))   ###########################################################################################################3
# b = b / max(np.a)   ###########################################################################################################3
print (b)

# def set_cross_w1( x, y):
#     c = np.zeros(x.shape)
#     for i in range (c.shape[0]):
#         for j in range (c.shape[1]):
#             c[i][j] = x[i][j] if random.randint(0,1) else y[i][j]
#     return c
# print (set_cross_w1(a,b))
# a=[1,5, ['23','23']]
# z=random.randint(0,1)

# COUNT_BR = 31



# def convert_bit(a):
#     if a > 1: 
#         a = 1
#     b=[]
#     a = bin(int(a * COUNT_BR))[2:]
#     for i in range(1000):
#         if pow(2, i) == COUNT_BR + 1: 
#             while len (a) < i:
#                 a = '0' + a
#             break


#     for i in a:
#         b.append(int(i))
#     return b

# print(convert_bit(0.2))

# for i in range (12):
#     tmp = i % 6
#     tmp = tmp % 3
#     mut = 2 if tmp == 0 else 1 if tmp == 1 else 1/2
#     print(i, i%2, mut)
# print(math.log(300, 1.3))
# print(pow(400, 1/2))
MUTATION_P = 2
P = MUTATION_P / (15)
print (P)
for i in range (2):
    for j in range (4):
        print ( P > random.random())
        # self.w1[i][j] += 0 if P > random.random() else rand_mut[i][j]
