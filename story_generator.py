"""Compose unique Hebrew bedtime stories from templates and a child's week."""

from __future__ import annotations

import base64
import hashlib
import json
import random
import re
import secrets
import zlib
from pathlib import Path
from typing import Any, Iterable

from story_catalog import (
    COMPANIONS,
    FORMATS,
    MORALS,
    THEMES,
    companion_by_id,
    make_template,
)

ROOT = Path(__file__).resolve().parent
TEMPLATES_PATH = ROOT / "data" / "templates.json"

FEMALE_NAMES = {
    "נועה", "מאיה", "תמר", "שירה", "יעל", "דנה", "מיכל", "נעמי", "אביגיל",
    "עלמה", "ליאה", "אמה", "נגה", "הילה", "רות", "רותם", "טלי", "טליה",
    "איילה", "אילה", "אגם", "אריאל", "אריאלה", "גאיה", "דפנה", "הדס",
    "ויויאן", "חן", "יהלי", "יוכבד", "יסמין", "ליבי", "ליה", "לילך",
    "מורן", "מלכה", "נעמה", "סיון", "עדי", "ענבל", "צליל", "קרן",
    "רוני", "רחל", "שחר", "שלי", "שמחה", "שרה", "תאיר", "תהל", "אבישג",
    "אליה", "בר", "גלי", "הודיה", "ורד", "זינה", "חיה", "טובה", "יהודית",
    "נויה", "ניב", "סתיו", "עומר", "עמליה", "פנינה", "ציונה", "רינה",
    "שושנה", "תניה", "אנה", "סופי", "מיקה", "נוגה", "אלין", "אלמה",
    "יהב", "לורן", "נטע", "שירי", "עמית", "דניאל", "טום",
}

MALE_NAMES = {
    "יוסי", "דני", "איתי", "ארי", "עידו", "יונתן", "אלון", "רועי", "גיא",
    "אורי", "אדם", "אבי", "אבנר", "אהרן", "אוהד", "אופיר", "אייל", "איתן",
    "אלי", "אמיר", "אסף", "אריק", "בועז", "בן", "בני", "גד", "דוד",
    "הלל", "זאב", "חיים", "טל", "יהונתן", "יואב", "יונה", "יעקב", "יצחק",
    "ליאם", "מיכאל", "מתן", "נדב", "נועם", "ניר", "נתן", "עודד", "עילי",
    "עמוס", "ערן", "פאי", "צבי", "רון", "רם", "שאול", "שמואל",
    "תום", "תמיר", "עומרי", "אור", "סהר", "ים", "דור", "הראל", "לביא",
    "אריאל", "יובל", "איליי", "אלעד", "הוד", "זוהר", "חגי",
}

FEMALE_ENDINGS = ("ה", "ית", "יה", "ת")

# Process-wide uniqueness: same book (fingerprint) is never emitted twice.
_produced_fingerprints: set[str] = set()
TEMPLATES: list[dict[str, Any]] = []


def load_templates(path: Path | None = None) -> list[dict[str, Any]]:
    p = path or TEMPLATES_PATH
    if not p.is_file():
        from story_catalog import build_all_templates

        return build_all_templates()
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, list) or len(data) < 250:
        raise RuntimeError(f"templates catalog too small: {p}")
    return data


def _ensure_catalog() -> list[dict[str, Any]]:
    global TEMPLATES
    if not TEMPLATES:
        TEMPLATES = load_templates()
    return TEMPLATES


def catalog_stats() -> dict[str, Any]:
    cat = _ensure_catalog()
    formats = sorted({t.get("format") or "" for t in cat if t.get("format")})
    themes = sorted({t.get("theme") or "" for t in cat if t.get("theme")})
    return {
        "template_count": len(cat),
        "formats": formats,
        "themes": themes,
    }


def guess_gender(name: str, rng: random.Random) -> str:
    key = name.strip()
    if key in FEMALE_NAMES:
        return "f"
    if key in MALE_NAMES:
        return "m"
    if key.endswith(FEMALE_ENDINGS) and key not in {"אדם", "נועם"}:
        return "f"
    return rng.choice(("f", "m"))


def age_phrase(age: int, gender: str) -> str:
    if gender == "f":
        return f"בת ה־{age}"
    return f"בן ה־{age}"


def poss(gender: str) -> str:
    return "ה" if gender == "f" else "ו"


class Voice:
    """Tiny Hebrew agreement helper for a single child."""

    def __init__(self, gender: str):
        self.gender = gender

    @property
    def sf(self) -> str:
        return "ה" if self.gender == "f" else ""

    @property
    def op(self) -> str:
        return "ה" if self.gender == "f" else "ו"

    @property
    def s_adj(self) -> str:
        return "ת" if self.gender == "f" else ""

    @property
    def come(self) -> str:
        return "בואי" if self.gender == "f" else "בוא"

    @property
    def tell(self) -> str:
        return "ספרי" if self.gender == "f" else "ספר"

    def word(self, masc: str) -> str:
        if self.gender != "f":
            return masc
        irregular = {"ראה": "ראתה", "עשה": "עשתה", "בנה": "בנתה"}
        if masc in irregular:
            return irregular[masc]
        sofit = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"}
        last = masc[-1]
        if last in sofit:
            return masc[:-1] + sofit[last] + "ה"
        return masc + "ה"

    def fmt(self, template: str, **kwargs) -> str:
        template = re.sub(
            r"([א-ת׳\']+)\{sf\}",
            lambda m: self.word(m.group(1)),
            template,
        )
        mapping = {
            "sf": self.sf,
            "op": self.op,
            "s_adj": self.s_adj,
            "poss": poss(self.gender),
            "come": self.come,
            "tell": self.tell,
            **kwargs,
        }

        class _Safe(dict):
            def __missing__(self, key):
                return "{" + key + "}"

        return template.format_map(_Safe(mapping))


def _clean(text: str, limit: int) -> str:
    collapsed = " ".join((text or "").split())
    collapsed = collapsed.replace("{", "(").replace("}", ")")
    return collapsed[:limit].strip()


def validate_input(name: str, age, events: Iterable[str]) -> list[str]:
    errors: list[str] = []
    name = _clean(str(name or ""), 40)
    if len(name) < 2:
        errors.append("צריך שם, לפחות שתי אותיות.")
    try:
        age_i = int(age)
        if age_i < 3 or age_i > 9:
            errors.append("הגיל הוא בין 3 ל־9.")
    except (TypeError, ValueError):
        errors.append("הגיל הוא בין 3 ל־9.")
        age_i = None
    evs = [_clean(e, 120) for e in list(events or [])]
    while len(evs) < 3:
        evs.append("")
    for i, e in enumerate(evs[:3], start=1):
        if len(e) < 2:
            errors.append(f"צריך דבר {i} מהשבוע, לפחות שתי אותיות.")
    return errors


def story_plain_text(story: dict) -> str:
    pages = story.get("pages") or []
    chunks = [story.get("title") or "", story.get("moral") or ""]
    chunks.extend(p.get("t") or p.get("text") or "" for p in pages)
    return "\n".join(chunks)


def make_fingerprint(name: str, age: int, events: list[str], template_id: str) -> str:
    norm_name = " ".join((name or "").split()).casefold()
    norm_events = "|".join(" ".join((e or "").split()).casefold() for e in events[:3])
    raw = f"{norm_name}|{int(age)}|{norm_events}|{template_id}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _pick_scene(text: str, page_kind: str, theme: str) -> str:
    if page_kind in {"opening"}:
        return theme or "window"
    if page_kind in {"turning"}:
        return theme or "blanket"
    if page_kind in {"moral_landing"}:
        return theme or "garden"
    if page_kind in {"bedtime_close"}:
        return "bedtime"
    keys = (
        (("שן", "שיניים"), "tooth"),
        (("עוגה", "אפה", "אפינו", "סבתא", "מטבח", "בצק", "עוגי"), "kitchen"),
        (("כלב", "גורה", "כלבלב"), "dog"),
        (("חתול", "חתלתול"), "cat"),
        (("ים", "בריכה", "מים", "שחה", "גלים"), "water"),
        (("גשם", "שלולית", "מטריה"), "rain"),
        (("אופניים", "גלגל", "רכיבה"), "bike"),
        (("גן", "חבר", "חברה", "נדנדה", "משחק", "כדור"), "garden"),
        (("בית ספר", "גננת", "כיתה", "מורה"), "school"),
        (("יום הולדת", "עוגת", "בלון", "מתנה"), "party"),
        (("כוכב", "ירח", "שמיים"), "sky"),
        (("סבא", "סבתא", "משפחה"), "kitchen"),
        (("יער", "עץ", "עצים", "טיול"), "forest"),
    )
    for words, scene in keys:
        if any(w in text for w in words):
            return scene
    return theme or "garden"


def _page_prompt(base: str, kind: str, age: int, event: str = "") -> str:
    extras = {
        "opening": "gentle introduction at the start of evening, child arriving in the scene",
        "event_1": "first story moment, child noticing something small and kind",
        "event_2": "middle of the story, warm narrative scene",
        "event_3": "third story moment, child holding a memory",
        "turning": "quiet turning point, child realizing something gentle",
        "moral_landing": "warm moral landing, peaceful understanding, no lecturing",
        "bedtime_close": "bedtime close, child in bed, very calm, nightlight glow",
        "bridge": "a quiet in-between moment on the way through the story",
    }
    bit = extras.get(kind, "a warm story moment")
    ev = ("scene suggesting: " + event[:80]) if event else ""
    return (
        f"{base}, {bit} {ev}, child around age {age}, "
        "children's picture book illustration, watercolor, warm light, child-safe, "
        "no text, no watermark, not photorealistic, not horror"
    )


def evolve_template(base: dict[str, Any], salt: str | int) -> dict[str, Any]:
    """Synthesize a new template by swapping format + theme + moral, and persist it."""
    cat = _ensure_catalog()
    rng = random.Random(str(salt))
    fmt_id = base.get("format")
    theme_id = base.get("theme")
    moral_he = base.get("moral_he")
    new_fmt = rng.choice([f for f in FORMATS if f["id"] != fmt_id] or FORMATS)
    new_theme = rng.choice([t for t in THEMES if t["id"] != theme_id] or THEMES)
    new_moral = rng.choice([m for m in MORALS if m["he"] != moral_he] or MORALS)
    companion = companion_by_id(base.get("companion") or "moon")
    if rng.random() > 0.4:
        companion = rng.choice(COMPANIONS)
    age_min = int(base.get("age_min") or 3)
    age_max = int(base.get("age_max") or 9)
    serial = 9000 + (abs(hash(str(salt))) % 90000)
    extra = re.sub(r"[^a-zA-Z0-9_-]+", "", str(salt))[:24] or "x"
    tmpl = make_template(
        new_theme,
        new_fmt,
        new_moral,
        companion,
        variant=rng.randrange(3),
        age_min=age_min,
        age_max=age_max,
        serial=serial,
        extra_id=extra,
    )
    existing = {t["id"] for t in cat}
    if tmpl["id"] in existing:
        tmpl["id"] = tmpl["id"] + f"-{rng.randint(1, 10**9)}"
    cat.append(tmpl)
    return tmpl


def _fits_age(t: dict[str, Any], age: int) -> bool:
    return int(t.get("age_min") or 3) <= age <= int(t.get("age_max") or 9)


def pick_template(
    age: int,
    name: str,
    events: list[str],
    rng: random.Random,
    used_template_ids: set[str] | None = None,
    used_fingerprints: set[str] | None = None,
) -> dict[str, Any]:
    cat = _ensure_catalog()
    used_tids = set(used_template_ids or [])
    used_fps = set(used_fingerprints or []) | _produced_fingerprints
    candidates: list[dict[str, Any]] = []
    for t in cat:
        if not _fits_age(t, age):
            continue
        if t["id"] in used_tids:
            continue
        fp = make_fingerprint(name, age, events, t["id"])
        if fp in used_fps:
            continue
        candidates.append(t)
    if candidates:
        return rng.choice(candidates)
    bases = [t for t in cat if _fits_age(t, age)] or cat
    base = rng.choice(bases)
    salt = f"{rng.randint(1, 10**9)}-{name[:8]}"
    return evolve_template(base, salt)


def generate_story(
    name: str,
    age: int,
    events: list[str],
    rng: random.Random | None = None,
    used_template_ids: Iterable[str] | None = None,
    used_fingerprints: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Return a 6–8 page story dict. Same fingerprint is never produced twice."""
    rng = rng or random.Random(secrets.randbits(64))
    name = _clean(name, 40)
    age = int(age)
    events = [_clean(e, 120) for e in list(events)[:3]]
    if len(events) != 3 or not name:
        raise ValueError("name, age, and 3 events are required")

    used_tids = set(used_template_ids or [])
    used_fps = set(used_fingerprints or [])
    template = pick_template(age, name, events, rng, used_tids, used_fps)

    gender = guess_gender(name, rng)
    voice = Voice(gender)
    companion = companion_by_id(template.get("companion") or "moon")
    seed = rng.randint(1, 2**31 - 1)
    fp = make_fingerprint(name, age, events, template["id"])

    ctx = {
        "name": name,
        "age": age,
        "age_phrase": age_phrase(age, gender),
        "companion": companion["he_the"],
        "companion_he": companion["he"],
        "event": "",
    }

    title = voice.fmt(template["title_he"], **ctx)
    beats = template["beats"]

    kinds: list[tuple[str, str, str]] = []
    kinds.append(("opening", beats["opening"], ""))
    if age >= 8:
        kinds.append(
            (
                "bridge",
                f"{{name}} נשם{{sf}} והקשיב{{sf}}. {companion['he_the']} אמר שכדאי לשמוע את השבוע עד הסוף, בלי לדלג.",
                "",
            )
        )
    kinds.append(("event_1", beats["event_1"], events[0]))
    kinds.append(("event_2", beats["event_2"], events[1]))
    kinds.append(("event_3", beats["event_3"], events[2]))
    if age <= 4:
        merged = beats["turning"] + " " + beats["moral_landing"]
        kinds.append(("moral_landing", merged, ""))
    else:
        kinds.append(("turning", beats["turning"], ""))
        kinds.append(("moral_landing", beats["moral_landing"], ""))
    kinds.append(("bedtime_close", beats["bedtime_close"], ""))

    pages: list[dict[str, Any]] = []
    theme = template.get("theme") or "garden"
    base_prompt = template.get("illustration_prompt_en") or (
        "children's picture book illustration, watercolor, warm light, child-safe, no text"
    )

    for kind, frame, ev in kinds:
        extra = dict(ctx)
        extra["event"] = ev
        text = " ".join(voice.fmt(frame, **extra).split())
        prompt = _page_prompt(base_prompt, kind, age, ev)
        pages.append(
            {
                "t": text,
                "k": _pick_scene(text, kind, theme),
                "p": kind,
                "pr": prompt,
            }
        )

    n = len(pages)
    if not (6 <= n <= 8):
        raise RuntimeError(f"unexpected page count {n}")

    _produced_fingerprints.add(fp)

    return {
        "v": 2,
        "name": name,
        "age": age,
        "gender": gender,
        "title": title,
        "seed": seed,
        "companion": companion["id"],
        "template_id": template["id"],
        "fingerprint": fp,
        "moral": template.get("moral_he") or "",
        "theme": theme,
        "format": template.get("format") or "",
        "pages": pages,
    }


def encode_story(story: dict) -> str:
    payload = {
        "v": story.get("v", 2),
        "name": story.get("name"),
        "age": story.get("age"),
        "gender": story.get("gender"),
        "title": story.get("title"),
        "seed": story.get("seed"),
        "companion": story.get("companion"),
        "template_id": story.get("template_id"),
        "fingerprint": story.get("fingerprint"),
        "moral": story.get("moral"),
        "theme": story.get("theme"),
        "format": story.get("format"),
        "pages": story.get("pages"),
    }
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    token = base64.urlsafe_b64encode(zlib.compress(raw, 9)).decode("ascii")
    return token.rstrip("=")


def decode_story(token: str) -> dict:
    pad = "=" * (-len(token) % 4)
    raw = zlib.decompress(base64.urlsafe_b64decode(token + pad))
    story = json.loads(raw.decode("utf-8"))
    if not isinstance(story, dict) or not story.get("pages"):
        raise ValueError("invalid story")
    if not story.get("title"):
        raise ValueError("invalid story")
    return story
