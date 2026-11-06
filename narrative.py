"""Plan a coherent Hebrew bedtime story before rendering its sentences.

A real bedtime frame connects three memories without inventing a causal order
for the parent's week. Facts, negation and unresolved problems survive the prose.
"""
from __future__ import annotations

from dataclasses import dataclass
import random
import re
from typing import Any


TAG_DEFS = {
    "tooth": ("שן", "שיניים"),
    "fear_dark": ("חושך", "חשכה", "חשוך", "מפחד", "פחדה", "פחדתי", "פחד"),
    "baking": ("אפתה", "אפיתי", "אפינו", "אפה", "הכין עוגה", "הכינה עוגה", "הכנתי עוגה", "הכין עוגיות", "ערבב בצק", "ערבבה בצק"),
    "grandparent": ("סבתא", "סבא", "סבתי", "סבי"),
    "friend": ("חבר", "חברה", "חברים", "חברות", "שיתף", "שיתפה", "שיתפתי", "שתף", "עזר", "עזרה", "עזרתי", "חיבק", "חיבקה", "אחותו", "אחותה"),
    "forgot": ("שכח", "שכחה", "שכחתי", "איבד", "איבדה", "איבדתי", "אבדה"),
    "skill": ("למד", "למדה", "למדתי", "תרגל", "תרגלה", "ניסה", "ניסתה", "ניסיתי", "הצליח", "הצליחה", "הצלחתי", "פעם ראשונה"),
    "school": ("בית ספר", "גננת", "כיתה", "מורה", "גן חובה", "שיעור", "בגן", "לגן"),
    "animal": ("כלב", "כלבלב", "כלבה", "חתול", "חתולה", "ארנב", "ציפור", "ציפורים", "סוס", "דג", "קיפוד"),
    "birthday": ("יום הולדת", "בלון", "בלונים", "מתנה"),
    "rain": ("גשם", "שלולית", "מטריה", "טיפות"),
    "water": ("בריכה", "ים", "מים", "שחה", "שחיתי", "שחייה", "גלים", "מקלחת"),
    "bike": ("אופניים", "גלגלי עזר", "רכיבה על אופניים"),
    "apology": ("סליחה", "ריב", "רבו", "רב עם", "רבה עם", "רבתי", "כעס", "כעסה", "מריבה", "התנצל", "התנצלה", "התפייס", "התפייסה", "השלים", "השלימה"),
    "treat": ("ארטיק", "גלידה", "שוקו", "שוקולד", "ממתק", "סוכריה", "עוגה", "עוגיות"),
    "sleep": ("לישון", "מיטה", "נרדם", "נרדמה", "ישן", "ישנה", "ישנתי", "פיג׳מה", "פיג'מה"),
    "drawing": ("צייר", "ציירה", "ציירתי", "ציור", "צבע", "צבעים"),
    "flowers": ("פרח", "פרחים", "גינה", "ליקטה", "ליקט"),
    "building": ("מגדל", "לגו", "בנה", "בנתה", "בניתי", "קוביות"),
    "letter": ("מכתב", "כתב", "כתבה", "כתבתי", "גלויה"),
    "forest": ("יער", "עצים", "חורשה"),
    "music": ("שיר", "שרה", "שרתי", "פסנתר", "חליל", "לנגן", "ניגנה", "ניגן", "ריקוד", "רקד", "רקדה"),
    "market": ("שוק", "קניות", "מכולת", "פירות"),
    "shabbat": ("שבת", "חלות", "נרות שבת", "קידוש"),
}
# Short words must not match suffixes (חברים→ים, ישן→שן, שוקולד→שוק).
PREFIXES = "ובכלמה"
HEBREW = r"א-ת"


def _normal(text: str) -> str:
    return re.sub(r"[\u0591-\u05c7]", "", str(text or "")).replace("־", " ")


def _contains(text: str, word: str) -> bool:
    return bool(re.search(r"(?<![א-ת])[" + PREFIXES + r"]{0,2}" + re.escape(word) + r"(?![א-ת])", text))


def classify_event(text: str) -> list[str]:
    raw = _normal(text)
    tags = [tag for tag, words in TAG_DEFS.items() if any(_contains(raw, word) for word in words)]
    return tags or ["everyday"]


def choose_flavor_theme(tags_list: list[list[str]], template_theme: str) -> str:
    """Choose a relevant memory illustration, never infer baking from a relative."""
    tags = {tag for event_tags in tags_list for tag in event_tags}
    choices = [("baking", "grandparent-kitchen"), ("fear_dark", "stars"), ("rain", "rainy-window"),
               ("water", "sea"), ("forest", "forest"), ("bike", "park"), ("school", "schoolyard"),
               ("drawing", "library-nook"), ("building", "library-nook"), ("letter", "library-nook"),
               ("shabbat", "shabbat-table"), ("animal", "park"), ("flowers", "garden")]
    return next((theme for tag, theme in choices if tag in tags), "library-nook")


def _g(voice: Any) -> str:
    return "f" if getattr(voice, "gender", voice) == "f" else "m"


def _v(voice: Any, masculine: str, feminine: str) -> str:
    return feminine if _g(voice) == "f" else masculine


CONFLICT = r"(?:רב(?:ה|תי|ו)? עם|מריבה|ריב|כעס(?:ה|תי)?|הציק|העליב|לא שיתף|לא שיתפה)"
REPAIR = r"(?:השלים|השלימה|השלמתי|התפייס|התפייסה|התפייסתי|התנצל|התנצלה|התנצלתי|ביקש סליחה|ביקשה סליחה|ביקשתי סליחה)"
FAILURE = r"(?:הפסיד|הפסידה|הפסדתי|לא הצליח|לא הצליחה|לא הצלחתי|נכשל|נכשלה|נפל|נפלה|נפלתי|התאכזב|התאכזבה)"
LOSS = r"(?<![א-ת])(?:נפטר|נפטרה|מת|מתה|באבל|געגוע|מתגעגע|מתגעגעת)(?![א-ת])"
FIRST_PERSON = r"^(?:אני\s+|[א-ת]+תי(?:\s|$)|[א-ת]+נו(?:\s|$))"


@dataclass(frozen=True)
class EventFact:
    raw: str
    tags: tuple[str, ...]
    focus: str
    unresolved: bool
    negated: bool
    first_person: bool
    symbol: str
    scene: str
    scene_en: str


SYMBOLS = {
    "tooth": "שן קטנה", "fear_dark": "מנורה קטנה", "baking": "קערה וכף", "grandparent": "חלון של בית",
    "friend": "שתי ידיים", "conflict": "שני כיסאות רחוקים", "repair": "שני כיסאות קרובים",
    "failure": "שביל עם עיקול", "grief": "לב קטן", "forgot": "סימן שאלה", "skill": "מדרגות קטנות",
    "school": "תיק", "animal": "טביעת כף", "birthday": "בלון", "rain": "טיפת גשם", "water": "גל קטן",
    "bike": "גלגל", "apology": "שתי ידיים", "treat": "כוכב קטן", "sleep": "כרית", "drawing": "עיפרון",
    "flowers": "פרח", "building": "שלוש קוביות", "letter": "מעטפה", "forest": "עלה", "music": "תו",
    "market": "סל", "shabbat": "נר", "everyday": "עיגול צבעוני", "negated": "סימן שאלה", "confidence": "כוכב קטן",
}
SCENES = {
    "tooth": ("tooth", "a child remembering a lost baby tooth, small tooth in a palm"),
    "fear_dark": ("stars", "a child in a cozy bedroom with a small night light, dark sky outside"),
    "baking": ("kitchen", "a child baking in a kitchen, bowl, spoon, cake in an oven"),
    "grandparent": ("window", "a child remembering a grandparent, warm home, no assumed baking"),
    "friend": ("garden", "a child recalling a kind moment with another person"),
    "conflict": ("garden", "two children with space between them after a disagreement, calm not violent"),
    "repair": ("garden", "children listening to each other and making up after a disagreement"),
    "failure": ("library-nook", "a child reflecting on a difficult attempt, thoughtful, no assumed victory"),
    "grief": ("window", "a child drawing a small heart in a quiet room, gentle space for sadness"),
    "forgot": ("library-nook", "a child drawing a question mark in a memory book, no magically recovered object"),
    "skill": ("library-nook", "a child remembering practice, concentration and small steps"),
    "school": ("school", "a child recalling kindergarten or a classroom"),
    "animal": ("garden", "a child recalling an animal from the week"),
    "birthday": ("party", "a small birthday memory, paper balloon drawing"),
    "rain": ("rain", "rain outside a window and a child drawing a droplet"),
    "water": ("water", "a calm water memory, shoreline or pool, safe scene"),
    "bike": ("bike", "a bicycle memory on a safe path, helmet, no assumed fall"),
    "treat": ("garden", "a child recalling a small sweet treat"),
    "sleep": ("bedtime", "a quiet bedtime memory with a familiar blanket"),
    "drawing": ("library-nook", "a child drawing at a table with pencils"),
    "flowers": ("garden", "a child noticing a flower in a garden"),
    "building": ("library-nook", "a child recalling building a block tower, no assumed collapse"),
    "letter": ("library-nook", "a child with a letter or envelope and a pencil"),
    "forest": ("forest", "a child remembering trees on a forest walk"),
    "music": ("library-nook", "a child recalling music and drawing a note"),
    "market": ("neighborhood-market", "a family shopping memory, fruit stalls"),
    "shabbat": ("shabbat-table", "a quiet Shabbat table memory with candles"),
    "everyday": ("library-nook", "a child reflecting on a weekly memory and drawing in a book"),
    "negated": ("library-nook", "a child reflecting on something that did not happen, no invented success"),
    "confidence": ("bedtime", "a child calmly remembering a moment of confidence, not afraid"),
}


def extract_fact(raw: str) -> EventFact:
    text = _normal(raw)
    tags = tuple(classify_event(text))
    negated = bool(re.search(r"(?<![א-ת])לא(?![א-ת])", text))
    # The final stated outcome wins; local negation must not reverse a fact.
    outcomes = []
    for kind, pattern in (("repair", REPAIR), ("conflict", CONFLICT), ("failure", FAILURE),
                          ("confidence", r"(?:ניצח|ניצחה|הצליח|הצליחה)")):
        for match in re.finditer(r"(?<![א-ת])(?:ו)?" + pattern + r"(?![א-ת])", text):
            before = text[max(0, match.start()-12):match.start()]
            if re.search(r"(?:לא|כמעט)\s*$", before):
                outcomes.append((match.start(), "failure" if kind == "confidence" and re.search(r"לא\s*$", before) else "negated"))
            else:
                outcomes.append((match.start(), kind))
    last_outcome = max(outcomes, default=(-1, ""))[1]
    repair = last_outcome == "repair"
    conflict = last_outcome == "conflict" or (last_outcome == "negated" and bool(re.search(r"לא (?:השלים|השלימה|התפייס|התפייסה)(?![א-ת])", text)))
    failure = last_outcome == "failure"
    grief = bool(re.search(LOSS, text))
    if grief:
        focus = "grief"
    elif repair:
        focus = "repair"
    elif conflict:
        focus = "conflict"
    elif failure:
        focus = "failure"
    elif last_outcome == "confidence" or (negated and re.search(r"לא (?:פחד|פחדה|פחדתי|נפל|נפלה|נפלתי)(?![א-ת])", text)):
        focus = "confidence"
    elif negated or last_outcome == "negated":
        # Do not turn 'did not swim' into a swimming scene or 'did not fear' into fear.
        focus = "negated"
    else:
        priority = ("tooth", "baking", "fear_dark", "bike", "water", "letter", "music", "building", "drawing",
                    "forest", "animal", "birthday", "rain", "school", "sleep", "friend", "grandparent",
                    "flowers", "market", "shabbat", "treat", "forgot", "skill", "everyday")
        focus = next((tag for tag in priority if tag in tags), "everyday")
    scene, english = SCENES[focus]
    if focus == "animal":
        scene = "dog" if "כלב" in text else "cat" if "חתול" in text else "garden"
    if focus == "letter" and "סבא" in text:
        english += ", a letter to grandfather"
    if focus == "grandparent":
        english += ", grandfather" if "סבא" in text and "סבתא" not in text else ", grandmother" if "סבתא" in text else ""
    return EventFact(raw.strip(), tags, focus, conflict or failure or grief or focus == "forgot",
                     negated, bool(re.search(FIRST_PERSON, text)), SYMBOLS[focus], scene, english)


@dataclass(frozen=True)
class StoryPlan:
    arc: str
    question: str
    decision: str
    moral: str
    facts: tuple[EventFact, ...]
    palette: tuple[str, str, str]
    title: str


def plan_story(name: str, voice: Any, facts: tuple[EventFact, ...], rng: random.Random) -> StoryPlan:
    focuses = {fact.focus for fact in facts}
    all_tags = {tag for fact in facts for tag in fact.tags}
    female = _g(voice) == "f"
    if any(f.focus == "conflict" and any(later.focus == "repair" for later in facts[i+1:]) for i, f in enumerate(facts)) and facts[-1].focus != "conflict":
        arc = "repair"
        question = "איך מציירים שבוע שהיה בו גם ריב?"
        decision = "גם הריב וגם ההתקרבות יישארו בספר. אפשר לזכור את שניהם."
        moral = "כשיש ריב, אפשר להקשיב, לבקש סליחה ולנסות להתקרב שוב."
        titles = (f"{name} ומקום לשנינו", f"{name} והעמוד שחיבר")
    elif "grief" in focuses:
        arc = "room-for-feelings"
        question = "איפה שמים בספר רגע שקשה להיזכר בו?"
        decision = "העמוד הזה יישאר ליד האחרים. לא צריך להפוך אותו לשמח."
        moral = "גם לרגע עצוב יש מקום. אפשר להיות איתו יחד."
        titles = (f"{name} ולב קטן על הדף", f"הספר השקט של {name}")
    elif "fear_dark" in focuses and ("tooth" in focuses or "skill" in all_tags):
        arc = "growing-and-asking"
        question = "אם אני כבר גדלה, למה לפעמים אני עוד מפחדת?" if female else "אם אני כבר גדל, למה לפעמים אני עוד מפחד?"
        decision = "אפשר לגדול, ואפשר גם לבקש אור קטן. שני הדברים ייכנסו לאותו ספר."
        moral = "אפשר לגדול, לקחת זמן ולבקש עזרה. לא צריך לעשות הכול לבד."
        titles = (f"{name} והאור הקטן", f"{name} וספר של אומץ קטן")
    elif "failure" in focuses or any("skill" in fact.tags and not fact.negated for fact in facts):
        arc = "effort"
        question = "האם לשמור רק את הרגעים שבהם הכול הצליח?"
        decision = "גם הניסיון ייכנס לספר. הוא חלק מהדרך, אפילו כשהתוצאה עוד לא מוכנה."
        moral = ("גם ניסיון שלא הצליח שייך לדרך. מותר לנוח ולנסות שוב." if "failure" in focuses
                 else "כשלומדים משהו חדש, מותר לקחת זמן, לנוח ולבקש עזרה.")
        titles = (f"{name} ועוד צעד קטן", f"{name} והעמוד שלא דילגנו עליו")
    elif any(fact.unresolved for fact in facts):
        arc = "unfinished"
        question = "מה עושים עם רגע שלא נגמר כמו שרציתי?"
        decision = "גם לרגע הזה יש מקום. לא חייבים להמציא לו סוף כדי לשמור אותו."
        moral = "מותר להשאיר שאלה פתוחה ולבקש עזרה. לא הכול צריך להיפתר הערב."
        titles = (f"{name} והעמוד שעוד נשאר", f"שלושה רגעים של {name}")
    elif "grandparent" in all_tags or "letter" in focuses:
        arc = "connection"
        question = "איך שומרים קרוב רגע שכבר נגמר?"
        decision = "לא צריך להחזיר את היום. ציור קטן יכול להזכיר עם מי הייתי ומה היה חשוב לי."
        moral = "כשמספרים על רגע משותף, נותנים לו מקום להישאר קרוב."
        titles = (f"{name} ורגע שנשאר קרוב", f"{name} והספר שאוסף חיבורים")
    else:
        arc = "whole-week"
        question = "באיזה רגע כדאי להתחיל את הספר שלי?"
        decision = "אתחיל ברגע הראשון שעולה לי, ואשאיר מקום גם לאחרים. לא צריך לבחור רק אחד."
        moral = "לפעמים דברים קטנים ושונים מצטרפים לזיכרון גדול אחד."
        titles = (f"{name} והצבעים של השבוע", f"הספר הקטן של {name}", f"{name} ושלושת הציורים")
    palette = rng.choice((("כחול", "כתום", "ירוק"), ("סגול", "צהוב", "כחול"), ("ירוק", "אדום", "זהוב")))
    return StoryPlan(arc, question, decision, moral, facts, palette, rng.choice(titles))


def _memory_clause(name: str, voice: Any, fact: EventFact) -> str:
    raw = fact.raw.rstrip(".!?…")
    if raw.startswith(name + " "):
        return f"{name} {_v(voice, 'נזכר', 'נזכרה')} ברגע: ״{raw}״."
    if fact.first_person:
        return f"המשפט ״{raw}״ חזר אל {name}, יחד עם הזיכרון."
    # Common finite third-person clauses fit naturally after 'how'.
    first = raw.split()[0] if raw.split() else ""
    if re.match(r"^(?:איבד|אפת|אפה|פחד|רכב|רכבה|אכל|פגש|בנה|בנתה|שחה|ישן|ישנה|צייר|רא[הת]|שמע|כתב|ליקט|שתף|שיתף|חיבק|למד|ניס|הצליח|הפסיד|השלימ|השלים|התפייס|התנצל|עזר|ביקר|היה|הייתה|שיחק|טייל|רב|רבה|שר|רקד|קיבל|קיבלה|לא$)", first):
        return f"{name} {_v(voice, 'נזכר', 'נזכרה')} איך {raw}."
    return f"בזיכרון הבא של {name} היו המילים ״{raw}״."


def _scene_detail(name: str, voice: Any, fact: EventFact, rng: random.Random, short: bool) -> str:
    """Fictional sensory texture stays consistent with the supplied outcome."""
    details = {
        "conflict": "בזיכרון נשאר מרחק בין שניים. גם עכשיו היד היססה לפני שנגעה בדף. ליד הציור נשאר קצת מקום ריק.",
        "repair": "המרחק שבין השניים התחיל להצטמצם. הפעם היה בזיכרון מקום למילים אחרות, וגם לאוזן שמקשיבה.",
        "failure": "הייתה שם אכזבה. העיפרון התגלגל לרגע על השולחן ונעצר; אפשר היה לאסוף אותו ולהמשיך בקצב אחר.",
        "grief": "העיפרון נעצר. ליד הלב הקטן נשאר מקום לבן. החדר היה שקט, ולא היה צורך למהר למלא אותו.",
        "negated": "לרגע הזה היה מקום משלו בין דפי הספר. העיפרון חיכה, בלי למהר לשנות את מה שהיה.",
        "confidence": "מן הזיכרון חזרה תחושה שקטה של אומץ. זה היה רגע קטן, אבל היה נעים לשמור אותו.",
        "forgot": "בזיכרון נשארה שאלה בלי תשובה. על הדף אפשר היה להשאיר לה פינה, ולחשוב מחר ממי כדאי לבקש עזרה.",
        "tooth": "הלשון חיפשה את המקום החדש בפה. השן כבר לא הייתה שם, אבל החיוך עוד היה אותו חיוך, רק קצת אחר.",
        "fear_dark": "בזיכרון היה חושך. בחדר עכשיו דלקה מנורה קטנה; האור שלה הגיע עד קצה השמיכה.",
        "baking": "הכף הסתובבה בקערה, ובסוף הגיע תורו של התנור. הריח המתוק עוד לא היה מוכן; היה צריך לחכות לו קצת.",
        "grandparent": "קול מוכר חזר מתוך הזיכרון, ואיתו תחושה של זמן יחד. הדף הריק הרגיש פתאום קצת פחות ריק.",
        "friend": "בתוך הרגע הזה היה עוד מישהו. הזיכרון נעשה רחב יותר כשנשאר בו מקום לשניים.",
        "skill": "דבר חדש דרש תשומת לב. היו בו תנועות שעוד לא נעשו מעצמן, ורצון לגלות איך הן מתחברות.",
        "school": "יום שלם עבר מאז, עם הרבה קולות ופרטים. דווקא הרגע הזה חזר עכשיו, ברור וקטן, אל החדר השקט.",
        "animal": "בדמיון הופיעה שוב החיה מן הזיכרון. קו קטן על הדף נעשה טביעת כף, ופתאום היה נדמה שהיא ממש קרובה.",
        "birthday": "משהו מן ההתרגשות חזר לרגע. העיפרון הקיף עיגול באוויר, כאילו הוא מחזיק חוט של בלון.",
        "rain": "הטיפות שבזיכרון נשמעו כמעט כמו נקישות על החלון. בחדר היה עכשיו יבש ושקט, והקצב הקטן נשאר בראש.",
        "water": "הזיכרון החזיר איתו תנועה של מים. העיפרון נע על הדף בקו עולה ויורד, כמו גל שמגיע לחוף.",
        "bike": "שני עיגולים על הדף הזכירו גלגלים. פתאום היה אפשר כמעט להרגיש שוב את הדרך מתחתם ואת האוויר בדרך.",
        "treat": "הטעם חזר לזיכרון לרגע, כמעט ממש. חיוך קטן הספיק כדי לשמור ממנו משהו, גם כשהמתוק עצמו כבר נגמר.",
        "sleep": "כרית ושמיכה הופיעו בזיכרון. עכשיו אפשר היה להרגיש גם את השמיכה שכאן, ואת המיטה שמחכה לסוף הספר.",
        "drawing": "צבע וקו חזרו מן הזיכרון אל היד. על הדף החדש קו אחד התעקם קצת, ודווקא הוא נעשה מעניין.",
        "flowers": "פרט קטן מן הגינה חזר במחשבה. על הדף נפתח מקום לפרח, והצבע שלו האיר את הפינה הלבנה.",
        "building": "קובייה ליד קובייה, והזיכרון קיבל צורה. על הדף אפשר היה לראות שוב איך דברים קטנים נעשו יחד משהו גדול יותר.",
        "letter": "מילים על נייר יכלו לחצות מרחק. כשהעיפרון נגע בדף, היה נעים לחשוב על מי שנמצא בצד השני של המכתב.",
        "forest": "העצים נפרשו שוב בזיכרון. לרגע היה אפשר כמעט לשמוע רשרוש של עלים בתוך החדר השקט.",
        "music": "צליל מן הזיכרון נשאר בראש עוד קצת. היד התנועעה איתו, ונתנה לקצב פינה קטנה על הדף.",
        "market": "צבעים וקולות חזרו מן הדרך. פרט קטן אחד מהם עצר עכשיו, כאילו חיכה לתורו להיכנס לספר.",
        "shabbat": "האור של אותו ערב חזר אל הזיכרון. קו בצבע זהוב הספיק כדי לתת לו פינה חמה על הדף.",
        "everyday": "היה שם פרט שרק הזיכרון הזה ידע לשמור. העיפרון חיכה רגע, ואז הניח על הדף סימן קטן בצבע.",
    }
    detail = details.get(fact.focus, details["everyday"])
    return detail.split(". ")[0].rstrip(".") + "." if short else detail


def _bridge(plan: StoryPlan, name: str, voice: Any) -> str:
    first, second, _ = plan.facts
    if plan.arc == "growing-and-asking":
        return f"{name} {_v(voice, 'הסתכל', 'הסתכלה')} בשני הציורים. כבר היו בספר שני רגעים, אבל השאלה מהדף הראשון עוד לא נענתה. אולי הציור הבא יעזור להסתכל עליה אחרת."
    if plan.arc == "repair":
        return "הספר עוד לא היה גמור. לשני הרגעים כבר היה מקום, וגם לרגע הבא נשאר דף. כשהדפים יהיו יחד, אפשר יהיה להביט בהם שוב."
    if plan.arc == "effort":
        return "שני הציורים נשארו זה לצד זה. אף אחד מהם לא היה מבחן, ולא היה צריך להוסיף להם ציון. נשאר עוד עמוד אחד."
    if first.focus == second.focus:
        return "שני הציורים עסקו בדברים דומים, אבל הזיכרונות לא היו אותו זיכרון. לכל אחד נשאר דף משלו. עכשיו הגיע תורו של הרגע השלישי."
    return f"בעמוד אחד היה ציור של {first.symbol}, ובשני ציור של {second.symbol}. {name} {_v(voice, 'השאיר', 'השאירה')} מקום ביניהם. לא הכול היה צריך להיראות אותו דבר כדי להיות באותו ספר."


def _validate_render(plan: StoryPlan, pages: list[dict], age: int) -> list[str]:
    """Guardrails are backed by facts and page roles, not a self-awarded score."""
    problems = []
    kinds = [page["p"] for page in pages]
    if not 6 <= len(pages) <= 8:
        problems.append("page-count")
    if len({page["t"] for page in pages}) != len(pages):
        problems.append("duplicate-pages")
    for i, fact in enumerate(plan.facts, 1):
        scene = next((page for page in pages if page["p"] == f"event_{i}"), None)
        if scene is None or fact.raw.rstrip(".!?…") not in scene["t"]:
            problems.append(f"missing-event-{i}")
    if kinds[0] != "opening" or kinds[-1] != "bedtime_close":
        problems.append("frame-order")
    maximum = 75 if age <= 4 else 100
    if any(len(page["t"].split()) > maximum for page in pages):
        problems.append("page-too-long")
    if plan.moral not in " ".join(page["t"] for page in pages):
        problems.append("missing-resolution")
    return problems


def compose_pages(name: str, voice: Any, age: int, events: list[str], companion: dict | None = None,
                  theme: dict | None = None, rng: random.Random | None = None, template: dict | None = None) -> dict:
    rng = rng or random.Random()
    facts = tuple(extract_fact(event) for event in events)
    if len(facts) != 3:
        raise ValueError("exactly three memories are required")
    plan = plan_story(name, voice, facts, rng)
    short = age <= 4
    he = "היא" if _g(voice) == "f" else "הוא"
    said = _v(voice, "אמר", "אמרה")
    drew = _v(voice, "צייר", "ציירה")
    looked = _v(voice, "הסתכל", "הסתכלה")
    remembered = _v(voice, "נזכר", "נזכרה")
    age_words = f"בת ה־{age}" if _g(voice) == "f" else f"בן ה־{age}"
    book_cover = (companion or {}).get("he") or "ירח"
    opening = (f"לפני השינה {name} {age_words} {_v(voice, 'פתח', 'פתחה')} ספר קטן עם שלושה דפים ריקים. "
               f"על הכריכה היה ציור של {book_cover}. לידו חיכו שלושה צבעים. "
               f"״{plan.question}״, {said} {name}. הדף הראשון נשאר פתוח.")
    def pack(kind, text, fact=None, scene="library-nook"):
        return {"p":kind,"t":text,"k":fact.scene if fact else scene,
                "event":fact.raw if fact else "", "scene_en":fact.scene_en if fact else "a child in a cozy bedroom making a small three-page memory book, paper and colored pencils"}
    pages = [pack("opening", opening, scene="bedtime")]
    for i, fact in enumerate(facts):
        detail = _scene_detail(name, voice, fact, rng, short)
        action = f"בצבע {plan.palette[i]} {drew} {name} {fact.symbol} על הדף."
        if i == 0:
            action += " זה היה הציור הראשון בספר."
        elif i == 1 and not short:
            action += " הדף החדש נשאר ליד הראשון."
        elif i == 2:
            action += " עכשיו היו בספר שלושה ציורים."
        text = " ".join((_memory_clause(name, voice, fact), detail, action))
        pages.append(pack(f"event_{i+1}", text, fact))
        if i == 1 and not short:
            pages.append(pack("bridge", _bridge(plan, name, voice)))
    symbols = ", ".join(fact.symbol for fact in facts[:2]) + " ו" + facts[2].symbol
    if plan.arc == "repair":
        turning = f"{name} {looked} שוב בספר. הריב לא נמחק, אבל גם הרגע של ההתקרבות נשאר. הציורים סיפרו לא רק מה קרה, אלא מה השתנה בדרך."
    elif plan.arc == "growing-and-asking":
        meanings = {"tooth":"הגוף משתנה", "baking":"אפייה צריכה זמן", "fear_dark":"בחושך מותר לבקש אור קטן", "skill":"דבר חדש צריך תרגול"}
        insight = ", ".join(dict.fromkeys(meanings[f.focus] for f in facts if f.focus in meanings))
        turning = f"{name} {looked} בשלושת הציורים — {symbols}. {insight}. פתאום השאלה מהדף הראשון הרגישה פחות קשה."
    elif plan.arc == "effort":
        turning = f"{name} {looked} בציורים והוסיף קו קטן ביניהם." if _g(voice) == "m" else f"{name} {looked} בציורים והוסיפה קו קטן ביניהם."
        turning += " הקו לא קיצר את הדרך ולא שינה את מה שקרה. הוא רק הזכיר שאפשר להמשיך מרגע אחד לרגע הבא, עם מה שכבר למדנו."
    elif plan.arc == "connection":
        turning = f"{name} {looked} בשלושת הציורים — {symbols}."
        turning += " ליד הציורים נשאר מקום לשמות של מי שהיו שם. עכשיו הספר שמר גם את הרגעים וגם את האנשים שבתוכם."
    elif plan.arc == "unfinished":
        turning = f"{name} {looked} שוב בציורים. היו דברים נעימים ודברים שעוד נשארו פתוחים. הספר לא תיקן אותם, אבל עזר לזכור שאפשר לספר גם עליהם."
    else:
        turning = f"{name} {looked} בשלושת הציורים — {symbols}. כל אחד הזכיר רגע אחר. הם לא התחלפו זה בזה, ויחד כבר היה להם מקום בתוך אותו ספר."
    landing = f"״{plan.decision}״, {said} {name}. {plan.moral}"
    if short:
        # Younger listeners get a single, short choice rather than two abstract explanation pages.
        pages.append(pack("moral_landing", f"{name} {looked} בשלושת הציורים. {plan.moral}"))
    else:
        pages.append(pack("turning", turning))
        pages.append(pack("moral_landing", landing))
    close = (f"{name} {_v(voice, 'סגר', 'סגרה')} את הספר {_v(voice, 'והניח', 'והניחה')} אותו על השידה. "
             f"הצבעים חזרו לקופסה, והשמיכה עלתה עד הכתפיים. "
             f"למחר נשארו דפים חדשים; לעכשיו היה מספיק. לילה טוב, {name}.")
    pages.append(pack("bedtime_close", close, scene="bedtime"))
    issues = _validate_render(plan, pages, age)
    if issues:
        raise RuntimeError("invalid narrative: " + ", ".join(issues))
    return {"title":plan.title,"moral_he":plan.moral,"moral_id":plan.arc,"pages":pages,
            "tags_list":[list(fact.tags) for fact in facts],
            "plan":{"arc":plan.arc,"question":plan.question,"event_focuses":[fact.focus for fact in facts],
                    "unresolved_events":[i for i,fact in enumerate(facts) if fact.unresolved],"checks":issues}}
