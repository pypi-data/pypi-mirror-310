# jvalue - extract json value

Extract values from json data via simplified json path.

## Install

```
pip install jvalue
```

## Example

```Python
from jvalue import JsonValue

artist = {
    "name": "David Bowie",
    "albums": [
        {"title": "Ziggy Stardust", "year": 1972},
        {"title": "Blackstar", "year": 2016},
    ],
}

jv = JsonValue(artist)

assert jv.find("$") == artist
assert jv.find("") == artist
assert jv.find("albums[].title") == ["Ziggy Stardust", "Blackstar"]
assert jv.find("albums[*].year") == [1972, 2016]
assert jv.find("albums[0].year") == 1972
assert jv.find("albums[2].year") is None
```

or, you can use `json_extract` as a function directly

```Python
from jvalue import json_extract

assert json_extract(artist, "albums[0].title") == "Ziggy Stardust"
```
