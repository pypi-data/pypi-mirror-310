from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    onetime: _ClassVar[EventType]
    prevent: _ClassVar[EventType]
onetime: EventType
prevent: EventType

class CreateOneTimeEventRequest(_message.Message):
    __slots__ = ("event_start", "event_end", "one_time_event_temp", "temp", "unit_ids", "event_id", "type")
    EVENT_START_FIELD_NUMBER: _ClassVar[int]
    EVENT_END_FIELD_NUMBER: _ClassVar[int]
    ONE_TIME_EVENT_TEMP_FIELD_NUMBER: _ClassVar[int]
    TEMP_FIELD_NUMBER: _ClassVar[int]
    UNIT_IDS_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    event_start: str
    event_end: str
    one_time_event_temp: str
    temp: float
    unit_ids: _containers.RepeatedScalarFieldContainer[str]
    event_id: str
    type: EventType
    def __init__(self, event_start: _Optional[str] = ..., event_end: _Optional[str] = ..., one_time_event_temp: _Optional[str] = ..., temp: _Optional[float] = ..., unit_ids: _Optional[_Iterable[str]] = ..., event_id: _Optional[str] = ..., type: _Optional[_Union[EventType, str]] = ...) -> None: ...

class DeleteOneTimeEventRequest(_message.Message):
    __slots__ = ("event_id", "unit_ids")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    UNIT_IDS_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    unit_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, event_id: _Optional[str] = ..., unit_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateScheduleRequest(_message.Message):
    __slots__ = ("cron", "unit_id", "ignore_external_devices", "target_temperature", "schedule_id", "timezone")
    CRON_FIELD_NUMBER: _ClassVar[int]
    UNIT_ID_FIELD_NUMBER: _ClassVar[int]
    IGNORE_EXTERNAL_DEVICES_FIELD_NUMBER: _ClassVar[int]
    TARGET_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_ID_FIELD_NUMBER: _ClassVar[int]
    TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    cron: str
    unit_id: str
    ignore_external_devices: bool
    target_temperature: float
    schedule_id: str
    timezone: str
    def __init__(self, cron: _Optional[str] = ..., unit_id: _Optional[str] = ..., ignore_external_devices: bool = ..., target_temperature: _Optional[float] = ..., schedule_id: _Optional[str] = ..., timezone: _Optional[str] = ...) -> None: ...

class DeleteScheduleRequest(_message.Message):
    __slots__ = ("schedule_id",)
    SCHEDULE_ID_FIELD_NUMBER: _ClassVar[int]
    schedule_id: str
    def __init__(self, schedule_id: _Optional[str] = ...) -> None: ...

class CompanyRequest(_message.Message):
    __slots__ = ("company_id", "check_interval")
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    CHECK_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    company_id: str
    check_interval: int
    def __init__(self, company_id: _Optional[str] = ..., check_interval: _Optional[int] = ...) -> None: ...

class ScheduleResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class CompanyResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
