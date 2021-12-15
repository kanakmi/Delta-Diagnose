# import the required libraries

import numpy as np
import os
import cv2
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import tensorflow as tf
from tensorflow.keras import optimizers
from tensorflow.keras.models import Model, load_model
import tensorflow_model_optimization as tfmot

# Global Variables for later use

IMG_SIZE = 256
X_train = [] # To store train images
y_train = [] # To store train labels

train_path = './dataset/train/' # path containing training images
test_path = './dataset/test/' # path containing training images

model = None
q_aware_model = None

# function that would read an image provided the image path, preprocess and return it back
'''
labels -
0 - Covid
1 - Viral Pneumonia
2 - Normal
'''
def read_and_preprocess(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR) # reading the image
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE)) # resizing it (I just like it to be powers of 2)
    img = np.array(img, dtype='float32') # convert its datatype so that it could be normalized
    img = img/255 # normalization (now every pixel is in the range of 0 and 1)
    return img

# read the data from the disk provided the data path
def get_data(path):
    X = []
    y = []
    for folder in os.scandir(path):
        for entry in os.scandir(path + folder.name):

            X.append(read_and_preprocess(path + folder.name + '/' + entry.name))
        
            if folder.name[0]=='C':
                y.append(0) # Covid
            elif folder.name[0]=='V':
                y.append(1) # Viral Pneumonia
            else:
                y.append(2) # Normal

    X = np.array(X)
    y = np.array(y)
    
    return X, y

# Image Augmentation
def image_augmentation():
    global X_train, y_train
    X_aug = []
    y_aug = []

    for i in range(0, len(y_train)):
        X_new = np.fliplr(X_train[i])
        X_aug.append(X_new)
        y_aug.append(y_train[i])

    X_aug = np.array(X_aug)
    y_aug = np.array(y_aug)

    X_train = np.append(X_train, X_aug, axis=0) # appending augmented images to original training samples
    y_train = np.append(y_train, y_aug, axis=0) # appending augmented labels to original training labels

def split_data(test_size=0.2, random_state=109):
    global X_train, y_train
    '''
    We have splitted our data in a way that - 
    1. The samples are shuffled
    2. The ratio of each class is maintained (stratify)
    3. We get same samples every time we split our data (random state)
    '''
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=test_size, shuffle=True, stratify=y_train, random_state=random_state)
    return X_train, X_val, y_train, y_val

# Load pretrained model (best saved one)
def load_model():
    with open('covid_classifier_model.json', 'r') as json_file:
        json_savedModel= json_file.read()
    # load the model  
    model = tf.keras.models.model_from_json(json_savedModel)
    model.load_weights('covid_classifier_weights.h5')
    opt = optimizers.Adam(learning_rate=0.0001)
    model.compile(loss = 'sparse_categorical_crossentropy', optimizer=opt, metrics= ["accuracy"])

def quantize_model():
    global q_aware_model

    # Converting the saved model to TFLite Model
    quantize_model = tfmot.quantization.keras.quantize_model
    # q_aware stands for for quantization aware.
    q_aware_model = quantize_model(model)
    # `quantize_model` requires a recompile.
    q_aware_model.compile(optimizer=optimizers.Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    X_train, X_val, y_train, y_val = split_data(test_size=0.15, random_state=123)

    # retraining the model for better accuracy
    history = q_aware_model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs = 5)


# Evaluating the Trained Model
def evaluate_model():
    global q_aware_model

    # reading the test data
    X_test, y_test = get_data(test_path)
    # We have 185 images for testing

    # making predictions
    predictions = q_aware_model.predict(X_test)

    # Obtain the predicted class from the model prediction
    predict = []

    for i in predictions:
        predict.append(np.argmax(i))

    predict = np.asarray(predict)

    # Obtain the accuracy of the model
    accuracy = accuracy_score(y_test, predict)
    print(accuracy)

    # Obtaining the complete classification report of our model
    report = classification_report(y_test, predict)
    print(report)

def save_model():
    # saving the Quantised model
    global q_aware_model

    converter = tf.lite.TFLiteConverter.from_keras_model(q_aware_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]

    tflite_qaware_model = converter.convert()

    with open("covid_classifier.tflite", 'wb') as f:
        f.write(tflite_qaware_model)

def main():
    global X_train, y_train, model

    # reading the training data
    X_train, y_train = get_data(train_path)
    # We have 1955 training samples in total

    # applying image augmentation on training data
    image_augmentation()

    # loading the saved model from memory
    load_model()

    # quantizing the pretrained model
    quantize_model()

    # evaluating the quantized model's performance
    evaluate_model()

    # saving the quantized model
    save_model()

if __name__ == "__main__":
    main()