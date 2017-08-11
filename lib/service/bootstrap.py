# Bootstrap module
import sys
from http_service import HTTPService
from gpio_button_service import GPIOButtonService
from joystick_service import JoystickService

from secondscreen.secondscreen_receiver import *

http = HTTPService()
gpio_button = GPIOButtonService()
joystick = JoystickService()

def start_server():
    joystick.start()
    gpio_button.start()
    http.start()

def stop_server():
    joystick.stop()
    gpio_button.stop()
    http.stop()
