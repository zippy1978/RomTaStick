# Event receivers registered
event_receivers = []

def register_event_receiver(receiver):
    assert isinstance(receiver, BaseEventReceiver)
    event_receivers.append(receiver)

def notify_event_receivers(event):
    for er in event_receivers:
        er.on_event(event)

class Event(object):

    type = None
    data = None

    def __init__(self, type, data=None):
        self.type = type
        self.data = data

class BaseEventReceiver(object):

    def on_event(self, event):
        raise NotImplementedError('Method not implemented')
