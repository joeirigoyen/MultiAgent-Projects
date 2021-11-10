from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules.ChartVisualization import ChartModule
from cleaning_model import CleaningModel
from histogram_module import HistogramModule

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


grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
chart = ChartModule([{"Label": "Dirty cells", "Color": "orange"}], data_collector_name='dirtycell_datacollector')
histogram = HistogramModule(list(range(10)), 100, 200)
server = ModularServer(CleaningModel, [grid, histogram, chart], "Cleaning Model", {"agents": 10, "M": 20, "N": 20, "dirty_percent": 99})
server.port = 8521

server.launch()