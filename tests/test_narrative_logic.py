"""Regressions from reading generated books, including contradictory outcomes."""
import random
import pytest
from narrative import extract_fact, classify_event
from story_generator import generate_story, story_plain_text, encode_story, decode_story

CASES = [
    ("נועה", 6, "f", ["איבדה שן", "אפתה עם סבתא", "פחדה מהחושך"]),
    ("איתי", 5, "m", ["רכב על אופניים", "רב עם חבר", "השלים עם החבר"]),
    ("מאיה", 4, "f", ["ציירה עם אמא", "שיחקה עם חתול", "אכלה גלידה"]),
    ("נועם", 8, "m", ["הפסיד במשחק", "למד לנגן בפסנתר", "עזר לאחותו"]),
    ("תמר", 7, "f", ["שיחקה עם חברים", "ראתה עצים בטיול", "כתבה מכתב לסבא"]),
    ("דני", 3, "m", ["היה אצל סבא", "בנה מגדל", "לא רצה ללכת לישון"]),
]

@pytest.mark.parametrize("text,focus", [
    ("רב עם חבר", "conflict"), ("לא רב עם חבר", "negated"),
    ("רב עם חבר ואז השלים איתו", "repair"),
    ("השלים עם חבר ואז רב עם חבר", "conflict"),
    ("לא השלים עם החבר", "conflict"),
    ("לא פחד מהחושך", "confidence"), ("לא שחה בבריכה", "negated"),
    ("לא נפל מהאופניים", "confidence"), ("הפסיד במשחק", "failure"), ("לא הצליח במשימה", "failure"),
    ("כמעט הפסיד אבל ניצח", "confidence"),
    ("סבא נפטר", "grief"), ("צייר אבל לא סיים", "negated"),
    ("היה אצל סבא", "grandparent"), ("אכל עוגה", "treat"),
])
def test_outcome_and_negation(text, focus):
    assert extract_fact(text).focus == focus

@pytest.mark.parametrize("name,age,voice,events", CASES)
def test_editorial_cases_across_seeds(name, age, voice, events):
    for seed in range(20):
        story = generate_story(name, age, events, gender=voice, rng=random.Random(seed))
        pages = story["pages"]
        assert len(pages) == (6 if age <= 4 else 8)
        assert story["narrative_plan"]["checks"] == []
        for i, event in enumerate(events, 1):
            assert event in next(p["t"] for p in pages if p["p"] == f"event_{i}")
        assert max(len(p["t"].split()) for p in pages) <= (75 if age <= 4 else 100)
        assert decode_story(encode_story(story))["pages"] == pages


def test_grandfather_does_not_invent_grandmother_or_baking():
    story = generate_story("דני", 3, ["היה אצל סבא", "בנה מגדל", "לא רצה לישון"], gender="m")
    text = story_plain_text(story)
    assert not any(word in text for word in ("סבתא", "עוגה", "קערה", "תנור"))


def test_unresolved_conflict_has_no_invented_reconciliation():
    story = generate_story("דני", 6, ["השלים עם חבר", "שיחק בגן", "רב עם חבר"], gender="m")
    assert story["narrative_plan"]["arc"] == "unfinished"
    assert "הרגע של ההתקרבות נשאר" not in story_plain_text(story)


def test_learning_does_not_imply_failure():
    story = generate_story("דני", 7, ["למד לנגן", "בנה מגדל", "אכל גלידה"], gender="m")
    assert "לא הצליח" not in story["moral"]


def test_explicit_voice_overrides_ambiguous_name():
    for voice, opening in (("f", "נועם בת ה־6 פתחה"), ("m", "נועם בן ה־6 פתח")):
        story = generate_story("נועם", 6, ["צייר ציור", "ראה חתול", "אכל גלידה"], gender=voice)
        assert opening in story["pages"][0]["t"]

@pytest.mark.parametrize("events", [
    ["נועה ציירה ציור", "נועה ראתה חתול", "נועה אכלה גלידה"],
    ["ציירתי ציור", "ראיתי חתול", "אכלתי גלידה"],
    ["ציור", "ציור", "ציור"],
    ["נסיעה במכונית", "מחשבה משונה", "ביקור בבית"],
])
def test_fragments_first_person_and_duplicate_inputs(events):
    story = generate_story("נועה", 4, events, gender="f")
    assert len(set(p["t"] for p in story["pages"])) == len(story["pages"])


def test_short_keyword_boundaries():
    assert "water" not in classify_event("שיחק עם חברים")
    assert "tooth" not in classify_event("ישן במיטה")
    assert "market" not in classify_event("אכל שוקולד")
    assert "bike" not in classify_event("רכב במכונית")
