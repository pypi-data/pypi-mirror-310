from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from enum import Enum, unique
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any, Generic, Never, TypeVar, assert_never, cast

from orjson import (
    OPT_PASSTHROUGH_DATACLASS,
    OPT_PASSTHROUGH_DATETIME,
    OPT_SORT_KEYS,
    dumps,
    loads,
)
from typing_extensions import override

from utilities.dataclasses import Dataclass, asdict_without_defaults
from utilities.functions import get_class_name
from utilities.iterables import OneEmptyError, one
from utilities.math import MAX_INT64, MIN_INT64
from utilities.whenever import (
    parse_date,
    parse_local_datetime,
    parse_time,
    parse_timedelta,
    parse_zoned_datetime,
    serialize_date,
    serialize_local_datetime,
    serialize_time,
    serialize_timedelta,
    serialize_zoned_datetime,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Set as AbstractSet

    from utilities.types import StrMapping


_T = TypeVar("_T")


@unique
class _Prefixes(Enum):
    dataclass = "dc"
    date = "d"
    datetime = "dt"
    frozenset_ = "f"
    path = "p"
    set_ = "s"
    timedelta = "td"
    time = "tm"
    tuple_ = "tu"


def serialize2(
    obj: Any,
    /,
    *,
    before: Callable[[Any], Any] | None = None,
    after: Callable[[Any], Any] | None = None,
    dataclass_final_hook: Callable[[type[Dataclass], StrMapping], StrMapping]
    | None = None,
    fallback: bool = False,
) -> bytes:
    """Serialize an object."""
    obj_use = _pre_process(
        obj, before=before, after=after, dataclass_final_hook=dataclass_final_hook
    )
    try:
        return dumps(
            obj_use,
            default=partial(
                _serialize2_default,
                before=before,
                after=after,
                dataclass_final_hook=dataclass_final_hook,
                fallback=fallback,
            ),
            option=OPT_PASSTHROUGH_DATACLASS | OPT_PASSTHROUGH_DATETIME | OPT_SORT_KEYS,
        )
    except TypeError:
        raise _Serialize2TypeError(obj=obj) from None


def _pre_process(
    obj: Any,
    /,
    *,
    before: Callable[[Any], Any] | None = None,
    after: Callable[[Any], Any] | None = None,
    dataclass_final_hook: Callable[[type[Dataclass], StrMapping], StrMapping]
    | None = None,
) -> Any:
    if before is not None:
        obj = before(obj)
    match obj:
        case int():
            if not (MIN_INT64 <= obj <= MAX_INT64):
                raise _Serialize2IntegerError(obj=obj)
        case list():
            return [
                _pre_process(
                    o,
                    before=before,
                    after=after,
                    dataclass_final_hook=dataclass_final_hook,
                )
                for o in obj
            ]
        case dict():
            return {
                k: _pre_process(
                    v,
                    before=before,
                    after=after,
                    dataclass_final_hook=dataclass_final_hook,
                )
                for k, v in obj.items()
            }
        case frozenset():
            return _FrozenSetContainer(
                as_list=[
                    _pre_process(
                        o,
                        before=before,
                        after=after,
                        dataclass_final_hook=dataclass_final_hook,
                    )
                    for o in list(obj)
                ]
            )
        case set():
            return _SetContainer(
                as_list=[
                    _pre_process(
                        o,
                        before=before,
                        after=after,
                        dataclass_final_hook=dataclass_final_hook,
                    )
                    for o in list(obj)
                ]
            )
        case tuple():
            return _TupleContainer(
                as_list=[
                    _pre_process(
                        o,
                        before=before,
                        after=after,
                        dataclass_final_hook=dataclass_final_hook,
                    )
                    for o in list(obj)
                ]
            )
        case Dataclass():
            obj = asdict_without_defaults(
                obj, final=partial(_dataclass_final, hook=dataclass_final_hook)
            )
            return {
                k: _pre_process(
                    v,
                    before=before,
                    after=after,
                    dataclass_final_hook=dataclass_final_hook,
                )
                for k, v in obj.items()
            }
        case _:
            pass
    return obj if after is None else after(obj)


@dataclass(kw_only=True, slots=True)
class _FrozenSetContainer(Generic[_T]):
    as_list: list[_T]


@dataclass(kw_only=True, slots=True)
class _SetContainer(Generic[_T]):
    as_list: list[_T]


@dataclass(kw_only=True, slots=True)
class _TupleContainer(Generic[_T]):
    as_list: list[_T]


def _dataclass_final(
    cls: type[Dataclass],
    mapping: StrMapping,
    /,
    *,
    hook: Callable[[type[Dataclass], StrMapping], StrMapping] | None = None,
) -> StrMapping:
    if hook is not None:
        mapping = hook(cls, mapping)
    return {f"[{_Prefixes.dataclass.value}|{cls.__qualname__}]": mapping}


def _serialize2_default(
    obj: Any,
    /,
    *,
    before: Callable[[Any], Any] | None = None,
    after: Callable[[Any], Any] | None = None,
    dataclass_final_hook: Callable[[type[Dataclass], StrMapping], StrMapping]
    | None = None,
    fallback: bool = False,
) -> str:
    if isinstance(obj, dt.datetime):
        if obj.tzinfo is None:
            ser = serialize_local_datetime(obj)
        else:
            ser = serialize_zoned_datetime(obj)
        return f"[{_Prefixes.datetime.value}]{ser}"
    if isinstance(obj, dt.date):  # after datetime
        ser = serialize_date(obj)
        return f"[{_Prefixes.date.value}]{ser}"
    if isinstance(obj, dt.time):
        ser = serialize_time(obj)
        return f"[{_Prefixes.time.value}]{ser}"
    if isinstance(obj, dt.timedelta):
        ser = serialize_timedelta(obj)
        return f"[{_Prefixes.timedelta.value}]{ser}"
    if isinstance(obj, Path):
        ser = str(obj)
        return f"[{_Prefixes.path.value}]{ser}"
    if isinstance(obj, _FrozenSetContainer):
        ser = serialize2(
            obj.as_list,
            before=before,
            after=after,
            dataclass_final_hook=dataclass_final_hook,
        ).decode()
        return f"[{_Prefixes.frozenset_.value}]{ser}"
    if isinstance(obj, _SetContainer):
        ser = serialize2(
            obj.as_list,
            before=before,
            after=after,
            dataclass_final_hook=dataclass_final_hook,
        ).decode()
        return f"[{_Prefixes.set_.value}]{ser}"
    if isinstance(obj, _TupleContainer):
        ser = serialize2(
            obj.as_list,
            before=before,
            after=after,
            dataclass_final_hook=dataclass_final_hook,
        ).decode()
        return f"[{_Prefixes.tuple_.value}]{ser}"
    if fallback:
        return str(obj)
    raise TypeError


@dataclass(kw_only=True, slots=True)
class Serialize2Error(Exception):
    obj: Any


@dataclass(kw_only=True, slots=True)
class _Serialize2TypeError(Serialize2Error):
    @override
    def __str__(self) -> str:
        from rich.pretty import pretty_repr

        cls = get_class_name(self.obj)
        return f"Unable to serialize object of type {cls!r}:\n{pretty_repr(self.obj)}"


@dataclass(kw_only=True, slots=True)
class _Serialize2IntegerError(Serialize2Error):
    @override
    def __str__(self) -> str:
        return f"Integer {self.obj} is out of range"


def deserialize2(
    data: bytes, /, *, objects: AbstractSet[type[Dataclass]] | None = None
) -> Any:
    """Deserialize an object."""
    return _object_hook(loads(data), data=data, objects=objects)


_DATACLASS_PATTERN = re.compile(r"^\[" + _Prefixes.dataclass.value + r"\|(.+?)\]$")
_DATE_PATTERN = re.compile(r"^\[" + _Prefixes.date.value + r"\](.+)$")
_FROZENSET_PATTERN = re.compile(r"^\[" + _Prefixes.frozenset_.value + r"\](.+)$")
_PATH_PATTERN = re.compile(r"^\[" + _Prefixes.path.value + r"\](.+)$")
_LOCAL_DATETIME_PATTERN = re.compile(r"^\[" + _Prefixes.datetime.value + r"\](.+)$")
_SET_PATTERN = re.compile(r"^\[" + _Prefixes.set_.value + r"\](.+)$")
_TIME_PATTERN = re.compile(r"^\[" + _Prefixes.time.value + r"\](.+)$")
_TIMEDELTA_PATTERN = re.compile(r"^\[" + _Prefixes.timedelta.value + r"\](.+)$")
_TUPLE_PATTERN = re.compile(r"^\[" + _Prefixes.tuple_.value + r"\](.+)$")
_ZONED_DATETIME_PATTERN = re.compile(
    r"^\[" + _Prefixes.datetime.value + r"\](.+\+\d{2}:\d{2}\[.+?\])$"
)


def _object_hook(
    obj: bool | float | str | dict[str, Any] | list[Any] | Dataclass | None,  # noqa: FBT001
    /,
    *,
    data: bytes,
    objects: AbstractSet[type[Dataclass]] | None = None,
) -> Any:
    match obj:
        case bool() | int() | float() | Dataclass() | None:
            return obj
        case str():
            # ordered
            if match := _ZONED_DATETIME_PATTERN.search(obj):
                return parse_zoned_datetime(match.group(1))
            if match := _LOCAL_DATETIME_PATTERN.search(obj):
                return parse_local_datetime(match.group(1))
            # unordered
            if match := _DATE_PATTERN.search(obj):
                return parse_date(match.group(1))
            if match := _PATH_PATTERN.search(obj):
                return Path(match.group(1))
            if match := _TIME_PATTERN.search(obj):
                return parse_time(match.group(1))
            if match := _TIMEDELTA_PATTERN.search(obj):
                return parse_timedelta(match.group(1))
            # containers
            if match := _FROZENSET_PATTERN.search(obj):
                return frozenset(deserialize2(match.group(1).encode(), objects=objects))
            if match := _SET_PATTERN.search(obj):
                return set(deserialize2(match.group(1).encode(), objects=objects))
            if match := _TUPLE_PATTERN.search(obj):
                return tuple(deserialize2(match.group(1).encode(), objects=objects))
            return obj
        case list():
            return [_object_hook(o, data=data, objects=objects) for o in obj]
        case dict():
            if len(obj) == 1:
                key, value = one(obj.items())
                if (match := _DATACLASS_PATTERN.search(key)) and isinstance(
                    value, dict
                ):
                    if objects is None:
                        raise _Deserialize2NoObjectsError(data=data, obj=obj)
                    qualname = match.group(1)
                    try:
                        cls = one(o for o in objects if o.__qualname__ == qualname)
                    except OneEmptyError:
                        raise _Deserialize2ObjectEmptyError(
                            data=data, obj=obj, qualname=qualname
                        ) from None
                    return cls(**{
                        k: _object_hook(v, data=data, objects=objects)
                        for k, v in value.items()
                    })
                return {
                    k: _object_hook(v, data=data, objects=objects)
                    for k, v in obj.items()
                }
            return {
                k: _object_hook(v, data=data, objects=objects) for k, v in obj.items()
            }
        case _ as never:  # pyright: ignore[reportUnnecessaryComparison]
            assert_never(cast(Never, never))


@dataclass(kw_only=True, slots=True)
class Deserialize2Error(Exception):
    data: bytes
    obj: Any


@dataclass(kw_only=True, slots=True)
class _Deserialize2NoObjectsError(Deserialize2Error):
    @override
    def __str__(self) -> str:
        return f"Objects required to deserialize {self.obj!r} from {self.data!r}"


@dataclass(kw_only=True, slots=True)
class _Deserialize2ObjectEmptyError(Deserialize2Error):
    qualname: str

    @override
    def __str__(self) -> str:
        return f"Unable to find object {self.qualname!r} to deserialize {self.obj!r} (from {self.data!r})"


__all__ = ["Deserialize2Error", "Serialize2Error", "deserialize2", "serialize2"]
