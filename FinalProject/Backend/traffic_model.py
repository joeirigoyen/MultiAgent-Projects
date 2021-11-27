from mesa import Model
from mesa.time import RandomActivation
from mesa.space import Grid, MultiGrid
from traffic_agents import *
from agent_types import AgentTypes as agt
from directions import Directions as dirs
from grid_manager import *

COLS = 26
ROWS = 26
CARS = 11


class TrafficModel(Model):
    def __init__(self, max_steps: int) -> None:
        # Define model attributes
        self.cols = COLS
        self.rows = ROWS
        self.grid = MultiGrid(COLS, ROWS, False)
        self.schedule = RandomActivation(self)
        self.running = True
        # Define class attributes
        self.cars = CARS
        self.max_steps = max_steps
        self.arrivals = 0
        self.agent_uid = 0
        # Initialize standard car map and destination list
        self.standard_map = make_grid(ROWS, COLS, self)
        self.destinations = []
        # Create agents using a text file
        with open("Backend\\map.txt") as m:
            # Initialize agents from txt file
            lines = m.readlines()
            for row in range(len(lines)):
                # For every character in a line, check which agent to make depending on the character
                for col in range(len(lines[row])):
                    agent = None
                    if lines[row][col] == "s":
                        # Create light agent
                        agent = Light(self.agent_uid, self)
                        if lines[row][col - 1] == "<" or lines[row][col + 1] == "<":
                            agent.direction = dirs.LEFT
                            self.standard_map[row][col].direction = dirs.LEFT
                        elif lines[row][col - 1] == ">" or lines[row][col + 1] == ">":
                            agent.direction = dirs.RIGHT
                            self.standard_map[row][col].direction = dirs.RIGHT
                    elif lines[row][col] == "S":
                        # Create light agent
                        agent = Light(self.agent_uid, self)
                        if lines[row - 1][col] == "^" or lines[row + 1][col] == "^":
                            agent.direction = dirs.UP
                            self.standard_map[row][col].direction = dirs.UP
                        elif lines[row - 1][col] == "v" or lines[row + 1][col] == "v":
                            agent.direction = dirs.DOWN
                            self.standard_map[row][col].direction = dirs.DOWN
                    elif lines[row][col] == "#":
                        # Create building agents
                        agent = Building(self.agent_uid, self)
                        self.standard_map[row][col].state = NodeTypes.OBSTACLE
                    elif lines[row][col] == "D":
                        # Create destination point
                        agent = Destination(self.agent_uid, self)
                        self.destinations.append(agent)
                    # If cell is part of the road, assign it's direction
                    elif lines[row][col] == "^":
                        self.standard_map[row][col].direction = dirs.UP
                    elif lines[row][col] == "v":
                        self.standard_map[row][col].direction = dirs.DOWN
                    elif lines[row][col] == "<":
                        self.standard_map[row][col].direction = dirs.LEFT
                    elif lines[row][col] == ">":
                        self.standard_map[row][col].direction = dirs.RIGHT
                    # If agent is not None, add agent to the model's grid
                    if agent:
                        self.schedule.add(agent)
                        self.grid.place_agent(agent, (row, col))
                        self.agent_uid += 1
        # Set directions of every node
        init_neighborhood(self.standard_map)

        # Add cars in random positions without crashing them beforehand
        for _ in range(self.cars):
            car_pos = self.get_unique_pos()
            car = Car(self.agent_uid, self, car_pos)
            self.schedule.add(car)
            self.grid.place_agent(car, car_pos)
            self.agent_uid += 1
            

    # Get a position where a cell is empty
    def get_unique_pos(self) -> tuple:
        random_pos = lambda r, c: (self.random.randrange(r), self.random.randrange(c))
        new_pos = random_pos(self.rows, self.cols)
        while not self.grid.is_cell_empty(new_pos):
            new_pos = random_pos(self.rows, self.cols)
        return new_pos

    # Get a destination from the destination list
    def get_unique_destination(self) -> tuple or None:
        if len(self.destinations) > 0:
            return self.destinations.pop()
        else:
            return None

    def step(self) -> None:
        # If the number of cars that have arrived to their destinations are still less than the number of cars, keep running
        if self.arrivals < self.cars and self.schedule.steps < self.max_steps:
            # Advance one step
            self.schedule.step()
            # Change the lights' state every 10 steps
            if self.schedule.steps % 10 == 0:
                for agent in self.schedule.agents:
                    if agent.type_id == agt.LIGHT:
                        agent.state = not agent.state
        else:
            self.running = False
