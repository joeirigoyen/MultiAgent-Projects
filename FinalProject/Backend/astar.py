from os import O_APPEND
from typing import Counter
from grid_manager import NodeTypes
from grid_manager import Node, h
from queue import PriorityQueue


def get_nodes_in_path(came_from: dict, current: Node):
    path = []
    while current in came_from:
        path.append((current.row, current.col))
        current = came_from[current]
    path.reverse()
    return path        


def get_shortest_path(grid: list, start: Node, end: Node) -> list or None:
    # Initialize counter, queue and set
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    # Initialize each cell's f score and g score
    g_score = {node: float("inf") for row in grid for node in row}
    f_score = {node: float("inf") for row in grid for node in row}
    # Declare start node's scores
    g_score[start] = 0
    f_score[start] = h(start, end)
    # Returns nodes in priority queue
    open_set_hash = {start}
    # Run until the open set is empty
    while not open_set.empty():
        # Current node will be the start node
        current = open_set.get()[2]
        # Remove current node from the open set hash
        open_set_hash.remove(current)
        # Check if current node is already the destination
        if current == end:
            return get_nodes_in_path(came_from, current)
        # Check the neighbors of the current node and add a temporary g score
        for neighbor in current.neighbors:
            # Check each neighbor's g score and look for the smallest one
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:
                # Tell program that the current path comes from the current node
                came_from[neighbor] = current
                # Set the neighbor's g score the new g score
                g_score[neighbor] = temp_g
                f_score[neighbor] = temp_g + h(neighbor, end)
                # If neighbor has not been visited, change it's state and add it to the priority queue
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.state = NodeTypes.VISITED
                if current != start:
                    current.state = NodeTypes.CLOSED
    return []
