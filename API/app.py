from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from io import BytesIO
from PIL import Image
import numpy as np
import tensorflow as tf
import urllib.request

description = """
This API helps you classify Chest MRI images as COVID-19, Viral Pneumonia or Normal. 🚀

## How to use it?
- Send a POST request on [https://delta-diagnose-api.herokuapp.com/](https://delta-diagnose-api.herokuapp.com/) with a JSON file containing url of the image you want to classify.
- Alternatively, try uploading the image directly on this page using try-it-out functionality in predict_image route.

## Response Format
It will return you 2 two things - 
1. class - covid/viral_pneumonia/normal (String Datatype)
2. class_probablity - The probablity by which model is predicting that the image belongs to the given class (Float Datatype)

You are free to use this API in your own Applications. Please use it responsibly and consider giving a star on its GitHub Repo. 
"""

app = FastAPI(
    title="Delta Diagnose API",
    version="2.1",
    description=description,
    contact={
        "name": "Delta Diagnose",
        "url": "https://github.com/kanakmi/Delta-Diagnose"
    }
)

interpreter = tf.lite.Interpreter(model_path='./saved_model/covid_classifier.tflite')
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test model on random input data.
input_shape = input_details[0]['shape']
output_shape = output_details[0]['shape']

labels = {0: "covid", 1: "viral_pneumonia", 2: "normal"}

def classify_image(img):
    img = img.convert("RGB")
    img = img.resize((256, 256))
    img = np.array(img, dtype='Float32')
    img = img/255
    img = img.reshape((1, 256, 256, 3))
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])
    pred = np.argmax(predictions[0])
    result = {
        'class': labels[pred],
        'class_probablity': np.round(predictions[0][pred]*100,2)
    }
    return result

class img_url(BaseModel):
    url: str

    class Config:
        schema_extra = {
            "example": {
                "url" : "https://i.ibb.co/FBSztPS/0120.jpg"
            }
        }

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

@app.post(
    "/predict_image", 
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "class": "covid",
                        "class_probablity": 97.42
                    }
                }
            }
        }
    }
)
async def predict(
    file: UploadFile = File(...)
):
    image = Image.open(BytesIO(await file.read()))
    response = classify_image(image)
    return response

@app.post(
    "/",
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "class": "viral_pneumonia",
                        "class_probablity": 99.94
                    }
                }
            }
        }
    }
)
async def classify_url(item: img_url):
    req = urllib.request.urlretrieve(item.url, "saved")
    image = Image.open("saved")
    response = classify_image(image)
    return response