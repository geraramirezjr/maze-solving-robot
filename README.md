# Maze Solving Robot
Project repository for a maze solving robot. Developed a robot that automatically solves hand drawn mazes. System consists of an ESP32 camera, drawing plotter, computer vision (OpenCV), custom maze data structures and algorithms (Python), and CNC robot motion (Arduino and G-code).

![hero](images/solution.gif)
[Video file](images/solution.MOV)

## System Overview
System first prompts user to hand draw maze in an indicated region and then captures an image with an ESP32-Cam. System then proceeds to process maze into a graph structure and solve with a graph algorithm. Finally, solution is converted into G-code and an Arduino and drawing plotter are used to draw the maze solution path trajectory.

![](images/system_overview.png)

## Camera Integration
A custom camera bracket assembly was designed to integrate the ESP32-Cam with the drawing plotter. Components were 3D printed and assembly was mounted on the CNC tool head.

![](images/ESP32-CAM_overview.png)

## Computer Vision and Image Processing

## Maze Graph and Solution Algorithm

## Motion Control
