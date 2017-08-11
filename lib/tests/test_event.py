import sys
sys.path.append('../events')

import os
import unittest
import events

class FakeReceiver(events.BaseEventReceiver):

    def on_event(self, event):
        pass

class NotReceiverClass(object):

    def on_event(self, event):
        pass


class TestSettings(unittest.TestCase):

    def test_register_event_receiver(self):
        rcv = FakeReceiver()
        events.register_event_receiver(rcv)

    def test_register_event_receiver_with_wrong_object(self):
        rcv = NotReceiverClass()
        try:
            events.register_event_receiver(rcv)
            self.fail('Should raise error')
        except AssertionError:
            self.assertFalse(isinstance(rcv, events.BaseEventReceiver))

if __name__ == '__main__':
    unittest.main()
