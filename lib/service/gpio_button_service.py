import RPi.GPIO as GPIO
import time
import threading
import logging

from events.events import *

class GPIOButtonService(object):

    started = False
    button_gpios = [17, 18]

    def __init__(self):
        # GPIO buttons are 17 and 18
        GPIO.setmode(GPIO.BCM)
        self._gpio_setup()

    def _gpio_setup(self):
        for gpio_num in self.button_gpios:
            GPIO.setup(gpio_num, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def _is_button_pressed(self, btn_num):
        return GPIO.input(btn_num) == False

    def _loop(self):
        while self.started:
            for gpio_num in self.button_gpios:
                if self._is_button_pressed(gpio_num):
                    e = Event('gpio_button_pressed', {'button_num': gpio_num})
                    notify_event_receivers(e)
            time.sleep(0.1)

    def start(self):
        logging.info('Starting GPIO Button service...')
        self.started = True
        t = threading.Thread(target=self._loop)
        t.daemon = True
        t.start()

    def stop(self):
        self.started = False
