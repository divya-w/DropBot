from djitellopy import tello

import KeyPressModule as kp

import numpy as np

from time import sleep

import cv2

import math

import sys

me = tello.Tello()
me.connect()
print(me.get_battery())

points = [(0, 0), (0, 0)]


# Function to take coordinate input
def goto(goal_x, goal_y, take_off, cur_x, cur_y):
    # Starting position is 0,0
    # yaw = -65 is pointing north
    #to_rotate = -65 - (me.get_yaw())
    # Calculate angle and distance
    if x == 0:
        angle = 0
    else:
        angle = int(math.degrees(math.atan(goal_y / goal_x)))
    dist = int(math.sqrt(((goal_x) ** 2) + ((goal_y) ** 2)))
    if cur_x == 0:
        ret_angle = 0
    else:
        ret_angle = int(math.degrees(math.atan(cur_y/cur_x)))
    # print(angle, dist)


    # 1. Rotate drone to desired coordinate
    # 2. Fly in straight line (forward)
    if take_off == 1:
        me.takeoff()
        #me.rotate_counter_clockwise(to_rotate)
        me.rotate_counter_clockwise(angle)
        me.move_forward(dist)
    elif take_off == 0:
        me.rotate_counter_clockwise(-me.get_yaw() + angle)
        me.move_forward(dist)
    elif take_off == -1:
        #angle = int(math.degrees(math.atan(cur_x / cur_y)))
        angle = me.get_yaw()
        dist = int(math.sqrt((cur_x**2)+(cur_y**2)))
        print(angle, dist, cur_x, cur_y)
        if cur_y >= 0 and cur_x < 0: # 2nd Quadrant
            me.rotate_counter_clockwise(-angle + (180 - ret_angle))
        elif cur_y >= 0 and cur_x >= 0: #1st Quadrant 
            me.rotate_counter_clockwise(-angle + 180 - ret_angle)
        elif cur_y < 0 and cur_x < 0: #3rd Quadrant
            me.rotate_counter_clockwise(-angle - (90 - ret_angle))
        elif cur_y < 0 and cur_x >= 0: #4th Quadrant
            me.rotate_counter_clockwise(-angle + 90 - ret_angle)
        me.move_forward(dist)
        me.land()


def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)

    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)

    cv2.putText(img, f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m', (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)


if __name__ == '__main__':
    # Extracting user input for coords
    cur_x = 0
    cur_y = 0
    cur_angle = 0
    while True:
        # Setting up mapping image
        img = np.zeros((1000, 1000, 3), np.uint8)
        # User input for coordi0nates
        coordinates = str(input())
        coords = coordinates.split(',')
        x = int(coords[0].strip())
        y = int(coords[1].strip())
        take_off = int(coords[2].strip())
        cur_x += x
        cur_y += y
        if x != 0:
            cur_angle = (cur_angle + int(math.degrees(math.atan(y / x)))) % 360
        else:
            cur_angle = (cur_angle + 0) % 360
        points.append((cur_x, cur_y))
        # drawPoints(img, points)
        # cv2.imshow("Output", img)
        # cv2.waitKey(0)
        print(x, y, take_off)
        # Go to state if exists
        if 1 >= take_off >= -1:
            goto(x, y, take_off, cur_x, cur_y)
        else:
            continue
        # Getting current location to add point to image

        #cur_angle = me.get_yaw()
        #cur_dist = me.get_distance_tof()
        #cur_x = cur_angle * math.cos(cur_dist)
        #cur_y = cur_angle * math.sin(cur_dist)
