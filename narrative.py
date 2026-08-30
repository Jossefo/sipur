"""Event-driven Hebrew bedtime narrative — lived scenes, not template pastes."""

from __future__ import annotations

import random
import re
from typing import Any, Callable

# Primary tag -> illustration / keepsake / English scene.
TAG_DEFS: list[tuple[str, tuple[str, ...]]] = [
    ("tooth", ("שן", "שיניים", "השן", "נשלה", "נשרה")),
    ("fear_dark", ("חושך", "פחד", "פחדה", "פחדתי", "מפחיד", "חשכה", "חשוך")),
    ("baking", ("אפתה", "אפינו", "אפה", "עוגה", "עוגי", "קמח", "בצק", "תנור", "סינר")),
    ("grandparent", ("סבתא", "סבא", "סבתי", "סבי")),
    ("friend", ("חבר", "חברה", "חברים", "שתף", "שיתף", "עזר", "עזרה", "חיבק", "חיבוק")),
    ("forgot", ("שכח", "שכחה", "איבדתי", "אבד", "שכחתי")),
    ("skill", ("למד", "תרגל", "ניסה", "ניסיתי", "הצליח", "תרגול", "פעם ראשונה")),
    ("school", ("בית ספר", "גננת", "כיתה", "מורה", "גן חובה", "שיעור")),
    ("animal", ("כלב", "כלבלב", "גורה", "חתול", "חתלתול", "ארנב", "ציפור", "סוס", "דג")),
    ("birthday", ("יום הולדת", "בלון", "בלונים", "מתנה", "נרות יום")),
    ("rain", ("גשם", "שלולית", "מטריה", "טיפות")),
    ("water", ("בריכה", "ים", "שחה", "שחיה", "גלים", "מים", "מקלחת")),
    ("bike", ("אופניים", "גלגל", "רכיבה", "רכב על")),
    ("apology", ("סליחה", "רבו", "ריב", "כעס", "מריבה", "התנצל", "תיקון")),
    ("treat", ("ארטיק", "גלידה", "שוקו", "שוקולד", "ממתק", "סוכריה")),
    ("sleep", ("ישן", "לישון", "פיג׳מה", "פיג'מה", "מיטה", "נרדם")),
    ("drawing", ("צייר", "ציירה", "ציור", "צבע", "צבעים")),
    ("flowers", ("פרח", "פרחים", "ליקט", "גינה")),
    ("building", ("מגדל", "לגו", "בנה", "בנתה", "קוביות")),
    ("letter", ("מכתב", "כתב", "כתבה", "גלויה")),
    ("forest", ("יער", "עצים", "חורשה", "טיול ביער")),
    ("music", ("שיר", "זמר", "פסנתר", "חליל", "ריקוד", "רקד")),
    ("market", ("שוק", "קניות", "מכולת", "פירות")),
    ("shabbat", ("שבת", "חלות", "נרות שבת", "קידוש")),
]


VERBS: dict[str, tuple[str, str]] = {
    "looked": ("הסתכל", "הסתכלה"),
    "felt": ("הרגיש", "הרגישה"),
    "asked": ("ביקש", "ביקשה"),
    "waited": ("חיכה", "חיכתה"),
    "put": ("הניח", "הניחה"),
    "went": ("הלך", "הלכה"),
    "sat": ("ישב", "ישבה"),
    "smiled": ("חייך", "חייכה"),
    "understood": ("הבין", "הבינה"),
    "took": ("לקח", "לקחה"),
    "said": ("אמר", "אמרה"),
    "slept": ("נרדם", "נרדמה"),
    "held": ("אחז", "אחזה"),
    "breathed": ("נשם", "נשמה"),
    "stood": ("עמד", "עמדה"),
    "raised": ("הרים", "הרימה"),
    "heard": ("שמע", "שמעה"),
    "saw": ("ראה", "ראתה"),
    "came": ("הגיע", "הגיעה"),
    "learned": ("למד", "למדה"),
    "wanted": ("רצה", "רצתה"),
    "knew": ("ידע", "ידעה"),
    "grew": ("גדל", "גדלה"),
    "opened": ("פתח", "פתחה"),
    "closed_eyes": ("עצם", "עצמה"),
    "returned": ("חזר", "חזרה"),
    "stopped": ("עצר", "עצרה"),
    "continued": ("המשיך", "המשיכה"),
    "remembered": ("זכר", "זכרה"),
    "entered": ("נכנס", "נכנסה"),
    "found": ("מצא", "מצאה"),
    "gave": ("נתן", "נתנה"),
    "thought": ("חשב", "חשבה"),
    "was": ("היה", "הייתה"),
    "nodded": ("הנהן", "הנהנה"),
    "touched": ("נגע", "נגעה"),
    "left": ("יצא", "יצאה"),
    "stayed": ("נשאר", "נשארה"),
    "told": ("סיפר", "סיפרה"),
    "drew": ("צייר", "ציירה"),
    "tasted": ("טעם", "טעמה"),
    "rode": ("רכב", "רכבה"),
    "built": ("בנה", "בנתה"),
    "met": ("פגש", "פגשה"),
    "hugged": ("חיבק", "חיבקה"),
    "helped": ("עזר", "עזרה"),
    "wrote": ("כתב", "כתבה"),
    "lay": ("שכב", "שכבה"),
    "woke": ("התעורר", "התעוררה"),
    "washed": ("שטף", "שטפה"),
    "mixed": ("ערבב", "ערבבה"),
    "listened": ("הקשיב", "הקשיבה"),
}

KEEPSAKE = {
    "tooth": "כוס השן",
    "fear_dark": "האור הקטן ליד המיטה",
    "baking": "ריח העוגה",
    "grandparent": "הידיים של סבתא",
    "friend": "המקום ליד החבר",
    "forgot": "הדבר שנשמר",
    "skill": "התרגול הקטן",
    "school": "תיק הגן",
    "animal": "החיה שנפגשה",
    "birthday": "בלון שנשאר",
    "rain": "הטיפות על החלון",
    "water": "המים השקטים",
    "bike": "האופניים ליד הקיר",
    "apology": "המילה סליחה",
    "treat": "הטעם המתוק",
    "sleep": "השמיכה החמה",
    "drawing": "הציור על הדף",
    "flowers": "פרח בכוס מים",
    "building": "המגדל שנשאר",
    "letter": "המכתב על השידה",
    "forest": "עלה בכיס",
    "music": "שיר שנשאר באוזן",
    "market": "פרי בתיק",
    "shabbat": "אור הנרות",
    "everyday": "הרגע מהשבוע",
}

TAG_SCENE_EN = {
    "tooth": "a child looking closely at a small fallen baby tooth in the palm, a little cup by the bed, growing-up bathroom-bedroom, wonder not pain",
    "fear_dark": "a child in a dim cozy bedroom asking for a small night light, a kind adult sitting nearby, gentle not scary, warm glow",
    "baking": "a child baking a cake with grandmother in a warm kitchen, flour on hands, mixing bowl, waiting by the oven",
    "grandparent": "a child with a grandparent in a warm home kitchen, wooden table, golden indoor light, making something together",
    "friend": "two children sharing a kind moment in a playground, making space for a friend, warm afternoon",
    "forgot": "a child remembering a small responsibility, finding a lost thing, gentle lesson, indoor home",
    "skill": "a child practicing a small new skill, trying again slowly, proud and gentle",
    "school": "a kindergarten yard or classroom at late afternoon, child with a teacher or backpack, warm and safe",
    "animal": "a child meeting a friendly dog or cat gently, outdoor park or garden, kind and calm",
    "birthday": "a small birthday moment, a balloon or cake, warm indoor party light, child-safe celebration",
    "rain": "a child watching rain through a window, droplets on glass, warm room light, boots by the door",
    "water": "a child at a calm pool or gentle shore, safe shallow water, warm evening light",
    "bike": "a child riding a bicycle on a quiet path, learning balance, park in late afternoon",
    "apology": "two children making up kindly, a soft apology, no shame, warm indoor or garden",
    "treat": "a child tasting a popsicle or cocoa, summer or kitchen, simple joy",
    "sleep": "a child in pajamas at a grandparent house or own bed, very calm, nightlight",
    "drawing": "a child drawing a sun with crayons at a small table, papers, warm lamp",
    "flowers": "a child picking or holding small flowers in a garden, watering can, sunset",
    "building": "a child building a block tower on the floor, concentration, home interior",
    "letter": "a child writing or holding a small letter, pencil, window light",
    "forest": "a gentle forest path at dusk, child noticing trees and moss, lantern light, child-safe",
    "music": "a child singing or dancing a small song at home, warm lamp, joy",
    "market": "a small neighborhood market, fruit crates, child with a grownup, afternoon light",
    "shabbat": "a peaceful Shabbat table, candles, challah, family calm, child nearby",
    "everyday": "a child living a real ordinary weekly moment at home, watercolor, warm light",
}

TAG_THEME = {
    "baking": "grandparent-kitchen",
    "grandparent": "grandparent-kitchen",
    "tooth": "library-nook",
    "fear_dark": "stars",
    "rain": "rainy-window",
    "water": "sea",
    "bike": "park",
    "school": "schoolyard",
    "animal": "park",
    "birthday": "garden",
    "friend": "park",
    "shabbat": "shabbat-table",
    "market": "neighborhood-market",
    "forest": "forest",
    "flowers": "garden",
    "drawing": "library-nook",
    "letter": "library-nook",
    "sleep": "stars",
    "treat": "park",
    "building": "library-nook",
}

WILD_THEMES = {"desert", "forest", "mountain-path", "orchard", "riverbank", "sea"}
DOMESTIC_TAGS = {
    "tooth", "baking", "grandparent", "fear_dark", "sleep", "drawing",
    "letter", "building", "forgot", "shabbat",
}

PHRASE_EN: list[tuple[str, str]] = [
    ("איבדה שן", "lost a tooth"),
    ("אפתה עם סבתא", "baked with grandmother"),
    ("פחדה מהחושך", "was afraid of the dark"),
    ("רכב על אופניים", "rode a bicycle"),
    ("אכל ארטיק", "ate a popsicle"),
    ("פגש כלב בגן", "met a dog in the park"),
    ("בנה מגדל", "built a tower"),
    ("שחה בבריכה", "swam in the pool"),
    ("ישן אצל סבא", "slept at grandpa's house"),
    ("ציירה שמש", "drew a sun"),
    ("אכלה שוקו", "drank cocoa"),
    ("ראתה חתול", "saw a cat"),
    ("ליקטה פרחים", "picked flowers"),
    ("שמעה גשם", "heard the rain"),
    ("כתבה מכתב", "wrote a letter"),
    ("שתף צבע", "shared a crayon"),
    ("חיבק חבר", "hugged a friend"),
]


def _gender(voice: Any) -> str:
    g = getattr(voice, "gender", voice)
    return "f" if g == "f" else "m"


def V(voice: Any, key: str) -> str:
    masc, fem = VERBS[key]
    return fem if _gender(voice) == "f" else masc


FEMALE_COMPANIONS = {"firefly", "owl"}
COMP_VERBS = {
    "said": ("אמר", "אמרה"),
    "heard": ("שמע", "שמעה"),
    "sat": ("ישב", "ישבה"),
    "stayed": ("נשאר", "נשארה"),
    "took": ("לקח", "לקחה"),
    "quiet": ("שתק", "שתקה"),
    "extinguished": ("כבה", "כבתה"),
    "whispered": ("לחש", "לחשה"),
    "saw": ("ראה", "ראתה"),
    "kept": ("שמר", "שמרה"),
    "nodded": ("הנהן", "הנהנה"),
    "brought": ("הביא", "הביאה"),
    "lit": ("הדליק", "הדליקה"),
}


def companion_fem(companion: dict[str, str] | None) -> bool:
    cid = (companion or {}).get("id") or ""
    he = (companion or {}).get("he_the") or (companion or {}).get("he") or ""
    if cid in FEMALE_COMPANIONS:
        return True
    return any(w in he for w in ("גחלילית", "אוחה"))


def CV(companion: dict[str, str] | None, key: str) -> str:
    masc, fem = COMP_VERBS[key]
    return fem if companion_fem(companion) else masc


def pronoun(voice: Any) -> str:
    return "היא" if _gender(voice) == "f" else "הוא"


def poss_adj(voice: Any) -> str:
    return "שלה" if _gender(voice) == "f" else "שלו"


def child_word(voice: Any) -> str:
    return "ילדה" if _gender(voice) == "f" else "ילד"


def allowed_word(voice: Any) -> str:
    return "מותרת" if _gender(voice) == "f" else "מותר"


def age_phrase(age: int, voice: Any) -> str:
    if _gender(voice) == "f":
        return f"בת ה־{age}"
    return f"בן ה־{age}"


def _clean_join(*parts: str) -> str:
    text = " ".join(p.strip() for p in parts if p and str(p).strip())
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.!?])", r"\1", text)
    return text.strip()


def classify_event(text: str) -> list[str]:
    """Return ordered tags for a parent-written weekly event."""
    raw = text or ""
    tags: list[str] = []
    for tag, words in TAG_DEFS:
        if any(w in raw for w in words):
            tags.append(tag)
    if not tags:
        tags.append("everyday")
    return tags


def choose_flavor_theme(tags_list: list[list[str]], template_theme: str) -> str:
    """Pick a place that matches the week; never contradict domestic events with a desert quest."""
    flat: list[str] = []
    for ts in tags_list:
        flat.extend(ts)
    for tag in (
        "baking",
        "grandparent",
        "water",
        "rain",
        "school",
        "bike",
        "forest",
        "shabbat",
        "market",
        "animal",
        "birthday",
        "fear_dark",
        "tooth",
        "flowers",
        "sleep",
        "drawing",
        "letter",
        "friend",
        "treat",
        "building",
    ):
        if tag in flat:
            return TAG_THEME.get(tag, template_theme or "garden")
    if (template_theme in WILD_THEMES) and any(t in DOMESTIC_TAGS for t in flat):
        return "garden"
    return template_theme or "garden"


def event_to_english(event: str, tags: list[str] | None = None) -> str:
    tags = tags or classify_event(event)
    low = event or ""
    for heb, en in PHRASE_EN:
        if heb in low:
            primary = TAG_SCENE_EN.get(tags[0], TAG_SCENE_EN["everyday"])
            return f"{primary}, specifically: {en}"
    bits = [TAG_SCENE_EN.get(t, "") for t in tags]
    bits = [b for b in bits if b]
    if bits:
        return bits[0]
    return "a child living a real weekly moment, ordinary and warm, not a fantasy quest"


def keepsake_for(event: str, tags: list[str] | None = None) -> str:
    tags = tags or classify_event(event)
    for t in tags:
        if t in KEEPSAKE and t != "everyday":
            return KEEPSAKE[t]
    # last words of the event as a small object
    words = (event or "").split()
    if words:
        return "מה שהיה: " + " ".join(words[-2:])
    return KEEPSAKE["everyday"]


def scene_from_event(
    name: str,
    voice: Any,
    age: int,
    event: str,
    index: int,
    companion: dict[str, str] | None = None,
    rng: random.Random | None = None,
) -> str:
    """Expand an event into 2–4 lived Hebrew sentences.

    Includes the child's name and the event's own words, wrapped in action,
    feeling, and a before/during/after beat. Never a colon-paste of the raw string.
    """
    rng = rng or random.Random(f"{name}:{event}:{index}")
    tags = classify_event(event)
    primary = tags[0]
    builders: dict[str, Callable[..., str]] = {
        "tooth": _scene_tooth,
        "fear_dark": _scene_fear,
        "baking": _scene_baking,
        "grandparent": _scene_grandparent,
        "friend": _scene_friend,
        "forgot": _scene_forgot,
        "skill": _scene_skill,
        "school": _scene_school,
        "animal": _scene_animal,
        "birthday": _scene_birthday,
        "rain": _scene_rain,
        "water": _scene_water,
        "bike": _scene_bike,
        "apology": _scene_apology,
        "treat": _scene_treat,
        "sleep": _scene_sleep,
        "drawing": _scene_drawing,
        "flowers": _scene_flowers,
        "building": _scene_building,
        "letter": _scene_letter,
        "forest": _scene_forest,
        "music": _scene_music,
        "market": _scene_market,
        "shabbat": _scene_shabbat,
        "everyday": _scene_everyday,
    }
    # Prefer the most cinematic tag if several match.
    for key in (
        "tooth",
        "baking",
        "fear_dark",
        "bike",
        "water",
        "animal",
        "birthday",
        "apology",
        "rain",
        "school",
        "drawing",
        "building",
        "letter",
        "treat",
        "sleep",
        "friend",
        "grandparent",
        "forest",
        "flowers",
        "music",
        "market",
        "shabbat",
        "forgot",
        "skill",
        "everyday",
    ):
        if key in tags:
            primary = key
            break
    fn = builders.get(primary, _scene_everyday)
    text = fn(name, voice, age, event, index, rng)
    if companion and rng.random() > 0.45:
        c = companion.get("he_the") or companion.get("he") or ""
        if c:
            extras = [
                f"{c} {CV(companion, 'stayed')} בפתח בלי לקחת את הרגע.",
                f"{c} {CV(companion, 'saw')} את זה בשקט, כמו עד רך.",
                f"ליד {name} היה גם {c}, בלי לדחוף.",
            ]
            text = _clean_join(text, extras[index % len(extras)])
    if event not in text:
        # Guarantee the parent's words appear as a lived clause, not after a colon.
        text = _clean_join(f"{name} {event}.", text)
    return text


def _scene_tooth(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    she = pronoun(voice)
    a, b, c = [
        (
            f"{name} {event}. השן הקטנה ישבה בכף היד, לבנה וקלה כמו אורז, ו{name} {v('looked')} עליה ארוכות.",
            f"הלשון חיפשה את החלל החדש בפה, ו{name} {v('felt')} שהגוף יודע לגדול בלי רשות מיוחדת.",
            f"אחר כך {she} {v('put')} את השן בכוס קטנה ליד המיטה, כמו שמניחים דבר חשוב שלא זורקים.",
        ),
        (
            f"ליד הכיור {name} {event}. מים קרים על הסנטר, ואז השן הייתה בחוץ, קטנה ואמיתית.",
            f"{name} {v('raised')} אותה אל האור ו{v('saw')} שגוף יכול להשתנות ביום רגיל.",
            f"לפני השינה הכוס חיכתה על השידה, ו{name} {v('smiled')} אל החלל בפה.",
        ),
        (
            f"זה התחיל בטעם מוזר, ואז {name} {event}. לא דרקון ולא יער — פה, יד, שן.",
            f"{name} {v('sat')} על שולי האמבטיה ו{v('looked')} על מה שיצא מהגוף.",
            f"אחרי כן {she} {v('knew')} שמשהו קטן נגמר, ומשהו גדול מתחיל לאט.",
        ),
    ][index % 3]
    return _clean_join(a, b, c)


def _scene_baking(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    she = pronoun(voice)
    a, b, c = [
        (
            f"במטבח היה חם וריח של קמח. {name} {event}.",
            f"הידיים התלכלכו, הקערה נעשתה כבדה, ו{name} {v('waited')} ליד התנור בלי לדחוף את השעון.",
            f"העוגה ביקשה זמן. {she} {v('learned')} שאפשר לעשות יחד, ואחר כך לחכות יחד.",
        ),
        (
            f"סבתא הגישה כף עץ, ו{name} {event}. קמח על האף, בצק על המרפק, צחוק קטן באמצע.",
            f"{name} {v('mixed')} לאט, כי משהו טוב לא רץ.",
            f"כשהעוגה הייתה בפנים, {she} {v('sat')} על הכיסא ו{v('looked')} בחלון עד שהריח מילא את הבית.",
        ),
        (
            f"השולחן היה מפה של קמח. שם {name} {event}, לא כמתכון בדף אלא כעבודה של ידיים.",
            f"{name} {v('felt')} את החום מהתנור על הברכיים.",
            f"לפני שטעמו, {she} {v('waited')}. אחרי שטעמו, {name} {v('smiled')} מתוק ומלא.",
        ),
    ][index % 3]
    return _clean_join(a, b, c)


def _scene_fear(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    she = pronoun(voice)
    a, b, c = [
        (
            f"בלילה החדר נעשה גדול מדי. {name} {event}.",
            f"השמיכה לא כיסתה את הפינות, ו{name} {v('asked')} לאור קטן, או ליד שתישב קרוב.",
            f"החושך לא נעלם לגמרי. הוא נהיה רך יותר, כי {she} {v('asked')} ולא {v('stayed')} לבד עם הפחד.",
        ),
        (
            f"כשכבו את האור הגדול, {name} {event}. הלב דפק כמו צעדים במסדרון.",
            f"{name} {v('said')} בקול קטן: תישאר איתי. מישהו נשאר. נדלק פנס לילה.",
            f"אחר כך {she} {v('breathed')} לאט. החושך היה אותו חושך, אבל {name} כבר לא {v('was')} לבד בתוכו.",
        ),
        (
            f"{name} {event}, והקיר נראה רחוק. זה היה פחד אמיתי בגובה {child_word(voice)}.",
            f"{name} {v('held')} את השמיכה ו{v('asked')} לאור בגודל כפית.",
            f"כשהאור הקטן בא, {she} {v('understood')} שאפשר לבקש עזרה בלי בושה.",
        ),
    ][index % 3]
    # Fix "נשארה" for male in first variant — use stayed verb instead in a gender-safe way.
    if _gender(voice) == "m":
        text = _clean_join(a, b, c).replace("ולא נשארה לבד", "ולא נשאר לבד")
        text = text.replace("כבר לא היה לבד", "כבר לא היה לבד")
        return text
    return _clean_join(a, b, c)


def _scene_grandparent(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"בבית החם {name} {event}.",
        f"הידיים הגדולות היו ליד הידיים הקטנות, ו{name} {v('felt')} איך עושים דבר ביחד.",
        f"אחר כך {pronoun(voice)} {v('sat')} קרוב, עם ריח של בית ישן וטוב, ולא מיהר{'' if _gender(voice)=='m' else 'ה'} לשום מקום.",
    )


def _scene_friend(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"בחצר {name} {event}.",
        f"{name} {v('went')} קצת הצידה כדי שיהיה מקום לעוד ברך במעגל.",
        f"המשחק נעשה רחב יותר. {pronoun(voice)} {v('smiled')}, כי חבר נכנס כשעושים לו מקום.",
    )


def _scene_forgot(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"לרגע משהו הלך לאיבוד, ו{name} {event}.",
        f"{name} {v('stopped')} ו{v('thought')}. אחר כך {v('found')} מה שצריך לשמור.",
        f"אחריות, גילה {pronoun(voice)}, מתחילה בדבר קטן שמחזירים למקום.",
    )


def _scene_skill(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"{name} {event}. בהתחלה זה יצא עקום, ואז פחות עקום.",
        f"{name} {v('wanted')} שוב, לאט, בלי לצחוק על עצמ{'ה' if _gender(voice)=='f' else 'ו'}.",
        f"בסוף {pronoun(voice)} {v('smiled')}: לנסות שוב זה גם הצלחה.",
    )


def _scene_school(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"בחצר ובכיתה {name} {event}.",
        f"התיק היה כבד קצת, השמש על הקיר, ו{name} {v('heard')} את הקולות מסביב.",
        f"אחר כך {pronoun(voice)} {v('returned')} הביתה עם יום שלם בכיסים.",
    )


def _scene_animal(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"בגן, לאט לאט, {name} {event}.",
        f"{name} {v('held')} את היד קרוב לגוף קודם, ואז הושיט{'ה' if _gender(voice)=='f' else ''} אותה בעדינות.",
        f"החיה לא הייתה סיפור. היא הייתה חיה, חמה ונושמת, ו{name} {v('learned')} לגשת בלי לקפוץ.",
    )


def _scene_birthday(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"האור היה צבעוני וחם, ו{name} {event}.",
        f"בלון נגע בתקרה, מישהו שר, ו{name} {v('felt')} את היום יושב על הכתפיים כמו גלימה קלה.",
        f"אחר כך {pronoun(voice)} {v('put')} רגע אחד בכיס: מישהו חגג את {name}.",
    )


def _scene_rain(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"מאחורי הזכוכית {name} {event}.",
        f"הטיפות ציירו קווים, ו{name} {v('listened')} לקול הגשם כאילו הוא מספר.",
        f"בפנים היה יבש וחם. {pronoun(voice)} {v('put')} כף יד על החלון הקר ואחר כך חזר{'ה' if _gender(voice)=='f' else ''} אל החדר.",
    )


def _scene_water(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"ליד המים {name} {event}.",
        f"המים החזיקו את {name} לאט, ו{pronoun(voice)} {v('breathed')} מעל פני השטח ואז צלל{'ה' if _gender(voice)=='f' else ''} קצת.",
        f"אחרי המגבת {name} {v('felt')} מלח או כלור על העור, ושמחה קטנה של גוף רטוב.",
    )


def _scene_bike(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"על השביל {name} {event}.",
        f"הגלגלים מצאו שיווי משקל, הרוח על הפנים, ו{name} {v('held')} את הכידון כמו שאוחזים אומץ בגובה ידיים.",
        f"פעם אחת כמעט נפל{'' if _gender(voice)=='m' else 'ה'}, ואז {v('continued')}. בסוף {pronoun(voice)} {v('smiled')} רחוק יותר מאתמול.",
    )


def _scene_apology(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"הלב היה קצת מקומט כש{name} {event}.",
        f"{name} {v('said')} מילה עגולה, לא חדה: סליחה. אף אחד לא בוש.",
        f"אחר כך {pronoun(voice)} {v('felt')} איך תיקון הוא גשר, לא עונש.",
    )


def _scene_treat(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"בשמש או במטבח {name} {event}.",
        f"הטעם היה קר או מתוק, ו{name} {v('tasted')} לאט כדי שלא ייגמר מהר מדי.",
        f"אחר כך נשארה טיפה על השפה, ו{pronoun(voice)} {v('smiled')} על דבר קטן שעשה יום שלם.",
    )


def _scene_sleep(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"כשהבית היה אחר, {name} {event}.",
        f"השמיכה הריחה אחרת, והכרית הייתה אורחת, ו{name} {v('lay')} בכל זאת.",
        f"לפני ש{name} {v('slept')}, {pronoun(voice)} {v('heard')} את הבית החדש נושם.",
    )


def _scene_drawing(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"על הדף {name} {event}.",
        f"הצבע יצא מחוץ לקו, ו{name} {v('continued')} בכל זאת, כי שמש לא חייבת להיות עגולה לגמרי.",
        f"אחר כך {pronoun(voice)} {v('raised')} את הציור אל האור והבית קיבל עוד חלון.",
    )


def _scene_flowers(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"בין העלים {name} {event}.",
        f"{name} {v('held')} גבעול בלי למעוך, ו{v('smiled')} אל הצבע.",
        f"בבית הושמה הכוס במים. משהו חי המשיך לשתות גם אחרי הטיול.",
    )


def _scene_building(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"על הרצפה {name} {event}.",
        f"קומה על קומה, נשימה על נשימה. פעם אחת נפל, ו{name} {v('built')} שוב, נמוך יותר וחזק יותר.",
        f"בסוף {pronoun(voice)} {v('looked')} על מה שעמד, ולא על מה שהיה יכול להיות מושלם.",
    )


def _scene_letter(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"עם עיפרון ועם לב {name} {event}.",
        f"האותיות יצאו גדולות, ו{name} {v('wrote')} מה שהיה אמיתי, בלי לבקש מתנה.",
        f"אחר כך {pronoun(voice)} {v('put')} את הדף על החלון, כאילו אור יכול לקרוא.",
    )


def _scene_forest(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"בין העצים {name} {event}.",
        f"ריח של אדמה לחה, אור ירוק־זהוב, ו{name} {v('went')} לאט כדי לשמוע עלים.",
        f"אחר כך {pronoun(voice)} {v('put')} עלה בכיס, לא כאוצר — כזיכרון.",
    )


def _scene_music(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"בבית {name} {event}.",
        f"הקול יצא קצת עקום ואחר כך נכון יותר, ו{name} {v('heard')} את עצמ{'ה' if _gender(voice)=='f' else 'ו'}.",
        f"כשנגמר, השיר נשאר בחדר כמו אור שלא כבו.",
    )


def _scene_market(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"בין הארגזים {name} {event}.",
        f"ריח תפוזים, קול של מוכר, ו{name} {v('took')} פרי ביד כדי להרגיש שהוא כבד ואמיתי.",
        f"בדרך הביתה התיק נדנד, ו{pronoun(voice)} {v('smiled')} אל מה שנקנה יחד.",
    )


def _scene_shabbat(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    return _clean_join(
        f"ליד המפה הלבנה {name} {event}.",
        f"הנרות עשו עיגול זהוב, ו{name} {v('listened')} לשקט שנכנס אחרי החול.",
        f"אחר כך {pronoun(voice)} {v('felt')} שהשולחן מחזיק את כולם בלי לומר הרבה.",
    )


def _scene_everyday(name, voice, age, event, index, rng) -> str:
    v = lambda k: V(voice, k)
    she = pronoun(voice)
    beats = [
        (
            f"בשבוע הזה {name} לא המציא{'ה' if _gender(voice)=='f' else ''} הרפתקה רחוקה. {name} {event}.",
            f"לפני כן {she} {v('breathed')} רגיל. בתוך כך הידיים והלב היו שם. אחרי כן {name} {v('remembered')} איך זה הרגיש.",
            f"{name} {v('took')} את הרגע הלאה, לא ככותרת — כדבר שקרה לגוף.",
        ),
        (
            f"{name} {event}, באמצע יום שנראה רגיל עד שלא היה.",
            f"{name} {v('stopped')} רגע, {v('looked')}, ו{v('felt')} שזה שייך {poss_adj(voice)}.",
            f"אחר כך {she} {v('continued')} את היום, כבר עם הרגע בכיס.",
        ),
        (
            f"אף אחד לא צילם. פשוט {name} {event}.",
            f"האוויר היה האוויר של הבית או החצר, ו{name} {v('was')} בתוכו לגמרי.",
            f"בערב {she} {v('told')} את זה שוב, כדי שלא יישבר בדרך אל השינה.",
        ),
    ][index % 3]
    return _clean_join(*beats)


def moral_from_week(
    name: str,
    voice: Any,
    events: list[str],
    tags_list: list[list[str]],
) -> tuple[str, str]:
    """A moral ABOUT THIS WEEK, echoing concrete things — not a canned slogan."""
    s: set[str] = set()
    for ts in tags_list:
        s.update(ts)

    def has(*xs: str) -> bool:
        return all(x in s for x in xs)

    def has_any(*xs: str) -> bool:
        return any(x in s for x in xs)

    # Noa sample and close cousins — connect body / waiting / asking.
    if has("tooth", "baking", "fear_dark") or (
        has("tooth", "fear_dark") and has_any("baking", "grandparent")
    ):
        return (
            "לפעמים הגוף משתנה, העוגה צריכה זמן, והחושך נהיה רך יותר כשמבקשים אור קטן.",
            "grow-wait-ask",
        )
    if has("tooth", "baking") or (has("tooth") and has_any("baking", "grandparent")):
        return (
            "השן מלמדת שהגוף גדל, והעוגה עם סבתא מלמדת לחכות — שניהם צריכים זמן.",
            "grow-wait",
        )
    if has("tooth", "fear_dark"):
        return (
            "מותר לגדול כשהשן יוצאת, ומותר לבקש אור קטן כשהחושך גדול מדי.",
            "grow-ask",
        )
    if has_any("baking", "grandparent") and has("fear_dark"):
        return (
            "כמו עוגה בתנור של סבתא, גם האומץ מגיע לאט, ואור קטן עוזר לחושך להתרכך.",
            "wait-ask",
        )
    if has("fear_dark") and has_any("friend", "sleep"):
        return (
            "כשמבקשים יד או אור בחושך, הפחד לא נמחק — הוא מתחלק.",
            "ask-help",
        )
    if has("fear_dark"):
        ask = "מבקשת" if _gender(voice) == "f" else "מבקש"
        return (
            f"כש{name} {ask} אור קטן, החושך נהיה רך יותר. לבקש עזרה זה אומץ.",
            "ask-help",
        )
    if has("tooth"):
        return (
            f"שן שיוצאת אומרת ל{name} שהגוף משתנה, ואפשר להסתכל על השינוי בלי פחד.",
            "grow-body",
        )
    if has_any("baking", "grandparent"):
        return (
            "עוגה עם סבתא צריכה זמן, ידיים משותפות, ולא לרוץ על מה שעוד מתבשל.",
            "patience",
        )
    if has("bike") and has("animal"):
        return (
            "על האופניים לומדים שיווי משקל, וליד כלב לומדים רוך — שניהם אומץ בגובה ילד.",
            "try-again",
        )
    if has("bike") and has("treat"):
        return (
            "אחרי רכיבה מגיע טעם מתוק, והגוף זוכר גם את המאמץ וגם את השמחה.",
            "try-again",
        )
    if has("bike"):
        return (
            "על האופניים נופלים קצת וקמים, וזה חלק מהנסיעה לא חלק מהכישלון.",
            "try-again",
        )
    if has("water") and has("sleep"):
        return (
            "אחרי מים בא שינה במקום אחר, והגוף לומד שהוא יכול להיות בטוח גם לא בבית.",
            "gentleness",
        )
    if has("water"):
        return (
            "במים לומדים לסמוך על הגוף, לנשום, ולחזור אל היבשה עם שמחה רטובה.",
            "try-again",
        )
    if has("animal") and has("treat"):
        return (
            "אפשר לטעום מתוק ולפגוש חיה בעדינות — השבוע קורה ביד ובפה, לא בסיסמה.",
            "gentleness",
        )
    if has("animal"):
        return (
            "חיה נפגשת לאט. יד רכה שומרת גם על הילד וגם על מי שיש לו פרווה.",
            "gentleness",
        )
    if has("apology") or has("friend") and "סליחה" in " ".join(events):
        return (
            "סליחה אמיתית מתקנת יותר מתירוץ, ומחזירה מקום במעגל.",
            "sorry",
        )
    if has("friend"):
        return (
            "חבר נכנס כשעושים לו מקום במעגל, וגם כשמשתפים צבע או חיבוק.",
            "include-friend",
        )
    if has("rain") and has("letter"):
        return (
            "גשם על החלון ומכתב על הדף — שניהם דרכים להגיד משהו בלי לצעוק.",
            "listening",
        )
    if has("rain"):
        return (
            "אפשר לשמוע גשם מאחורי חלון וללמוד שהעולם ממשיך גם כשנשארים בפנים.",
            "patience",
        )
    if has("drawing") and has("treat"):
        return (
            "שמש על דף ושוקו בכוס — דברים קטנים שצובעים יום שלם.",
            "gratitude",
        )
    if has("drawing") and has("animal"):
        return (
            "אפשר לצייר שמש ולראות חתול, ולשמור את שני הרגעים בלי לבחור מי חשוב יותר.",
            "notice-others",
        )
    if has("building") and has("water"):
        return (
            "מגדל על הרצפה ומים בבריכה — בשניהם בונים שיווי משקל, ואז נופלים וקמים.",
            "try-again",
        )
    if has("building"):
        return (
            "מגדל שנפל מלמד לבנות שוב, נמוך יותר ושמח יותר.",
            "try-again",
        )
    if has("school"):
        return (
            "יום בגן נשמר בתיק, ואפשר לספר אותו בערב בלי לצמצם אותו לציוּן.",
            "listening",
        )
    if has("birthday"):
        return (
            "יום הולדת הוא לא רק עוגה — הוא לראות שמישהו שמח שאתה בעולם.",
            "gratitude",
        )
    if has("forgot"):
        return (
            "מה ששוכחים אפשר עוד להחזיר, ואחריות מתחילה בדבר קטן ששומרים עליו.",
            "responsibility",
        )
    if has("skill"):
        return (
            "לנסות שוב, לאט, זה גם הצלחה — לא רק הפעם שבה כבר יודעים.",
            "try-again",
        )
    if has("sleep"):
        return (
            "לישון במקום אחר זה אומץ שקט, והשמיכה החדשה נהיית מוכרת אם נשארים.",
            "gentleness",
        )
    if has("treat"):
        return (
            "טעם מתוק נגמר מהר אם בולעים. לאט — והיום מתארך.",
            "patience",
        )
    if has("letter"):
        return (
            "מכתב קטן יכול לשאת לב גדול, בלי לבקש מתנה בחזרה.",
            "gratitude",
        )
    if has("flowers"):
        return (
            "פרח שנלקח בעדינות ממשיך לשתות בבית, אם זוכרים לתת לו מים.",
            "nature-care",
        )
    if has("shabbat"):
        return (
            "אור נרות מלמד לעצור. לא כל ערב צריך לרוץ.",
            "patience",
        )
    if has("music"):
        return (
            "שיר עקום בהתחלה עדיין שיר, אם ממשיכים לשים לב לקול.",
            "try-again",
        )

    # Fallback: echo the week's own words as meaning, not a kindness sticker.
    e1, e2 = events[0], events[1] if len(events) > 1 else events[0]
    return (
        f"מתוך מה שהיה ל{name} השבוע — {e1}, ואחר כך {e2} — אפשר להרגיש, לעשות, ולספר. זה השיעור, לא סיסמה כללית.",
        "this-week",
    )


def _opening(
    name: str,
    voice: Any,
    age: int,
    events: list[str],
    tags_list: list[list[str]],
    companion: dict[str, str],
    theme: dict[str, str] | None,
    rng: random.Random,
    template: dict[str, Any] | None = None,
) -> str:
    ap = age_phrase(age, voice)
    c = companion.get("he_the") or companion.get("he") or "הלילה"
    light = (theme or {}).get("light") or "אור רך"
    air = (theme or {}).get("air") or "אוויר של ערב"
    v = lambda k: V(voice, k)
    e1, e2, e3 = events[0], events[1], events[2]
    flat = {t for ts in tags_list for t in ts}
    place_note = ""
    if "forest" in flat:
        place_note = "גם בין עצים, "
    elif "baking" in flat or "grandparent" in flat:
        place_note = "גם במטבח החם, "
    variants = [
        (
            f"השבוע של {name}, {ap}, לא היה מסע בארץ רחוקה. "
            f"הוא היה השבוע שבו {name} {e1}, ואחר כך {e2}, ובלילה כמעט {e3}. "
            f"{light}. {air}. {c} {CV(companion, 'sat')} על אדן החלון ו{CV(companion, 'said')}: הערב נספר את מה שהיה באמת."
        ),
        (
            f"{name} {ap} {v('came')} אל הערב עם שבוע שלם בגוף. "
            f"{place_note}לא דרקון ולא מפה — {name} {e1}, ואחר כך {name} {e2}, ואחר כך {name} {e3}. "
            f"{c} {CV(companion, 'heard')} קודם, ורק אחר כך {CV(companion, 'said')} ל{name}: נלך לאט על מה שקרה."
        ),
        (
            f"ל{name} {ap} היה שבוע עם שלושה דברים חיים. "
            f"{c} לא {CV(companion, 'brought')} הרפתקה. {CV(companion, 'brought')} אוזן. {light}. "
            f"{name} {v('breathed')} ואמר{'ה' if _gender(voice)=='f' else ''}: היה השבוע שבו {e1}, ואז {e2}, ואז {e3}."
        ),
    ]
    text = rng.choice(variants)
    fmt = (template or {}).get("format") or ""
    c = companion.get("he_the") or companion.get("he") or "הלילה"
    flavor = {
        "quiet-evening": f"הבית דיבר בלחש, ו{c} לא מיהר.",
        "two-voices": f"שני קולות ישבו זה ליד זה: {name} ו{c}.",
        "letter-to-the-moon": f"{name} ליטף עיפרון, לא כדי לבקש מתנה — כדי לספר.",
        "recipe-of-the-heart": f"על השולחן חיכתה קערה, רק אם השבוע עצמו ביקש להתבשל.",
        "listening-ear": f"{c} {CV(companion, 'brought')} אוזן רכה, והשבוע נכנס אליה עד הסוף.",
        "wait-for-morning": f"אפשר לחכות לבוקר בלי לזרוק את הערב.",
        "circle-of-friends": f"{name} השאיר מקום ליד הברך, שייכנס עוד סיפור.",
        "whisper-walk": f"הצעדים היו קטנים בכוונה.",
        "lantern-path": f"{c} {CV(companion, 'lit')} אור קטן, לא זרקור.",
        "treasure-of-small-things": f"אוצר אמיתי נכנס לכיס: שלושה רגעים.",
        "first-time": f"אפשר לנסות לאט. לא צריך לדעת הכול מראש.",
        "lost-and-found": f"מה שהיה השבוע לא אבד — הוא חיכה שיסתכלו עליו.",
        "apology": f"אם משהו נשבר, אפשר לתקן במילים. בלי בושה.",
    }
    extra = flavor.get(fmt, "")
    return _clean_join(text, extra)


def _bridge(
    name: str,
    voice: Any,
    e1: str,
    e2: str,
    t1: list[str],
    t2: list[str],
    companion: dict[str, str],
    rng: random.Random,
) -> str:
    v = lambda k: V(voice, k)
    c = companion.get("he_the") or "הלילה"
    s1, s2 = set(t1), set(t2)
    if "tooth" in s1 and ("baking" in s2 or "grandparent" in s2):
        return _clean_join(
            f"מהשן הקטנה עד המטבח היה מרחק של כמה שעות, אבל בלב של {name} הם ישבו יחד.",
            f"דבר אחד משתנה בפה, ואחרי ש{name} {e2}, העוגה ביקשה זמן בתנור.",
            f"{c} {CV(companion, 'said')} ששניהם שייכים לאותו שבוע: לגדול, ולחכות.",
        )
    if "baking" in s1 and "fear_dark" in s2:
        return _clean_join(
            f"ריח העוגה נשאר בשיער כש{name} {v('went')} אל הלילה.",
            f"מהמטבח אל החושך: אחרי ש{name} {e1}, החדר ביקש משהו אחר.",
            f"{name} {v('understood')} שחום של תנור וחום של יד ליד המיטה הם קרובי משפחה.",
        )
    if "bike" in s1 and ("treat" in s2 or "animal" in s2):
        return _clean_join(
            f"הברכיים עוד זכרו את האופניים כש{name} {v('came')} אל הרגע הבא.",
            f"אחרי ש{name} {e1}, הגוף היה מוכן גם ל{e2}.",
            f"שיווי משקל ואחר כך שמחה — {c} {CV(companion, 'nodded')}.",
        )
    return _clean_join(
        f"אחרי ש{name} {e1}, היום לא נגמר. הוא התגלגל הלאה.",
        f"ושם, בלי למחוק את מה שהיה, {name} {e2} כבר חיכה באוויר.",
        f"{name} {v('felt')} איך שני הרגעים מדברים זה עם זה, ו{c} {CV(companion, 'kept')} שלא יאבד אחד מהם.",
    )


def _turning(
    name: str,
    voice: Any,
    events: list[str],
    tags_list: list[list[str]],
    companion: dict[str, str],
    rng: random.Random,
) -> str:
    v = lambda k: V(voice, k)
    e1, e2, e3 = events
    s = {t for ts in tags_list for t in ts}
    c = companion.get("he_the") or "הלילה"
    if "tooth" in s and ("baking" in s or "grandparent" in s) and "fear_dark" in s:
        return _clean_join(
            f"{name} {v('thought')} על השן, על סבתא והעוגה, ועל החושך בחדר.",
            f"הפה השתנה, העוגה ביקשה זמן, והחושך ביקש אור קטן.",
            f"{name} {v('understood')} שמותר לגדול, מותר לחכות, ומותר לבקש. {c} {CV(companion, 'quiet')}, כי זה כבר היה ברור.",
        )
    if "tooth" in s and "fear_dark" in s:
        return _clean_join(
            f"השן לימדה שינוי, והחושך לימד לבקש. {name} {v('held')} את שני השיעורים.",
            f"{e1}. {e3}. שניהם אמיתיים. {c} {CV(companion, 'said')}: אפשר את שניהם בערב אחד.",
        )
    keeps = [keepsake_for(e, t) for e, t in zip(events, tags_list)]
    return _clean_join(
        f"{name} {v('saw')} את שלושת הרגעים יחד, לא כרשימה — כשבוע אחד.",
        f"{e1}. אחר כך {e2}. ואז {e3}.",
        f"הם החזיקו זה את זה כמו {keeps[0]} ליד {keeps[1]} ליד {keeps[2]}. {name} {v('nodded')}.",
    )


def _moral_landing(name: str, voice: Any, moral: str, companion: dict[str, str], rng: random.Random) -> str:
    v = lambda k: V(voice, k)
    c = companion.get("he_the") or "הלילה"
    variants = [
        f"ו{name} {v('found')} משפט שנשאר, לא כשיעור מורה אלא כטעם של השבוע: {moral} {c} לא מחא כף. רק {CV(companion, 'nodded')}.",
        f"{c} {CV(companion, 'whispered')} בלי להטיף. {name} {v('heard')}: {moral} זה היה על מה שקרה, לא על ילד מדומיין.",
        f"על הכרית נשאר דבר אחד חם: {moral} {name} {v('put')} את זה ליד הלב, לא ליד ציון.",
    ]
    return _clean_join(rng.choice(variants))


def _close(
    name: str,
    voice: Any,
    events: list[str],
    tags_list: list[list[str]],
    companion: dict[str, str],
    rng: random.Random,
) -> str:
    v = lambda k: V(voice, k)
    c = companion.get("he_the") or "הלילה"
    keeps = [keepsake_for(e, t) for e, t in zip(events, tags_list)]
    return _clean_join(
        f"{name} {v('returned')} אל המיטה. על השידה נשארו {keeps[0]}, {keeps[1]}, ו{keeps[2]}.",
        f"{c} {CV(companion, 'extinguished')} את היום לאט. {name} {v('closed_eyes')} עיניים.",
        f"לילה טוב, {name}. לילה טוב לשבוע שהיה אמיתי.",
    )


def title_from_week(
    name: str,
    voice: Any,
    events: list[str],
    tags_list: list[list[str]],
    companion: dict[str, str],
    rng: random.Random,
) -> str:
    s = {t for ts in tags_list for t in ts}
    c = companion.get("he") or companion.get("he_the") or ""
    options = [
        f"השבוע של {name}",
        f"{name} והשבוע שהיה",
        f"{name} ו{c}" if c else f"ערב של {name}",
    ]
    if "tooth" in s and ("baking" in s or "grandparent" in s) and "fear_dark" in s:
        options.append(f"השן, העוגה והלילה של {name}")
        options.append(f"{name} והשבוע שהשתנה לאט")
    elif "tooth" in s:
        options.append(f"השן של {name}")
    elif "baking" in s or "grandparent" in s:
        options.append(f"העוגה של {name}")
    elif "bike" in s:
        options.append(f"{name} והאופניים")
    elif "water" in s:
        options.append(f"{name} והמים")
    elif "animal" in s:
        options.append(f"{name} והמפגש הרך")
    return rng.choice(options)


def _scene_key(kind: str, text: str, tags: list[str], theme_id: str) -> str:
    if kind == "bedtime_close":
        return "bedtime"
    if kind == "opening":
        return theme_id or "window"
    if kind in {"turning", "moral_landing"}:
        return theme_id or "blanket"
    priority = [
        ("tooth", "tooth"),
        ("baking", "kitchen"),
        ("grandparent", "kitchen"),
        ("fear_dark", "stars"),
        ("water", "water"),
        ("rain", "rain"),
        ("bike", "bike"),
        ("animal", "dog" if "כלב" in text else "cat" if "חתול" in text else "garden"),
        ("school", "school"),
        ("birthday", "party"),
        ("forest", "forest"),
        ("friend", "garden"),
        ("shabbat", "shabbat-table"),
        ("market", "neighborhood-market"),
        ("flowers", "garden"),
        ("drawing", "library-nook"),
        ("letter", "library-nook"),
        ("sleep", "bedtime"),
        ("treat", "garden"),
    ]
    for tag, scene in priority:
        if tag in tags:
            return scene
    return theme_id or "garden"


def compose_pages(
    name: str,
    voice: Any,
    age: int,
    events: list[str],
    companion: dict[str, str] | None = None,
    theme: dict[str, str] | None = None,
    rng: random.Random | None = None,
    template: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build 6–8 pages: opening, event scenes, bridge, turning, moral, close."""
    rng = rng or random.Random()
    companion = companion or {"id": "moon", "he": "הירח", "he_the": "הירח", "en": "a kind crescent moon"}
    events = list(events)[:3]
    while len(events) < 3:
        events.append("קרה דבר קטן")
    tags_list = [classify_event(e) for e in events]
    theme = theme or {}
    theme_id = theme.get("id") or "garden"

    moral_he, moral_id = moral_from_week(name, voice, events, tags_list)
    title = title_from_week(name, voice, events, tags_list, companion, rng)

    opening = _opening(name, voice, age, events, tags_list, companion, theme, rng, template=template)
    scenes = [
        scene_from_event(name, voice, age, events[i], i, companion=companion, rng=rng)
        for i in range(3)
    ]
    bridge = _bridge(name, voice, events[0], events[1], tags_list[0], tags_list[1], companion, rng)
    turning = _turning(name, voice, events, tags_list, companion, rng)
    landing = _moral_landing(name, voice, moral_he, companion, rng)
    close = _close(name, voice, events, tags_list, companion, rng)

    def pack(kind: str, text: str, event: str = "", tags: list[str] | None = None) -> dict[str, Any]:
        tags = tags or []
        scene_en = ""
        if kind.startswith("event") and event:
            scene_en = event_to_english(event, tags)
        elif kind == "opening":
            scene_en = (
                "a child at the start of evening with a kind companion, at home, "
                "about to tell this week's real moments, not a fantasy quest"
            )
            if theme.get("prompt"):
                scene_en += ", " + theme["prompt"]
        elif kind == "bridge":
            scene_en = (
                "a quiet in-between moment connecting two real weekly scenes, "
                f"{event_to_english(events[0], tags_list[0])}; then {event_to_english(events[1], tags_list[1])}"
            )
        elif kind == "turning":
            scene_en = (
                "a child realizing how three real weekly moments connect: "
                + "; ".join(event_to_english(e, t) for e, t in zip(events, tags_list))
            )
        elif kind == "moral_landing":
            scene_en = (
                "warm moral landing about this specific week, peaceful understanding, "
                "watercolor, the week's concrete objects nearby"
            )
        elif kind == "bedtime_close":
            scene_en = (
                "bedtime close, child in bed, nightlight glow, keepsakes from the week nearby: "
                + ", ".join(event_to_english(e, t) for e, t in zip(events, tags_list))
            )
        return {
            "t": text,
            "k": _scene_key(kind, text, tags, theme_id),
            "p": kind,
            "event": event,
            "scene_en": scene_en,
        }

    pages: list[dict[str, Any]] = [pack("opening", opening)]
    pages.append(pack("event_1", scenes[0], events[0], tags_list[0]))
    pages.append(pack("event_2", scenes[1], events[1], tags_list[1]))
    if age >= 5:
        pages.append(pack("bridge", bridge))
    pages.append(pack("event_3", scenes[2], events[2], tags_list[2]))
    if age <= 4:
        merged = _clean_join(turning, landing)
        pages.append(pack("moral_landing", merged))
    else:
        pages.append(pack("turning", turning))
        pages.append(pack("moral_landing", landing))
    pages.append(pack("bedtime_close", close))
    return {
        "title": title,
        "moral_he": moral_he,
        "moral_id": moral_id,
        "pages": pages,
        "tags_list": tags_list,
    }
