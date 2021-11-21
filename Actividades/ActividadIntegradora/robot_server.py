from flask import Flask, request, jsonify
from robot_agents import *
from robot_model import	*


# Initial variables
AGENTS = 5
WIDTH = 20
HEIGHT = 20
BOXES = 25
MODEL = None

# App initialization
app = Flask("Robot example")

# Initial route
@app.route('/init', methods=['POST', 'GET'])
def init_model():
    if request.method == 'POST':
        pass