import numpy as np
import cv2
import scipy.spatial as sp
from maze_graph_algorithm import *

def print_image(original_image):
    img = cv2.imread(original_image)
    cv2.imshow('', img)

def save_image(image, file_name):
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    cv2.imwrite(file_name, image)

def source_end_locator(input_image):
    hsv = cv2.imread(input_image)
    hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
    hsv = cv2.resize(hsv, (320,240))
    lower_red_mask = cv2.inRange(hsv, (0,150,100), (10,255,255))
    upper_red_mask = cv2.inRange(hsv, (170,150,100), (180,255,255))
    red_mask = lower_red_mask + upper_red_mask
    green_mask = cv2.inRange(hsv, (36,80,40), (70,255,255))
    red_ret,red_thresh = cv2.threshold(red_mask,127,255,0)
    green_ret,green_thresh = cv2.threshold(green_mask,127,255,0)
    coordinates = []

    black_mask = cv2.inRange(hsv, (0,0,0), (180,255,100))
    image_output = cv2.subtract(black_mask, red_mask)
    image_output = cv2.subtract(black_mask, green_mask)
    image_output = cv2.bitwise_not(image_output)
    skeleton = cv2.ximgproc.thinning(image_output)
    skeleton = cv2.add(skeleton, red_mask)
    skeleton = cv2.add(skeleton, green_mask)
    skeleton = cv2.cvtColor(skeleton,cv2.COLOR_GRAY2RGB)
    image_output = cv2.cvtColor(image_output, cv2.COLOR_GRAY2RGB)

    red_contours, red_hierarchy = cv2.findContours(red_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    max_red_contour = max(red_contours, key=len)
    M = cv2.moments(max_red_contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    coordinates.append([cY,cX])

    green_contours, green_hierarchy = cv2.findContours(green_thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    max_green_contour = max(green_contours, key=len)
    M = cv2.moments(max_green_contour)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    coordinates.append([cY,cX])
    resize = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

    kernel = np.ones((3,3),np.uint8)
    image_output = cv2.drawContours(image=image_output, contours=[max_red_contour], contourIdx=-1, color=(255,0,0), thickness=cv2.FILLED)
    image_output = cv2.drawContours(image=image_output, contours=[max_green_contour], contourIdx=-1, color=(0,255,0), thickness=cv2.FILLED)

    skeleton = cv2.dilate(skeleton, kernel, iterations=1)
    skeleton = cv2.drawContours(image=skeleton, contours=[max_red_contour], contourIdx=-1, color=(255,0,0), thickness=cv2.FILLED)
    skeleton = cv2.drawContours(image=skeleton, contours=[max_green_contour], contourIdx=-1, color=(0,255,0), thickness=cv2.FILLED)

    return resize, coordinates, image_output, skeleton

def image_processing(input_image):
    img = input_image
    black, white, red, green = (0,0,0), (255,255,255), (255,0,0), (0,255,0)
    main_colors = [black,white,red,green]

    # Updating image pixels to nearest color in main_colors and generating PixelNodes for new PixelGraph
    h,w,bpp = np.shape(img)
    graph = MazeGraph()
    for py in range(0,h):
        for px in range(0,w):
            pixel_color = (img[py][px][0],img[py][px][1],img[py][px][2])      

            # Updating graph created from image
            node = PixelNode(py,px)
            graph.add_node(node)
            if pixel_color == white:
                node.set_color("white")
            elif pixel_color == red:
                node.set_color("red")
            elif pixel_color == green:
                node.set_color("green")
            
            # Updating graph edges
            index = len(graph.nodes) - 1
            if node.color != "black":
                # Add edge to top node
                if index-w >= 0:
                    if graph.nodes[index-w].color != "black":
                        graph.add_edge(node, graph.nodes[index-w])
                # Add edge to left node
                if index-1 >= 0 and index%w != 0:
                    if graph.nodes[index-1].color != "black":
                        graph.add_edge(node, graph.nodes[index-1])

    return img, graph, h, w

def solution_image(h, w, solution_coordinates):
    white = (255,255,255)
    red = (255,0,0)
    img = np.zeros((h,w,3), np.uint8)
    img[:] = white

    for pixel in solution_coordinates:
        img[pixel[0]][pixel[1]] = red
    
    return img

def source_end_nodes(source_end_coordinates, graph):
    for node in graph.nodes:
        if node.coordinates == source_end_coordinates[0]:
            source_node = node
        if node.coordinates == source_end_coordinates[1]:
            end_node = node
    return source_node, end_node

def solution_overlay(img, solution_path):
    for node in reversed(solution_path):
        y = node.y
        x = node.x
        img[y,x] = [255,0,0]
