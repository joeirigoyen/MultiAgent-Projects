from enum import Enum, auto
from mesa import Model
from directions import Directions as dirs


class NodeTypes(Enum):
    START = auto()
    END = auto()
    OBSTACLE = auto()
    CLOSED = auto()
    UNVISITED = auto()
    VISITED = auto()


class Node:
    def __init__(self, col: int, row: int, model: Model) -> None:
        self.col = col
        self.row = row
        self.state = NodeTypes.UNVISITED
        self.direction = None
        self.model = model
        self.neighbors = []
    
    # Update the adjacent nodes of a node
    def update_adj(self) -> None:
        # Update every adjacent node
        self.model.standard_map[self.row][self.col + 1].update_neighbors()
        self.model.standard_map[self.row][self.col - 1].update_neighbors()
        self.model.standard_map[self.row + 1][self.col].update_neighbors()
        self.model.standard_map[self.row - 1][self.col].update_neighbors()
    
    # Update the neighbor list of a node
    def update_neighbors(self) -> None:
        self.neighbors.clear()
        if self.col < self.model.cols - 1 and not self.model.standard_map[self.row][self.col + 1].state == NodeTypes.OBSTACLE:
            if self.model.standard_map[self.row][self.col].direction != dirs.LEFT:
                if not (self.model.standard_map[self.row][self.col].direction == dirs.UP and self.model.standard_map[self.row][self.col + 1].direction == dirs.LEFT):
                    self.neighbors.append(self.model.standard_map[self.row][self.col + 1])
        if self.col > 0 and not self.model.standard_map[self.row][self.col - 1].state == NodeTypes.OBSTACLE:
            if self.model.standard_map[self.row][self.col].direction != dirs.RIGHT:
                if not (self.model.standard_map[self.row][self.col].direction == dirs.DOWN and self.model.standard_map[self.row][self.col - 1].direction == dirs.RIGHT):
                    self.neighbors.append(self.model.standard_map[self.row][self.col - 1])
        if self.row < self.model.rows - 1 and not self.model.standard_map[self.row + 1][self.col].state == NodeTypes.OBSTACLE:
            if self.model.standard_map[self.row][self.col].direction != dirs.UP:
                if not (self.model.standard_map[self.row][self.col].direction == dirs.RIGHT and self.model.standard_map[self.row + 1][self.col].direction == dirs.UP) and not (self.model.standard_map[self.row][self.col].direction == dirs.LEFT and self.model.standard_map[self.row + 1][self.col].direction == dirs.UP):
                    self.neighbors.append(self.model.standard_map[self.row + 1][self.col])
        if self.row > 0 and not self.model.standard_map[self.row - 1][self.col].state == NodeTypes.OBSTACLE:
            if self.model.standard_map[self.row][self.col].direction != dirs.DOWN:
                if not (self.model.standard_map[self.row][self.col].direction == dirs.RIGHT and self.model.standard_map[self.row - 1][self.col].direction == dirs.DOWN) and not (self.model.standard_map[self.row][self.col].direction == dirs.LEFT and self.model.standard_map[self.row - 1][self.col].direction == dirs.DOWN):
                    self.neighbors.append(self.model.standard_map[self.row - 1][self.col])


# Update every node's neighbor list
def init_neighborhood(grid: list) -> None:
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j].update_neighbors()


# Create a grid with empty nodes
def make_grid(rows: int, cols: int, model: Model) -> list:
    grid = []
    for row in range(rows):
        temp = []
        for col in range(cols):
            node = Node(col, row, model)
            temp.append(node)
        grid.append(temp)
    return grid


# Get Manhattan distance from one node to another
def h(n1: Node, n2: Node):
    return abs(n1.col - n2.col) + abs(n1.row - n2.row)
