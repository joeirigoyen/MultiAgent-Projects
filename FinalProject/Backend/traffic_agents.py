from random import randint
from re import A
from mesa import Agent, Model
from agent_types import AgentTypes as agt
from directions import Directions as dirs
from grid_manager import NodeTypes
from astar import *


class Building(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.type_id = agt.BUILDING
      
        
class Light(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.type_id = agt.LIGHT
        self.state = bool(randint(0, 1))
        self.direction = dirs.UP        


class Destination(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.type_id = agt.DESTINATION
        self.occupied = False


class Car(Agent):
    def __init__(self, unique_id: int, model: Model, start_pos: tuple) -> None:
        super().__init__(unique_id, model)
        # Set initial attributes
        self.type_id = agt.CAR
        self.destination = self.model.get_unique_destination()
        self.has_arrived = False
        # Set start and end in map
        self.map = model.standard_map
        self.map[start_pos[0]][start_pos[1]].state = NodeTypes.START
        self.map[self.destination.pos[0]][self.destination.pos[1]].state = NodeTypes.END
        # Find path to destination
        self.path = get_shortest_path(self.map, self.map[start_pos[0]][start_pos[1]], self.map[self.destination.pos[0]][self.destination.pos[1]])
        self.next_cell = self.path[0]
        self.last_dir = self.map[start_pos[0]][start_pos[1]].direction

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

    # Check if a car will let other car go first in a cell
    def give_priority(self, other: Agent):
        other_last_dir = other.last_dir
        if (other_last_dir == dirs.LEFT or other_last_dir == dirs.RIGHT) and (self.last_dir == dirs.UP or self.last_dir == dirs.DOWN):
            return False
        else:
            return True
    
    # Check if next cell is being targeted by other agents and return if car can go to it
    def can_get_to_next_cell(self) -> bool:
        print(f"Checking cell: {self.next_cell}")
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
                            print(f"This car will go to: {agent.next_cell} and has a direction to the: {agent.last_dir}")
                            # If they're going to the same cell, check if this car will let the other go first
                            if agent.next_cell == self.next_cell:
                                return not self.give_priority(agent)
            # If no agents were found in that cell, let the car advance
            print(f"Car can advance to {self.next_cell}")
            return True
        # Otherwise, check if the contents of the next cell contain a car
        else:
            print(f"Cell {self.next_cell} is not empty")
            contents = self.model.grid.get_cell_list_contents(self.next_cell)
            print(f"Cell {self.next_cell} contains agents {contents}")
            for agent in contents:
                print(f"Agent is of type {agent.type_id}")
                # If agent is a car, don't let it advance
                if agent.type_id == agt.CAR:
                    print(f"Car will not advance")
                    return False
            # If no car was found, let the car advance
            print(f"Car can advance to {self.next_cell}")
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
                # If the cell the agent moved to is it's destination, set it's has_arrived attribute to True
                if self.next_cell == self.destination:
                    self.has_arrived = True
        
    def step(self) -> None:
        # If car hasn't arrived to it's destination
        if not self.has_arrived:
            # Set car's current direction
            self.last_dir = self.map[self.pos[0]][self.pos[1]].direction
            # If path still has remaining cells, assign the first one to the car's next cell
            if len(self.path) > 0:
                # Remove the next cell from the path
                self.next_cell = self.path[0]
                # Check if the car can advance given the next cell contents
                self.move_next()