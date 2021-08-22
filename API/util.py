import numpy as np
import cv2
import tensorflow as tf
import urllib

with open('./saved_model/covid_classifier_model.json', 'r') as json_file:
    json_savedModel = json_file.read()

# load the model architecture
model = tf.keras.models.model_from_json(json_savedModel)
model.load_weights('./saved_model/covid_classifier_weights.h5')
opt = tf.keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=opt, loss="sparse_categorical_crossentropy", metrics=["accuracy"])

labels = {0: "covid", 1: "viral_pneumonia", 2: "normal"}

def classify_image(image_url):
    req = urllib.request.urlopen(image_url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    img = cv2.resize(img,(256,256))
    img = np.array(img)
    img = img/255
    img = img.reshape((1, 256, 256, 3))
    predictions = model.predict(img)
    result = {
        'class': labels[np.argmax(predictions[0])],
        'class_probablity': np.round(max(predictions[0])*100,2)
    }
    return result