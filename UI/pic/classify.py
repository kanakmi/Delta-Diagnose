def classify(url):
    import json
    import requests

    URL = "http://covidclassifier.herokuapp.com/classify_image"

    PARAMS = {
        "url" : url
    }
    r = requests.post(url = URL, json=PARAMS)
    data = r.text
    return data