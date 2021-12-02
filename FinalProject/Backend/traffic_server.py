__author__ = "Raúl Youthan Irigoyen Osorio"

from flask import Flask, request, jsonify
from mesa import agent
from traffic_agents import *
from traffic_model import *

# Set initial variables' values
max_steps = 1000
cars = 20
step = 0
model = None

# Initialize app
app = Flask("Traffic Model")


# Return the key needed to sort the cars' positions list
def get_key(elem: tuple) -> int:
    return elem[0]


# Return a list with the second element of each tuple within a list
def get_second_from(arr: list) -> list:
    return [elem[1] for elem in arr]


# Route to initialize model
@app.route("/begin", methods=["POST", "GET"])
def start_model():
    global max_steps, model
    if request.method == "POST":
        # Once a form has been received, set initial values
        cars = int(request.form.get("cars"))
        max_steps = int(request.form.get("max_steps"))
        # Start model
        model = TrafficModel(cars, max_steps)
        # Return JSON message if post method completed
        print(f"Model initialized [cars: {cars} max_steps: {max_steps}]")
        return jsonify({"status": "OK"}) 


# Get trajectories from cars
@app.route("/cars", methods=["GET"])
def get_cars_paths():
    global model
    if request.method == "GET":
        # Make a list with unique id's and positions, and one with positions only
        car_full_tuples, car_positions = [], []
        # Iterate through the positions in every car
        for (agents, x, z) in model.grid.coord_iter():
            # If the agent list has content, keep adding positions to the lists
            if len(agents) > 0:
                for a in agents:
                    if a.type_id == agt.CAR:
                        car_full_tuples.append((a.unique_id, {"x": x - 0.25, "y": 0, "z": z - 0.25}))
        car_full_tuples.sort(key=get_key)
        car_positions = get_second_from(car_full_tuples)
        return jsonify({"positions": car_positions})


# Get positions from lights
@app.route("/lightsPositions", methods=["GET"])
def get_lights_positions():
    global model
    if request.method == "GET":
        # Make a list with unique id's and positions, and one with positions only
        light_full_tuples, light_positions = [], []
        # Iterate through the positions in every car
        for (agents, x, z) in model.grid.coord_iter():
            # If the agent list has content, keep adding positions to the lists
            if len(agents) > 0:
                for a in agents:
                    if a.type_id == agt.LIGHT:
                        light_full_tuples.append((a.unique_id, {"x": x, "y": 0, "z": z}))
        light_full_tuples.sort(key=get_key)
        light_positions = get_second_from(light_full_tuples)
        return jsonify({"positions": light_positions})
    

# Get states from lights
@app.route("/lightStates", methods=["GET"])
def get_lights_states():
    global model
    if request.method == "GET":
        # Make a list with unique id's and positions, and one with positions only
        light_full_tuples, light_states = [], []
        # Iterate through the positions in every car
        for (agents, _, _) in model.grid.coord_iter():
            # If the agent list has content, keep adding positions to the lists
            if len(agents) > 0:
                for a in agents:
                    if a.type_id == agt.LIGHT:
                        light_full_tuples.append((a.unique_id, {"x": int(a.state), "y": 0, "z": 0}))
        light_full_tuples.sort(key=get_key)
        light_states = get_second_from(light_full_tuples)
        return jsonify({"positions": light_states})
    
    
# Get states from lights
@app.route("/carStates", methods=["GET"])
def get_cars_states():
    global model
    if request.method == "GET":
        # Make a list with unique id's and positions, and one with positions only
        car_full_tuples, car_states = [], []
        # Iterate through the positions in every car
        for (agents, _, _) in model.grid.coord_iter():
            # If the agent list has content, keep adding positions to the lists
            if len(agents) > 0:
                for a in agents:
                    if a.type_id == agt.CAR:
                        car_full_tuples.append((a.unique_id, {"x": int(a.has_arrived), "y": 0, "z": 0}))
        car_full_tuples.sort(key=get_key)
        car_states = get_second_from(car_full_tuples)
        print(car_states)
        return jsonify({"positions": car_states})


# Make model advance one step further
@app.route("/step", methods=["GET"])
def update_model():
    global robot_model, step, model
    if request.method == "GET":
        model.step()
        step += 1
        return jsonify({"step": step})


if __name__ == "__main__":
    app.run(host="localhost", port=8585, debug=True)
