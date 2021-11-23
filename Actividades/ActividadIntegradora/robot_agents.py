"""Robot Model Agents

Defines the actions and properties of every agent involved in the model
so it's goals can be achieved.

This file can also be imported as a module to run the model separately.
"""

__author__ = "Raúl Youthan Irigoyen Osorio"

from mesa import Agent, Model
from mesa.space import Grid
from agent_types import AgentType as agt


class Depot(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.type_id = agt.DEPOT
        self.stack = 0


class Box(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.type_id = agt.BOX
        self.targeted = False
        self.is_grabbed = False
        self.finished = False
        self.grabber = None
        self.y_pos = 0.5
        self.target_depot = None


class Robot(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.type_id = agt.ROBOT
        self.grabbed_box = None
        self.target_box = None

    # Get a box's position from the model's found_boxes list
    def get_found_box(self) -> Agent:
        # If a robot is not holding a box, get a box to target
        if self.grabbed_box == None:
            # If there are available boxes in the model's list, get one
            if len(self.model.found_boxes) > 0:
                new_box = self.model.found_boxes.pop()
                # If that box is not being targeted by any other agent trying to target the same box, target at it
                if not new_box.targeted:
                    new_box.targeted = True
                    print(
                        f"Agent {self.unique_id - 18} is now targeting box at {new_box.pos}"
                    )
                    return new_box
                # Otherwise keep looking
                else:
                    return None
            else:
                return None
        else:
            return None

    # Add boxes to found_boxes model list if an agent is not able to carry them
    def add_extra_box(self, neighborhood: list) -> None:
        # Check every cell in neighborhood
        for cell in neighborhood:
            # If cell is not empty, check its contents
            contents = self.model.grid.get_cell_list_contents(cell)
            if len(contents) > 0:
                # If a cell contains a box, check it's attributes
                for c in contents:
                    if c.type_id == agt.BOX:
                        # If it's not already in a deposit or it's not grabbed, add it to the found_boxes model list
                        if (not c.finished and not c.is_grabbed
                                and c not in self.model.found_boxes):
                            self.model.found_boxes.append(c)
                            print(
                                f"Agent {self.unique_id - 18} found a box at {c.pos}"
                            )

    # Find an available depot within the model's dictionary
    def find_depot(self) -> tuple:
        # Check every depot
        for pos, count in self.model.depot_stacks.items():
            if count < 5:
                print(f"Agent {self.unique_id - 18} will deposit box at {pos}")
                return pos
        return (-1, -1)

    # Move the agent towards a target
    def move_towards(self, target: tuple) -> None:
        # Initialize next position
        next_pos = tuple()
        x_distance, y_distance = (target[0] - self.pos[0],
                                  target[1] - self.pos[1])
        # If the x distance is more than the y distance, move horizontally
        if abs(x_distance) > abs(y_distance):
            if x_distance > 0:
                next_pos = (self.pos[0] + 1, self.pos[1])
            else:
                next_pos = (self.pos[0] - 1, self.pos[1])
        # If the y distance is more than the x distance, move vertically
        else:
            if y_distance > 0:
                next_pos = (self.pos[0], self.pos[1] + 1)
            else:
                next_pos = (self.pos[0], self.pos[1] - 1)
        # Avoid getting past the border
        if next_pos[0] >= self.model.width:
            next_pos = (next_pos[0] - 1, next_pos[1])
        elif next_pos[1] >= self.model.height:
            next_pos = (next_pos[0], next_pos[1] - 1)
        self.model.grid.move_agent(self, next_pos)

    # Move agent randomly to find a box
    def move_randomly(self) -> None:
        # Get possible next cells
        neighborhood = self.model.grid.get_neighborhood(self.pos,
                                                        moore=False,
                                                        include_center=False)
        free_cells = list(
            map(self.model.is_available_robot_space, neighborhood))
        possible_steps = [c for c in range(len(neighborhood)) if free_cells[c]]
        # Get empty cell or fake tuple from get_next_pos()
        if len(possible_steps) > 0:
            next_pos = neighborhood[self.random.choice(possible_steps)]
            # If next_pos is not a fake tuple, move it to the given position
            if next_pos[0] != -1:
                self.model.grid.move_agent(self, next_pos)

    # Pick a box
    def grab_box(self, n: Agent) -> None:
        self.grabbed_box = n
        self.grabbed_box.is_grabbed = True
        self.grabbed_box.grabber = self
        self.grabbed_box.targeted = False
        self.grabbed_box.y_pos = 1.5
        self.target_box = self.get_found_box()
        print(f"Agent {self.unique_id - 18} grabbed box at {n.pos}")
        self.move_box()

    # Grab a box if the agent is able to
    def check_box(self, n: Agent) -> None:
        # If a neighbor is a box and no agent is holding it, check if the robot can grab it
        if n.type_id == agt.BOX:
            if not n.is_grabbed and not n.finished:
                # If the agent found a box but is currently carrying another one, add it to the model's found_boxes list
                if self.grabbed_box != None:
                    if n not in self.model.found_boxes:
                        print(
                            f"Agent {self.unique_id - 18} found a box at {n.pos}"
                        )
                        self.model.found_boxes.append(n)
                # Otherwise, if the robot is currently looking for a box, check if it's the same box
                elif self.target_box != None:
                    if self.target_box == n:
                        self.grab_box(n)
                # Otherwise, if the box isn't already targeted, grab it
                elif not n.targeted:
                    self.grab_box(n)

    # Check if an agent can grab a box and then grab it if it can
    def check_for_boxes(self) -> None:
        # Get neighborhood
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=False)
        # Iterate through neighborhood
        for cell in neighborhood:
            # If the neighbor cell is occupied, check it's contents
            contents = self.model.grid.get_cell_list_contents(cell)
            if len(contents) > 0:
                for n in contents:
                    self.check_box(n)

    # Look for a depot and try to move towars it
    def seek_depot(self) -> None:
        # Find an available depot
        depot_pos = self.find_depot()
        self.grabbed_box.target_depot = depot_pos
        # Get current neighbors
        neighborhood = self.model.grid.get_neighborhood(self.pos,
                                                        moore=False,
                                                        include_center=False)
        # Check if there are other boxes within the neighborhood so they can be added to the model's found_boxes list
        self.add_extra_box(neighborhood)
        # If the depot is within the neighbors, drop the box in it's position
        if depot_pos in neighborhood:
            print(f"Agent {self.unique_id - 18} dropped box at {depot_pos}")
            self.drop_box(depot_pos)
        # If the depot is not a neighbor, move towards the depot's position
        else:
            if depot_pos[0] != -1:
                self.move_towards(depot_pos)

    # Move robot to find a box, whether it is a random or targeted movement
    def seek_box(self) -> None:
        # Look in neighborhood for boxes
        self.check_for_boxes()
        # If agent is not currently targeting any box, find a box to target
        if self.target_box == None:
            temp_target = self.get_found_box()
            # If there is a box to be grabbed, assign it as the agent's current target
            if temp_target != None:
                self.target_box = temp_target
            else:
                self.move_randomly()
        # If agent is targeting a box, check if it hasn't been taken by another agent
        else:
            if not self.target_box.is_grabbed:
                self.move_towards(self.target_box.pos)
            else:
                print(
                    f"Agent {self.unique_id - 18}'s target has been grabbed by other agent. Setting agent's target to None."
                )
                self.target_box = None

    # Move box along with the robot
    def move_box(self) -> None:
        # Change the box's position to the robot's position
        if self.grabbed_box != None:
            new_box_pos = self.pos
            self.grabbed_box.y_pos = 1.5
            self.model.grid.move_agent(self.grabbed_box, new_box_pos)

    # Drop a box in a depot
    def drop_box(self, depot_pos: tuple) -> None:
        # Put box in depot
        self.model.grid.move_agent(self.grabbed_box, depot_pos)
        self.grabbed_box.y_pos = self.model.depot_stacks[
            self.grabbed_box.target_depot] + 0.5
        # Change box's attributes
        self.grabbed_box.finished = True
        self.grabbed_box.targeted = False
        self.grabbed_box.grabber = None
        self.grabbed_box.stacked_pos = self.model.depot_stacks
        # Change agent's attributes
        self.grabbed_box = None
        # Change depot's stack count
        self.model.depot_stacks[depot_pos] += 1
        self.model.stacked_boxes += 1

    def step(self) -> None:
        # Debug
        if self.target_box != None:
            print(
                f"Agent {self.unique_id - 18} is looking for box at {self.target_box.pos}"
            )
        # Move
        if self.grabbed_box is None:
            self.seek_box()
            self.move_box()
        else:
            self.seek_depot()
            self.move_box()
