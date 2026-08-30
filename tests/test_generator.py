from story_generator import (
    decode_story,
    encode_story,
    generate_story,
    story_plain_text,
    validate_input,
)


def _story():
    return generate_story(
        "נועה",
        6,
        ["איבדה שן", "אפתה עם סבתא", "פחדה מהחושך"],
    )


def test_includes_name_age_and_all_three_events():
    story = _story()
    text = story_plain_text(story)
    assert "נועה" in text
    assert "6" in text
    assert "איבדה שן" in text
    assert "אפתה עם סבתא" in text
    assert "פחדה מהחושך" in text


def test_two_runs_differ():
    a = story_plain_text(_story())
    b = story_plain_text(_story())
    assert a != b


def test_page_count_is_five_to_seven():
    for _ in range(12):
        n = len(_story()["pages"])
        assert 5 <= n <= 7


def test_uses_second_child_and_events():
    story = generate_story("יוסי", 4, ["רכב על אופניים", "אכל ארטיק", "פגש כלב בגן"])
    text = story_plain_text(story)
    assert "יוסי" in text
    assert "4" in text
    assert "רכב על אופניים" in text
    assert "אכל ארטיק" in text
    assert "פגש כלב בגן" in text


def test_encode_roundtrip():
    story = _story()
    again = decode_story(encode_story(story))
    assert again["title"] == story["title"]
    assert again["pages"][0]["t"] == story["pages"][0]["t"]
    assert story_plain_text(again) == story_plain_text(story)


def test_validation():
    assert validate_input("", 6, ["א", "ב", "ג"])
    assert validate_input("נועה", 2, ["אחד", "שניים", "שלוש"])
    assert not validate_input("נועה", 6, ["איבדה שן", "אפתה עם סבתא", "פחדה מהחושך"])
