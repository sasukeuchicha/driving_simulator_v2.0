import RPi.GPIO as GPIO
import time
from socket import *

# clientinformation
host = "192.168.0.2"
port = 13001
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)

# set GPIO numbering mode and define input pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
count = 0
# initailize any values that need to be initialized
# 13 = brake
# 16 = accelerator

def push_brake():
    data = "Brake"
    UDPSock.sendto(data.encode("utf-8"), addr)
    print(data)
def push_accelerator():
    data = "Accelerator"
    UDPSock.sendto(data.encode("utf-8"), addr)
    print(data)
def release_brake():
    data = "Brake Release"
    UDPSock.sendto(data.encode("utf-8"), addr)
    print(data)
def release_accelerator():
    data = "Accelerator Release"
    UDPSock.sendto(data.encode("utf-8"), addr)
    print(data)
try:
    Release = set()
    Release.add("Release Both")
    Release.add("Release Brake")
    Release.add("Release Acc")
    button_history = "Release Both"
    Push = set()
    Push.add("Push Both")
    Push.add("Push Acc")
    Push.add("Push Brake")
    
    while True:
        if GPIO.input(13) == GPIO.HIGH and GPIO.input(16) == GPIO.HIGH:
            push_brake()
            push_accelerator()
            button_history = "Push Both"
            time.sleep(0.05)
            print("1")
            continue
        elif GPIO.input(13)==GPIO.HIGH:
            push_brake()
            button_history = "Push Brake"
            time.sleep(0.05)
            print("3")
            continue
        elif GPIO.input(16) == GPIO.HIGH:
            push_accelerator()
            button_history = "Push Acc"
            time.sleep(0.05)
            print("4")
            continue
        elif GPIO.input(13) == GPIO.LOW and GPIO.input(16) == GPIO.LOW and (button_history not in Release):
            release_brake()
            release_accelerator()
            button_history = "Release Both"
            print("2")
        elif GPIO.input(13) == GPIO.LOW and (button_history not in Release):
            release_brake()
            button_history = "Release Brake"
            print("5")
        elif GPIO.input(16) == GPIO.LOW and (button_history not in Release):
            release_accelerator()
            button_history = "Release Acc"
            print("6")
        time.sleep(0.1)

finally:
    GPIO.cleanup()
