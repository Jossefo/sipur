"""Generate reproducible fictional books for human editorial review."""
from pathlib import Path
import random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from story_generator import generate_story

CASES = [
    ("נועה", 6, "f", ["איבדה שן", "אפתה עם סבתא", "פחדה מהחושך"]),
    ("איתי", 5, "m", ["רכב על אופניים", "רב עם חבר", "השלים עם החבר"]),
    ("מאיה", 4, "f", ["ציירה עם אמא", "שיחקה עם חתול", "אכלה גלידה"]),
    ("נועם", 8, "m", ["הפסיד במשחק", "למד לנגן בפסנתר", "עזר לאחותו"]),
    ("תמר", 7, "f", ["שיחקה עם חברים", "ראתה עצים בטיול", "כתבה מכתב לסבא"]),
    ("דני", 3, "m", ["היה אצל סבא", "בנה מגדל", "לא רצה ללכת לישון"]),
]

HEADER = """# Narrative quality: six complete fictional books

These examples were generated with fixed seeds and read for continuity, Hebrew phrasing, preservation of supplied facts, and whether the ending follows the opening question. They are examples for human review, not a numerical quality score.

The previous engine sometimes treated a fight as a cheerful sharing scene, inferred baking with Grandma from a visit to Grandpa, repeated two events in one passage, or put abstract memories on a bedside table. Version 3 plans facts and outcomes first. A shared bedtime memory-book frame connects unrelated events without inventing the order of the child's week.

The planner recognizes common Hebrew event/outcome phrases, scopes immediate negation, prefers the final stated outcome within a sentence, and selects among seven thematic arcs. It preserves sadness and unresolved problems. Runtime checks require all three events, distinct pages, an opening/closing frame, a resolution, and age-specific word limits. The explicit voice control handles ambiguous names.

**Validation:** 62 tests, including 120 generated books across six editorial cases and 20 seeds. Tests cover negation, reversal of outcomes, unresolved conflict, grief, first-person input, name-prefixed input, fragments, repeated events, grammatical voice and share-link round trips. The real browser worker was also checked through the form and reader.

**Limits:** this remains a bounded rule-based storyteller, using one memory-book frame. Complex Hebrew, sarcasm, who did what to whom, and nuanced time/negation are not fully understood. Structural checks cannot certify literary quality. Broader parent/editor review and more narrative frames remain necessary before claiming production-level narrative quality. Existing shared books retain their original text; generate a new book to use the new engine. Illustrations are curated scene art and procedural SVG, not literal renderings of each fact.

Reproduce these samples with `python scripts/evaluate_stories.py`; the optional first argument is an output Markdown path.

"""

def render():
    out = [HEADER]
    for i, (name, age, voice, events) in enumerate(CASES):
        story = generate_story(name, age, events, gender=voice, rng=random.Random(100+i))
        out += [f"## {story['title']}\n", f"Age: {age}; inputs: {' / '.join(events)}\n", f"Plan: `{story['narrative_plan']['arc']}`\n"]
        for number, page in enumerate(story['pages'], 1):
            out += [f"### Page {number}\n", page['t'] + "\n"]
        out += [f"Moral: {story['moral']}\n"]
    return "\n".join(out)

if __name__ == '__main__':
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'docs/story-quality.md'
    target.write_text(render(), encoding='utf8')
    print(f'Wrote six fictional review books to {target}')
