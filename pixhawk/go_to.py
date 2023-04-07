import time
import os
import platform
import sys

from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil

vehicle = connect('/dev/ttyAMA0', baud=57600, wait_ready=True)
# Select /dev/ttyAMA0 for UART. /dev/ttyACM0 for USB

def arm_and_takeoff(targetHeight):
        print("Basic pre-arm checks")
        while vehicle.is_armable != True:
                print("Waiting for vehicle to become armable.")
                time.sleep(1)

        print("Arming motors")
        vehicle.mode = VehicleMode("GUIDED")
        vehicle.armed = True

        while vehicle.mode != 'GUIDED':
                print("Waiting for drone to enter GUIDED flight mode")
                time.sleep(1)
        print("Vehicle now in GUIDED MODE. Have fun!!")

        while vehicle.armed != True:
            print("Waiting for vehicle to arm")
            time.sleep(1)

        print("Taking off!")
        vehicle.simple_takeoff(targetHeight)  # meters

        while True:
                print("Current Altitude: %d" % vehicle.location.global_relative_frame.alt)
                if vehicle.location.global_relative_frame.alt >= .95*targetHeight:
                        break
                time.sleep(1)
        print("Target altitude reached!!")

        return None

############ MAIN###############

# Set pointHome to current location of drone
pointHome = vehicle.location.global_relative_frame

# Arms and flies drone into air
arm_and_takeoff(3)

#Setting vehicle speed
print("Setting speed to 2")
vehicle.airspeed = 0.5
time.sleep(1)

# Send vehicle to coordinate
print("Going to first point for 10 seconds")
point1 = LocationGlobalRelative(29.7187102, -95.4054397, 3)
vehicle.simple_goto(point1)
time.sleep(10)

# Land
vehicle.mode = VehicleMode("LAND")
while vehicle.mode != 'LAND':
    time.sleep(1)
    print("Waiting for drone to land")
print("Landed")
time.sleep(10)

# Take Off
arm_and_takeoff(3)
print("Taking Off")
vehicle.airspeed = 0.5

# Return to launch
print("Returning to launch")
vehicle.simple_goto(pointHome)
time.sleep(10)

# Land at launch
vehicle.mode = VehicleMode("LAND")
while vehicle.mode != 'LAND':
    time.sleep(1)
    print("Waiting for drone to land")
print("Landed")

print("Closing vehicle")
vehicle.close()
