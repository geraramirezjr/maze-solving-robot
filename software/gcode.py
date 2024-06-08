import numpy as np
import serial
import time

def scale_coordinates(solution_coordinates):
    scale_factor_y = 0.51
    offset_factor_y = 3.0
    scale_factor_x = 0.52
    offset_factor_x = 3.2
    scaled_coordinates = np.asfarray(solution_coordinates)
    scaled_coordinates[:,0] *= scale_factor_y
    scaled_coordinates[:,0] += offset_factor_y
    scaled_coordinates[:,1] *= scale_factor_x
    scaled_coordinates[:,1] += offset_factor_x
    scaled_coordinates = np.around(scaled_coordinates, 2)
    return scaled_coordinates

def insert_line(f, text):
	f.write(f"{text}\n") 

def G_function(f, g, x, y):
	f.write(f"G{g} X{x} Y{y}\n")

def initialization_gcode(gcode_file_name):
    f = open(gcode_file_name, 'w')
    insert_line(f, "$22=1")
    insert_line(f, "$23=1")
    insert_line(f, "$H")
    G_function(f, 92, 0, 0)
    insert_line(f, "G21")
    insert_line(f, "G90")

def camera_gcode(gcode_file_name):
    f = open(gcode_file_name, 'w')
    G_function(f, 0, 90, -220)

def maze_solution_gcode(solution_coordinates, gcode_file_name):
    f = open(gcode_file_name, 'w')
    G_function(f, 0, -90, 185)         #top left image location relative to camera center location
    G_function(f, 92, 0, 0)         #setting new zero
    insert_line(f, "G1 F5000")
    insert_line(f, "S255")
    G_function(f, 0, solution_coordinates[-1][1], -1*solution_coordinates[-1][0])      #move to source (red)
    insert_line(f, "G1 Z9 F5000")
    for coordinate in reversed(solution_coordinates[:-1]):
        G_function(f, 1, coordinate[1], -1*coordinate[0])
    insert_line(f, "G1 Z1 F5000")
    G_function(f, 0, 0, 35)   #move back home. don't want to crash, needs to update based on new zero location

def gcode_file_grbl_motion(gcode_file):
    # Open grbl serial port
    s = serial.Serial('COM10',115200)

    # Open g-code file
    f = open(gcode_file,'r');

    # Wake up grbl
    s.write("\r\n\r\n".encode())
    time.sleep(2)   # Wait for grbl to initialize 
    s.flushInput()  # Flush startup text in serial input
     
    # Stream g-code to grbl
    for line in f:
        l = line.strip() # Strip all EOL characters for consistency
        print('Sending: ', l),
        s.write(l.encode()) # Send g-code block to grbl
        s.write('\n'.encode()) # New line
        #s.write(l + '\n'.encode()) # Send g-code block to grbl
        grbl_out = s.readline() # Wait for grbl response with carriage return
        print(' : ', grbl_out.strip())

    # Wait here until grbl is finished to close serial port and file.
    input("  Press <Enter> to exit and disable grbl.") 

    # Close file and serial port
    f.close()
    s.close()
