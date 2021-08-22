def classify(url):
    import json
    import requests

    URL = "http://delta-diagnose-api.herokuapp.com/"

    PARAMS = {
        "url" : url
    }
    r = requests.post(url = URL, json=PARAMS)
    data = r.json()
    print(data)
    return data