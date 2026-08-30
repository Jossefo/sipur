from story_generator import decode_story, generate_story, story_plain_text


def test_home_ok(client):
    r = client.get("/")
    assert r.status_code == 200
    html = r.data.decode("utf-8")
    assert "לצור סיפור" in html
    assert 'dir="rtl"' in html
    assert "וואטסאפ" not in html


def test_create_form(client):
    r = client.get("/create")
    assert r.status_code == 200
    html = r.data.decode("utf-8")
    assert 'name="name"' in html
    assert 'name="event3"' in html


def test_create_validates(client):
    r = client.post("/create", data={"name": "", "age": "1", "event1": "", "event2": "", "event3": ""})
    assert r.status_code == 400
    assert "שם" in r.data.decode("utf-8")


def test_create_redirects_to_shareable_story(client):
    r = client.post(
        "/create",
        data={
            "name": "נועה",
            "age": "6",
            "event1": "איבדה שן",
            "event2": "אפתה עם סבתא",
            "event3": "פחדה מהחושך",
        },
        follow_redirects=False,
    )
    assert r.status_code == 302
    loc = r.headers["Location"]
    assert loc.startswith("/s/")
    page = client.get(loc)
    assert page.status_code == 200
    html = page.data.decode("utf-8")
    assert "נועה" in html
    assert "איבדה שן" in html
    assert "אפתה עם סבתא" in html
    assert "פחדה מהחושך" in html
    assert "<svg" in html
    assert "לצור סיפור נוסף" in html


def test_story_refresh_and_share_url(client):
    r = client.post(
        "/create",
        data={
            "name": "יוסי",
            "age": "5",
            "event1": "בנה מגדל",
            "event2": "שחה בבריכה",
            "event3": "ישן אצל סבא",
        },
        follow_redirects=False,
    )
    loc = r.headers["Location"]
    first = client.get(loc)
    second = client.get(loc)
    assert first.status_code == 200
    assert second.data == first.data
    assert "יוסי" in first.data.decode("utf-8")


def test_bad_token_404(client):
    r = client.get("/s/not-a-real-token")
    assert r.status_code == 404


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["ok"] is True


def test_two_submissions_differ(client):
    payload = {
        "name": "מאיה",
        "age": "7",
        "event1": "ציירה שמש",
        "event2": "אכלה שוקו",
        "event3": "ראתה חתול",
    }
    a = client.post("/create", data=payload, follow_redirects=False).headers["Location"]
    b = client.post("/create", data=payload, follow_redirects=False).headers["Location"]
    assert a != b
    ta = decode_story(a.rsplit("/", 1)[-1])
    tb = decode_story(b.rsplit("/", 1)[-1])
    assert story_plain_text(ta) != story_plain_text(tb)


def test_illustrations_are_inline_svg_not_hotlinked(client):
    r = client.post(
        "/create",
        data={
            "name": "תמר",
            "age": "8",
            "event1": "ליקטה פרחים",
            "event2": "שמעה גשם",
            "event3": "כתבה מכתב",
        },
        follow_redirects=True,
    )
    html = r.data.decode("utf-8")
    assert html.count("<svg") >= 5
    assert "unsplash" not in html.lower()
    assert "placehold" not in html.lower()
    assert "http://images" not in html.lower()
