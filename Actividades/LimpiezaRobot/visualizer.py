from re import A
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules.ChartVisualization import ChartModule
from cleaning_model import CleaningModel
from histogram_module import HistogramModule

COLS = 20
ROWS = 20
AGENTS = 5
DIRTYP = 50

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.4}
    
    if agent.found_dirty:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.6
    else:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
    
    return portrayal


grid = CanvasGrid(agent_portrayal, COLS, ROWS, 500, 500)
chart = ChartModule([{"Label": "Dirty cells", "Color": "orange"}], data_collector_name='dirtycell_datacollector')
histogram = HistogramModule(list(range(AGENTS)), 100, 200)
server = ModularServer(CleaningModel, [grid, histogram, chart], "Cleaning Model", {"agents": AGENTS  , "M": COLS, "N": ROWS, "dirty_percent": DIRTYP})
server.port = 8521

server.launch()