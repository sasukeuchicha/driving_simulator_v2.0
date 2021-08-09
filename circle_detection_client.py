from socket import *
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

#intitalize values here
host = "192.168.0.2"
port = 13000
addr = (host,port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
#initializing memory management array
camera_width = 640
camera_height = 480
width,height = camera_width,camera_height
# define the lower and upper boundaries of the "blue" object in the HSV color space
# https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv
blueLower = np.array([110, 50, 50])
blueUpper = np.array([255, 255, 255])
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (camera_width, camera_height)
camera.framerate = 60
rawCapture = PiRGBArray(camera, size=(camera_width, camera_height))
# allow the camer
time.sleep(1.0)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    frame = frame.array
    #blur frame captured
    frame_gau_blur = cv2.GaussianBlur(frame,(3, 3), 0)
    #convert bgr to hsv
    hsv = cv2.cvtColor(frame_gau_blur, cv2.COLOR_BGR2HSV)
    # getting the range of blue color in frame
    blue_range = cv2.inRange(hsv, blueLower, blueUpper)
    res_blue = cv2.bitwise_and(frame_gau_blur,frame_gau_blur, mask=blue_range)
    blue_s_gray = cv2.cvtColor(res_blue, cv2.COLOR_BGR2GRAY)
    canny_edge = cv2.Canny(blue_s_gray, 50, 240)
    # applying HoughCircles

    circles = cv2.HoughCircles(canny_edge, cv2.HOUGH_GRADIENT, dp=1, minDist=10, param1=10, param2=20, minRadius=5, maxRadius=15)
    cir_cen = []
    #cv2.circle(canny_edge, (320, 240), 0, (0, 255, 0), 4)
    #cv2.imshow("canny", frame)
    #print(circles)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        circles = np.round(circles[0, : ]).astype("int")
        # loop over (x, y) and radius
        # [[21,21,4], [231,231,5]]
        for (x, y, r) in circles:
            cir_cen.append([x, y])
            # draw circle on output image and rectangle
            print(cir_cen)
            UDPSock.sendto(str(cir_cen).encode("utf-8"), addr)
            time.sleep(0.01)
            # corresponding to the center of thecircle
            #cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            #cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        #cv2.imshow("output", np.hstack([frame, frame]))
    #print (cir_cen)
    #cv2.imshow('circles', frame)
    #cv2.imshow('gray', blue_s_gray)
    #cv2.imshow('canny', canny_edge)
    k = cv2.waitKey(5) & 0xFF
    if k == ord("q"):
        break
    # show the frame
    #cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
UDPSock.close()
'''
while True:
    data = input("Enter message here : ")
    UDPSock.sendto(data.encode("utf-8"), addr)
    if data == "exit":
        break
UDPSock.close()
'''
'''
x = 640/2
y = 0
top = (x, y)
center = (640/2, 480) -->0
#320 = camera_width/2 and 240 = camera_height/2
z = ((x-640/2)/320)+(y/480)


'''







