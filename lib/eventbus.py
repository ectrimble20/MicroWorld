"""
Event handling module

This module is designed to allow "globalized" event handling via a bind system.

An event type can be bound to any callable method.  When an event of a specific type is detected, it is then handed
off to the bound method.  The raw event (PyGame Event object) is passed directly to the method handling the event,
this means that the receiving event must handle at least 1 argument.

Custom events can be defined using the register_new_event method.  This returns a new ID for use when creating an
event with the build_event method.

Note that this module does not keep track of new event types created and this should be handled as needed by whatever
is creating the new event types.

@version 0.0.2
"""
import logging
from pygame import USEREVENT
from pygame.event import Event, get, post, custom_type


__all__ = ['bind_listener', 'unbind_listener', 'clear_listeners', 'post_event', 'process_event_queue',
           'register_new_event', 'set_current_ui', 'unset_current_ui', 'ui_event_map']


# Dict of bound listeners, EventType => List[callable, ...]
_listeners = {}

# Dict of greedy listeners, these over-write the base listeners and effectively pause everything else from listening
_greedy = {}

# this is a hook for the UI manager from PyGameGUI
_current_ui_mgr = None

ui_event_map = {}


def set_current_ui(ui_manager):
    global _current_ui_mgr
    _current_ui_mgr = ui_manager


def unset_current_ui():
    global _current_ui_mgr
    _current_ui_mgr = None


# change:  Added *event_types to allow the function to accept multiple event types for a single listener
def bind_listener(listener: callable, *event_types) -> None:
    """
    Bind a listener function to event types
    :param listener: callable
    :param event_types: List[int]
    :return: None
    """
    for event_type in event_types:
        if event_type not in _listeners.keys():
            _listeners[event_type] = []
        _listeners[event_type].append(listener)
        logging.debug(f"Listener<{listener}> bound to event type {event_type}")


# change: Added *event_types to allow the function to accept multiple event types for a single listener
def unbind_listener(listener: callable, *event_types) -> None:
    """
    Unbind a listener function from an event type
    Note: prints warnings if an invalid event type or a non-existent listener is passed
    :param listener: callable
    :param event_types: List[int]
    :return: None
    """
    for event_type in event_types:
        if event_type not in _listeners.keys():
            logging.debug(f"Event type {event_type} not present in listener binds")
            return None
        if listener not in _listeners[event_type]:
            logging.warning(f"Listener <{listener}> not present in listener binds")
            return None
        _listeners[event_type].remove(listener)
        logging.debug(f"Listener<{listener}> unbound from event type {event_type}")


# change: added greedy binding
def bind_greedy(listener: callable, *event_types):
    for event_type in event_types:
        if event_type not in _greedy.keys():
            _greedy[event_type] = []
        _greedy[event_type].append(listener)
        logging.debug(f"Listener<{listener}> greedily bound to event type {event_type}")


# change: added greedy unbinding
def unbind_greedy(listener: callable, *event_types):
    for event_type in event_types:
        if event_type not in _greedy.keys():
            logging.debug(f"Event type {event_type} not present in listener binds")
            return None
        if listener not in _greedy[event_type]:
            logging.warning(f"Listener <{listener}> not present in listener binds")
            return None
        _greedy[event_type].remove(listener)
        # lastly, check if the greedy list for the event type is empty, if so, remove it
        if len(_greedy[event_type]) == 0:
            del _greedy[event_type]
        logging.debug(f"Listener<{listener}> greedily unbound from event type {event_type}")


def clear_listeners() -> None:
    """
    Clears the listener binds, useful when switching out of a scene that simply needs to not respond to events anymore
    :return: None
    """
    _listeners.clear()
    logging.debug("All listeners cleared")


def post_event(event_type_id: int, **kwargs) -> None:
    """
    Create and post an event to the SDL event queue
    :param event_type_id: event type ID
    :param kwargs: key,value pairs of arguments to pass to the event
    :return:
    """
    post(Event(event_type_id, **kwargs))


def process_event_queue() -> None:
    """
    Processes the PyGame event queue and hands off events to any listeners registered to handle them

    If an event is set in the greedy listeners, it will call that instead of the regular listener group.  This allows
    a greedy listener to effectively block other listeners from receiving the event.  The purpose of this is to allow
    a focused element to grab all events of a type without them being propagated to another listener.  An example of
    this might be an input box accepting text and there might be another listener that will cause the scene to end if
    the 'q' key is entered.  Without a greedy block, typing "Hey quit it" would cause the scene to stop at the 'q' due
    to the other listener still processing the key input.

    :return: None
    """
    for event in get():
        # handle custom event mapping from PyGameGUI USEREVENT calls.
        if event.type == USEREVENT:
            if event.user_type in ui_event_map.keys():
                post_event(ui_event_map[event.user_type], ui_element=event.ui_element)
        if event.type in _greedy.keys():
            for listener in _greedy[event.type]:
                listener(event)
        elif event.type in _listeners.keys():
            for listener in _listeners[event.type]:
                listener(event)
        # propagate to the UI manager if it's set
        if _current_ui_mgr is not None:
            _current_ui_mgr.process_events(event)


def register_new_event() -> int:
    """
    Calls the custom_type function from the PyGame event module to create a new user type, effectively registering a new
    event type ID that can be used.
    :return: int
    """
    n_type = custom_type()
    logging.debug(f"New Event Type {n_type} registered")
    return n_type

