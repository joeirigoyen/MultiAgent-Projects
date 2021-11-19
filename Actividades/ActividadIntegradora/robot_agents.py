from mesa import Agent, Model


class Box(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.type_id = 2
        self.is_grabbed = False
        

class Robot(Agent):
    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.type_id = 1
        self.grabbed_box = None
    
    # Check if there is an available space for the agent to move given it's possible next cells
    def get_next_pos(self, possible_steps: list) -> tuple:
        # Check every possible cell
        for position in possible_steps:
            # If a cell is empty, stop iterating and return it's position
            if len(self.model.grid.get_cell_contents(position)) == 0:
                return position
        # If no empty cells were found, return a fake tuple
        return (-1, -1)

    # Move agent randomly to find a box
    def seek_box(self) -> None:
        # Get possible next cells
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        # Get empty cell or fake tuple from get_next_pos()
        next_pos = self.get_next_pos(possible_steps)
        # If next_pos is not a fake tuple, move it to the given position
        if next_pos[0] != -1:
            self.model.grid.move_agent(next_pos)

    # Move agent to follow one of the coordinates of the depositing area
    def seek_depot(self, home: Agent) -> None:
        # Get distance from agent to depositing cell
        distance = (home.pos[0] - self.pos[0], home.pos[1] - self.pos[1])
        # If the x distance is bigger than, or equal to the y distance, move horizontally
        if abs(distance[0]) >= abs(distance[1]) and distance[0] != 0:
            # If the x distance is negative, go one cell to the left
            if (distance[0] < 0):
                new_pos = (self.pos[0] - 1, self.pos[1])
                self.model.grid.move_agent(new_pos)
            # Otherwise, move one cell to the right
            else:
                new_pos = (self.pos[0] + 1, self.pos[1])
                self.model.grid.move_agent(new_pos)
        # If the y distance is bigger than the x distance, move vertically
        elif abs(distance[1]) > abs(distance[0]) and distance[1] != 0:
            # If the y distance is negative, go down one cell 
            if (distance[1] < 0):
                new_pos = (self.pos[0], self.pos[1] - 1)
                self.model.grid.move_agent(new_pos)
            # Otherwise, go up one cell 
            else:
                new_pos = (self.pos[0], self.pos[1] + 1)
                self.model.grid.move_agent(new_pos)
    
    # Check if robot can grab box
    def found_box(self) -> tuple:
        # If the robot is not currently grabbing any box
        if not self.is_grabbing:
            # Get neighborhood
            neighbors = self.model.grid.get_cell_list_contents(self.pos)
            if len(neighbors) > 1:
                for n in neighbors:
                    if n.type_id == 2:
                        return n.pos
        else:
            return False
    
    def step(self):
        if self.is_grabbing:
            self.seek_box()
        else:
            self.seek_depot()