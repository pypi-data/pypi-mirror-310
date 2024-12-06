from jvalue import JsonValue


def test_jv():
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
    assert jv.find("reviews") is None
    assert jv.find("albums.title") is None
