""" Robot Model Server

Runs a Flask server to send and receive information using 
JSON objects in order to exchange the agents' paths on each step
for waypoints to be generated by a third-party.
"""

__author__ = "Raúl Youthan Irigoyen Osorio"

from typing import Any
from flask import Flask, request, jsonify
from robot_agents import *
from robot_model import *

# Initial variables
agents = 5
width = 20
height = 20
boxes = 25
step = 0
depot_x = 2
depot_y = 2
max_steps = 0
robot_model = None

# App initialization
app = Flask("Robot example")


# Sort a list using a tuple's first element
def get_first_in(elem: tuple) -> Any:
    return elem[0]


# Return a list with the second element of each tuple in a given list
def get_second_elems_from(arr: list) -> list[Any]:
    return [elem[1] for elem in arr]


# Route to initialize model
@app.route("/init", methods=["POST", "GET"])
def init_model():
    global agents, width, height, boxes, robot_model, step, depot_x, depot_y, max_steps
    if request.method == "POST":
        # Define model's initial variables
        agents = int(request.form.get("agents"))
        width = int(request.form.get("width"))
        height = int(request.form.get("height"))
        boxes = int(request.form.get("boxes"))
        depot_x = int(request.form.get("depot_x"))
        depot_y = int(request.form.get("depot_y"))
        max_steps = int(request.form.get("max_steps"))
        step = 0
        # Initialize model
        print(agents, boxes, width, height, depot_x, depot_y, max_steps)
        print(request.form)
        robot_model = RobotModel(agents, width, height, boxes, depot_x,
                                 depot_y, max_steps)
        # Return JSON message if post method was OK
        return jsonify({"message": "accepted"})


# Get trajectories from robots
@app.route("/getRobotPath", methods=["GET"])
def get_robot_path():
    global robot_model
    robot_position_tuples, robot_positions = [], []
    if request.method == "GET":
        for (a, x, z) in robot_model.grid.coord_iter():
            if len(a) > 0:
                for agent in a:
                    if agent.type_id == agt.ROBOT:
                        print("Added robot to list")
                        robot_position_tuples.append((agent.unique_id, {
                            "x": x,
                            "y": 0,
                            "z": z
                        }))
        robot_position_tuples.sort(key=get_first_in)
        robot_positions = get_second_elems_from(robot_position_tuples)
        print(robot_position_tuples)
        return jsonify({"positions": robot_positions})


# Get trajectories from boxes
@app.route("/getBoxPath", methods=["GET"])
def get_box_path():
    global robot_model
    box_position_tuples, box_positions = [], []
    if request.method == "GET":
        for (a, x, z) in robot_model.grid.coord_iter():
            if len(a) > 0:
                for agent in a:
                    if agent.type_id == agt.BOX:
                        print("Added box to list")
                        y = agent.y_pos
                        box_position_tuples.append((agent.unique_id, {
                            "x": x,
                            "y": y,
                            "z": z
                        }))
        box_position_tuples.sort(key=get_first_in)
        print(box_position_tuples)
        box_positions = get_second_elems_from(box_position_tuples)
        return jsonify({"positions": box_positions})


# Get trajectories from depots
@app.route("/getDepotPath", methods=["GET"])
def get_depot_path():
    global robot_model
    depot_positions = []
    if request.method == "GET":
        for (a, x, z) in robot_model.grid.coord_iter():
            if len(a) > 0:
                for agent in a:
                    if agent.type_id == agt.DEPOT:
                        print("Added depot to list")
                        depot_positions.append({"x": x, "y": 0, "z": z})
                        print(depot_positions)
        return jsonify({"positions": depot_positions})


# Make model advance one step further
@app.route("/step", methods=["GET"])
def update_model():
    global robot_model, step
    if request.method == "GET":
        robot_model.step()
        step += 1
        return jsonify({"step": step})

if __name__ == "__main__":
    app.run(host="localhost", port=8585, debug=True)
   