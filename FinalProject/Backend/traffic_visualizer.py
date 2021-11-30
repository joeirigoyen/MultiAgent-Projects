import random
from mesa import Agent
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from agent_types import AgentTypes as agt
from traffic_model import TrafficModel

MAX_STEPS = 1000
MODEL = TrafficModel(MAX_STEPS)
GRID_WIDTH = 500
GRID_HEIGHT = 500


def agent_portrayal(agent: Agent) -> dict[str, str]:
    portrayal = {"Filled": "true",
                 "Shape": "circle"}

    r = lambda: random.randint(0,255)
    color = '#%02X%02X%02X' % (r(),r(),r())
    if agent.type_id == agt.CAR:
        portrayal["Layer"] = 2
        portrayal["r"] = 0.5
        portrayal["Color"] = color
    if agent.type_id == agt.BUILDING:
        portrayal["Layer"] = 0
        portrayal["r"] = 1.1
        portrayal["Color"] = "#192b36"
    if agent.type_id == agt.DESTINATION:
        portrayal["Layer"] = 1
        portrayal["r"] = 1
        portrayal["Color"] = "#b600d6"
    if agent.type_id == agt.LIGHT:
        portrayal["Layer"] = 0
        portrayal["r"] = 0.8
        if agent.state:
            portrayal["Color"] = "#00d62e"
        else:
            portrayal["Color"] = "#c20000"
    return portrayal

    
if __name__ == "__main__":
    grid = CanvasGrid(agent_portrayal, MODEL.cols, MODEL.rows, GRID_WIDTH, GRID_HEIGHT)
    server = ModularServer(TrafficModel, [grid], "Traffic Model", {"max_steps": MAX_STEPS})
    server.port = 8521
    server.launch()