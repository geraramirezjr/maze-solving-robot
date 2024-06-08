import time
import requests
import numpy as np
import cv2
import scipy.spatial as sp
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from image_processing import *
from maze_graph_algorithm import *
from gcode import *
start_time = time.time()


# 01 Initialization routine and hand drawing maze
initialization_gcode('initialization_gcode.nc')
gcode_file_grbl_motion('initialization_gcode.nc')
print("--- Initialization routine complete ---\n")
input("Hand draw maze inside indicated region. When finished press enter to continue...\n\n")


# 02 Taking photo and downloading image from ESP32-CAM web server
camera_gcode('camera_gcode.nc')
gcode_file_grbl_motion('camera_gcode.nc')
print("--- Camera centered over maze drawing ---\n")
input("Press enter to take photo...\n\n")
esp32_img_url = "http://192.168.0.130/capture?_cb=1704314223794"
esp32_img = requests.get(esp32_img_url).content
with open('maze.jpg', 'wb') as handler:
    handler.write(esp32_img)
print("--- Photo capture and image download complete ---\n")
input("Press enter to continue...\n\n")


# 03 Processing image, generating maze graph, and solving maze graph
original_image = 'maze.jpg'
resize, source_end_coordinates, image_output, skeleton = source_end_locator(original_image)
save_image(skeleton, 'skeleton.png')
img, graph_m, h, w = image_processing(skeleton)
source_node, end_node = source_end_nodes(source_end_coordinates, graph_m)
solution_path, solution_coordinates = dijkstra(graph_m, source_node, end_node)
solution_overlay(image_output, solution_path)
save_image(image_output, 'maze_output.png')
solution_img = solution_image(h, w, solution_coordinates)
save_image(solution_img, 'solution_only.png')
for pixel in solution_coordinates:
    resize[pixel[0]][pixel[1]] = (255,0,0)
save_image(resize, 'original_image_resized_with_solution_overlay.png')
print("--- Image processing and maze graph solution complete ---\n")
input("Press enter for robot to draw maze solution...\n\n")


# 04 Converting solution into gcode and solving maze with robot
scaled_coordinates = scale_coordinates(solution_coordinates)
maze_solution_gcode(scaled_coordinates, 'maze_solution_gcode.nc')
gcode_file_grbl_motion('maze_solution_gcode.nc')
print("--- Robot maze solving complete ---\n")
input("Press enter to complete program...\n")

# 05 Printing program time and displaying image output solution
print("--- %s seconds ---" % (time.time() - start_time))
print_image(original_image)
plt.imshow(image_output)
plt.show()