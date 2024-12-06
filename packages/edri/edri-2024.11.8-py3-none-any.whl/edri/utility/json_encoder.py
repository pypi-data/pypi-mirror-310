from enum import Enum
from json import JSONEncoder
from pathlib import Path
from typing import Any


class CustomJSONEncoder(JSONEncoder):
    """
    A custom JSON encoder for converting various data types to JSON-compatible
    formats, including support for Enums, datetime objects, Paths, bytes, and
    more.

    Inherits from JSONEncoder to override the default() method for custom serialization.
    """

    def __init__(self, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False, indent=None,
                 separators=None, default=None, session):
        super().__init__(skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular, allow_nan=allow_nan,
                         sort_keys=sort_keys, indent=indent, separators=separators, default=default)
        self.session = session

    def default(self, data) -> Any:
        if hasattr(data, "to_json"):
            return data.to_json()
        elif hasattr(data, "isoformat"):
            return data.isoformat()
        elif isinstance(data, Path):
            return data.as_posix()
        elif isinstance(data, bytes) or isinstance(data, bytearray):
            return data.hex()
        elif isinstance(data, Enum):
            return data.value
        else:
            return super().default(data)
