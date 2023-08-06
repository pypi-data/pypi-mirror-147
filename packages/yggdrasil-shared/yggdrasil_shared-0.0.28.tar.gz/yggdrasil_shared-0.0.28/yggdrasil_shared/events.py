import dataclasses
from copy import deepcopy
from datetime import datetime
from functools import wraps
import logging
import typing

_logger = logging.getLogger(__name__)


class BaseEvent:
    _event_name = None

    def send(self, dispatch):
        dispatch(self._event_name, {
            "EVENT_NAME": self._event_name,
            "body": dataclasses.asdict(self),
        })
        _logger.debug(f"Event dispatched: {self._event_name}")


@dataclasses.dataclass
class GenericEvent:
    object_type: str  # e.g. iaas.instance
    action_type: str  # e.g. created, updated
    object_details: dict
    object_id: str
    created_at: datetime
    user: typing.Optional[str] = None  # user-id, null in case of system event
    meta: typing.Optional[dict] = None  # Optionally some more details about the action

    @property
    def name(self):
        return f"{self.object_type}.{self.action_type}"

    @property
    def payload(self):
        payload = dataclasses.asdict(self)
        payload['created_at'] = payload['created_at'].isoformat()
        return payload


class EventSource:
    """
    The responsibility of this decorator is to raise a generic event based on the
    parameters describing some action.
    It is meant to be used on controllers' methods and it expects:
    * the method to return a JSON serializable representation of a business object.
    * The service has an attribute named `dispatch` which should be provided
      via `nameko.events.EventDispatcher`

    for example imagine we have a method in a controller like this:

    @rpc
    def create_network(access_info, network_params):
      network_obj = self.net_service.create(access_info, network_params)
      return schemas.NetworkSchema().dump(network_obj)

    We could apply this decorator so we have an event in the system when someone creates
    a network.
    All you need to do is to apply the decorator like:

    @EventSource.publish("iaas.network", "created")

    where the first parameter is the object type and the second parameter is the type of
    action.

    You can directly use `dispatch_event` method on this class to raise a GenericEvent
    object in the system too.


    """
    dispatch = 'dispatch'

    @staticmethod
    def publish(object_type: str, action_type: str, exclude_fields: list = None):
        """

        exclude_fields is a list of field names that you don't want to be in the event data
        for example in OSS create access-key we return secret-key for user but we don't want to have
        secret-key in somewhere else.
        :param object_type:
        :param action_type:
        :param exclude_fields:
        :return:
        """
        def decorator(method):
            @wraps(method)
            def wrapper(svc, *args, **kwargs):
                try:
                    user_id = args[0]['user']['id']
                except (KeyError, IndexError):
                    user_id = None
                result = method(svc, *args, **kwargs)
                dispatch = getattr(svc, EventSource.dispatch)
                if dispatch is None:
                    raise Exception("'dispatch' dependency is not defined in the service")
                event_details = deepcopy(result)
                if exclude_fields:
                    for field in exclude_fields:
                        event_details.pop(field)
                EventSource.dispatch_event(
                    dispatch=dispatch,
                    event=GenericEvent(
                        object_type=object_type,
                        action_type=action_type,
                        object_details=event_details,
                        user=user_id,
                        object_id=event_details.get('id', None),
                        created_at=datetime.utcnow(),
                    )
                )
                return result
            return wrapper
        return decorator

    @staticmethod
    def dispatch_event(dispatch, event: GenericEvent):
        dispatch(event.name, event.payload)
        _logger.debug(f"Event dispatched: {event.name} -> {event.payload}")

