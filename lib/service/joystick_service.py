import time
import threading
import logging
import struct

from events.events import *

class JoystickEventProducer(object):

    started = False
    file = None
    index = 0

    def __init__(self, file, index):
        self.file = file
        self.index = index

    def _loop(self):

        js = open(self.file, 'rb')

        while self.started:
            evbuf = js.read(8)
            if evbuf:
                time, value, type, number = struct.unpack('IhBB', evbuf)
                if not (type & 0x80) and (type & 0x01):
                    if value == 1:
                        e = Event('joystick_button_pressed', {'joystick_num': self.index, 'button_num': number})
                        notify_event_receivers(e)

    def start(self):
        self.started = True
        t = threading.Thread(target=self._loop)
        t.daemon = True
        t.start()

    def stop(self):
        self.started = False


class JoystickService(object):

    started = False

    event_producers = [JoystickEventProducer('/dev/input/js0', 0), JoystickEventProducer('/dev/input/js1', 1)]

    def __init__(self):
        pass

    def _loop(self):

        for producer in self.event_producers:
            producer.start()


    def start(self):
        logging.info('Starting Joystick service...')
        self.started = True
        t = threading.Thread(target=self._loop)
        t.daemon = True
        t.start()

    def stop(self):
        for producer in self.event_producers:
            producer.stop()
        self.started = False
