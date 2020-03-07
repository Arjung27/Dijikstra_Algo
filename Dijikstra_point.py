import sys
import os
import argparse
import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
import heapq

class Node:

    def __init__(self, x_coord, y_coord, cost, parentID):

        self.x = x_coord
        self.y = y_coord
        self.cost = cost
        self.parentID = parentID

    def __lt__(self,other):
        return self.cost < other.cost
    # def __eq__(self,other):
    #     return self.cost == other.cost

def possible_steps():

    steps_with_cost = np.array([
                                [0, 1, 1],              # Move_up
                                [1, 1, np.sqrt(2)],     # Move_right_top
                                [1, 0, 1],              # Move_right
                                [1, -1, np.sqrt(2)],    # Move_right_bottom
                                [0, -1, 1],             # Move_down
                                [-1, -1, np.sqrt(2)],   # Move_left_bottom
                                [-1, 0, 1],             # Move_left
                                [-1, 1, np.sqrt(2)]])   # Move_left_top

    return steps_with_cost

def generate_gui(width, height, radius):

    x_coord, y_coord = np.mgrid[0:height+2, 0:width+2]
    grid = np.full((height+2, width+2), True, dtype=bool)
    grid[x_coord < radius] = False
    grid[x_coord > height - radius] = False
    grid[y_coord < radius] = False
    grid[y_coord > width - radius] = False
    # Obstacles:
    # Ellipse
    ellipse = ((40+radius)*(x_coord - 100))**2 + ((20+radius)*(y_coord - 150))**2
    grid[ellipse <= ((40+radius)*(20+radius))**2] = False
    
    # Circle
    circle = (x_coord - 150)**2 + (y_coord - 225)**2
    grid[circle <= (25+radius)**2] = False
    
    # Rectangle Tilted with coords = ((30, 67.5), (95,30), (100, 38.66), (35, 76.16))
    l1 = x_coord + 0.57692*y_coord - (84.8079 - radius*np.sqrt(1 + 0.57692**2))
    l2 = x_coord - 1.732*y_coord - (15.54 + radius*np.sqrt(1 + 1.732**2))
    l3 = x_coord - 1.732*y_coord - (-134.54 - radius*np.sqrt(1 + 1.732**2))
    l4 =x_coord + 0.57692*y_coord - (96.35230 + radius*np.sqrt(1 + 0.57692**2)) 
    grid[(l1 >= 0) & (l2 <= 0) & (l3 >= 0) & (l4 <= 0)] = False

    # Rectangle that is in shape of a diamond ((200, 25), (225, 10), (250, 25), (225, 40))
    l1 = x_coord + 0.6*y_coord - (145 - radius*np.sqrt(1 + 0.6**2))
    l2 = x_coord - 0.6*y_coord - (-95 + radius*np.sqrt(1 + 0.6**2))
    l3 = x_coord - 0.6*y_coord - (-125 - radius*np.sqrt(1 + 0.6**2))
    l4 =x_coord + 0.6*y_coord - (175 + radius*np.sqrt(1 + 0.6**2)) 
    grid[(l1 >= 0) & (l2 <= 0) & (l3 >= 0) & (l4 <= 0)] = False

    # Polygon
    l1 = x_coord - 13*y_coord - (-140 + radius*np.sqrt(1 + 13**2))
    l2 = x_coord - (185 + radius)
    l3 = x_coord + 1.4*y_coord - (290 + radius*np.sqrt(1 + 1.4**2))
    l4 = x_coord - 1.2*y_coord - (30 - radius*np.sqrt(1 + 1.2**2))
    l5 = x_coord + 1.2*y_coord - (210 - radius*np.sqrt(1 + 1.2**2))
    l6 = x_coord - 1*y_coord - (100 - radius*np.sqrt(1 + 1**2))
    grid[(l1 <= 0) & (l2 <= 0) & (l3 <= 0) & (l4 >= 0) & ((l5 >= 0) | (l6 >= 0))] = False
    
    grid = grid.astype(np.uint8)*255

    return grid

def is_valid(point_x, point_y, grid, width, height):

    # print(point_y, point_x)
    # print(grid[point_y][point_x])

    if ( not grid[int(point_y)][int(point_x)]):
        return False
    if ((point_y < 0) or (point_x) < 0):
        return False
    if ((point_y > height) or (point_x > width)):
        return False
    return True

def is_goal(current, goal):

    return (current.x == goal.x) and (current.y == goal.y)

def path_search_algo(start_node, end_node, grid, width, height):

    current_node = start_node
    goal_node = end_node
    steps_with_cost = possible_steps()

    if is_goal(current_node, goal_node):
        return 1

    open_nodes = {}
    open_nodes[start_node.x*width + start_node.y] = start_node
    closed_nodes = {}
    cost = []
    all_nodes = []
    heapq.heappush(cost, [start_node.cost, start_node])

    while (len(cost) != 0):

        current_node = heapq.heappop(cost)[1]
        all_nodes.append([current_node.x, current_node.y])
        # all_nodes_y.append(current_node.y)
        current_id = current_node.x*width + current_node.y
        
        if is_goal(current_node, end_node):
            end_node.parentID = current_node.parentID
            end_node.cost = current_node.cost
            print("Path found")
            return 1, all_nodes

        if current_id in closed_nodes:
            continue
        else:
            closed_nodes[current_id] = current_node

        del open_nodes[current_id]

        for i in range(steps_with_cost.shape[0]):

            new_node = Node(current_node.x + steps_with_cost[i][0], \
                            current_node.y + steps_with_cost[i][1], \
                            current_node.cost + steps_with_cost[i][2], \
                            current_node)

            new_node_id = new_node.x*width + new_node.y

            if not is_valid(new_node.x, new_node.y, grid, width, height):
                continue
            elif new_node_id in closed_nodes:
                continue

            if new_node_id in open_nodes:
                if new_node.cost < open_nodes[new_node_id].cost:
                    open_nodes[new_node_id].cost = new_node.cost
                    open_nodes[new_node_id].parentID = new_node.parentID
            else:
                open_nodes[new_node_id] = new_node

            heapq.heappush(cost, [ open_nodes[new_node_id].cost, open_nodes[new_node_id]])

    return 0, all_nodes

def find_path(start_node, end_node, height, grid, all_nodes):

    x_coord = [end_node.x]
    y_coord = [end_node.y]

    iD = end_node.parentID
    while iD != -1:
        # current_node = iD.parentID
        x_coord.append(iD.x)
        y_coord.append(iD.y)
        iD = iD.parentID

    print("Plotting........")
    x_coord.reverse()
    y_coord.reverse()
    grid = np.dstack([grid, grid, grid])
    grid = cv2.flip(grid, 0)

    for i in range(len(all_nodes)):
        grid[201 - int(all_nodes[i][1]), int(all_nodes[i][0]), 0:3] = 200
        grid[201 - int(all_nodes[i][1]), int(all_nodes[i][0]), 0:3].astype(np.uint8)
        # print(grid.shape)
        # exit(-1)
        cv2.imshow("image", grid)
        # video_writer.write(grid)
        cv2.waitKey(1)

    for i in range(len(x_coord)):

        grid[201 - int(y_coord[i]), int(x_coord[i]), 0:3] = (255, 0,0)
        grid[201 - int(y_coord[i]), int(x_coord[i]), 0:3].astype(np.uint8)
        cv2.imshow("image", grid)
        # video_writer.write(grid)
    cv2.waitKey(0)


if __name__ == '__main__':

    # Take input radius and clearance value
    radius = input("Enter Robot radius: ")
    clearance = input("Enter clearance value: ")
    radius = int(radius)
    clearance = int(clearance)
    gui_width = 300
    gui_height = 200
    grid = generate_gui(gui_width, gui_height, radius+clearance)

    # Take start coordinates as input
    start_coord = input("Enter start coordinates: ")
    start_x, start_y = start_coord.split()
    start_x = int(start_x)
    start_y = int(start_y)
    if not is_valid(start_x, start_y, grid, gui_width, gui_height):
        print("INVALID start node.")
        exit(-1)

    # Take end coordinates as input
    end_coord = input("Enter end coordinates: ")
    end_x, end_y = end_coord.split()
    end_x = int(end_x)
    end_y = int(end_y)
    if (not is_valid(end_x, end_y, grid, gui_width, gui_height)):
        print("INVALID end node.")
        exit(-1)

    start_node = Node(start_x, start_y, 0.0, -1)
    end_node = Node(end_x, end_y, 0.0, -1)
    start = time.time()
    flag, all_nodes = path_search_algo(start_node, end_node, grid, gui_width, gui_height)
    end = time.time()
    print("Time taken to find the path ", (end - start))
    grid = generate_gui(gui_width, gui_height, 0)
    if (flag):
        find_path(start_node, end_node, gui_height, grid, all_nodes)
    else:
        print("Path could not be found")
