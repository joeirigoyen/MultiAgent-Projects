from mesa import Agent
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from robot_model import RobotModel
from agent_types import AgentType as agt

AGENTS = 5
WIDTH = 10
HEIGHT = 10
BOXES = 20
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

model = RobotModel(AGENTS, WIDTH, HEIGHT, BOXES)

def agent_portrayal(agent) -> dict[str, str]:
    portrayal = {"Filled": "true"}
    if agent.type_id == agt.ROBOT:
        portrayal["Shape"] = "circle"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.5
        if agent.unique_id == BOXES + 4:
            portrayal["Color"] = "#cc0e04"
        elif agent.unique_id == BOXES + 5:
            portrayal["Color"] = "#27ccdb"
        elif agent.unique_id == BOXES + 6:
            portrayal["Color"] = "#109c06"
        elif agent.unique_id == BOXES + 7:
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


if __name__ == '__main__':
    grid = CanvasGrid(agent_portrayal, WIDTH, HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT)
    server = ModularServer(RobotModel, [grid], "Robot Model", {"agents": AGENTS, "width": WIDTH, "height": HEIGHT, "boxes": BOXES})
    server.port = 8521
    server.launch()
