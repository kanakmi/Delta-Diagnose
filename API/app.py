from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/classify_image', methods=['POST'])
def classify_image():
    image_url = request.json["url"]

    response = jsonify(util.classify_image(image_url))

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    app.run()