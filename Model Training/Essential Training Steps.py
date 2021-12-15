# import the required libraries

import numpy as np
import os
import cv2
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
import tensorflow as tf
from tensorflow.keras import layers, optimizers
from tensorflow.keras.layers import *
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Global Variables for later use

IMG_SIZE = 256
X_train = [] # To store train images
y_train = [] # To store train labels

train_path = './dataset/train/' # path containing training images
test_path = './dataset/test/' # path containing training images

model = None

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

            X.append(read_and_preprocess(train_path + folder.name + '/' + entry.name))
        
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

# Designing and Training the Model
def create_model():
    model = tf.keras.Sequential([
        Conv2D(filters=32, kernel_size=(2,2), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        MaxPooling2D((4,4)),
        
        Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'),
        MaxPooling2D((3,3)),
        Dropout(0.3), # for regularization
        
        Conv2D(filters=64, kernel_size=(4,4), activation='relu', padding='same'),
        Conv2D(filters=128, kernel_size=(5,5), activation='relu', padding='same'),
        MaxPooling2D((2,2)),
        Dropout(0.4),
        
        Conv2D(filters=128, kernel_size=(5,5), activation='relu', padding='same'),
        MaxPooling2D((2,2)),
        Dropout(0.5),
        
        Flatten(), # flattening for feeding into ANN
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.3),
        Dense(128, activation='relu'),
        Dense(3, activation='softmax')
    ])
    return model

# training the model
def train_model():
    global X_train, y_train, model

    # splitting the training data into training and validation
    X_train, X_val, y_train, y_val = split_data(test_size=0.15, random_state=123)
    # we will use 3323 images for training the model
    # we will use 587 images for validating the model's performance

    # Slowing down the learning rate
    opt = optimizers.Adam(learning_rate=0.0001)

    # compile the model
    model.compile(loss = 'sparse_categorical_crossentropy', optimizer=opt, metrics= ["accuracy"])

    # use early stopping to exit training if validation loss is not decreasing even after certain epochs (patience)
    earlystopping = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=20)

    # save the best model with least validation loss
    checkpointer = ModelCheckpoint(filepath="covid_classifier_weights.h5", verbose=1, save_best_only=True)

    history = model.fit(X_train, y_train, epochs = 100, validation_data=(X_val, y_val), batch_size=32, shuffle=True, callbacks=[earlystopping, checkpointer])

# save the model architecture to json file for future use
def save_model():
    global model
    model_json = model.to_json()
    with open("covid_classifier_model.json","w") as json_file:
        json_file.write(model_json)

# Load pretrained model (best saved one)
def load_model():
    with open('covid_classifier_model.json', 'r') as json_file:
        json_savedModel= json_file.read()
    # load the model  
    model = tf.keras.models.model_from_json(json_savedModel)
    model.load_weights('covid_classifier_weights.h5')
    opt = optimizers.Adam(learning_rate=0.0001)
    model.compile(loss = 'sparse_categorical_crossentropy', optimizer=opt, metrics= ["accuracy"])

# Evaluating the Trained Model
def evaluate_model():
    # Load pretrained model (best saved one)
    model = load_model()

    # reading the test data
    X_test, y_test = get_data(test_path)
    # We have 185 images for testing

    # making predictions
    predictions = model.predict(X_test)

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

def main():
    global X_train, y_train, model

    # reading the training data
    X_train, y_train = get_data(train_path)
    # We have 1955 training samples in total

    # applying image augmentation on training data
    image_augmentation()
    
    # designing the model architecture
    model = create_model()

    # training the model
    train_model()

    # saving the model
    save_model()

    # evaluating the saved model's performance
    evaluate_model()

if __name__ == "__main__":
    main()