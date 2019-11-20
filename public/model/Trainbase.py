from keras.models import Sequential
from keras.layers import Dropout, Input, Dense, Conv2D,Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.callbacks import TensorBoard
from keras import backend as K
from keras.models import load_model
from keras.applications import VGG19
import tensorflow as tf
import numpy as np
import os
import automaticTrain
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K.clear_session()
model_dir = basePath + '/model/assets/vgg19model.h5'
trainLabels_dir = basePath + '/model/assets/labelrgb.npy'

class Trainbase:
    def __init__(self):
        self.train_labels = np.load(trainLabels_dir)
        self.model = load_model(model_dir)
        self.model.predict(np.zeros((1, 224,224,3))) # warmup
        self.session = K.get_session()
        self.graph = tf.get_default_graph()
        self.graph.finalize() # finalize

    def verif(self, img):
        with self.session.as_default():
            with self.graph.as_default():
                score = self.model.predict(img)
                ynew = np.argmax(score)
        return list([ynew, self.train_labels, score])

class TrainModel:
    graph_dir = basePath + '/model/Graph/'
    def createModel(self, base_dir):
        automaticTrain.createModel(base_dir)
        