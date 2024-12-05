import logging
import traceback
from typing import Callable, Optional, Union

from atap_corpus_loader.controller.events import EventType


class EventManager:
    def __init__(self, logger_name: str):
        self.logger_name = logger_name

        self.callback_mapping: dict[EventType, list[Callable]] = {}
        self.reset_callbacks()

    def log(self, msg: str, level: int):
        logger = logging.getLogger(self.logger_name)
        logger.log(level, msg)

    def reset_callbacks(self):
        self.callback_mapping = {e: [] for e in EventType}

    def register_event_callback(self, event_type: Union[str, EventType], callback: Callable, first: bool):
        if not callable(callback):
            raise TypeError("Provided callback function must be callable")
        if isinstance(event_type, str):
            try:
                event_type = EventType[event_type.upper()]
            except KeyError:
                raise ValueError(f"Provided event_type string does not correspond to an EventType value: {event_type}")
        callback_ls = self.callback_mapping[event_type]
        position = len(callback_ls)
        if first:
            position = 0
        self.callback_mapping[event_type].insert(position, callback)
        self.log(f"New callback registered for event '{event_type.name}'. Callback: {callback}", logging.INFO)

    def trigger_callbacks(self, event_type: Union[str, EventType], *callback_args):
        if isinstance(event_type, str):
            try:
                event_type = EventType[event_type.upper()]
            except KeyError:
                raise ValueError(f"Provided event_type string does not correspond to an EventType value: {event_type}")

        callback_list: Optional[list[Callable]] = self.callback_mapping.get(event_type)
        if callback_list is None:
            raise ValueError(f"No callbacks registered for event type: {event_type.name}")
        for callback in callback_list:
            try:
                callback(*callback_args)
                self.log(f"Callback executed for event '{event_type.name}'. Callback: {callback}", logging.INFO)
            except Exception as e:
                self.log(f"Exception while executing callback for event '{event_type.name}': \n{traceback.format_exc()}", logging.ERROR)
