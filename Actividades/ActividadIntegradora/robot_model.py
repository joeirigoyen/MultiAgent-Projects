"""Robot Model

Initializes a model using the mesa multi-agent package in order to let
a series of agents look for boxes so they can be stacked in depots using a
cooperative system. 

This file can also be imported as a module to run it separately in other projects.
"""

__author__ = "Raúl Youthan Irigoyen Osorio"

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from robot_agents import *
from agent_types import *


class RobotModel(Model):
    def __init__(self, agents: int, width: int, height: int, boxes: int,
                 depot_x: int, depot_y: int, max_steps: int) -> None:
        # Initialize grid and activation attributes
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True
        # Initialize model attributes
        self.found_boxes = list()
        self.depot_stacks = dict()
        self.agents = agents
        self.width = width
        self.height = height
        self.boxes = boxes
        self.depots = depot_x * depot_y
        self.current_steps = 0
        self.max_steps = max_steps
        # Create depot attributes
        self.starting_depot_x = width // 2 - depot_x // 2
        self.starting_depot_y = height // 2 - depot_y // 2
        # Create global counters
        self.total_agent_count = 0
        self.stacked_boxes = 0
        for i in range(depot_x):
            for j in range(depot_y):
                # Initialize depot
                depot = Depot(self.total_agent_count, self)
                self.schedule.add(depot)
                self.total_agent_count += 1
                # Add depot to grid
                self.grid.place_agent(
                    depot,
                    (self.starting_depot_x + i, self.starting_depot_y + j))
                # Add depot's stack count to a dictionary using it's position as the key
                self.depot_stacks[(self.starting_depot_x + i,
                                   self.starting_depot_y + j)] = 0
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
        rand_pos = lambda w, h: (self.random.randrange(w),
                                 self.random.randrange(h))
        pos = rand_pos(self.grid.width, self.grid.height)
        while not self.grid.is_cell_empty(pos):
            pos = rand_pos(self.grid.width, self.grid.height)
        return pos

    def is_available_robot_space(self, pos: tuple) -> bool:
        contents = self.grid.get_cell_list_contents(pos)
        if len(contents) > 0:
            for c in contents:
                if c.type_id == agt.BOX:
                    if not c.finished:
                        return False
                elif c.type_id == agt.ROBOT:
                    return False
            return True
        else:
            return True

    def step(self):
        if self.stacked_boxes < self.boxes and self.stacked_boxes < self.depots * 5 and self.current_steps < self.max_steps:
            self.schedule.step()
            self.current_steps += 1
        else:
            self.running = False
