from djitellopy import tello
import KeyPressModule as kp
import math

### Bug 1 Algorithm:
# 1. Head to goal
# 2. If obstacle is encountered circumnavigate it (remember how close to goal)
# 3. Return to closest point and continue heading to goal

me = tello.Tello()
me.connect()
print(me.get_battery())

def HeadToGoal(goal_x, goal_y):
    # Starting position is 0,0
    # yaw = -65 is pointing north
    to_rotate = -65 - (me.get_yaw())

    # Calculate angle and distance 
    angle = int(math.degrees(math.atan(goal_y/goal_x)))
    dist = int(math.sqrt((goal_x **2) + (goal_y **2)))
    #print(angle, dist)

    # 1. Rotate drone to desired coordinate 
    # 2. Fly in straight line (forward)
    me.takeoff()
    me.rotate_counter_clockwise(to_rotate)
    me.rotate_counter_clockwise(angle)
    me.move_forward(dist)
    me.land()


def WallFollow():
    pass

if __name__ == "__main__":
    HeadToGoal(1, 20)