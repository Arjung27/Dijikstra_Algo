import sys
import os
import argparse
import numpy as np
import cv2
import matplotlib.pyplot as plt

def generate_gui(width, height, radius):

    print(height)
    x_coord, y_coord = np.mgrid[0:height, 0:width]
    grid = np.full((height, width), True, dtype=bool)
    print(grid.shape)
    grid[x_coord < radius] = False
    grid[x_coord > height - radius] = False
    grid[y_coord < radius] = False
    grid[y_coord > width - radius] = False
    # Obstacles:
    # Ellipse
    ellipse = (40*(x_coord - 100))**2 + (20*(y_coord - 150))**2
    grid[ellipse <= (40*20 + radius)**2] = False
    
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
    # cv2.imshow("image", grid)
    # cv2.waitKey(0)
    grid = grid.astype(np.uint8)*255
    fig, ax = plt.subplots()
    ax.set_ylim(0, height)
    ax.grid(True)
    plt.imshow(grid)
    plt.show()

if __name__ == '__main__':

    # Parser = argparse.ArgumentParser()
    # Parser.add_argument('--start')
    radius = int(radius)
    clearance = int(clearance)
    gui_width = 300
    gui_height = 200
    grid, obs_x, obs_y = generate_gui(gui_width, gui_height, radius+clearance)
    start_coord = input("Enter start coordinates: ")
    end_coord = input("Enter end coordinates: ")
    start_x, start_y = start_coord.split()
    start_x = int(start_x)
    start_y = int(start_y)
    if (is_obstacle(start_x, start_y)):

    radius = input("Enter Robot radius: ")
    clearance = input("Enter clearance value: ")
    end_x, end_y = end_coord.split()
    end_x = int(end_x)
    end_y = int(end_y)
