"""Robot Model Visualizer

Utilizes robot_model and robot_agents to create a visual grid
containing the agents' positions on each step in order for the 
project to be easily debugged and interpreted.
"""

__author__ = "Raúl Youthan Irigoyen Osorio"

from mesa import Agent
from mesa.visualization.modules import CanvasGrid, BarChartModule, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from robot_model import RobotModel
from agent_types import AgentType as agt

AGENTS = 5
WIDTH = 10
HEIGHT = 10
BOXES = 45
DEPOT_X = 3
DEPOT_Y = 3
DEPOTS = DEPOT_X * DEPOT_Y
MAX_STEPS = 300
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

model = RobotModel(AGENTS, WIDTH, HEIGHT, BOXES, DEPOT_X, DEPOT_Y, MAX_STEPS)


def agent_portrayal(agent: Agent) -> dict[str, str]:
    portrayal = {"Filled": "true"}
    if agent.type_id == agt.ROBOT:
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
        if agent.unique_id == BOXES + (DEPOTS) + 1:
            portrayal["Color"] = "#cc0e04"
        elif agent.unique_id == BOXES + (DEPOTS) + 2:
            portrayal["Color"] = "#27ccdb"
        elif agent.unique_id == BOXES + (DEPOTS) + 3:
            portrayal["Color"] = "#109c06"
        elif agent.unique_id == BOXES + (DEPOTS) + 4:
            portrayal["Color"] = "#ff8812"
        else:
            portrayal["Color"] = "#0500a3"
    if agent.type_id == agt.BOX:
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.3
        portrayal["Color"] = "red"
    if agent.type_id == agt.DEPOT:
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 0
        portrayal["r"] = 1
        portrayal["Color"] = "black"
    return portrayal


if __name__ == "__main__":
    grid = CanvasGrid(agent_portrayal, WIDTH, HEIGHT, CANVAS_WIDTH,
                      CANVAS_HEIGHT)
    bar_chart = BarChartModule([{
        "label": "Moves",
        "Color": "#AA0000"
    }],
                               scope="agent",
                               sorting="ascending",
                               sort_by="Moves")
    server = ModularServer(
        RobotModel,
        [grid],
        "Robot Model",
        {
            "agents": AGENTS,
            "width": WIDTH,
            "height": HEIGHT,
            "boxes": BOXES,
            "depot_x": DEPOT_X,
            "depot_y": DEPOT_Y,
            "max_steps": MAX_STEPS
        },
    )
    server.port = 8521
    server.launch()
