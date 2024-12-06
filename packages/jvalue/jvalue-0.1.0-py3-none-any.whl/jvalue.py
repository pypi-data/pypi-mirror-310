"""Extract value from json via simple json path.

It supports basic json path only, similar to the
`json_extract` function in sqlite:
https://www.sqlite.org/json1.html#jex

This is implemented in pure python without dependency
to any other library.

Notes:
  It doesn't work when key has special characters such as "." and I
  don't intend to fix it, since I probably never need to use such
  keys in json.
"""

__version__ = "0.1.0"


import re
from typing import Any


class JsonValue:
    def __init__(self, data: Any):
        self._data = data

    def find(self, path: str) -> Any:
        return json_extract(self._data, path)


def json_extract(data: Any, path: str) -> Any:
    """similar but not equal to the json_extract from sqlite3"""

    if data is None or path.startswith("."):
        return None

    if not path or path == "$":
        return data

    if "." in path:
        key, path = path.split(".", 1)
    else:
        key, path = path, ""

    # decide if accessing to a list
    idx = None
    m = re.search(r"^(.*?)\[(-?\d+)\]$", key)
    if m is not None:
        # read an index in a list
        key, idx = m.group(1), int(m.group(2))
    elif key.endswith(("[]", "[*]")):
        # read all from a list
        key = key[: key.rfind("[")]
        idx = "*"

    if key in {"", "$"}:
        value = data
    elif isinstance(data, dict):
        value = data.get(key)
    else:
        return None

    if idx is None:
        return json_extract(value, path)
    elif isinstance(value, list):
        if idx == "*":
            return [json_extract(v, path) for v in value]
        try:
            return json_extract(value[idx], path)
        except IndexError:
            return None
    else:
        return None
