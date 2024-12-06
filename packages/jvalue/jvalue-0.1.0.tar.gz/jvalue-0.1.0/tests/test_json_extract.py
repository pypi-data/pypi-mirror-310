from jvalue import json_extract

data = {
    "a": 2,
    "c": [4, 5, {"f": 7}],
    "x.y": 100,
    "artist": {"name": "bowie"},
}


def test_empty_path():
    assert json_extract(data, "$") == data
    assert json_extract(data, "") == data


def test_simple_extract():
    assert json_extract(data, "$.a") == 2
    assert json_extract(data, "a") == 2

    assert json_extract(data, "$.c") == [4, 5, {"f": 7}]
    assert json_extract(data, "c") == [4, 5, {"f": 7}]

    assert json_extract(data, "$.x") is None
    assert json_extract(data, "x") is None

    assert json_extract(data, "$.artist") == {"name": "bowie"}
    assert json_extract(data, "artist") == {"name": "bowie"}
    assert json_extract(data, "artist.name") == "bowie"
    assert json_extract(data, "artist.album") is None


def test_list():
    assert json_extract(data, "c[2]") == {"f": 7}
    assert json_extract(data, "$.c[2]") == {"f": 7}
    assert json_extract(data, "$.c[2].f") == 7
    assert json_extract(data, "c[2].f") == 7
    assert json_extract(data, "$.c[-2]") == 5
    assert json_extract(data, "$.c[-3]") == 4
    assert json_extract(data, "$.c[*]") == [4, 5, {"f": 7}]
    assert json_extract(data, "$.c[*].f") == [None, None, 7]
    assert json_extract(data, "$.c[*].g") == [None, None, None]

    assert json_extract(data, "$.c[3]") is None
    assert json_extract(data, "$.c[-4]") is None
    assert json_extract(data, "$.c[2]x") is None

    assert json_extract([1, 2, 3], "$[0]") == 1
    assert json_extract([1, 2, 3], "[0]") == 1
    assert json_extract([1, 2, 3], "[2]") == 3
    assert json_extract([1, 2, 3], "[3]") is None
    assert json_extract([1, 2, 3], ".[0]") is None
    assert json_extract([1, 2, 3], "[]") == [1, 2, 3]
    assert json_extract([1, 2, 3], "[*]") == [1, 2, 3]


def test_non_dict():
    assert json_extract("xyz", "$") == "xyz"
    assert json_extract("xyz", "") == "xyz"
    assert json_extract(100, "$") == 100
    assert json_extract(100, "") == 100
    assert json_extract(True, "$") is True
    assert json_extract(True, "") is True

    assert json_extract("xyz", "$.a") is None
    assert json_extract("xyz", "a") is None
    assert json_extract("xyz", "a.b") is None
