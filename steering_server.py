from socket import *
import vgamepad as vg
import time
import math


def steer():
    gamepad = vg.VX360Gamepad()
    # initialize all values
    camera_height = 480
    camera_width = 640
    error_compensate = 20
    height_from_bottom_to_top = 130
    x2, y2 = 320, 50  # reference point on the semi circle
    radius = 300  # bottom to top (center to top blue)
    host = ""
    port = 13000
    buf = 1024
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.bind(addr)
    print("waiting to receive message....")
    # the direction at a certain point
    def direction(x1, y1, x2, y2):
        # x1<=340 and x1>=300
        #if (camera_width / 2) + error_compensate >= x1 and  x1 >= (camera_width / 2) - error_compensate:
        #    gamepad.left_joystick(x_value=0, y_value=0)
        #    gamepad.update()
        #else:
        distance_square = (x1 - x2) ** 2 + (y1 - y2) ** 2
        theta = math.acos(1 - (distance_square / (2 * radius * radius)))
        l_arc = theta * radius
        if x1 > camera_width / 2:
            l_arc = l_arc * -1
        print(int(l_arc))
        turn = l_arc*81
        gamepad.left_joystick(x_value=int(turn), y_value=0) # x values between -32768 and 32767
        gamepad.update()
        time.sleep(0)

        return

    while True:
        (data, addr) = UDPSock.recvfrom(buf)
        data = str(data) #convert bytes to string
        if data == "quit": break
        data = data.split("]")[0] # get only 2 coordinates
        data = data.replace("[", "")
        # print(matches)
        x1, y1 = data.split(",")[0], data.split(",")[1]
        x1 = x1[2:]
        x1, y1 = int(x1.strip()), int(y1.strip())
        direction(x1, y1, x2, y2)

    UDPSock.close()


steer()
"""
law of cosines
length of arc is given as L = r times theta
r = radius
theta = angle of circle
theta = cos_inverse(1-(d_square/2*radius_square))
Hence the arc length will have uniform values accross

"""
