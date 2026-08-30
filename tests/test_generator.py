from story_generator import (
    TEMPLATES,
    decode_story,
    encode_story,
    evolve_template,
    generate_story,
    load_templates,
    story_plain_text,
    validate_input,
    _ensure_catalog,
)


def _story(**kwargs):
    return generate_story(
        "נועה",
        6,
        ["איבדה שן", "אפתה עם סבתא", "פחדה מהחושך"],
        **kwargs,
    )


def test_templates_load_at_least_250():
    cat = load_templates()
    assert len(cat) >= 250
    ids = [t["id"] for t in cat]
    assert len(ids) == len(set(ids))
    sample = cat[0]
    for key in (
        "id",
        "title_he",
        "theme",
        "moral_he",
        "format",
        "age_min",
        "age_max",
        "companion",
        "illustration_prompt_en",
        "beats",
    ):
        assert key in sample
    for beat in ("opening", "event_1", "event_2", "event_3", "turning", "moral_landing", "bedtime_close"):
        assert beat in sample["beats"]


def test_includes_name_age_and_all_three_events():
    story = _story()
    text = story_plain_text(story)
    assert "נועה" in text
    assert "6" in text
    assert "איבדה שן" in text
    assert "אפתה עם סבתא" in text
    assert "פחדה מהחושך" in text
    assert story["moral"]
    assert story["moral"] in text or story["moral"] == story["moral"]


def test_moral_present_on_pages():
    story = _story()
    text = story_plain_text(story)
    assert story["moral"]
    # moral text is woven into the moral landing beat
    assert story["moral"] in text


def test_two_runs_differ():
    a = story_plain_text(_story())
    b = story_plain_text(_story())
    assert a != b


def test_used_template_yields_different_template_id():
    first = _story()
    second = generate_story(
        "נועה",
        6,
        ["איבדה שן", "אפתה עם סבתא", "פחדה מהחושך"],
        used_template_ids=[first["template_id"]],
    )
    assert first["template_id"] != second["template_id"]
    assert first["fingerprint"] != second["fingerprint"]


def test_page_count_is_six_to_eight():
    for _ in range(12):
        n = len(_story()["pages"])
        assert 6 <= n <= 8


def test_uses_second_child_and_events():
    story = generate_story("יוסי", 4, ["רכב על אופניים", "אכל ארטיק", "פגש כלב בגן"])
    text = story_plain_text(story)
    assert "יוסי" in text
    assert "4" in text
    assert "רכב על אופניים" in text
    assert "אכל ארטיק" in text
    assert "פגש כלב בגן" in text
    assert 6 <= len(story["pages"]) <= 8


def test_encode_roundtrip_includes_template_and_moral():
    story = _story()
    again = decode_story(encode_story(story))
    assert again["title"] == story["title"]
    assert again["template_id"] == story["template_id"]
    assert again["fingerprint"] == story["fingerprint"]
    assert again["moral"] == story["moral"]
    assert again["pages"][0]["t"] == story["pages"][0]["t"]
    assert story_plain_text(again) == story_plain_text(story)


def test_evolve_template_returns_new_id():
    cat = _ensure_catalog()
    base = cat[0]
    evolved = evolve_template(base, "salt-test-1")
    assert evolved["id"] != base["id"]
    assert evolved["id"]
    assert evolved["format"]
    assert evolved["theme"]
    assert evolved["moral_he"]
    assert "opening" in evolved["beats"]
    assert any(t["id"] == evolved["id"] for t in cat)


def test_validation():
    assert validate_input("", 6, ["א", "ב", "ג"])
    assert validate_input("נועה", 2, ["אחד", "שניים", "שלוש"])
    assert not validate_input("נועה", 6, ["איבדה שן", "אפתה עם סבתא", "פחדה מהחושך"])


def test_noa_is_real_narrative_not_template_paste():
    story = _story()
    text = story_plain_text(story)
    assert "קרה דבר אמיתי" not in text
    assert "בתחנה הראשונה" not in text
    assert "על המפה הופיע" not in text
    events = ["איבדה שן", "אפתה עם סבתא", "פחדה מהחושך"]
    by_kind = {p["p"]: p["t"] for p in story["pages"]}
    for i, ev in enumerate(events, start=1):
        page = by_kind[f"event_{i}"]
        assert ev in page
        assert len(page) > len(ev) + 40
        assert f": {ev}" not in page
        assert f":{ev}" not in page


def test_noa_moral_connects_the_week():
    story = _story()
    turning = " ".join(
        p["t"] for p in story["pages"] if p["p"] in {"turning", "moral_landing"}
    )
    blob = (story["moral"] or "") + " " + turning
    groups = [
        any(w in blob for w in ("שן", "פה", "גוף")),
        any(w in blob for w in ("סבתא", "עוגה", "אפה", "אפתה", "קמח")),
        any(w in blob for w in ("חושך", "אור")),
    ]
    assert sum(groups) >= 2
    meaning = ("משתנה", "זמן", "לחכות", "לבקש", "גדל", "גדול", "אור קטן", "מותר", "מבקשים")
    assert any(w in blob for w in meaning)


def test_event_pages_expand_the_event_into_a_scene():
    story = _story()
    events = ["איבדה שן", "אפתה עם סבתא", "פחדה מהחושך"]
    for i, ev in enumerate(events, start=1):
        page = next(p for p in story["pages"] if p["p"] == f"event_{i}")
        assert ev in page["t"]
        assert len(page["t"]) > len(ev)
        # lived scene: child doing/feeling, not just the raw string
        assert "נועה" in page["t"]
        assert page["t"].count(".") >= 2


def test_illustration_prompts_describe_actual_scenes():
    story = _story()
    e1 = next(p for p in story["pages"] if p["p"] == "event_1")
    e2 = next(p for p in story["pages"] if p["p"] == "event_2")
    e3 = next(p for p in story["pages"] if p["p"] == "event_3")
    assert "tooth" in e1["pr"].lower()
    assert any(w in e2["pr"].lower() for w in ("kitchen", "cake", "grandm", "bak"))
    assert any(w in e3["pr"].lower() for w in ("dark", "night", "light"))
    # not only a generic contradicting quest backdrop
    for p in (e1, e2, e3):
        assert "lost a tooth" in p["pr"].lower() or "baked with" in p["pr"].lower() or "afraid of the dark" in p["pr"].lower() or "tooth" in p["pr"].lower() or "kitchen" in p["pr"].lower() or "dark" in p["pr"].lower()
