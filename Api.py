from flask import Flask
from flask import request
import random
import string
from ApiHelper import APIHelper

app = Flask(__name__)

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

helpers = {}

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/getRiskMap")
def get_risk_map():
    location = request.args.get('location')
    box = request.args.get('box')
    name = request.args.get('name')
    accuracy = request.args.get('accuracy')
    id = randomString()
    helper = APIHelper()
    helpers[id] = helper
    helper.get_risk_map(location, box, name, accuracy)
    return id

@app.route("/getProgress")
def get_progress():
    id = request.args.get('id')
    helper = helpers[id]
    return helper.get_progress()

@app.route("/download")
def get_progress():
    id = request.args.get('id')
    helper = helpers[id]
    return helper.get_progress(id)
        

if __name__ == "__main__":
    app.run()