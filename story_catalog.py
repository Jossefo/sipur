"""Building blocks for 270+ Hebrew bedtime-story templates.

Used both to write data/templates.json and to synthesize new variants at runtime.
"""

from __future__ import annotations

from typing import Any


THEMES: list[dict[str, str]] = [
    {
        "id": "forest",
        "he": "היער",
        "place": "בין העצים הרכים",
        "in_place": "ביער הקטן",
        "air": "ריח של אדמה לחה ועלים",
        "light": "אור ירוק־זהוב בין הגזעים",
        "prompt": "a gentle forest at dusk, soft moss, tall friendly trees, warm lantern light among leaves",
    },
    {
        "id": "sea",
        "he": "הים",
        "place": "על החול הקר ליד המים",
        "in_place": "על שפת הים השקטה",
        "air": "רוח מלוחה ועדינה",
        "light": "אור כסוף על הגלים הקטנים",
        "prompt": "a calm sea shore at evening, gentle small waves, warm sand, a child-safe quiet beach",
    },
    {
        "id": "city-balcony",
        "he": "המרפסת",
        "place": "על המרפסת מעל הרחוב",
        "in_place": "על מרפסת העיר",
        "air": "ריח ארוחת ערב מהחלונות",
        "light": "אורות קטנים בבתים ממול",
        "prompt": "a cozy city balcony at dusk, potted plants, warm window lights across the street, quiet rooftops",
    },
    {
        "id": "grandparent-kitchen",
        "he": "המטבח של סבא וסבתא",
        "place": "ליד שולחן העץ במטבח",
        "in_place": "במטבח החם של סבא וסבתא",
        "air": "ריח עוגה וקינמון",
        "light": "אור צהוב מנורת התקרה",
        "prompt": "a warm grandparent kitchen, wooden table, mixing bowl, golden indoor light, cozy and safe",
    },
    {
        "id": "schoolyard",
        "he": "חצר הגן",
        "place": "ליד הנדנדה בחצר",
        "in_place": "בחצר הגן אחרי היום",
        "air": "ריח דשא וחול רך",
        "light": "שמש אחרונה על הקיר",
        "prompt": "a gentle kindergarten yard at late afternoon, swing, sandbox, warm low sun, peaceful children play area",
    },
    {
        "id": "desert",
        "he": "המדבר",
        "place": "על גבעה קטנה של חול זהוב",
        "in_place": "במדבר הרך לקראת ערב",
        "air": "אוויר יבש ושקט",
        "light": "זהב ארוך על החול",
        "prompt": "a soft desert at sunset, golden dunes, wide calm sky, warm safe light, no danger",
    },
    {
        "id": "rainy-window",
        "he": "החלון הגשום",
        "place": "על אדן החלון מול הגשם",
        "in_place": "ליד החלון הגשום",
        "air": "ריח גשם על האדמה",
        "light": "טיפות כסופות על הזכוכית",
        "prompt": "a rainy window indoors, droplets on glass, warm room light, a child watching rain safely from inside",
    },
    {
        "id": "shabbat-table",
        "he": "שולחן השבת",
        "place": "ליד המפה הלבנה",
        "in_place": "ליד שולחן השבת",
        "air": "ריח חלות ונרות",
        "light": "אור נרות שבת רך",
        "prompt": "a peaceful Shabbat table, white cloth, two candles, challah, warm indoor glow, family calm",
    },
    {
        "id": "park",
        "he": "הפארק",
        "place": "על ספסל מתחת לעץ",
        "in_place": "בפארק לעת ערב",
        "air": "ריח דשא גזום",
        "light": "אור זהוב בין הענפים",
        "prompt": "a quiet city park at evening, wooden bench, trees, warm path lights, peaceful playground in distance",
    },
    {
        "id": "stars",
        "he": "הכוכבים",
        "place": "על הגג או על השמיכה בחצר",
        "in_place": "תחת שמי הכוכבים",
        "air": "אוויר קריר ונקי",
        "light": "נקודות אור רחוקות ורכות",
        "prompt": "a child-safe starry night, warm blanket outdoors, gentle moon, sparkling stars, watercolor sky",
    },
    {
        "id": "garden",
        "he": "הגינה",
        "place": "בין הערוגות הקטנות",
        "in_place": "בגינה מאחורי הבית",
        "air": "ריח עגבניות ועלים",
        "light": "אור שקיעה על העלים",
        "prompt": "a small backyard garden, vegetable beds, flowers, watering can, warm sunset light",
    },
    {
        "id": "library-nook",
        "he": "פינת הספרים",
        "place": "בין המדפים הנמוכים",
        "in_place": "בפינת הספרים השקטה",
        "air": "ריח נייר ודפים",
        "light": "אור מנורה קטנה על כריכות",
        "prompt": "a cozy children's library nook, low bookshelves, cushions, warm lamp, quiet and inviting",
    },
    {
        "id": "neighborhood-market",
        "he": "השוק הקטן",
        "place": "ליד דוכן הפירות",
        "in_place": "בשוק השכונתי",
        "air": "ריח תפוזים ולחם",
        "light": "אור אחרי הצהריים על הארגזים",
        "prompt": "a small friendly neighborhood market, fruit crates, bread, warm afternoon light, kind vendors",
    },
    {
        "id": "orchard",
        "he": "הפרדס",
        "place": "בין עצי הפרי",
        "in_place": "בפרדס השקט",
        "air": "ריח תפוזים ופריחה",
        "light": "אור מנוקד דרך העלים",
        "prompt": "a gentle fruit orchard, orange trees, speckled sunlight, a quiet path, child-safe countryside",
    },
    {
        "id": "riverbank",
        "he": "גדת הנחל",
        "place": "על האבנים החלקות",
        "in_place": "ליד הנחל הרדוד",
        "air": "ריח מים ומנטות בר",
        "light": "נצנוץ על המים הרדודים",
        "prompt": "a shallow gentle riverbank, smooth stones, clear water, reeds, warm late light, perfectly safe",
    },
    {
        "id": "mountain-path",
        "he": "שביל ההר",
        "place": "על שביל האבן הצר",
        "in_place": "על שביל בהר הנמוך",
        "air": "אוויר גבוה וצלול",
        "light": "אור רחב על העמק",
        "prompt": "a gentle low mountain path, stones, wildflowers, wide calm view, warm evening light, child-safe hike",
    },
    {
        "id": "bakery",
        "he": "המאפייה",
        "place": "מול הוויטרינה החמה",
        "in_place": "במאפייה הקטנה",
        "air": "ריח לחם ושוקולד",
        "light": "אור זהוב מהתנור",
        "prompt": "a small neighborhood bakery, bread on shelves, warm oven glow, glass case, cozy and kind",
    },
    {
        "id": "rooftop-evening",
        "he": "גג הבניין",
        "place": "על הגג בין עציצים",
        "in_place": "על גג הבניין לעת ערב",
        "air": "רוח קלה מעל הרחובות",
        "light": "שמיים כתומים מעל העיר",
        "prompt": "a safe building rooftop garden at evening, potted plants, city skyline far away, warm orange sky",
    },
]


FORMATS: list[dict[str, Any]] = [
    {
        "id": "quest",
        "flavor": "a child on a tiny gentle quest along a path, collecting three small moments",
        "titles": [
            "{name} והמסע {in_place}",
            "השביל הקטן של {name}",
            "{name} הולך{sf} אחרי אור",
        ],
        "opening": [
            "בערב הרך הגיע {companion} אל {name} {age_phrase}. {in_place} חיכה שביל קטן. {air}. {name} לקח{sf} נשימה ואמר{sf}: נלך לאט, בלי לרוץ.",
            "{name} {age_phrase} עמד{sf} {place}. {light}. {companion} הגיש מפה מקומטת מחיוך: הערב נאסוף את השבוע, צעד אחרי צעד.",
            "{in_place} נפתח מסע בגובה ילד. {name} {age_phrase} אחז{sf} ביד של {companion}, ו{air} אמר שהדרך כבר מתחילה.",
        ],
        "event_1": [
            "בתחנה הראשונה קרה דבר אמיתי: {event}. {name} עצר{sf}. {companion} אמר: גם זה חלק מהדרך, לא שוליים.",
            "הצעד הראשון היה בדיוק זה: {event}. {name} שם{sf} את הרגע בכיס כמו אבן חלקה.",
            "על המפה הופיע סימן ראשון. שם {event}. {name} {age_phrase} הנהן{sf}, כי הרגיש{sf} את המשקל הקל.",
        ],
        "event_2": [
            "השביל התעקל {place}. שם {event}. {name} שם{sf} יד על הלב והמשיך{sf} בעדינות.",
            "באמצע הדרך, בין {light} לבין הנשימה: {event}. {name} לא דילג{sf}. {name} הסתכל{sf}.",
            "{companion} לחץ בעדינות: כאן. {event}. {name} שמר{sf} את זה ליד הצעד הקודם.",
        ],
        "event_3": [
            "לפני סוף המסע הקטן: {event}. {name} הבין{sf} שהשבוע הלך יחד אית{op}, לא מאחור.",
            "התחנה השלישית הייתה שקטה וברורה: {event}. {name} {age_phrase} חייך{sf} אל {companion}.",
            "ואז, כמעט בסוף השביל, {event}. שלושה צעדים כבר היו ביד.",
        ],
        "turning": [
            "שלושה צעדים ישבו עכשיו על המפה. {name} לא חיפש{sf} אוצר. האוצר כבר היה בידיים.",
            "{name} עצר{sf} {place}. {light}. המסע לא ביקש להיות גדול. הוא ביקש להיות אמיתי.",
            "השביל התקפל לגודל של כף יד. {name} ראה{sf} איך שלושת הרגעים מחזיקים זה את זה.",
        ],
        "moral": [
            "ו{name} גילה{sf} משהו רך, בלי שמישהו דרש: {moral_he} כך נראה אור קטן בסוף שביל.",
            "{companion} לא נתן שיעור. רק לחש: {moral_he} {name} הנהן{sf}, כי זה כבר היה בלב.",
            "המפה נסגרה. נשאר משפט אחד חם: {moral_he} {name} {age_phrase} לקח{sf} אותו אל הכיס.",
        ],
        "close": [
            "{companion} קיפל את המפה. {name} חזר{sf} אל המיטה, והשביל נשאר מאחור כמו חיוך. לילה טוב, {name}.",
            "המסע נגמר בגובה כרית. {name} {age_phrase} עצם{sf} עיניים. {companion} שמר על השביל עד הבוקר. לילה טוב.",
            "אין צורך לרוץ מחר. {name} מניח{sf} את שלושת הצעדים ליד המים. לילה טוב, {name}. לילה טוב, שביל קטן.",
        ],
    },
    {
        "id": "quiet-evening",
        "flavor": "a quiet evening indoors, child and companion sitting still, listening to the week",
        "titles": [
            "ערב שקט ל{name}",
            "{name} והלילה שלא מיהר",
            "השעה הרכה של {name}",
        ],
        "opening": [
            "הבית דיבר בלחש. {name} {age_phrase} ישב{sf} {place}. {air}. {companion} בא בלי לדפוק, כי ערבים כאלה פתוחים.",
            "{light}. {name} לבש{sf} פיג׳מה. {in_place} הזמן התארך כמו שמיכה, ו{companion} התיישב קרוב.",
            "לא היה צריך הרפתקה. ל{name} {age_phrase} היה ערב. {in_place} {companion} אמר: נשמע את השבוע לאט.",
        ],
        "event_1": [
            "הלחישה הראשונה הייתה: {event}. {name} שמע{sf} אותה כמו פעמון רחוק ורך.",
            "מן השבוע עלה דבר ראשון: {event}. {name} לא דחק{sf} אותו. נתן{sf} לו כיסא.",
            "{companion} שאל בקול נוצה, ו{name} ענה{sf}: {event}. המילים התיישבו {place}.",
        ],
        "event_2": [
            "אחר כך, בלי להרים את הקול: {event}. {name} הנהן{sf}. גם זה שייך לערב.",
            "בין כוס המים לחלון קרה הזיכרון השני: {event}. {name} {age_phrase} שמר{sf} אותו ליד הראשון.",
            "{air}. ובתוך האוויר הזה, {event}. {name} חייך{sf} חיוך קטן, בלי להסביר.",
        ],
        "event_3": [
            "והדבר השלישי בא אחרון, כמו כוכב מאחר: {event}. עכשיו הערב היה מלא בדיוק במידה.",
            "לפני שהעיניים כבדו: {event}. {name} אמר{sf} תודה בלחש, גם אם אף אחד לא דרש.",
            "שלוש לחישות. השלישית הייתה {event}. {companion} עצם עיניים רגע, כמסכים.",
        ],
        "turning": [
            "השקט כבר לא היה ריק. הוא היה מלא ב{name}. שלושה דברים ישבו על השמיכה ולא מיהרו.",
            "{name} ראה{sf} שהערב יודע להחזיק שבוע בלי לשבור אותו. {light}.",
            "לא היה צריך לסכם בקול גדול. {name} {age_phrase} רק נשם{sf} פעם אחת ארוכה.",
        ],
        "moral": [
            "ונשאר באוויר משפט רך: {moral_he} {name} שמע{sf} אותו כמו שמיכה נוספת.",
            "{companion} לחש, בלי להטיף: {moral_he} {name} הניח{sf} את זה ליד הכרית.",
            "הערב לימד בלי מורה: {moral_he} זה מספיק ללילה אחד, וגם למחר.",
        ],
        "close": [
            "העיניים של {name} כבדו כמו דבש. {companion} מנמיך את הקול. מחר מחכה בלי לדחוף. לילה טוב, {name}.",
            "{in_place} האור התקצר. {name} {age_phrase} נרדם{sf} בתוך השקט. לילה טוב.",
            "הלילה פרש שמיכה על כל מה שנאמר. {name} נשם{sf} פעם אחרונה לאט. לילה טוב, ערב קטן.",
        ],
    },
    {
        "id": "two-voices",
        "flavor": "a conversation in two voices between the child and a kind companion",
        "titles": [
            "{name} ו{companion} מדברים",
            "שני קולות ל{name}",
            "השיחה של {name} לפני השינה",
        ],
        "opening": [
            "״{come},״ אמר {companion}. ״יש לי אוזן.״ {name} {age_phrase} ישב{sf} {place}. {air}. השיחה התחילה בלי מצלמה.",
            "שני קולות {in_place}: קול של {name}, וקול של {companion}. {light}. אף אחד לא מיהר לנצח.",
            "{name} {age_phrase} אמר{sf}: אפשר לספר לאט? {companion} הנהן. {in_place} נפתח מקום לשני קולות.",
        ],
        "event_1": [
            "״מה היה ראשון?״ שאל {companion}. {name} אמר{sf}: {event}. ״שמעתי,״ ענה {companion}. ״באמת שמעתי.״",
            "{name} התחיל{sf}: {event}. {companion} לא תיקן ולא קיצר. רק חזר על המילים כמו הד רך.",
            "הקול הראשון היה של {name}: {event}. הקול השני אמר תודה שסיפרת.",
        ],
        "event_2": [
            "״ועוד משהו?״ {name} הוסיף{sf}: {event}. {companion} המתין עד הסוף, אפילו שהסוף היה שקט.",
            "השיחה פנתה: {event}. {name} {age_phrase} חיפש{sf} מילה, ו{companion} חיכה בלי למלא את החלל.",
            "״זה חשוב לי,״ אמר{sf} {name}. ״{event}.״ ״אז זה חשוב גם לי,״ אמר {companion}.",
        ],
        "event_3": [
            "המשפט השלישי יצא כמעט בלחש: {event}. שני הקולות נחו.",
            "״אחרון להערב,״ ביקש {companion}. {name} אמר{sf}: {event}. וזה הספיק.",
            "ואז {name} הוסיף{sf} דבר אחרון: {event}. {companion} שמר אותו בין שניהם.",
        ],
        "turning": [
            "לא היה ויכוח. הייתה הקשבה. {name} הרגיש{sf} איך להיות מובן זה כמו אור {in_place}.",
            "שני הקולות ישבו זה ליד זה, כמו שתי כוסות מים. {name} {age_phrase} לא היה לבד עם השבוע.",
            "{companion} אמר: לפעמים סיפור הוא פשוט מישהו שעונה ״אני כאן״. {name} חייך{sf}.",
        ],
        "moral": [
            "ומתוך השיחה עלה דבר פשוט: {moral_he} {name} הבין{sf} שזה לא שיעור — זה יחס.",
            "״אם נזכור משהו אחד,״ אמר {companion}, ״אז את זה: {moral_he}״ {name} הנהן{sf}.",
            "שני הקולות הסכימו בלי הצבעה: {moral_he} אחר כך היה אפשר לשתוק יחד.",
        ],
        "close": [
            "״לילה טוב,״ אמר {companion}. ״לילה טוב,״ לחש{sf} {name}. החדר שמר על שני הקולות עד הבוקר.",
            "השיחה נגמרה כמו דלת שנסגרת בעדינות. {name} {age_phrase} נרדם{sf}. לילה טוב.",
            "{in_place} נשארה דממה טובה. {name} עצם{sf} עיניים. לילה טוב, {name}. לילה טוב, אוזן טובה.",
        ],
    },
    {
        "id": "letter-to-the-moon",
        "flavor": "a child writing or sending a kind letter toward the moon",
        "titles": [
            "מכתב לירח מאת {name}",
            "{name} כותב{sf} לירח",
            "המכתב של {name} לפני השינה",
        ],
        "opening": [
            "{name} {age_phrase} לקח{sf} דף {in_place}. {light}. {companion} אמר: נכתוב לירח על השבוע, בלי לבקש מתנות — רק לספר.",
            "הירח חיכה מעל {place}. {air}. {name} ליטף{sf} עיפרון, ו{companion} הכתיב לאט, בקצב של נשימה.",
            "״לירח שלום,״ התחיל{sf} {name}. {in_place} המכתב נפתח כמו חלון.",
        ],
        "event_1": [
            "בשורה הראשונה כתב{sf} {name}: השבוע {event}. הנקודה בסוף הייתה עגולה ושקטה.",
            "״קודם דבר אחד אמיתי,״ ביקש {companion}. {name} כתב{sf}: {event}.",
            "המכתב קיבל משפט ראשון חם: {event}. {name} לא ייפה{sf}. רק סיפר{sf}.",
        ],
        "event_2": [
            "בשורה השנייה: {event}. {name} {age_phrase} צייר{sf} נקודה נוספת, כמו כוכב קטן בשולי הדף.",
            "״ועוד משהו שהיה,״ אמר {companion}. {name} הוסיף{sf}: {event}.",
            "הירח, לו היה קורא עכשיו, היה רואה: {event}. {name} חייך{sf} אל השורה.",
        ],
        "event_3": [
            "לפני החתימה בא משפט אחרון: {event}. הדף היה מלא במידה הנכונה.",
            "שורה שלישית, קצרה וברורה: {event}. {name} הניח{sf} את העיפרון.",
            "״זהו,״ לחש{sf} {name}. ״גם {event}.״ {companion} ניפנף בדף לייבש את המילים.",
        ],
        "turning": [
            "{name} קיפל{sf} את המכתב לשלושה. לא שלח אותו בדואר. שלח אותו בחלון, אל האור.",
            "הדף {in_place} נראה פתאום כמו ירח קטן. {name} הבין{sf} שסיפור אפשר גם לשלוח.",
            "{companion} אמר: ירח לא מתקן מכתבים. הוא רק מקבל. {name} {age_phrase} נשם{sf} לרווחה.",
        ],
        "moral": [
            "על הדף, מתחת לחתימה, נשאר משפט ל{name}: {moral_he} זה מה שהירח היה עונה, אילו דיבר.",
            "{name} קרא{sf} שוב את השורות והרגיש{sf}: {moral_he} המכתב לימד בלי להרצות.",
            "לפני שהדף ישן, {companion} הוסיף נקודה רכה: {moral_he}",
        ],
        "close": [
            "המכתב נח על אדן החלון. {name} נח על הכרית. הירח שמר על שניהם. לילה טוב, {name}.",
            "{name} {age_phrase} לחש{sf} לילה טוב לירח, ולמכתב, ול{companion}. העיניים נסגרו.",
            "אין צורך בתשובה מהירה. המכתב כבר הגיע. {name} ישן{sf}. לילה טוב.",
        ],
    },
    {
        "id": "recipe-of-the-heart",
        "flavor": "a cozy recipe of feelings, mixing weekly moments in a warm bowl",
        "titles": [
            "המתכון של {name}",
            "{name} מבשל{sf} סיפור",
            "קערת הלב של {name}",
        ],
        "opening": [
            "{in_place} הונחה קערה. {air}. {name} {age_phrase} גלגל{sf} שרוולים, ו{companion} אמר: הערב נבשל סיפור מהשבוע — בלי אש גדולה, רק חום.",
            "{name} עמד{sf} {place}. {light}. על השולחן: קערה, כף עץ, ושלושה דברים מהשבוע שעוד לא קיבלו שם של מתכון.",
            "״מה שמים קודם?״ שאל{sf} {name}. ״מה שהיה אמיתי,״ אמר {companion}. {in_place} התחילה הבלילה.",
        ],
        "event_1": [
            "הכפית הראשונה: {event}. {name} ערבב{sf} לאט, כדי לא לאבד את הטעם.",
            "אל הקערה נכנס דבר ראשון: {event}. {companion} הנהן. ״זה הבסיס.״",
            "{name} {age_phrase} שם{sf} פנימה: {event}. הקערה התחממה קצת.",
        ],
        "event_2": [
            "עוד כפית: {event}. {name} לא מיהר{sf}. מתכונים טובים לא רצים.",
            "הבלילה ביקשה עוד משהו, וזה היה: {event}. {name} חייך{sf} אל הכף.",
            "״ועכשיו?״ ״עכשיו {event}.״ {name} ערבב{sf} עד שהשבוע התחיל להחזיק יחד.",
        ],
        "event_3": [
            "הכפית האחרונה לפני האפייה: {event}. {name} טעם{sf} בקצה האצבע. בדיוק.",
            "שלושה מרכיבים. האחרון: {event}. הקערה הייתה מלאה בלי לגלוש.",
            "{companion} אמר: די. {name} הוסיף{sf} רק את זה: {event}. ואז הפסיק{sf}.",
        ],
        "turning": [
            "לא היה צורך בתנור אמיתי. החום בא מן הלב של {name}. הסיפור תפח בשקט.",
            "{name} {age_phrase} ראה{sf} איך שלושה דברים נהיים מאכל אחד. {in_place} הריח מתוק.",
            "הקערה חזרה ריקה, והלב מלא. {name} הבין{sf} שבישול כזה הוא בעצם סיפור.",
        ],
        "moral": [
            "ועל המתכון, בשולי הדף, נכתב בכתב יד רך: {moral_he} {name} קרא{sf} ולא מחק{sf}.",
            "{companion} ליקק כף מדומה ואמר: הטעם הוא {moral_he} {name} הסכים{sf}.",
            "המאכל של הערב לא נאכל — הוא הובן. {moral_he} זה מה שנשאר בפה.",
        ],
        "close": [
            "הקערה נשטפה. {name} לא. {name} נשאר{sf} מתוק ומלא. לילה טוב, {name}. לילה טוב, מתכון קטן.",
            "{in_place} כבה האור מעל השולחן. {name} {age_phrase} הלך{sf} לישון עם טעם של שבוע. לילה טוב.",
            "{companion} תלה את הסינר. המיטה הייתה התנור של הלילה. {name} נרדם{sf}. לילה טוב.",
        ],
    },
    {
        "id": "map",
        "flavor": "a hand-drawn map of the week, three places marked with kindness",
        "titles": [
            "המפה של {name}",
            "{name} מצייר{sf} את השבוע",
            "שלוש נקודות על המפה של {name}",
        ],
        "opening": [
            "{name} {age_phrase} פרש{sf} דף {in_place}. {light}. {companion} אמר: נצייר מפה של השבוע. לא של ארצות — של רגעים.",
            "על הדף הופיע קו ראשון. {air}. {name} ישב{sf} {place} וצייר{sf} בית קטן, ואחר כך שביל.",
            "״איפה היינו?״ שאל {companion}. {name} חייך{sf}. {in_place} המפה התחילה לחיות.",
        ],
        "event_1": [
            "סימן ראשון בעיגול: כאן {event}. {name} כתב{sf} שם קטן ליד הנקודה.",
            "המפה קיבלה מקום ראשון. שם {event}. {name} {age_phrase} דייק{sf}, בלי להגזים.",
            "{companion} הצביע: פה. {name} סיפר{sf}: {event}. הנקודה נעשתה זהובה.",
        ],
        "event_2": [
            "קו ממשיך, ואז נקודה שנייה: {event}. {name} חיבר{sf} אותה לשביל.",
            "באמצע המפה, לא במרכז הגדול אלא בדיוק איפה שצריך: {event}.",
            "{name} הוסיף{sf} עץ קטן ליד המקום שבו {event}. {companion} הנהן.",
        ],
        "event_3": [
            "הנקודה השלישית, כמעט בשולי הדף: {event}. עכשיו אפשר היה לראות מסלול.",
            "״אחרונה להערב,״ אמר {companion}. {name} צייר{sf} כוכב במקום שבו {event}.",
            "ואז {event}. {name} {age_phrase} סגר{sf} את המסלול בקו רך, לא בחומה.",
        ],
        "turning": [
            "{name} הרים{sf} את הדף. המפה הייתה קטנה מספיק כדי להיכנס ללב, וגדולה מספיק כדי להחזיק שבוע.",
            "שלוש נקודות. קו אחד. {in_place} {name} הבין{sf} שהשבוע היה דרך, לא ערבוביה.",
            "{companion} אמר: מפה טובה לא מפחידה אותך. היא מחזירה אותך הביתה. {name} חייך{sf}.",
        ],
        "moral": [
            "במקרא של המפה, בכתב קטן: {moral_he} {name} קרא{sf} את זה כמו שם של ארץ חדשה.",
            "האגדה של המפה הייתה משפט אחד: {moral_he} {name} {age_phrase} שמע{sf} ולא שכח{sf}.",
            "{companion} צייר חץ אל הלב וכתב: {moral_he}",
        ],
        "close": [
            "המפה נכנסה מתחת לכרית, לא כדי להישמר מסודרת — כדי לחלום עליה. לילה טוב, {name}.",
            "{name} קיפל{sf} את הדף. {in_place} כבה האור. לילה טוב, מפה קטנה.",
            "{companion} כבה את העיפרון. {name} {age_phrase} ישן{sf} בתוך הגבולות הרכים. לילה טוב.",
        ],
    },
    {
        "id": "lost-and-found",
        "flavor": "a gentle lost-and-found of small feelings and weekly moments",
        "titles": [
            "{name} והאבידה שנמצאה",
            "מה ש{name} מצא{sf}",
            "הקופסה החמה של {name}",
        ],
        "opening": [
            "{in_place} עמדה קופסה עם הכיתוב ״נמצא״. {air}. {name} {age_phrase} פתח{sf} אותה עם {companion}, לא כדי לקחת — כדי להחזיר לשבוע את מה ששייך לו.",
            "{name} חשב{sf} שמשהו אבד. {companion} אמר: לפעמים הרגע רק מחכה בקופסה. {place}. {light}.",
            "הערב היה מעין משרד אבדות עדין. {name} {age_phrase} ישב{sf} {place} ואמר{sf}: נחפש לאט.",
        ],
        "event_1": [
            "בתחתית הקופסה נמצא דבר ראשון: {event}. {name} זיהה{sf} אותו מיד, כמו גרב אהובה.",
            "״זה שלך,״ אמר {companion}. {name} הנהן{sf}: כן, {event}. החזיר{sf} אל הלב.",
            "המציאה הראשונה לא הייתה חפץ. הייתה רגע: {event}. {name} חייך{sf}.",
        ],
        "event_2": [
            "עוד פתק בקופסה: {event}. {name} {age_phrase} קרא{sf} לאט, כדי לא לערבב.",
            "בין שני פתקים נשמר גם זה: {event}. {name} שם{sf} אותו ליד הראשון.",
            "{companion} ניער בעדינות. יצא: {event}. ״גם זה לא אבוד,״ אמר{sf} {name}.",
        ],
        "event_3": [
            "ואחרון, כמעט שקוף: {event}. {name} מצא{sf} אותו בדיוק כשהיה צריך.",
            "הקופסה כמעט ריקה, ובכל זאת מלאה. האחרון: {event}.",
            "״זהו מה שנמצא הערב,״ אמר {companion}. {name} הוסיף{sf}: {event}. שלוש מציאות.",
        ],
        "turning": [
            "{name} הבין{sf} שלא באמת אבד דבר. רק חיכה שיסתכלו עליו יפה. {in_place} הקופסה נחה.",
            "להחזיר רגע אל הלב זה גם סוג של מציאה. {name} {age_phrase} ישב{sf} עם שלושה דברים ולא עם חוסר.",
            "{companion} סגר את המכסה בלי לנעול. דברים טובים לא נועלים.",
        ],
        "moral": [
            "על המכסה היה כתוב עכשיו, בכתב חדש: {moral_he} {name} קרא{sf} ושמח{sf} שהאבידה הייתה בעצם מתנה.",
            "מה שנמצא באמת היה זה: {moral_he} {name} לקח{sf} את המשפט הביתה.",
            "{companion} אמר בשקט: {moral_he} והקופסה הסכימה.",
        ],
        "close": [
            "הקופסה נשארה {in_place}. {name} הלך{sf} לישון בלי לחפש עוד. לילה טוב, {name}.",
            "מה שנמצא נשאר קרוב. {name} {age_phrase} עצם{sf} עיניים. לילה טוב, מציאות קטנות.",
            "{companion} לחש לילה טוב גם למה שלא אבד. {name} ישן{sf}. לילה טוב.",
        ],
    },
    {
        "id": "first-time",
        "flavor": "a first-time wonder, trying something new with a kind companion",
        "titles": [
            "הפעם הראשונה של {name}",
            "{name} מנסה{sf} לאט",
            "חדש בשביל {name}",
        ],
        "opening": [
            "{in_place} היה משהו חדש באוויר. {air}. {name} {age_phrase} עמד{sf} {place}, ו{companion} אמר: אפשר לנסות לאט. לא צריך לדעת הכול מראש.",
            "יש ערבים שהם ״פעם ראשונה״, אפילו אם היום כבר נגמר. {name} לקח{sf} אוויר. {light}.",
            "{companion} הושיט יד. {name} {age_phrase} אחז{sf} בה. {in_place} התחיל נסיון רך, בלי מבחן.",
        ],
        "event_1": [
            "הצעד הראשון החדש היה בעצם דבר שכבר קרה: {event}. {name} הסתכל{sf} עליו כאילו בפעם הראשונה.",
            "״קודם רואים מה היה,״ אמר {companion}. {name} אמר{sf}: {event}. וזה נעשה חדש כי סיפרו אותו.",
            "{name} גילה{sf} שגם {event} יכול להיות התחלה, לא רק זיכרון.",
        ],
        "event_2": [
            "אחר כך העז{sf} {name} להוסיף: {event}. הלב דפק קצת, ואז נרגע.",
            "הפעם השנייה של האומץ: {event}. {name} {age_phrase} לא צחק{sf} על עצמ{op}. רק ניסה{sf}.",
            "{companion} אמר: חדש לא חייב להיות מושלם. {event} — וזה בסדר.",
        ],
        "event_3": [
            "והדבר השלישי, כמעט בסוף: {event}. {name} הרגיש{sf} שהחדש נהיה מוכר קצת, כמו נעל אחרי שעה.",
            "״עוד אחד,״ לחש{sf} {name}: {event}. עכשיו כבר היה אומץ בגודל של כפית.",
            "שלוש פעמים ראשונות בערב אחד. האחרונה: {event}. {companion} מחא כף חרישית.",
        ],
        "turning": [
            "{name} הבין{sf} שאומץ אינו אריה. אומץ הוא לנסות, ולספר, ולנשום. {in_place} היה שקט גאה.",
            "החדש כבר לא הפחיד. הוא ישב ליד {name} כמו חבר חדש שמדברים איתו לאט.",
            "{light}. {name} {age_phrase} חייך{sf}: אפשר שוב מחר, בלי להיות מושלם.",
        ],
        "moral": [
            "ומה שנלמד, בלי ציון: {moral_he} {name} שם{sf} את זה בכיס ליד האומץ הקטן.",
            "{companion} אמר: {moral_he} זה המתכון ל״פעם ראשונה״ שחוזרת בעדינות.",
            "השיעור לא היה ״הצטיין״. היה: {moral_he} {name} אהב{sf} את זה.",
        ],
        "close": [
            "הפעם הראשונה נגמרה בלילה טוב. {name} נרדם{sf} עם חיוך של מי שניסה. לילה טוב, {name}.",
            "{in_place} כבה האור. {name} {age_phrase} לקח{sf} את האומץ הקטן למיטה. לילה טוב.",
            "{companion} לחש: מחר יהיו עוד דברים חדשים, ואפשר שוב לאט. לילה טוב, {name}.",
        ],
    },
    {
        "id": "apology",
        "flavor": "a gentle apology and repair, never shaming, always kind",
        "titles": [
            "התיקון של {name}",
            "{name} מחזיר{sf} מילה רכה",
            "סליחה, אמר{sf} {name}",
        ],
        "opening": [
            "{in_place} ישב{sf} {name} {age_phrase} עם לב קצת מקומט. {air}. {companion} אמר: אם משהו נשבר השבוע, אפשר לתקן במילים. בלי בושה.",
            "{name} לא היה רע. {name} היה ילד עם שבוע. {place}. {light}. {companion} פתח מרחב לסליחה רכה.",
            "יש תיקונים בגובה ילד. {name} {age_phrase} נשם{sf}. {in_place} התחיל סיפור של להחזיר רוך.",
        ],
        "event_1": [
            "קודם סיפרו מה היה, בלי האשמה: {event}. {name} הסתכל{sf} על זה ישר, בעדינות.",
            "השבוע הביא גם את זה: {event}. {companion} אמר: לראות זה כבר חצי תיקון.",
            "{name} אמר{sf} בקול נמוך: {event}. האוויר לא נעשה כבד. הוא נעשה כנה.",
        ],
        "event_2": [
            "ואז עוד רגע מהשבוע: {event}. {name} {age_phrase} שם{sf} אותו ליד הראשון, לא כדי להעניש — כדי להבין.",
            "בין שני דברים יש מקום לומר ״הייתי שם״. {event}. {name} היה שם.",
            "{companion} שאל: ומה עוד? {name} ענה{sf}: {event}. השיחה נשארה חמה.",
        ],
        "event_3": [
            "הדבר השלישי היה גם הוא חלק מהתיקון: {event}. {name} לא ברח{sf} ממנו.",
            "לקראת הסוף: {event}. {name} הרגיש{sf} שהלב מתחיל להתיישר כמו דף.",
            "שלושה רגעים על השולחן. האחרון: {event}. עכשיו אפשר היה לומר סליחה בלי להישבר.",
        ],
        "turning": [
            "{name} אמר{sf} סליחה אל מי שצריך, או אל עצמ{op}, או אל האוויר. המילה יצאה עגולה, לא חדה.",
            "תיקון אינו עונש. תיקון הוא גשר. {name} {age_phrase} דרך{sf} עליו לאט. {in_place} נעשה רך יותר.",
            "{companion} לא מחא כף גדולה. רק הניח יד על הכתף. {name} נשם{sf}.",
        ],
        "moral": [
            "ומה שנשאר אחרי הסליחה: {moral_he} {name} הבין{sf} שזה התיקון האמיתי.",
            "{companion} לחש: {moral_he} בלי להטיף, בלי להקטין. {name} הנהן{sf}.",
            "הלב המקומט התחליק. עליו היה כתוב: {moral_he}",
        ],
        "close": [
            "אפשר לישון אחרי תיקון. {name} הלך{sf} למיטה קל יותר. לילה טוב, {name}. לילה טוב, מילה רכה.",
            "{in_place} כבה האור. {name} {age_phrase} נרדם{sf} בלי לשמור כעס תחת הכרית. לילה טוב.",
            "{companion} שמר על הגשר עד הבוקר. {name} ישן{sf}. לילה טוב.",
        ],
    },
    {
        "id": "wait-for-morning",
        "flavor": "waiting kindly for morning, patience as a warm blanket",
        "titles": [
            "{name} מחכה{sf} לבוקר",
            "עד הבוקר, {name}",
            "הלילה ששומר על {name}",
        ],
        "opening": [
            "{name} {age_phrase} רצה{sf} כבר את המחר. {companion} אמר: אפשר לחכות יפה. {in_place} {light}. השעון לא מיהר, וגם אנחנו לא.",
            "הלילה היה חדר, לא מכשול. {name} ישב{sf} {place}. {air}. {companion} לימד איך ממתינים בלי לכעוס על הדקות.",
            "״מתי בוקר?״ שאל{sf} {name}. ״אחרי הסיפור,״ חייך {companion}. {in_place} התחילה המתנה רכה.",
        ],
        "event_1": [
            "כדי שההמתנה תהיה מלאה, נזכרו במה שכבר היה: {event}. {name} שם{sf} את זה על השמיכה.",
            "הדקה הראשונה של הסיפור הביאה את {event}. {name} {age_phrase} הקשיב{sf} במקום למדוד זמן.",
            "{companion} אמר: בזמן שמחכים, אפשר לספר. {name} התחיל{sf}: {event}.",
        ],
        "event_2": [
            "עוד קצת לילה, ועוד רגע מהשבוע: {event}. ההמתנה נעשתה מעניינת.",
            "בין עכשיו למחר יש מקום גם לזה: {event}. {name} לא דחף{sf} את השעון.",
            "{light}. ובתוך האור הזה, {event}. {name} חייך{sf} אל הדקה.",
        ],
        "event_3": [
            "לפני שהעיניים ניצחו: {event}. {name} הבין{sf} שההמתנה כבר מחזיקה שלושה דברים.",
            "הדבר השלישי בא כמו כוכב מאחר: {event}. הבוקר יכול לחכות עוד קצת.",
            "״ועוד משהו מהשבוע,״ לחש {companion}. {name} אמר{sf}: {event}.",
        ],
        "turning": [
            "לחכות זה לא ריק. לחכות זה לשמור מקום למחר בלי לזרוק את הערב. {name} {age_phrase} נשם{sf} לאט.",
            "{in_place} הזמן התרכך. {name} כבר לא משך{sf} בו. הזמן ישב ליד{op} כמו חבר.",
            "{companion} אמר: בוקר תמיד מגיע. התפקיד שלנו הוא לא לדחוף אותו. {name} הנהן{sf}.",
        ],
        "moral": [
            "והמשפט שנשאר עד הזריחה: {moral_he} {name} לקח{sf} אותו כשמיכה נוספת.",
            "ההמתנה לימדה: {moral_he} {name} {age_phrase} שמע{sf} ונרגע{sf}.",
            "{companion} לחש את המוסר כמו שיר ערש: {moral_he}",
        ],
        "close": [
            "הבוקר יבוא לבד. {name} לא צריך{sf} לשמור משמרת. לילה טוב, {name}. לילה טוב, מחר קטן.",
            "העפעפיים ניצחו את השעון. {name} ישן{sf}. {companion} חיכה במקומ{op}. לילה טוב.",
            "{in_place} החושך היה רך. {name} {age_phrase} נרדם{sf} בתוך ההמתנה. לילה טוב.",
        ],
    },
    {
        "id": "circle-of-friends",
        "flavor": "including a friend, a circle of kindness in a warm place",
        "titles": [
            "המעגל של {name}",
            "{name} מפנה{sf} מקום",
            "חבר ליד {name}",
        ],
        "opening": [
            "{in_place} נפתח מעגל על הרצפה. {air}. {name} {age_phrase} ישב{sf} {place}, ו{companion} אמר: תמיד אפשר להזיז קצת את הברך, שייכנס עוד אחד.",
            "יש מעגלים שסוגרים ויש מעגלים שפותחים. {name} בחר{sf} לפתוח. {light}.",
            "{companion} צייר עיגול באוויר. {name} {age_phrase} נכנס{sf} אליו, והשאיר{sf} מקום ליד.",
        ],
        "event_1": [
            "במעגל סיפרו דבר ראשון: {event}. מישהו הקשיב. {name} הרגיש{sf} איך הקשבה היא כיסא נוסף.",
            "השבוע נכנס למעגל עם {event}. אף אחד לא דחף אותו החוצה.",
            "{name} אמר{sf}: {event}. {companion} פנה קצת, כאילו גם הרגע הזה צריך מקום.",
        ],
        "event_2": [
            "עוד קול במעגל, ועוד רגע: {event}. {name} {age_phrase} לא לקח{sf} את כל האוויר.",
            "בין חבר לחבר עבר גם זה: {event}. המעגל התרחב בלי להישבר.",
            "{name} הזיז{sf} את הברך. נכנס עוד סיפור: {event}.",
        ],
        "event_3": [
            "ואחרון במעגל של הערב: {event}. עכשיו היה חם באמצע, כמו מדורה קטנה של מילים.",
            "המקום שנשאר התמלא ב{event}. {name} חייך{sf} אל מי שישב מול{op}.",
            "שלושה דברים במעגל אחד. השלישי: {event}. אף אחד לא נשאר מאחור.",
        ],
        "turning": [
            "{name} ראה{sf} שהמעגל אינו חומה. הוא חיבוק עם רווחים. {in_place} היה שקט שמח.",
            "להפנות מקום לא מקטין אותך. {name} {age_phrase} הרגיש{sf} גדול יותר אחרי שהזיז{sf} את הברך.",
            "{companion} אמר: חבר הוא מי שאתה עושה לו מקום, גם בסיפור. {name} הנהן{sf}.",
        ],
        "moral": [
            "ומה שהמעגל לחשו אל המרכז: {moral_he} {name} שמע{sf} משם, מהאמצע.",
            "הכלל היחיד במעגל הזה: {moral_he} {name} {age_phrase} לקח{sf} אותו הביתה.",
            "{companion} סיכם בלי שופט: {moral_he}",
        ],
        "close": [
            "המעגל התקפל לגודל של שמיכה. {name} נשאר{sf} בפנים. לילה טוב, {name}. לילה טוב, חברים קטנים.",
            "{in_place} כבו הקולות. {name} ישן{sf} עם מקום פנוי ליד הלב. לילה טוב.",
            "{companion} נשאר במעגל עד שהנשימות האטו. לילה טוב, {name}.",
        ],
    },
    {
        "id": "whisper-walk",
        "flavor": "a slow whisper-walk through a place, noticing small things",
        "titles": [
            "הטיול בלחש של {name}",
            "{name} הולך{sf} לאט",
            "צעדים רכים ל{name}",
        ],
        "opening": [
            "{in_place} יצאו {name} {age_phrase} ו{companion} לטיול בלחש. {air}. הצעדים היו קטנים בכוונה, כדי לשמוע את השבוע.",
            "לא רצים בערב. {name} הלך{sf} {place}. {light}. {companion} התאים את הצעד לצעד.",
            "״נלך כמו חתול,״ הציע {companion}. {name} {age_phrase} חייך{sf} והתחיל{sf} טיול שקט.",
        ],
        "event_1": [
            "אחרי עשרה צעדים נזכרו: {event}. {name} לחש{sf} את זה, כדי לא להבריח ציפורים.",
            "הלחישה הראשונה בשביל: {event}. {name} שמע{sf} גם את ההד הפנימי.",
            "{companion} עצר ליד אבן. {name} אמר{sf} בלחש: {event}.",
        ],
        "event_2": [
            "עוד כמה צעדים, עוד לחישה: {event}. העולם לא דרש קול גדול.",
            "באמצע הטיול, {place}, עלה {event}. {name} {age_phrase} שמר{sf} קול נמוך.",
            "הרוח בלבלבה מילה, ו{name} השלים{sf}: {event}.",
        ],
        "event_3": [
            "לפני החזרה הביתה: {event}. הלחישה השלישית הייתה ברורה לגמרי.",
            "הצעד האחרון נשא את {event}. {name} הרגיש{sf} שהטיול הושלם.",
            "״אחרונה בשביל,״ אמר {companion}. {name} לחש{sf}: {event}.",
        ],
        "turning": [
            "לחישות מחזיקות יותר ממה שחושבים. {name} עמד{sf} {in_place} עם שלושה דברים שלא נפלו בדרך.",
            "הטיול לא היה ארוך. הוא היה מדויק. {name} {age_phrase} הבין{sf} שלשים לב זה גם ללכת.",
            "{companion} אמר: מי שהולך לאט רואה יותר. {name} ראה{sf}.",
        ],
        "moral": [
            "על השביל נשאר משפט כמו חלוק נחל: {moral_he} {name} הרים{sf} אותו בכיס.",
            "הלחישה הגדולה של הערב הייתה: {moral_he} {name} הנהן{sf} בלחש.",
            "{companion} סיכם בנשימה: {moral_he}",
        ],
        "close": [
            "חזרו הביתה על בהונות. {name} נכנס{sf} למיטה בלי להעיר את הבית. לילה טוב, {name}.",
            "הטיול נגמר בכרית. {name} {age_phrase} ישן{sf} עם חול קל בנעליים של הלב. לילה טוב.",
            "{companion} סגר את הדלת בלחש. לילה טוב, {name}. לילה טוב, שביל.",
        ],
    },
    {
        "id": "lantern-path",
        "flavor": "a lantern lighting a kind path, warm glow on three moments",
        "titles": [
            "{name} והפנס הקטן",
            "שביל האור של {name}",
            "{name} מאיר{sf} לאט",
        ],
        "opening": [
            "{companion} הדליק פנס קטן. לא כדי לגרש חושך — כדי לראות יפה. {name} {age_phrase} אחז{sf} בידית. {in_place} {light}.",
            "עיגול אור חם נע {place}. {air}. {name} הלך{sf} בתוכו עם {companion}, והשבוע בא אל האור.",
            "פנס אחד הספיק. {name} {age_phrase} לא ביקש{sf} זרקור. {in_place} התחיל שביל מואר.",
        ],
        "event_1": [
            "באור הראשון נראה בבירור: {event}. {name} לא פחד{sf}. רק ראה{sf}.",
            "הפנס עצר. שם {event}. {name} אמר{sf} את זה בקול רך, והאור הנהן.",
            "מה שהיה בצל קיבל עיגול זהוב: {event}. {name} {age_phrase} חייך{sf}.",
        ],
        "event_2": [
            "האור זז קצת ימינה. הופיע: {event}. {name} שמר{sf} גם את זה.",
            "עוד צעד, עוד עיגול: {event}. הפנס לא שיפוט. הפנס רק האיר.",
            "{companion} הגביה מעט. {name} ראה{sf}: {event}.",
        ],
        "event_3": [
            "ולפני שהפנס הונמך: {event}. שלושה דברים עמדו עכשיו באור בלי להתבייש.",
            "העיגול האחרון להערב: {event}. {name} הבין{sf} שדי באור קטן.",
            "״עוד רגע אחד,״ ביקש{sf} {name}. הפנס הסכים, ושם היה {event}.",
        ],
        "turning": [
            "{name} גילה{sf} שאור אינו צועק. אור מזמין. {in_place} שלושת הרגעים נראו שייכים.",
            "הפנס לא שינה את השבוע. הוא רק נתן לו פנים. {name} {age_phrase} אהב{sf} את הפנים האלה.",
            "{companion} אמר: אפשר להאיר בלי לסינוור. {name} הנהן{sf}.",
        ],
        "moral": [
            "על זכוכית הפנס, אם מתקרבים, כתוב: {moral_he} {name} קרא{sf} לאור.",
            "האור לימד משפט אחד: {moral_he} {name} לקח{sf} אותו אל השינה.",
            "{companion} כבה מילה אחת מיותרת והשאיר: {moral_he}",
        ],
        "close": [
            "הפנס כבה. נשאר אור פנימי. {name} נרדם{sf}. לילה טוב, {name}. לילה טוב, עיגול חם.",
            "{in_place} החושך חזר להיות חדר. {name} {age_phrase} ישן{sf} בתוכו בשלווה. לילה טוב.",
            "{companion} הניח את הפנס ליד הנעליים. מחר ידליקו שוב אם צריך. לילה טוב, {name}.",
        ],
    },
    {
        "id": "treasure-of-small-things",
        "flavor": "treasuring small ordinary things from the week, never greedy",
        "titles": [
            "האוצר הקטן של {name}",
            "{name} שומר{sf} דברים קטנים",
            "שלוש אבנים ל{name}",
        ],
        "opening": [
            "{name} {age_phrase} פתח{sf} קופסת אוצר {in_place}. לא זהב — דברים קטנים. {air}. {companion} אמר: אוצר אמיתי נכנס לכיס.",
            "{place} הונחו שלוש אבנים חלקות. {light}. {name} ישב{sf} לשמור, לא לחטוף.",
            "יש ילדים שמחפשים דרקונים. {name} חיפש{sf} רגעים. {in_place} זה הספיק ל{companion}.",
        ],
        "event_1": [
            "האבן הראשונה קיבלה שם: {event}. {name} ליטף{sf} אותה באגודל.",
            "אל הקופסה נכנס אוצר ראשון: {event}. {name} לא התגאה{sf} בקול גדול. רק שמר{sf}.",
            "{companion} לחץ: זה שווה שמירה. {name} אמר{sf}: {event}.",
        ],
        "event_2": [
            "האבן השנייה: {event}. {name} {age_phrase} הניח{sf} אותה ליד הראשונה בלי שישקלו מי כבדה יותר.",
            "אוצר שני, לא גדול יותר ולא קטן יותר: {event}. הקופסה שמחה.",
            "{name} הוסיף{sf}: {event}. {companion} חייך אל הפשטות.",
        ],
        "event_3": [
            "ואבן שלישית, אחרונה להערב: {event}. הקופסה נסגרה בלחיצה רכה.",
            "האוצר הושלם ב{event}. {name} לא ביקש{sf} רביעית. ידע{sf} מתי די.",
            "שלושה דברים קטנים. השלישי: {event}. דיי להרגיש עשיר.",
        ],
        "turning": [
            "{name} הבין{sf} שעושר אינו ערימה. עושר הוא לבחור מה לשמור. {in_place} הקופסה הייתה קלה.",
            "אפשר להיות עשיר בשלושה רגעים. {name} {age_phrase} היה. {light}.",
            "{companion} אמר: מי ששומר קטן, לא מאבד גדול. {name} הנהן{sf}.",
        ],
        "moral": [
            "על מכסה הקופסה נחרט בעדינות: {moral_he} {name} קרא{sf} כמו מפת אוצר.",
            "האוצר האמיתי היה המשפט: {moral_he} {name} שם{sf} גם אותו בפנים.",
            "{companion} לא ספר מטבעות. ספר משפט: {moral_he}",
        ],
        "close": [
            "הקופסה ליד המיטה. {name} ליד החלום. לילה טוב, {name}. לילה טוב, אוצר קטן.",
            "{name} {age_phrase} נרדם{sf} עשיר ועדין. {in_place} שקט. לילה טוב.",
            "{companion} שמר שלא יתפזר האבק החשוב. לילה טוב, {name}.",
        ],
    },
    {
        "id": "listening-ear",
        "flavor": "learning to listen, a large kind ear for the week and for others",
        "titles": [
            "האוזן הטובה של {name}",
            "{name} מקשיב{sf}",
            "לשמוע כמו {name}",
        ],
        "opening": [
            "{companion} הביא אוזן גדולה מדומה, עשויה מרוח טובה. {name} {age_phrase} ישב{sf} {place}. {in_place} {air}. ״נשמע את השבוע עד הסוף,״ אמר {companion}.",
            "להקשיב זה לא לשתוק מבוישים. זה לפנות מקום לקול. {name} פנה{sf}. {light}.",
            "{name} {age_phrase} אמר{sf}: אני רוצה לשמוע יפה. {companion} חייך. {in_place} נפתחה האוזן.",
        ],
        "event_1": [
            "הקול הראשון שנכנס לאוזן: {event}. {name} לא קטע{sf}. חיכה{sf} לנקודה.",
            "{name} שמע{sf} עד הסוף: {event}. אחר כך רק הנהן{sf}.",
            "״סיפרתי,״ אמר השבוע. ״{event}.״ {name} ענה{sf}: שמעתי.",
        ],
        "event_2": [
            "עוד קול, בלי לדחוף את הראשון: {event}. {name} {age_phrase} החזיק{sf} שני דברים בלי לערבב.",
            "האוזן התרחבה. נכנס: {event}. {companion} לא תרגם. {name} הבין{sf} לבד.",
            "בין שמיעה לשמיעה, {event}. {name} שמר{sf} גם את השקט שאחרי.",
        ],
        "event_3": [
            "והקול השלישי, אחרון להערב: {event}. האוזן לא נסגרה מוקדם מדי.",
            "{name} שמע{sf} גם את מה שלא צעק: {event}. זה היה אולי החשוב.",
            "״עוד משהו,״ לחש השבוע. {name} היה שם: {event}.",
        ],
        "turning": [
            "{name} גילה{sf} שהקשבה היא חיבוק בלי ידיים. {in_place} היה רוגע של מי שנשמע, וגם של מי ששמע.",
            "לא כל תשובה צריכה לבוא מיד. {name} {age_phrase} למד{sf} לחכות לנקודה.",
            "{companion} אמר: אוזן טובה משנה ערב. {name} האמין{sf}, כי הרגיש{sf}.",
        ],
        "moral": [
            "מה שהאוזן לחשה פנימה: {moral_he} {name} שמע{sf} גם את זה עד הסוף.",
            "המשפט שנשאר אחרי כל הקולות: {moral_he} {name} הנהן{sf} ארוכות.",
            "{companion} סיכם בלחישה: {moral_he}",
        ],
        "close": [
            "האוזן הגדולה התקפלה. נשארה אוזן רגילה, מספיקה ללילה. {name} נרדם{sf}. לילה טוב, {name}.",
            "{in_place} השקט היה מלא שמיעה. {name} {age_phrase} ישן{sf} בתוכו. לילה טוב.",
            "{companion} לחש לילה טוב, ו{name} שמע{sf} גם את זה. לילה טוב.",
        ],
    },
]


MORALS: list[dict[str, str]] = [
    {"id": "kindness", "he": "טוב לב מתחיל במעשה קטן, לא בנאום.", "en": "kindness"},
    {"id": "honesty", "he": "אמת רכה עדיפה על סיפור מצוחצח.", "en": "honesty"},
    {"id": "patience", "he": "סבלנות היא לתת לדבר להגיע בלי לדחוף.", "en": "patience"},
    {"id": "sharing", "he": "כשחולקים, אין פחות — יש יותר לב.", "en": "sharing"},
    {"id": "ask-help", "he": "לבקש עזרה זה אומץ, לא חולשה.", "en": "courage to ask for help"},
    {"id": "listening", "he": "להקשיב עד הסוף זה כבר חיבוק.", "en": "listening"},
    {"id": "responsibility", "he": "אחריות מתחילה בדבר קטן ששומרים עליו.", "en": "responsibility for a small thing"},
    {"id": "include-friend", "he": "חבר נכנס כשעושים לו מקום במעגל.", "en": "including a friend"},
    {"id": "gratitude", "he": "תודה בלחש משנה את טעם היום.", "en": "gratitude"},
    {"id": "gentleness", "he": "עדינות היא כוח שלא שובר.", "en": "gentleness"},
    {"id": "try-again", "he": "לנסות שוב, לאט, זה גם הצלחה.", "en": "trying again"},
    {"id": "take-turns", "he": "לחכות לתור זה לאהוב גם את מי שלפניך.", "en": "taking turns"},
    {"id": "nature-care", "he": "שומרים על עלה ועל חבר באותה יד.", "en": "caring for nature"},
    {"id": "sorry", "he": "סליחה אמיתית מתקנת יותר מתירוץ.", "en": "saying sorry kindly"},
    {"id": "notice-others", "he": "לשים לב למישהו אחר מדליק אור בשניים.", "en": "noticing others"},
]


COMPANIONS: list[dict[str, str]] = [
    {"id": "moon", "he": "הירח", "he_the": "הירח", "en": "a kind crescent moon with a gentle face"},
    {"id": "fox", "he": "שועל קטן", "he_the": "השועל הקטן", "en": "a small friendly fox"},
    {"id": "bird", "he": "ינשוף קטן", "he_the": "הינשוף הקטן", "en": "a tiny kind owl"},
    {"id": "star", "he": "כוכב נייר", "he_the": "כוכב הנייר", "en": "a folded paper star companion"},
    {"id": "lamp", "he": "פנס לילה", "he_the": "פנס הלילה", "en": "a warm glowing night lantern"},
    {"id": "turtle", "he": "צב קטן", "he_the": "הצב הקטן", "en": "a small smiling turtle"},
    {"id": "cat", "he": "חתול ג׳ינג׳י", "he_the": "החתול הג׳ינג׳י", "en": "a ginger cat sitting calmly"},
    {"id": "firefly", "he": "גחלילית", "he_the": "הגחלילית", "en": "a gentle firefly of warm light"},
    {"id": "cloud", "he": "ענן רך", "he_the": "הענן הרך", "en": "a small friendly cloud"},
    {"id": "rabbit", "he": "ארנב לבן", "he_the": "הארנב הלבן", "en": "a white rabbit with kind eyes"},
    {"id": "owl", "he": "אוחה טובה", "he_the": "האוחה הטובה", "en": "a round gentle owl"},
    {"id": "snail", "he": "חילזון איטי", "he_the": "החילזון האיטי", "en": "a slow friendly snail"},
]


AGE_BANDS: list[tuple[int, int]] = [
    (3, 6),
    (3, 9),
    (4, 7),
    (5, 9),
    (6, 9),
    (3, 5),
]

THEME_KEYS = ("place", "air", "light", "theme_he", "in_place")


def companion_by_id(cid: str) -> dict[str, str]:
    for c in COMPANIONS:
        if c["id"] == cid:
            return c
    return COMPANIONS[0]


def theme_by_id(tid: str) -> dict[str, str]:
    for t in THEMES:
        if t["id"] == tid:
            return t
    return THEMES[0]


def format_by_id(fid: str) -> dict[str, Any]:
    for f in FORMATS:
        if f["id"] == fid:
            return f
    return FORMATS[0]


def moral_by_id(mid: str) -> dict[str, str]:
    for m in MORALS:
        if m["id"] == mid:
            return m
    return MORALS[0]


def _inject_theme(text: str, theme: dict[str, str]) -> str:
    merged = dict(theme)
    merged.setdefault("theme_he", theme.get("he") or "")
    out = text
    for key in THEME_KEYS:
        out = out.replace("{" + key + "}", merged.get(key) or "")
    return out


def make_template(
    theme: dict[str, str],
    fmt: dict[str, Any],
    moral: dict[str, str],
    companion: dict[str, str],
    variant: int,
    age_min: int,
    age_max: int,
    serial: int,
    extra_id: str = "",
) -> dict[str, Any]:
    v = variant % 3
    title = _inject_theme(fmt["titles"][v % len(fmt["titles"])], theme)
    beats = {
        "opening": _inject_theme(fmt["opening"][v % len(fmt["opening"])], theme),
        "event_1": _inject_theme(fmt["event_1"][v % len(fmt["event_1"])], theme),
        "event_2": _inject_theme(fmt["event_2"][v % len(fmt["event_2"])], theme),
        "event_3": _inject_theme(fmt["event_3"][v % len(fmt["event_3"])], theme),
        "turning": _inject_theme(fmt["turning"][v % len(fmt["turning"])], theme),
        "moral_landing": _inject_theme(fmt["moral"][v % len(fmt["moral"])], theme).replace(
            "{moral_he}", moral["he"]
        ),
        "bedtime_close": _inject_theme(fmt["close"][v % len(fmt["close"])], theme),
    }
    tid = f"tmpl-{fmt['id']}-{theme['id']}-{moral['id']}-{serial:03d}"
    if extra_id:
        tid = f"{tid}-{extra_id}"
    prompt = (
        "children's picture book illustration, watercolor, warm light, child-safe, "
        "no text in the image, no logos, no watermark, not photorealistic, not horror, "
        f"{theme['prompt']}, {fmt['flavor']}, {companion['en']} nearby, mood of {moral['en']}"
    )
    return {
        "id": tid,
        "title_he": title,
        "theme": theme["id"],
        "moral_he": moral["he"],
        "moral_id": moral["id"],
        "format": fmt["id"],
        "age_min": age_min,
        "age_max": age_max,
        "companion": companion["id"],
        "illustration_prompt_en": prompt,
        "beats": beats,
        "variant": v,
    }


def build_all_templates() -> list[dict[str, Any]]:
    """18 themes × 15 formats = 270 unique theme+format pairs."""
    templates: list[dict[str, Any]] = []
    serial = 0
    for fi, fmt in enumerate(FORMATS):
        for ti, theme in enumerate(THEMES):
            serial += 1
            i = serial - 1
            moral = MORALS[i % len(MORALS)]
            companion = COMPANIONS[(i * 5) % len(COMPANIONS)]
            age_min, age_max = AGE_BANDS[i % len(AGE_BANDS)]
            variant = (fi + ti) % 3
            templates.append(
                make_template(theme, fmt, moral, companion, variant, age_min, age_max, serial)
            )
    ids = [t["id"] for t in templates]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate template ids")
    if len(templates) < 250:
        raise RuntimeError(f"only {len(templates)} templates")
    return templates


def required_keys_ok(t: dict[str, Any]) -> bool:
    keys = {
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
    }
    if not keys.issubset(t.keys()):
        return False
    beats = t["beats"]
    need = {"opening", "event_1", "event_2", "event_3", "turning", "moral_landing", "bedtime_close"}
    return need.issubset(beats.keys())
