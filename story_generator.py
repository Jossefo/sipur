"""Compose unique Hebrew bedtime stories from a child's week."""

from __future__ import annotations

import base64
import json
import random
import re
import secrets
import zlib
from typing import Iterable


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
    "עמוס", "ערן", "פאי", "צבי", "רון", "רועי", "רם", "שאול", "שמואל",
    "תום", "תמיר", "עומרי", "אור", "סהר", "ים", "דור", "הראל", "לביא",
    "אריאל", "יובל", "איליי", "אלעד", "גיא", "הוד", "זוהר", "חגי",
}

FEMALE_ENDINGS = ("ה", "ית", "יה", "ת")

COMPANIONS = (
    {"id": "moon", "he": "הירח", "he_the": "הירח"},
    {"id": "fox", "he": "שועל קטן", "he_the": "השועל הקטן"},
    {"id": "bird", "he": "ינשוף קטן", "he_the": "הינשוף הקטן"},
    {"id": "star", "he": "כוכב נייר", "he_the": "כוכב הנייר"},
    {"id": "lamp", "he": "פנס לילה", "he_the": "פנס הלילה"},
)

TIMES = (
    "בערב הרך",
    "בשעת הלילה הכחולה",
    "אחרי המקלחת, כשהשיער עוד לח",
    "כשהווילון זז לאט",
    "כשהבית כבר דיבר בלחש",
    "כשהשעון במסדרון פסע לאטו",
    "כשהאור במטבח כבה אחרון",
)

PLACES = (
    "על סף החלון",
    "על שולחן העץ הקטן",
    "ליד המיטה עם השמיכה המקומטת",
    "על אדן האבן החמים",
    "בפינה שבין הארון לספרים",
    "מתחת למנורה העגולה",
)

MOODS = (
    "שקט כמו שמיכה",
    "מתוק כמו תפוח שנשאר בצלחת",
    "רחב כמו חלון פתוח",
    "עדין כמו גרב שנשמטה",
    "זהוב כמו פירור של דבש",
    "איטי כמו סיפור שחוזר פעם שנייה",
)

OPENING_FRAMES = (
    "{time} ישב{sf} {name} {age_phrase} {place}. {companion} בא והתיישב בלי לבקש רשות, כי בלילות כאלה לא צריך רשות — רק אוזן.",
    "{time} {name} {age_phrase} קיפל{sf} את היום כמו מפה. {companion} המתין {place}, והלילה הריח {mood}.",
    "ל{name} {age_phrase} היה לילה אחד שהתחיל לאט. {time} {companion} הגיע {place} ואמר: {come} נשמע מה השבוע השאיר.",
    "{name} {age_phrase} כבר לבש{sf} פיג׳מה כש{companion} נשען {place}. {time} העולם היה {mood}.",
    "השבוע של {name} {age_phrase} עוד היה חם בכיסים. {time} {companion} מצא אות{op} {place} ושאל בקול של נוצה: מה קרה?",
    "{time} האור התקצר, ו{name} {age_phrase} שמע{sf} איך הבית נושם. {companion} צייר עיגול קטן {place} ואמר: כאן מתחיל הסיפור.",
    "לא היה צריך דרקון. ל{name} {age_phrase} היה שבוע. {time} {companion} פתח דלת דמיונית {place}, והלילה נכנס יחף.",
    "{name} {age_phrase} חשב{sf} שהיום נגמר, אבל {companion} ידע אחרת. {time} הם ישבו {place}, והשבוע התחיל לדבר.",
)

BRIDGE_FRAMES = (
    "לפני שנכנסו למעמקי השמיכה, {companion} ביקש שלושה דברים קטנים — לא אוצרות, רק מה שקרה באמת.",
    "{name} שטף{sf} את היום מהידיים, אבל משהו נשאר מתחת לציפורניים: שלושה רגעים.",
    "הלילה לא חיפש הרפתקה גדולה. הוא חיפש את השבוע של {name}, בדיוק כמו שהוא היה.",
    "{companion} אמר שסיפור טוב לא ממציאים מהירח. אותו אוספים מהחדר, מהגן, מהלב.",
    "בין כוס המים לכרית, {name} מצא{sf} כיס פנימי. שם חיכו שלושה דברים.",
)

EVENT_FRAMES = (
    "ואז קרה דבר ראשון: {event}. {name} עצר{sf} רגע, כאילו מישהו הדליק נר קטן בתוך הגוף.",
    "בשבוע הזה {event} — לא סתם שורה ביומן, אלא רגע ש{name} לקח{sf} ביד כמו אבן חלקה מהים.",
    "יש דברים שעוברים לידם ויש דברים שנשארים. {event}: זה נשאר. {companion} הנהן, כי גם הוא הרגיש את המשקל הקל.",
    "״{tell} לי לאט,״ ביקש {companion}. {name} אמר{sf}: {event}. המילים התיישבו {place} ולא מיהרו ללכת.",
    "פתאום נזכר{sf} {name} ש{event}. זה לא היה רעש גדול. זה היה לחישה עם צבע.",
    "אם השבוע היה שביל, כאן היה פיתול: {event}. {name} הלך{sf} דרכו בזהירות, גאה קצת, מופתע{s_adj} קצת.",
    "העולם עשה טובה קטנה והביא את זה: {event}. {name} שמע{sf} איך הלב עונה ״הנה, גם אני הייתי שם.״",
    "בין ארוחת הערב ללילה נשאר טעם. הטעם היה: {event}. {companion} אמר שטעמים כאלה שומרים מתחת לכרית.",
    "לא כולם שמו לב, אבל {name} כן. {event}. מאז היה באוויר משהו {mood}.",
    "כמו דף שמתקפל באמצע, כך היה הרגע שבו {event}. {name} שמר{sf} את הקיפול.",
    "ועוד פלא בגובה ילד: {event}. {name} {age_phrase} לא צריך{sf} יותר מזה כדי שהשבוע יקבל שם.",
    "בבוקר או בצהריים או ממש לפני השקיעה — {event}. עכשיו, בלילה, {name} מחזיר{sf} את זה אל הסיפור כמו ציפור אל הקן.",
)

ARC_FRAMES = (
    "שלושה דברים ישבו עכשיו על השמיכה של {name}: {e1}, וגם {e2}, וגם {e3}. הם לא היו אותו דבר, ובכל זאת החזיקו ידיים.",
    "{name} ראה{sf} איך השבוע מתקפל: מ{e1}, דרך {e2}, עד {e3}. הקפל יצא רך. הקפל יצא של{poss}.",
    "קצת גאווה, קצת פליאה, קצת רוך — כך הרגיש הלב אחרי ש{e1}, ואחרי ש{e2}, ואחרי ש{e3}. {companion} לחש: זה קשת. קשת קטנה של שבוע.",
    "אם מישהו היה שואל את {name} {age_phrase} מה היה השבוע, היה אפשר לענות בשלוש נשימות: {e1}. {e2}. {e3}. ואז לחייך.",
    "הדברים לא נעלמו. {e1} נשאר כמו חלון. {e2} נשאר כמו ריח. {e3} נשאר כמו יד על הכתף. {name} הבין{sf} שאפשר לקחת אותם אל השינה.",
    "בין שלושת הרגעים נמתח חוט זהוב. {name} משך{sf} בו בעדינות, וכל מה שהיה — {e1}, {e2}, {e3} — בא והתיישב קרוב.",
)

ENDING_FRAMES = (
    "עכשיו העיניים של {name} כבדות כמו דבש. {companion} מנמיך את הקול. מחר מחכה מאחורי הווילון בלי לדחוף. לילה טוב, {name}.",
    "הלילה פרש שמיכה על כל מה שקרה. {name} {age_phrase} נשם{sf} פעם אחת ארוכה. {companion} נשאר משמר קטן ליד החלון. לילה טוב.",
    "אין צורך לסגור את השבוע במנעול. {name} מניח{sf} אותו ליד הכרית, ו{companion} שומר שלא יברח. השינה באה יחפה. לילה טוב, {name}.",
    "החושך כבר לא היה חושך. הוא היה חדר. {name} חייך{sf} אל {companion}, ואל שלושת הרגעים שישנו בצד. מחר יתחיל לאט. לילה טוב.",
    "{companion} כיבה כוכב אחד מיותר, השאיר בדיוק כמה שצריך. {name} {age_phrase} נכנע{sf} לרוך. הסיפור נשאר באוויר עוד רגע, ואז גם הוא ישן.",
    "״תודה שסיפרת,״ אמר {companion}. {name} לחש{sf} תודה בחזרה, בלי מילים. החלון שמר על הירח, והירח שמר על {name}. לילה טוב.",
    "השבוע התקפל לגודל של לחישה. {name} שם{sf} את הלחישה בכיס הפיג׳מה. {companion} נופף, והמיטה עשתה מקום. לילה טוב, {name}. לילה טוב, שבוע קטן.",
    "אין סוף גדול. יש רק עפעפיים. {name} {age_phrase} נרדם{sf} בתוך הסיפור כמו בתוך שרוול חם. {companion} לוחש לרוח שתשמור על {name}. לילה טוב.",
)

TITLES = (
    "{name} והשבוע שהפך לסיפור",
    "הלילה של {name}",
    "{name} והירח שלא מיהר",
    "שלושה פלאים ל{name}",
    "{name} מקפל{sf} את היום",
    "סיפור לילה טוב ל{name}",
    "{name} ו{companion_he} של השבוע",
    "הכיס החם של {name}",
    "{name}, {age}, ושלושה דברים",
    "לפני השינה, {name}",
    "{name} והאור הקטן בכיס",
    "איך {name} אסף{sf} את השבוע",
)

SPARKS = (
    "מישהו במסדרון צעד כמו חתול.",
    "ריח סבון נשאר באוויר עוד רגע.",
    "גלגל של אוטו רחוק אמר לילה טוב ראשון.",
    "הגרביים המזווגות חיכו על הכיסא כמו שני חברים.",
    "הספר על המדף נזכר שהוא גם היה פעם יום.",
    "טיפה אחרונה בברז החליטה לא ליפול.",
    "הצל של הווילון רקד בלי מוזיקה.",
    "כוכב אחד מצמץ מאוחר, כמו ילד בגן.",
)


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
        return template.format(
            sf=self.sf,
            op=self.op,
            s_adj=self.s_adj,
            poss=poss(self.gender),
            come=self.come,
            tell=self.tell,
            **kwargs,
        )


def _clean(text: str, limit: int) -> str:
    collapsed = " ".join((text or "").split())
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
    chunks = [story.get("title") or ""]
    chunks.extend(p.get("t") or p.get("text") or "" for p in pages)
    return "\n".join(chunks)


def _pick_scene(text: str, page_kind: str) -> str:
    if page_kind == "open":
        return "window"
    if page_kind == "bridge":
        return "hallway"
    if page_kind == "arc":
        return "blanket"
    if page_kind == "end":
        return "bedtime"
    keys = (
        (("שן", "שיניים", "שן"), "tooth"),
        (("עוגה", "אפה", "אפינו", "סבתא", "מטבח", "בצק", "עוגי"), "kitchen"),
        (("חושך", "פחד", "מפחיד", "צל"), "nightlight"),
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
        (("יער", "עץ", "עצים", "טיול"), "garden"),
    )
    for words, scene in keys:
        if any(w in text for w in words):
            return scene
    return "garden"


def generate_story(name: str, age: int, events: list[str], rng: random.Random | None = None) -> dict:
    """Return a 5–7 page story dict. Two calls without a shared rng will differ."""
    rng = rng or random.Random(secrets.randbits(64))
    name = _clean(name, 40)
    age = int(age)
    events = [_clean(e, 120) for e in events[:3]]
    if len(events) != 3 or not name:
        raise ValueError("name, age, and 3 events are required")

    gender = guess_gender(name, rng)
    voice = Voice(gender)
    companion = rng.choice(COMPANIONS)
    time = rng.choice(TIMES)
    place = rng.choice(PLACES)
    mood = rng.choice(MOODS)
    seed = rng.randint(1, 2**31 - 1)

    ctx = {
        "name": name,
        "age": age,
        "age_phrase": age_phrase(age, gender),
        "companion": companion["he_the"],
        "companion_he": companion["he"],
        "time": time,
        "place": place,
        "mood": mood,
        "e1": events[0],
        "e2": events[1],
        "e3": events[2],
    }

    title = voice.fmt(rng.choice(TITLES), **ctx)

    n_pages = rng.choice((5, 6, 6, 6, 7, 7))
    event_frames = rng.sample(EVENT_FRAMES, 3)
    opening = voice.fmt(rng.choice(OPENING_FRAMES), **ctx)
    spark = rng.choice(SPARKS)
    opening = f"{opening} {spark}"

    pages: list[dict] = []

    def add(kind: str, text: str) -> None:
        pages.append({"t": " ".join(text.split()), "k": _pick_scene(text, kind), "p": kind})

    add("open", opening)
    if n_pages == 7:
        add("bridge", voice.fmt(rng.choice(BRIDGE_FRAMES), **ctx))
    for ev, frame in zip(events, event_frames):
        add("event", voice.fmt(frame, event=ev, **ctx))
    if n_pages >= 6:
        add("arc", voice.fmt(rng.choice(ARC_FRAMES), **ctx))
    else:
        # Five-page book: fold the arc into the last event page, then a calm ending.
        pages[-1]["t"] += " " + voice.fmt(rng.choice(ARC_FRAMES), **ctx)
    add("end", voice.fmt(rng.choice(ENDING_FRAMES), **ctx))
    if not (5 <= len(pages) <= 7):
        raise RuntimeError(f"unexpected page count {len(pages)}")

    return {
        "v": 1,
        "name": name,
        "age": age,
        "gender": gender,
        "title": title,
        "seed": seed,
        "companion": companion["id"],
        "pages": pages,
    }



def encode_story(story: dict) -> str:
    raw = json.dumps(story, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    token = base64.urlsafe_b64encode(zlib.compress(raw, 9)).decode("ascii")
    return token.rstrip("=")


def decode_story(token: str) -> dict:
    pad = "=" * (-len(token) % 4)
    raw = zlib.decompress(base64.urlsafe_b64decode(token + pad))
    story = json.loads(raw.decode("utf-8"))
    if not isinstance(story, dict) or not story.get("pages"):
        raise ValueError("invalid story")
    return story
