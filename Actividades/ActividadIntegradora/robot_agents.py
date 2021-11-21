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
        
    def step(self):
        pass
        

class Robot(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.type_id = agt.ROBOT         
        self.grabbed_box = None
        self.target_box = None
        self.targeted_moves = 0
        self.max_targeted_moves = (self.model.width * self.model.height) // 2

    # Get a box's position from the model's found_boxes list 
    def get_found_box(self) -> tuple:
        box_positions: list = self.model.found_boxes
        if len(box_positions) > 0:
            new_box_pos = box_positions.pop()
            return new_box_pos
        else:
            return (-1, -1)
    
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
                        if not c.finished and not c.is_grabbed and not c.targeted:
                            c.targeted = True
                            self.model.found_boxes.append(c.pos)

    # Find an available depot within the model's dictionary
    def find_depot(self) -> tuple:
        # Check every depot
        for pos, count in self.model.depots.items():
            if count < 5:
                return pos
        return (-1, -1)
    
    # Move the agent towars a target
    def move_towards(self, target: tuple) -> None:
        # Initialize next position
        next_pos = tuple()
        # Get distance from agent to depot
        x_distance, y_distance = (target[0] - self.pos[0], target[1] - self.pos[1])
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
        if next_pos[0] >= self.model.width:
            next_pos[0] = next_pos[0] - 1
        elif next_pos[0] < 0:
            next_pos[0] = 0
        elif next_pos[1] >= self.model.height:
            next_pos[1] = next_pos[1] - 1
        elif next_pos[1] < 0:
            next_pos[1] = 0
            
        self.model.grid.move_agent(self, next_pos)
    
    # Look for a depot and try to move towars it
    def seek_depot(self) -> None:
        # Find an available depot
        depot_pos = self.find_depot()
        # Get current neighbors
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)     
        # Check if there are other boxes within the neighborhood so they can be added to the model's found_boxes list
        self.add_extra_box(neighborhood)        
        # If the depot is within the neighbors, drop the box in it's position
        if depot_pos in neighborhood:
            self.drop_box(depot_pos)
        # If the depot is not a neighbor, move towards the depot's position
        else:
            self.move_towards(depot_pos)

    # Move agent randomly to find a box
    def move_randomly(self) -> None:
        # Get possible next cells
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        free_cells = list(map(self.model.is_available_robot_space, neighborhood))
        possible_steps = [c for c in range(len(neighborhood)) if free_cells[c]]
        # Get empty cell or fake tuple from get_next_pos()
        if len(possible_steps) > 0:
            next_pos = neighborhood[self.random.choice(possible_steps)]
            # If next_pos is not a fake tuple, move it to the given position
            if next_pos[0] != -1:
                self.model.grid.move_agent(self, next_pos)
    
    # Check if an agent can grab a box and then grab it if it can
    def check_box(self) -> None:
    # Get neighborhood
        neighbors = self.model.grid.get_neighborhood(self.pos, moore=False)
        # Iterate through neighborhood
        for cell in neighbors:
            # If the neighbor cell is occupied, check it's contents
            contents = self.model.grid.get_cell_list_contents(cell)
            if len(contents) > 0:
                for n in contents:
                    # If a neighbor is a box and no agent is holding it, add the box to the robot's grabbed_box attribute
                    if n.type_id == agt.BOX:
                        if not n.is_grabbed and not n.finished:
                            # If the agent has a target, set the target as None again
                            if self.target_box != None:
                                self.target_box = None
                            print(f"Agent {self.unique_id} grabbed box: {n.unique_id}")
                            # If the agent found a box but is currently carrying another one, add it to the model's found_boxes list
                            if self.grabbed_box != None:
                                if not n.targeted:
                                    n.targeted = True
                                    self.model.found_boxes.append(n.pos)
                            # Otherwise, just grab the box
                            else:
                                self.grabbed_box = n
                                self.grabbed_box.is_grabbed = True
                                self.move_box()
                                
    # Move robot to find a box, whether it is a random or targeted movement
    def seek_box(self) -> None:
        # If agent is not currently targeting any box, find a box to target
        if self.target_box == None:
            temp_target = self.get_found_box()
            # If there is a box, assign it as the agent's current target
            if temp_target[0] != -1:
                self.target_box = temp_target
            else:
                self.move_randomly()
        else: 
            self.move_towards(self.target_box)
    
    # Move box along with the robot
    def move_box(self) -> None:
        # Change the box's position to the robot's position
        if self.grabbed_box != None:
            new_box_pos = self.pos
            self.model.grid.move_agent(self.grabbed_box, new_box_pos)

    # Drop a box in a depot      
    def drop_box(self, depot_pos: tuple) -> None:
        # Put box in depot
        self.model.grid.move_agent(self.grabbed_box, depot_pos)
        # Change box's attributes
        self.grabbed_box.is_finished = True
        # Change agent's attributes
        self.grabbed_box = None
        # Change depot's stack count
        self.model.depots[depot_pos] += 1
    
    def step(self) -> None:
        print(f"Agent grabbing box: {self.grabbed_box}")
        print(f"Agent targeting box: {self.target_box}")
        # Count targeted moves
        if self.target_box != None:
            self.targeted_moves += 1
        else:
            self.targeted_moves = 0
        # Avoid getting a robot stuck
        if self.targeted_moves > self.max_targeted_moves:
            self.target_box = None
        # Move
        if self.grabbed_box is None:
            self.check_box()
            self.seek_box()
        else:
            self.seek_depot()
            self.move_box()