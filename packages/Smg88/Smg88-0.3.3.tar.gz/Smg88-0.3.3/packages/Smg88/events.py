from json import JSONDecodeError
import json
from typing import Callable, Dict, List
from Smg88 import loghelp
from Smg88.errors import SafeCatchAll
import errors


class EventError(errors.Error):
    """The base class for all errors in this module
    """
    ...


class EventSubscriberCallbackError(EventError):
    """Class of error parenting all errors related to subscriber callbacks
    """
    ...


class EventSubscriberCallbackErrorNotCallable(EventSubscriberCallbackError):
    """Error raised when a subscriber callback is not callable
    """
    ...


class Event():
    """Event class represents an event that can be posted and subscribed to

    Attributes:
      channel: str
        The channel to which the event is said to be existing in
      name: str
        The name of the event, used for easy identification
      payload: str
        The payload of the event, used to convey the information of the event, usually in JSON format
    """
    channel: str = ...
    name: str = ...

    payload: str = ...

    def __init__(self, *, channel: str = ..., name: str = ..., payload: str = ..., **kwargs) -> None:
        self.channel = channel
        if self.channel is ...:
            # TODO add warning for instinating event without channel handle
            ...
        if type(self.channel) is not str:
            # TODO add warning for instinating event with non-serializable (not str) channel handle
            ...
        self.name = name
        if self.name is ...:
            # TODO add warning for instinating event without name handle
            ...
        if type(self.name) is not str:
            # TODO add warning for instinating event with non-serializable (not str) name handle
            ...
        self.payload = payload
        if self.payload is ...:
            # TODO add warning for instinating event without payload
            ...
        if type(self.payload) is not str:
            # TODO add warning for instinating event with non-serializable (not str) payload
            ...

    def send(self, /, stage=..., **kwargs) -> None:
        """Posts the event to the given EventStage as if EventStage.post(event=self) was called (hint it is : )

        Args:
          stage: EventStage
            The stage to which the event is sent too
            Note: Annotation for stage is not possible as this is a convenience method
        """
        try:
            stage.post(event=self)
        except SafeCatchAll as err:
            # TODO add warning for eventstage post failure
            raise err


class HeartBeatEvent(Event):
    """Event class representing a heartbeat event

    For __docs__ on Event, see Event.__doc__ NOT here!
    Attributes:
      channel: str = "Smg88::HeartBeat"
        The channel to which the event is said to be existing in
      name: str = f"Smg88 HeartBeat ({self.count}) at about {loghelp.now()}"
      payload: str = JSON Format below:
        {
          "count": int,
          "approxtime": str,
        }
    """
    count: int = ...

    def __init__(self, count: int = -1, *, channel: str = ..., name: str = ..., timestr: str = ..., payload: str = ..., **kwargs) -> None:
        self.count = count
        if type(self.count) is not int:
            # TODO add warning for non-serializable (not int) count
            ...
        self.timestr = timestr
        if self.timestr is ...:
            self.timestr = loghelp.now()
        if self.timestr is not str:
            # TODO add warning for non-serializable (not str) timestr
            ...
        self.payload = payload
        if self.payload is ...:
            self.payload = {
                "count": self.count,
                "approxtime": self.timestr,
            }
        self.name = name
        if self.name is ...:
            self.name = f"Smg88 HeartBeat ({self.count}) at about {self.timestr}"
        if self.name is not str:
            # TODO add warning for non-serializable (not str) name
            ...
        try:
            self._package = json.dumps(self.payload)
        except JSONDecodeError:
            ...
        super().__init__(channel=channel, name=name, payload=payload, **kwargs)


class EventStage():
    """Represents a place for events to occur
    Events are objects that have a channel and a name, all events are passed to all subscribers of that event's channel

    Events can be posted to this stage by instancing the 'Event' object and calling EventStageInstance.post(EventInstance)
    Or, shorthand, call 'send' on an Event instance with the EventStage instance

    Attributes:
      nameHandle: str
      A common name for the EventStage, needed to connect to the EventStage
      subscriptions: Dict[str, Callable.__name__]
      Is a property exposing the subscriptions of the stage, the key is the channel and the value is the name of the subscriber's function

      _subscriptions: Dict[str, Callable]
      A dictionary of channel names to functions that are subscribed to that channel name
      _eventBuffer: List[Event]
      A buffer of events to post to the stage
    """
    _subscriptions: Dict[str, Callable] = ...
    nameHandle: str = ...

    _eventBuffer: List[Event] = ...

    def __init__(self, nameHandle: str = ...) -> None:
        self.nameHandle = nameHandle
        if self.nameHandle is ...:
            # TODO add warning for instinating an EventStage without a nameHandle
            ...
        if type(self.nameHandle) is not str:
            # TODO add warning for instinating an EventStage without a serializable (str) nameHandle
            ...
        self._subscriptions = {}
        self._eventBuffer = []

    def post(self, event: Event = ..., /, **kwargs) -> None:
        if event is ...:
            # TODO add warning for not passing an event
            raise errors.InappropriateRequest("No event was passed to the post method",
                                              errorHandle=errors.ProgrammerErrorHandle("Must pass an event to the post method"))
        self._eventBuffer.append(event)

    def _post(self, /, num: int = 1, *, all: bool = False, retain: bool = ..., **kwargs) -> None:
        if all:
            if retain is ...:
                retain = True
            if not retain:
                # TODO Warn for purging buffer
                ...
            self._postn(num=len(self._eventBuffer),
                        retain=bool(retain) ** kwargs)

    def _postn(self, /, num: int = 1, *, retain: bool = False, **kwargs) -> None:
        for _ in range(num):
            self._eventBuffer.pop(0)

    def _handle(self, event: Event) -> None:
        subscribers = [subscriber for channel, subscriber in self._subscriptions.items()
                       if channel == event.channel]
        for subscriber in subscribers:
            try:
                subscriber(event=event)
            except SafeCatchAll as err:
                # TODO add warning for subscriber callback error
                raise err


class EventStageHeartbeat():
    stage: EventStage = ...

    def __init__(self, stage: EventStage = ...) -> None:
        ...


class AutoEventStage(EventStage):
    heartbeat: EventStageHeartbeat = ...

    def __init__(self, *, nameHandle: str = ..., /, heartbeat) -> None:
        super().__init__(nameHandle)
