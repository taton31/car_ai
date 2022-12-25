import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from tensorflow import keras
import numpy as np
from tf2_sup import *



class DenseNN(tf.Module):
    def __init__(self, outputs, activate="elu", trainable=True):
        super().__init__()
        self.outputs = outputs
        self.activate = activate
        self.fl_init = False
        self.trainable = trainable

    def __call__(self, x):
        
        if not self.fl_init:
            self.w = tf.random.normal((x.shape[-1], self.outputs), name="w")
            self.b = tf.zeros([self.outputs], dtype=tf.float32, name="b")

            self.w = tf.Variable(self.w, trainable=self.trainable)
            self.b = tf.Variable(self.b, trainable=self.trainable)

            self.fl_init = True

        y = x @ self.w + self.b

        if self.activate == "relu":
            return tf.nn.relu(y)
        elif self.activate == "softmax":
            return tf.nn.softmax(y)
        elif self.activate == "elu":
            return tf.nn.elu(y)

        return y


class SequentialModule(tf.Module):
    def __init__(self, actionSize, trainable=True):
        super().__init__()
        self.trainable = trainable
        self.layer_1 = DenseNN(16, trainable=self.trainable)
        self.layer_2 = DenseNN(16, trainable=self.trainable)
        self.layer_3 = DenseNN(actionSize, trainable=self.trainable)

    def __call__(self, x):
        return self.layer_3(self.layer_2(self.layer_1(x)))

    def copy(self, target):
        self.layer_1.w = target.layer_1.w
        self.layer_1.b = target.layer_1.b
        self.layer_2.w = target.layer_2.w
        self.layer_2.b = target.layer_2.b
        self.layer_3.w = target.layer_3.w
        self.layer_3.b = target.layer_3.b





class AI():
    def __init__(self):

        self.stateSize = 15
        self.actionSize = 9
        self.learningRate = 0.00025
        self.possibleActions = np.identity(self.actionSize, dtype=int)

        self.totalTrainingEpisodes = 100000
        self.maxSteps = 3600

        self.batchSize = 64
        self.memorySize = 100000

        self.maxEpsilon = 1
        self.minEpsilon = 0.01
        self.decayRate = 0.00001
        self.decayStep = 0
        self.gamma = 0.9
        self.training = True

        self.pretrainLength = self.batchSize

        self.maxTau = 10000
        self.tau = 0

        self.DQNetwork = SequentialModule(9)
        self.TargetNetwork = SequentialModule(9)
        self.opt = tf.optimizers.Adam(learning_rate=0.00025)

        self.memoryBuffer = PrioritisedMemory(self.memorySize)
        # self.pretrain()

        self.state = []
        self.trainingStepNo = 0

        self.newEpisode = False
        self.stepNo = 0
        self.episodeNo = 0


    def loss(self, output_DQ, output_TN):
        action = tf.math.argmax(output_TN)
        action = tf.cast(action, tf.float32)
        QValue = tf.reduce_sum(tf.multiply(output_DQ, action))
        QTargetValue = tf.reduce_sum(tf.multiply(output_TN, action))
        # absoluteError = abs(QValue - QTargetValue)  
        loss = tf.reduce_mean(tf.square(QTargetValue - QValue))
        return loss

    def metric(self, output_DQ, output_TN):
        action = tf.math.argmax(output_TN)
        action = tf.cast(action, tf.float32)
        QValue = tf.reduce_sum(tf.multiply(output_DQ, action))
        QTargetValue = tf.reduce_sum(tf.multiply(output_TN, action))
        absoluteError = abs(QValue - QTargetValue)
        return absoluteError


    def train_batch(self, x_batch, x_life, x_reward):
        TN_output = self.TargetNetwork(x_batch)
        tmp = []
        for i in range(len(TN_output)):
            terminalState = x_life[i]
            if terminalState:
                tmp.append(x_reward[i])
            else:
                tmp.append(x_reward[i] + 0.9 * TN_output[i])
        TN_output = tf.Variable(tmp)
        with tf.GradientTape() as tape:
            f_loss = self.loss(self.DQNetwork(x_batch), TN_output)

        grads = tape.gradient(f_loss, self.DQNetwork.trainable_variables)
        self.opt.apply_gradients(zip(grads, self.DQNetwork.trainable_variables))

        return f_loss

    def train(self, dataset):
        # for n in range(EPOCHS):
        # sum_loss = 0
        ret = []
        for j in range(len(dataset[0])):
            # sum_loss += train_batch(x_batch)
            for i in range (5):
                S_loss = self.train_batch([dataset[0][j]], [dataset[1][j]], [dataset[2][j]])
            ret.append(tf.math.argmax(self.DQNetwork(x_batch)))
        self.TargetNetwork.copy(self.DQNetwork)

        print(S_loss.numpy())
        return ret


    def pretrain(self):
        for i in range(self.pretrainLength):
            if i == 0:
                state = self.game.get_state()

            # pick a random movement and do it to populate the memory thing
            # choice = random.randInt(self.actionSize)
            # action = self.possibleActions[choice]
            action = random.choice(self.possibleActions)
            actionNo = np.argmax(action)
            # now we need to get next state
            reward = self.game.make_action(actionNo)
            nextState = self.game.get_state()
            self.newEpisode = False

            if self.game.is_episode_finished():
                reward = -100
                self.memoryBuffer.store((state, action, reward, nextState, True))
                self.game.new_episode()
                state = self.game.get_state()
                self.newEpisode = True
            else:
                self.memoryBuffer.store((state, action, reward, nextState, False))
                state = nextState

        print("pretrainingDone")



if __name__ == "__main__":


    x_train = [np.random.random(15) for i in range(1024)]
    x_train = tf.cast(x_train, tf.float32)
    w = np.random.random(1024)
    w = tf.cast(w, tf.float32)
    q = np.random.random(1024)
    q = tf.cast(q, tf.float32)
    train_dataset = tf.data.Dataset.from_tensor_slices(x_train)
    train_dataset = train_dataset.shuffle(buffer_size=1024).batch(16)

    zzz= AI()
    zzz.train([train_dataset, w, q])
