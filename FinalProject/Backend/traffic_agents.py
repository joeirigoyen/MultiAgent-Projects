from mesa import Agent, Model
from directions import Directions
from agent_types import AgentTypes as agt
from directions import Directions as dirs
from grid_manager import NodeTypes
from astar import *


# Represents a building, not much will be happening with this agent since it's not even going to be added to the scheduler
class Building(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.type_id = agt.BUILDING # Set the type of agent as Building


# Represents a traffic light, has a direction since it's part of the road, and a state for the cars to check and decide if they will advance
class Light(Agent):
    def __init__(self, unique_id: int, model: Model, direction: Directions) -> None:
        super().__init__(unique_id, model)
        self.type_id = agt.LIGHT                                                        # Agent type
        self.direction = direction                                                      # Direction of the road 
        self.state = False if direction == dirs.UP or direction == dirs.DOWN else True  # Initial state depending on it's direction


# Represents the place where a car will try to get to
class Destination(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)  
        self.type_id = agt.DESTINATION  # Agent type
        self.occupied = False           # Determines if a destination has a car inside it (obsolete after implementation of new car spawns)


# Represents a car within the model
class Car(Agent):
    def __init__(self, unique_id: int, model: Model, start_pos: tuple) -> None:
        super().__init__(unique_id, model)
        # Set initial attributes
        self.type_id = agt.CAR                                          # Agent type
        self.destination = self.random.choice(self.model.destinations)  # Random destination from the model's destinations list
        self.has_arrived = False                                        # Contains if the car has arrived or not
        # Set start and end in map                                      
        self.map = model.standard_map                                   # A copy of the model's graph
        self.map[start_pos[0]][start_pos[1]].state = NodeTypes.START
        self.map[self.destination.pos[0]][self.destination.pos[1]].state = NodeTypes.END
        # Find path to destination
        self.path = get_shortest_path(self.map, self.map[start_pos[0]][start_pos[1]], self.map[self.destination.pos[0]][self.destination.pos[1]], model)
        self.next_cell = None
        self.last_dir = self.map[start_pos[0]][start_pos[1]].direction
        self.turn_dir = None
        self.main_av = False

    # Check if destination cell is within the neighborhood
    def check_destination(self, neighborhood: list) -> tuple:
        # Check every cell in neighborhood
        for cell in neighborhood:
            # Check the content in every cell
            content = self.model.grid.get_cell_list_contents(cell)
            # Check every agent within the cell's content
            for agent in content:
                # Set next position as the destination cell
                if agent.type_id == agt.DESTINATION:
                    return agent.pos    
        # If nothing was found, don't return anything
        return None

    # Return whether the car is on a main avenue or not
    def is_in_main_av(self) -> bool:
        # If car is in the first two columns or in the last two columns, return True
        if (self.pos[0] >= 0 and self.pos[0] < 2) and (self.pos[0] >= self.model.cols - 2 and self.pos[0] < self.model.cols):
            return True
        # If car is in the first two rows or in the last two rows, return True
        elif (self.pos[1] >= 0 and self.pos[1] < 2) and (self.pos[1] >= self.model.rows - 2 and self.pos[1] < self.model.rows):
            return True
        # Otherwise, return False
        else:
            return False

    # Get the direction of the car's next move
    def get_turn_dir(self) -> tuple:
        return (self.next_cell[0] - self.pos[0], self.next_cell[1] - self.pos[1])
    
    # Check if a car will let other car go first in a cell
    def give_priority(self, other: Agent) -> bool:
        # If the car is in the main avenue but the other isn't, don't give priority
        if self.main_av and not other.main_av:
            return False
        # If this car is not in the main avenue but the other is, give priority
        elif not self.main_av and other.main_av:
            return True
        # If this car is going straight and the other car is going to turn
        elif self.turn_dir == self.last_dir and other.turn_dir != other.last_dir:
            return False
        # If both cars are going to turn
        elif other.turn_dir != other.last_dir and self.turn_dir != self.last_dir:
            return True
        # If both cars are going straight
        else:
            return True

    # Check if next cell is being targeted by other agents and return if car can go to it
    def can_get_to_next_cell(self) -> bool:
        # If next cell is not the car's destination, check if it can move towards it
        if self.next_cell != self.destination.pos:
            # If next cell is empty:
            if self.model.grid.is_cell_empty(self.next_cell):
                # Get next cell's neighbors
                next_neighbors = self.model.grid.get_neighborhood(self.next_cell, moore=False, include_center=False)
                # Remove self position from the neighborhood
                if self.pos in next_neighbors:
                    next_neighbors.remove(self.pos)
                # Check each cell within the neighborhood
                for cell in next_neighbors:
                    # Check each cell's contents
                    for agent in self.model.grid.get_cell_list_contents(cell):
                        # If there's a car in that cell, check if it's going to this cell too
                        if agent.type_id == agt.CAR:
                            if not agent.has_arrived:
                                # If they're going to the same cell, check if this car will let the other go first
                                if agent.next_cell == self.next_cell:
                                    return not self.give_priority(agent)
                # If no agents were found in that cell, let the car advance
                return True
            # Otherwise, check if the contents of the next cell contain a car
            else:
                contents = self.model.grid.get_cell_list_contents(self.next_cell)
                for agent in contents:
                    # If agent is a car, don't let it advance
                    if agent.type_id == agt.CAR:
                        return False
                # If no car was found, let the car advance
                return True
        # Else, just return True since it can move no matter what
        else:
            return True

    # Check if there are cars or lights in front of the car
    def has_green_light(self) -> bool:
        # If there's a light in the next cell, check if it's a light
        content = self.model.grid.get_cell_list_contents(self.next_cell)
        for agent in content:
            # If agent is a light, return it's state
            if agent.type_id == agt.LIGHT:
                return agent.state
        # If there is no light, advance to next cell
        return True

    # Try to move to the next cell
    def move_next(self) -> None:
        # Check if any other car is directed to the next cell
        if self.can_get_to_next_cell():
            # If there's a green light, advance to it
            if self.has_green_light():
                # Remove waypoint from path
                self.path.pop(0)
                # Move agent towards the next cell
                self.model.grid.move_agent(self, self.next_cell)

    # Return a boolean value representing if two cars are in the same position 
    def check_crashes(self) -> bool:
        # Get contents from current cell
        cell_content = self.model.grid.get_cell_list_contents(self.pos)
        # Remove self from content
        cell_content.remove(self)
        # Check if there's content in the cell other than self
        if len(cell_content) > 0:
            # Check every agent that is a car
            for agent in cell_content:
                if agent.type_id == agt.CAR:
                    # If the car's position is already in the car's definition, return false
                    if agent.pos == agent.destination.pos:
                        return False
                    # Otherwise, return true
                    else:
                        print(f"Crash in {self.pos}")
                        return True
            return False
        # Otherwise return false
        else:
            return False

    def step(self) -> None:
        # If car hasn't arrived to it's destination
        if not self.has_arrived:
            # Set car's current direction
            self.last_dir = self.map[self.pos[0]][self.pos[1]].direction
            # If path still has remaining cells, assign the first one to the car's next cell
            if len(self.path) > 0:
                # Remove the next cell from the path
                self.next_cell = self.path[0]
                self.turn_dir = self.get_turn_dir()
                self.main_av = self.is_in_main_av()
                self.turn_dir = self.map[self.next_cell[0]][self.next_cell[1]].direction
                # Try to move to the next cell
                self.move_next()
                # Check if car is in the same position as another car
                self.model.running = not self.check_crashes()
            # Otherwise, set the car's has_arrived attribute to True
            else:
                self.model.arrivals += 1
                self.has_arrived = True
