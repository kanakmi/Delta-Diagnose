import util
from fastapi import FastAPI
from pydantic import BaseModel

description = """
This API helps you classify Chest MRI images as COVID-19, Viral Pneumonia or Normal. 🚀

## How to use it?
Send a POST request on [https://delta-diagnose-api.herokuapp.com/](https://delta-diagnose-api.herokuapp.com/) with a JSON file containing url of the image you want to classify. <br>
It will return you 2 two things - 
1. class - covid/viral_pneumonia/normal (String Datatype)
2. class_probablity - The probablity by which model is predicting that the image belongs to the given class (Float Datatype)

You are free to use this API in your own Applications.
"""

app = FastAPI(
    title="Delta Diagnose API",
    version="2.0",
    description=description,
    contact={
        "name": "Delta Diagnose",
        "url": "https://github.com/kanakmi/Delta-Diagnose"
    }
)

class img_url(BaseModel):
    url: str

    class Config:
        schema_extra = {
            "example": {
                "url" : "https://i.ibb.co/FBSztPS/0120.jpg"
            }
        }

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
async def classify_image(item: img_url):
    response = util.classify_image(item.url)
    return response