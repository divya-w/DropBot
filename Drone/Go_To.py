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
def goto(goal_x, goal_y, take_off, start_angle):
    if take_off == 1:
        cur_x, cur_y = 0, 0
        cur_angle = 0
    if goal_x == 0 and goal_y == 0:
        pass
    elif goal_x - cur_x == 0 and goal_y - cur_y < 0: #directly behind it
        angle = 180
    elif goal_x - cur_x == 0 and goal_y - cur_y >= 0: #directly in front of it
        angle = 0
    elif goal_x - cur_x < 0 and goal_y - cur_y < 0:#3rd quadrant
        angle = 270 + int(math.degrees(math.atan((goal_y - cur_y) / (goal_x - cur_x))))
    elif goal_x - cur_x > 0 and goal_y - cur_y > 0: #1st quadrant
        angle = int(math.degrees(math.atan((goal_y - cur_y) / (goal_x - cur_x))))
    elif goal_x - cur_x > 0 and goal_y - cur_y < 0: #4th quadrant
        angle = 360 + int(math.degrees(math.atan((goal_y - cur_y) / (goal_x - cur_x))))
    elif goal_x - cur_x < 0 and goal_y - cur_y > 0: #2nd quadrant
        angle = 180 + int(math.degrees(math.atan((goal_y - cur_y) / (goal_x - cur_x))))
    dist = int(math.sqrt((goal_x - cur_x) ** 2) + ((goal_y - cur_y) ** 2))
    if cur_y == 0:
        ret_angle = 0
    else:
        ret_angle = int(math.degrees(math.atan(cur_x/cur_y)))
    # print(angle, dist)

    cur_x += goal_x
    cur_y += goal_y
    if x != 0:
        cur_angle = (cur_angle + angle) % 360
    else:
        cur_angle = (cur_angle + 0) % 360

    # 1. Rotate drone to desired coordinate
    # 2. Fly in straight line (forward)
    if take_off == 1:
        me.takeoff()
        me.rotate_counter_clockwise(angle)
        me.move_forward(dist)
        print(start_angle - me.get_yaw(), angle)
    elif take_off == 0:
        me.rotate_counter_clockwise(angle)
        me.move_forward(dist)
    elif take_off == -1:
        #angle = int(math.degrees(math.atan(cur_x / cur_y)))
        angle = (me.get_yaw() - start_angle)
        dist = int(math.sqrt((cur_x**2)+(cur_y**2)))
        print(angle, dist, cur_x, cur_y)
        if cur_y >= 0 and cur_x < 0: # 2nd Quadrant
            me.rotate_counter_clockwise(-angle + (180 + ret_angle))
            print("2nd", -angle, (180 - ret_angle), cur_x, cur_y, start_angle, cur_angle)
        elif cur_y >= 0 and cur_x >= 0: #1st Quadrant
            me.rotate_counter_clockwise(angle + 180 - ret_angle)
            print("1st", angle, -angle + 180 - ret_angle, ret_angle, cur_x, cur_y, start_angle, cur_angle)
        elif cur_y < 0 and cur_x < 0: #3rd Quadrant
            #angle -= 180
            me.rotate_counter_clockwise(-(angle - 180) - ret_angle)
            print("3rd", -angle, -angle - ret_angle)
        elif cur_y < 0 and cur_x >= 0: #4th Quadrant
            #angle -= 180
            me.rotate_counter_clockwise(angle - 180 + ret_angle)
            print("4th", -angle, -angle - ret_angle)
        me.move_forward(dist)
        me.land()
        return cur_x, cur_y, cur_angle


        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)

    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)

    cv2.putText(img, f'({(points[-1][0] - 500) / 100},{(points[-1][1] - 500) / 100})m', (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)


if __name__ == '__main__':
    # Extracting user input for coords
    cur_x = 0
    cur_y = 0
    cur_angle = 0
    start_angle = me.get_yaw()
    while True:
        # Setting up mapping image
        img = np.zeros((1000, 1000, 3), np.uint8)
        # User input for coordi0nates
        coordinates = str(input())
        coords = coordinates.split(',')
        x = int(coords[0].strip())
        y = int(coords[1].strip())
        take_off = int(coords[2].strip())
        print("main", x, y, take_off, cur_x, cur_y, start_angle)
        # Go to state if exists
        if 1 >= take_off >= -1:
            cur_x, cur_y, cur_angle = goto(-x, y, take_off, start_angle)
        else:
            continue
        points.append((cur_x, cur_y))
        # drawPoints(img, points)
        # cv2.imshow("Output", img)
        # cv2.waitKey(0)
        # Getting current location to add point to image

        #cur_angle = me.get_yaw()
        #cur_dist = me.get_distance_tof()
        #cur_x = cur_angle * math.cos(cur_dist)
        #cur_y = cur_angle * math.sin(cur_dist)
