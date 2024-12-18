import os
from typing import Callable, Union

from RATapi.rat_core import EventBridge, EventTypes, PlotEventData, ProgressEventData


def notify(event_type: EventTypes, data: Union[str, PlotEventData, ProgressEventData]) -> None:
    """Calls registered callbacks with the data when event type has
    been triggered.

    Parameters
    ----------
    event_type : EventTypes
        The event type that was triggered.
    data : str or PlotEventData or ProgressEventData
        The data sent by the event. The message event data is a string.

    """
    callbacks = __event_callbacks[event_type]
    for callback in callbacks:
        callback(data)


def get_event_callback(event_type: EventTypes) -> list[Callable[[Union[str, PlotEventData, ProgressEventData]], None]]:
    """Returns all callbacks registered for the given event type.

    Parameters
    ----------
    event_type : EventTypes
        The event type.

    Returns
    -------
    callback : Callable[[Union[str, PlotEventData, ProgressEventData]], None]
        The callback for the event type.

    """
    return list(__event_callbacks[event_type])


def register(event_type: EventTypes, callback: Callable[[Union[str, PlotEventData, ProgressEventData]], None]) -> None:
    """Registers a new callback for the event type.

    Parameters
    ----------
    event_type : EventTypes
        The event type to register.
    callback : Callable[[Union[str, PlotEventData, ProgressEventData]], None]
        The callback for when the event is triggered.

    """
    if not isinstance(event_type, EventTypes):
        raise ValueError("event_type must be a events.EventTypes enum")

    if len(__event_callbacks[event_type]) == 0:
        __event_impl.register(event_type)
    __event_callbacks[event_type].add(callback)


def clear(key=None, callback=None) -> None:
    """Clears all event callbacks or specific callback.

    Parameters
    ----------
    callback : Callable[[Union[str, PlotEventData, ProgressEventData]], None]
        The callback for when the event is triggered.

    """
    if key is None and callback is None:
        for key in __event_callbacks:
            __event_callbacks[key] = set()
    elif key is not None and callback is not None:
        __event_callbacks[key].remove(callback)

    for value in __event_callbacks.values():
        if value:
            break
    else:
        __event_impl.clear()


dir_path = os.path.dirname(os.path.realpath(__file__))
os.environ["RAT_PATH"] = os.path.join(dir_path, "")
__event_impl = EventBridge(notify)
__event_callbacks = {EventTypes.Message: set(), EventTypes.Plot: set(), EventTypes.Progress: set()}
