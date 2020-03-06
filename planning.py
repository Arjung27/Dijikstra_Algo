import sys
import os
import argparse
import numpy as np
import cv2

if __name__ == '__main__':

	# Parser = argparse.ArgumentParser()
	# Parser.add_argument('--start')
	start_coord = input("Enter start coordinates: ")
	end_coord = input("Enter end coordinates: ")
	start_x, start_y = start_coord.split()
	end_x, end_y = end_coord.split()
	start_x = int(start_x)
	start_y = int(start_y)
	end_x = int(end_x)
	end_y = int(end_y)
	gui_width = 300
	gui_height = 200

	grid, obs_x, obs_y = generate_gui(gui_width, gui_height)