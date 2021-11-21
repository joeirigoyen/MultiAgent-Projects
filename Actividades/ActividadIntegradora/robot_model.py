from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from robot_agents import *
from agent_types import *


class RobotModel(Model):
    def __init__(self, agents: int, width: int, height: int, boxes: int) -> None:
        # Initialize attributes
        self.grid = MultiGrid(width, height, False)
        self.found_boxes = list()
        self.depots = dict()
        self.agents = agents
        self.width = width
        self.height = height
        self.boxes = boxes
        self.schedule = RandomActivation(self)
        self.running = True
        # Create depot area (2x2)
        self.starting_depot_x = width // 2 - 1
        self.starting_depot_y = height // 2 - 1
        self.total_agent_count = 0
        for i in range(2):
            for j in range(2):
                # Initialize depot
                depot = Depot(self.total_agent_count, self)
                self.schedule.add(depot)
                self.total_agent_count += 1
                # Add depot to grid
                self.grid.place_agent(depot, (self.starting_depot_x + i, self.starting_depot_y + j))
                # Add depot's stack count to a dictionary using it's position as the key
                self.depots[(self.starting_depot_x + i, self.starting_depot_y + j)] = 0
        # Create boxes
        for i in range(boxes):
            # Initialize box
            box = Box(self.total_agent_count, self)
            self.schedule.add(box)
            self.total_agent_count += 1
            # Add box to grid
            pos = self.get_unique_pos()
            self.grid.place_agent(box, pos)
        # Create robots
        for i in range(agents):
            # Initialize robot
            robot = Robot(self.total_agent_count, self)
            self.schedule.add(robot)
            self.total_agent_count += 1
            # Add robot to grid
            pos = self.get_unique_pos()
            self.grid.place_agent(robot, pos)
    
    def get_unique_pos(self) -> tuple:
        rand_pos = lambda w, h: (self.random.randrange(w), self.random.randrange(h))
        pos = rand_pos(self.grid.width, self.grid.height)
        while not self.grid.is_cell_empty(pos):
            pos = rand_pos(self.grid.width, self.grid.height)
        return pos
    
    def is_available_robot_space(self, pos: tuple) -> bool:
        contents = self.grid.get_cell_list_contents(pos)
        if len(contents) > 0:
            for c in contents:
                if c.type_id == agt.BOX or c.type_id == agt.DEPOT or c.type_id == agt.ROBOT:
                    return False
            return True
        return True
    
    def step(self):
        self.schedule.step()