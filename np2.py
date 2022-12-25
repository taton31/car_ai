from constans import AI_INPUT_SHAPE, AI_OUTPUT_SHAPE, AI_MIDDLE_SHAPE
import numpy as np

import numpy as np
# class sequential(tf.keras.Sequential):
#     def __init__(self):
#         super().__init__([
#                             Input(AI_INPUT_SHAPE),
#                             Dense(AI_MIDDLE_SHAPE, activation = 'relu'),
#                             Dense(AI_OUTPUT_SHAPE, activation = 'softmax')
#                         ])
#         self(np.zeros((1,AI_INPUT_SHAPE)))

#     def weights_to_array(self):
#         weights = []
#         for i in self.layers:
#             for j in i.get_weights():
#                 weights.extend(np.reshape(j, (j.size)))
#         return weights

#     def weights_from_array(self, weights):
#         shift = 0
#         for i in range(len(self.layers)):
#             w_shape, b_shape = self.layers[i].get_weights()[0].shape, self.layers[i].get_weights()[1].shape
#             w_size, b_size = self.layers[i].get_weights()[0].size, self.layers[i].get_weights()[1].size
#             self.layers[i].set_weights([np.reshape(weights[shift: shift + w_size], w_shape), np.reshape(weights[shift + w_size: shift + w_size + b_size], b_shape)])
#             shift += w_size + b_size

#     def get_total_weights(self):
#         return len(self.weights_to_array())


def RELU(x):
    return np.array([z if z >= 0 else 0 for z in x])

def SOFTMAX(x):
    sum = np.sum(x)
    return x / sum

if __name__ == "__main__":
    x= np.array([-1, -0.2, 4,1])
    print(SOFTMAX(x))
    # model.weights_from_array(model.weights_to_array())  


