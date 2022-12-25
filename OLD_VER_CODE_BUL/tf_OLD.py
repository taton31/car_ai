import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from tensorflow import keras
import numpy as np
learningRate = 0.00025
class AI():
    
    # y_train = keras.utils.to_categorical(y_train, 10)
    def __init__(self, stateSize, actionSize, learningRate):
        self.stateSize = stateSize
        self.actionSize = actionSize
        self.learningRate = learningRate

        self.BATCH_SIZE = 16

        self.actions_ = tf.Variable(np.zeros(self.actionSize), dtype=tf.float32, name='actions') 
        self.targetQ = tf.Variable(0, dtype=tf.float32, name='target') 
        self.ISWeights_ = tf.Variable(0, dtype=tf.float32, name='ISWeights') 
        
        self.input = Input(shape=(self.stateSize,), name="inputs", dtype=tf.float32)
        self.x = Dense(16, activation=tf.nn.elu)(self.input)
        self.x = Dense(16, activation=tf.nn.elu)(self.x)
        self.output = Dense(self.actionSize, activation=None, name = 'output')(self.x)

        model = keras.Model(self.input, self.output, name="Model")
        model.summary()

        self.QValue = tf.reduce_sum(tf.multiply(self.output, self.actions_))
        self.absoluteError = abs(self.QValue - self.targetQ)  
        self.loss = tf.reduce_mean(self.ISWeights_ * tf.square(self.targetQ - self.QValue))

        model.compile(optimizer='adam',
                    loss=self.loss,
                    metrics=['accuracy'])

        # model.fit(x_train, y_train, batch_size=64, epochs=15, validation_split=0.2)

        # print( model.evaluate(x_test, y_test) )



if __name__ == "__main__":
    a=AI(15,10,learningRate)
