# importing the required libraries

import cv2
import numpy as np
import os
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import optimizers
from tensorflow.keras.models import Model, load_model

# function that would read an image provided the image path, preprocess and return it back

def read_and_preprocess(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR) # reading the image
    img = cv2.resize(img, (256, 256)) # resizing it (I just like it to be powers of 2)
    img = np.array(img, dtype='float32') # convert its datatype so that it could be normalized
    img = img/255 # normalization (now every pixel is in the range of 0 and 1)
    return img

X_train = [] # To store train images
y_train = [] # To store train labels

# labels -
# 0 - Covid
# 1 - Viral Pneumonia
# 2 - Normal

train_path = './dataset/train/' # path containing training image samples

for folder in os.scandir(train_path):
    for entry in os.scandir(train_path + folder.name):

        X_train.append(read_and_preprocess(train_path + folder.name + '/' + entry.name))
        
        if folder.name[0]=='C':
            y_train.append(0) # Covid
        elif folder.name[0]=='V':
            y_train.append(1) # Viral Pneumonia
        else:
            y_train.append(2) # Normal

X_train = np.array(X_train)
y_train = np.array(y_train)
# We have 1955 training samples in total

# Image Augmentation

X_aug = []
y_aug = []

for i in range(0, len(y_train)):
    X_new = np.fliplr(X_train[i])
    X_aug.append(X_new)
    y_aug.append(y_train[i])

X_aug = np.array(X_aug)
y_aug = np.array(y_aug)

X_train = np.append(X_train, X_aug, axis=0) # appending augmented images to original training samples

# We have splitted our data in a way that - 
# 1. The samples are shuffled
# 2. The ratio of each class is maintained (stratify)
# 3. We get same samples every time we split our data (random state)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.15, shuffle=True, stratify=y_train, random_state=123)

# we will use 3323 images for training the model
# we will use 587 images for validating the model's performance

# Load pretrained model (best saved one)
with open('./Saved Model/covid_classifier_model.json', 'r') as json_file:
    json_savedModel= json_file.read()
    
# load the model  
model = tf.keras.models.model_from_json(json_savedModel)
model.load_weights('./Saved Model/covid_classifier_weights.h5')
model.compile(loss = 'sparse_categorical_crossentropy', optimizer=optimizers.Adam(learning_rate=0.0001), metrics= ["accuracy"])

# Converting the saved model to TFLite Model
import tensorflow_model_optimization as tfmot
quantize_model = tfmot.quantization.keras.quantize_model
# q_aware stands for for quantization aware.
q_aware_model = quantize_model(model)
# `quantize_model` requires a recompile.
q_aware_model.compile(optimizer=optimizers.Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# retraining the model for better accuracy
history = q_aware_model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs = 5)

# Testing the quantised model

X_test = [] # To store test images
y_test = [] # To store test labels

test_path = './dataset/test/'

for folder in os.scandir(test_path):
    for entry in os.scandir(test_path + folder.name):

        X_test.append(read_and_preprocess(test_path + folder.name + '/' + entry.name))
        
        if folder.name[0]=='C':
            y_test.append(0)
        elif folder.name[0]=='V':
            y_test.append(1)
        else:
            y_test.append(2)
            
X_test = np.array(X_test)
y_test = np.array(y_test)

# making predictions
predictions = q_aware_model.predict(X_test)

# Obtain the predicted class from the model prediction
predict = []

for i in predictions:
  predict.append(np.argmax(i))

predict = np.asarray(predict)

# Obtain the accuracy of the model
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, predict)
print(accuracy)

# Obtain the complete classification report of the model
from sklearn.metrics import classification_report
report = classification_report(y_test, predict)
print(report)

# Finally saving the Quantised model
converter = tf.lite.TFLiteConverter.from_keras_model(q_aware_model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

tflite_qaware_model = converter.convert()

with open("covid_classifier.tflite", 'wb') as f:
    f.write(tflite_qaware_model)