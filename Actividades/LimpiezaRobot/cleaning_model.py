from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

# Get count of all the current dirty cells
def get_dirty_cells(model: Model) -> int:
    return model.dirty_cells_count


class CleaningModel(Model):
    def __init__(self, agents: int, M: int, N: int, dirty_percent: int) -> None:
        # Define attributes
        self.num_agents = agents
        self.total_cells = M * N
        self.dirty_cells_count = int(self.total_cells * (dirty_percent / 100))
        self.dirty_cells = dict()
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(M, N, True)
        self.ticks = 0
        self.running = True
        # Create agents
        for i in range(self.num_agents):
            # Initialize agent
            agent = CleaningAgent(i, self)
            self.schedule.add(agent)
            # Add agent to grid
            x = 1
            y = 1
            self.grid.place_agent(agent, (x, y))
        # Create dirty cells
        for i in range(self.dirty_cells_count):
            # Create cell
            while(True):
                x = self.random.randrange(M)
                y = self.random.randrange(N)
                if ((x, y) not in self.dirty_cells):
                    self.dirty_cells[(x, y)] = 1
                    break
        # Create data collector
        self.dirtycell_datacollector = DataCollector(model_reporters={"Dirty Cells": get_dirty_cells}, agent_reporters={"Moves": "moves"})

    # Perform actions on each step
    def step(self): 
        if (self.dirty_cells_count > 0):
            self.ticks += 1
        self.dirtycell_datacollector.collect(self)
        self.schedule.step()
        

class CleaningAgent(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        # Initialize agent moves
        self.moves = 0
        self.found_dirty = False

    # Move an agent to a random direction
    def move(self) -> None:
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_pos = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_pos)
        self.moves += 1

    # Check if a cell is dirty and clean it
    def clean_cell(self) -> None:
        # Check if current position is within the dirty cells dictionary
        if self.pos in self.model.dirty_cells:
            # Check if current cell is dirty
            if self.model.dirty_cells[self.pos] == 1:
                # Clean cell
                self.model.dirty_cells[self.pos] = 0
                self.model.dirty_cells_count -= 1
                self.found_dirty = True
            else:
                self.found_dirty = False
        else:
            self.found_dirty = False

    def step(self) -> None:
        # Try to clean cell
        self.clean_cell()
        # If agent did not clean a cell, move to a random position
        if not self.found_dirty:
            self.move()
            