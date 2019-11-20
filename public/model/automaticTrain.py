import os
from keras.models import Sequential
from keras.layers import Dropout, Input, Dense, Conv2D,Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from keras.callbacks import TensorBoard
from keras import backend as K
from keras.models import load_model
from keras.applications import VGG19
import numpy as np
def getFileData():
    f = open(basePath+"/model/trainFileHandling.txt", "r")
    try:
        num_clases = int(f.read())
    except Exception as e:
        num_clases = 0
    f.close()
    return num_clases
def setFileData(num_clases):
    f = open(basePath+"/model/trainFileHandling.txt", "wt")
    f.write(str(num_clases))
    f.close()
    return True
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
picturesDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/model/pictures/'
model_dir = basePath + '/model/assets/test.h5'
trainLabels_dir = basePath + '/model/assets/lbl.npy'
graph_dir = basePath + '/model/Graph/'
class TrainModel:
    def createModel(self,base_dir):
        img_width = 224
        img_height = 224
        batch_size = 32
        epochs = 10
        train_datagen = ImageDataGenerator(validation_split=0.2)
        train_generator = train_datagen.flow_from_directory(
            base_dir, 
            batch_size=batch_size,
            target_size= (img_width,img_height),
            class_mode='categorical',
            subset='training')
        validator_generator = train_datagen.flow_from_directory(
            base_dir, 
            batch_size=batch_size,
            target_size= (img_width,img_height),
            class_mode='categorical',
            subset='validation')
        train_labels = list(train_generator.class_indices.keys())
        num_classes = len(train_labels)

        callbacks = TensorBoard(log_dir=graph_dir)
        vgg19 = VGG19(weights="imagenet", include_top=False, input_shape=(img_width, img_height, 3))
        vgg19.trainable=False

        vgg19model = Sequential([vgg19])
        vgg19model.add(Flatten())
        vgg19model.add(Dense(256, activation='relu'))
        vgg19model.add(Dropout(0.2))
        vgg19model.add(Dense(32, activation='relu'))
        vgg19model.model.add(Dense(num_classes, activation='softmax'))
        adam = Adam(lr=0.0001)
        vgg19model.compile(optimizer=adam,
                        loss='categorical_crossentropy', metrics=['accuracy'])
        history =   vgg19model.fit_generator(
                    train_generator,
                    steps_per_epoch=train_generator.samples,
                    epochs=epochs,
                    validation_data=validator_generator,
                    validation_steps=validator_generator.samples, 
                    callbacks=[callbacks])
                
        vgg19model.save(model_dir)
        np.save(trainLabels_dir,train_labels)
        return str(history.history['acc'])
if __name__ == "__main__":
    dirNum = len(os.listdir(picturesDir))
    num = getFileData()
    if(int(dirNum) > 2 and int(num) > 0):
        TrainModel().createModel(picturesDir)
        new = getFileData()
        setNum = new - num
        setFileData(setNum)
