from typing import Callable
from src.event.event import Event
from src.eventbus.eventbus import EventBus
from src.eventbus_client.subscriber.closure_event_listener import ClosureEventListener
from src.eventbus_client.subscriber.local_eventbus_subscriber import LocalEventBusSubscriber


class LocalEventBusClosureSubscriber(LocalEventBusSubscriber, ClosureEventListener):
    """
    Subscriber which works with local eventbus, this class can be initialized and used stand-alone

    Author: Nicola Ricciardi
    """

    def __init__(self, eventbus_instance: EventBus, on_event_callback: Callable[[str, Event], None]):
        LocalEventBusSubscriber.__init__(self, eventbus_instance)
        ClosureEventListener.__init__(self, on_event_callback)