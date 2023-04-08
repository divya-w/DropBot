import time
import os
import platform
import sys
import release
import camera_capture

from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil

vehicle = connect('/dev/ttyAMA0', baud=57600, wait_ready=True)
# Select /dev/ttyAMA0 for UART. /dev/ttyACM0 for USB

def arm_and_takeoff(targetLat, targetLon, targetHeight):
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
        vehicle.airspeed = 0.5
        vehicle.simple_takeoff(1)
        vehicle.simple_goto(LocationGlobalRelative(targetLat, targetLon, targetHeight))
        #vehicle.simple_takeoff(targetHeight)  # meters

        while True:
                print("Current Altitude: %d" % vehicle.location.global_relative_frame.alt)
                if vehicle.location.global_relative_frame.alt >= .95*targetHeight:
                        break
                time.sleep(1)
        print("Target altitude reached!!")

        return None

############ MAIN###############

# Set pointHome to current location of drone
pointHome_lat = vehicle.location.global_relative_frame.lat
pointHome_lon = vehicle.location.global_relative_frame.lon

# Arms and flies drone into air
arm_and_takeoff(pointHome_lat, pointHome_lon, 4)

#Setting vehicle speed
print("Setting speed to 2")
vehicle.airspeed = 0.5
time.sleep(1)

# Send vehicle to coordinate
print("Going to first point for 10 seconds")
lat = 29.7192454
lon = -95.4038727
alt = 4
point1 = LocationGlobalRelative(lat, lon, alt)
vehicle.simple_goto(point1)
time.sleep(5)

# Land
vehicle.mode = VehicleMode("LAND")
while vehicle.mode != 'LAND':
    time.sleep(1)
    print("Waiting for drone to land")
print("Landed")
time.sleep(10)

#Dropping off package
release.release()
time.sleep(10)

# Take Off and set speed
arm_and_takeoff(lat, lon, 4)
print("Taking Off")
vehicle.airspeed = 0.5
time.sleep(5)

#Taking photo of package
camera_capture.capture()
time.sleep(5)

# Return to launch
newHome1 = LocationGlobalRelative(pointHome_lat, pointHome_lon, 4)
print("Returning to launch")
vehicle.simple_goto(newHome1)
time.sleep(10)
newHome2 = LocationGlobalRelative(pointHome_lat, pointHome_lon, 0.5)
print("Landing")
vehicle.simple_goto(newHome2)
time.sleep(3)


# Land at launch
vehicle.mode = VehicleMode("LAND")
while vehicle.mode != 'LAND':
    time.sleep(1)
    print("Waiting for drone to land")
print("Landed")

print(pointHome_lat, pointHome_lon)
print("Closing vehicle")
vehicle.close()
