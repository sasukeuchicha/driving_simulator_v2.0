# import vgamepad as vg
from socket import *
import time
# importing directkeys for using press key and release key functions
from directkeys import W, S
from directkeys import PressKey, ReleaseKey


def baa():

    host = ""
    port = 13001
    buf = 30
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.bind(addr)
    print("waiting to receive message....")

    # warm up the controller
    # gamepad = vg.VX360Gamepad()
    time.sleep(3.0)
    w_pressed = False
    s_pressed = False

    """
    # press a button to wake the device up
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(0.5)
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(0.5)
    """

    # press button
    try:
        while True:
            (data, addr) = UDPSock.recvfrom(buf)
            print(data)
            data = str(data.decode("utf-8"))
            if str(data) == "Brake Release" and s_pressed:
                print(str(data))
                # gamepad.left_trigger(0)
                # gamepad.update()
                ReleaseKey(S)
                s_pressed = False
                time.sleep(0.01)
            if str(data) == "Accelerator Release" and w_pressed:
                print(str(data))
                # gamepad.right_trigger(0)
                # gamepad.update()
                ReleaseKey(W)
                w_pressed = False
                time.sleep(0.01)
            if str(data) == "Accelerator" and not w_pressed:
                print(str(data))
                # gamepad.right_trigger(200)
                # gamepad.update()
                PressKey(W)
                w_pressed = True
                time.sleep(0.01)
            if str(data) == "Brake" and not s_pressed:
                print(str(data))
                # gamepad.left_trigger(200)
                # gamepad.update()
                PressKey(S)
                s_pressed = True
                time.sleep(0.01)

    finally:
        UDPSock.close()


baa()
