from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from traffic_agents import *
from agent_types import AgentTypes as agt
from directions import Directions as dirs
from grid_manager import *

COLS = 26
ROWS = 26
FILENAME = "D:\\irigx\\Documents\\School\\5to\\MAS\\MultiAgentes\\FinalProject\\Backend\\map.txt"

class TrafficModel(Model):
    def __init__(self, cars: int, max_steps: int) -> None:
        # Define model attributes
        self.cols = COLS
        self.rows = ROWS
        self.grid = MultiGrid(COLS, ROWS, False)
        self.schedule = RandomActivation(self)
        self.running = True
        # Define class attributes
        self.cars = cars
        self.max_steps = max_steps
        self.arrivals = 0
        self.agent_uid = 0
        # Initialize standard car map and destination list
        self.standard_map = make_grid(ROWS, COLS, self)
        self.destinations = []
        self.new_car_spawns = [[(0, 0), (0, 1)], [(self.cols - 1, self.rows - 1), (self.cols - 1, self.rows - 2)], [(0, self.rows - 1), (0, self.rows - 2)], [(self.cols - 1, 0), (self.cols - 1, 1)]]
        self.light_states = set()
        # Create agents using a text file
        with open(FILENAME) as m:
            # Initialize agents from txt file
            lines = m.readlines()
            for row in range(len(lines)):
                # For every character in a line, check which agent to make depending on the character
                for col in range(len(lines[row])):
                    agent = None
                    if lines[row][col] == "s":
                        # Create light agent
                        if lines[row][col - 1] == "<" or lines[row][col + 1] == "<":
                            agent = Light(self.agent_uid, self, dirs.LEFT)
                            self.standard_map[row][col].direction = dirs.LEFT
                            self.light_states.add((agent.unique_id, agent.state))
                        elif lines[row][col - 1] == ">" or lines[row][col + 1] == ">":
                            agent = Light(self.agent_uid, self, dirs.RIGHT)
                            self.standard_map[row][col].direction = dirs.RIGHT
                            self.light_states.add((agent.unique_id, agent.state))
                    elif lines[row][col] == "S":
                        # Create light agent
                        if lines[row - 1][col] == "^" or lines[row + 1][col] == "^":
                            agent = Light(self.agent_uid, self, dirs.UP)
                            self.standard_map[row][col].direction = dirs.UP
                            self.light_states.add((agent.unique_id, agent.state))
                        elif lines[row - 1][col] == "v" or lines[row + 1][col] == "v":
                            agent = Light(self.agent_uid, self, dirs.DOWN)
                            self.standard_map[row][col].direction = dirs.DOWN
                            self.light_states.add((agent.unique_id, agent.state))
                    elif lines[row][col] == "#":
                        # Create building agents
                        agent = Building(self.agent_uid, self)
                        self.standard_map[row][col].state = NodeTypes.OBSTACLE
                    elif lines[row][col] == "D":
                        # Create destination point
                        agent = Destination(self.agent_uid, self)
                        self.standard_map[row][col].state = NodeTypes.OBSTACLE
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
                        if agent.type_id != agt.BUILDING:
                            self.schedule.add(agent)
                        self.grid.place_agent(agent, (row, col))
                        self.agent_uid += 1
        # Set directions of every node
        print(self.light_states)
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
        if self.schedule.steps < self.max_steps:
            # Advance one step
            self.schedule.step()
            # Change the lights' state every 10 steps
            if self.schedule.steps % 10 == 0:
                for agent in self.schedule.agents:
                    if agent.type_id == agt.LIGHT:
                        agent.state = not agent.state
                # Create car agents in each entrance
                for i in range(len(self.new_car_spawns)):
                    car_pos = self.random.choice(self.new_car_spawns[i])
                    if self.grid.is_cell_empty(car_pos):
                        car = Car(self.agent_uid, self, car_pos)
                        self.schedule.add(car)
                        self.grid.place_agent(car, car_pos)
                        self.agent_uid += 1
            # Get every light's state
            new_states = set()
            for agent in self.schedule.agents:
                if agent.type_id == agt.LIGHT:
                    new_states.add((agent.unique_id, agent.state))
            self.light_states = new_states
            print(self.light_states)
        else:
            self.running = False    
