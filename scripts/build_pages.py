#!/usr/bin/env python3
"""Build a server-free GitHub Pages entry point around the shared Python engine."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app import app, _demo_story
from illustrator import page_image_url, page_svg
from story_generator import encode_story

ROUTES = {'/':'index.html', '/create':'create.html', '/library':'library.html', '/privacy':'privacy.html', '/demo':'reader.html'}

def static_html(html):
    html = html.replace('<html lang="he" dir="rtl">', '<html lang="he" dir="rtl" data-static="true">')
    html = html.replace('/demo?world=', './reader.html?demo=')
    for route, target in sorted(ROUTES.items(), key=lambda x:len(x[0]), reverse=True):
        html = html.replace('href="' + route + '"', 'href="./' + target + '"')
        html = html.replace('action="' + route + '"', 'action="./' + target + '"')
    html = html.replace('src="/static/', 'src="./static/').replace('href="/static/', 'href="./static/')
    html = html.replace('</body>', '  <script src="./static/js/pages.js" defer></script>\n</body>')
    return html

with app.test_client() as client:
    for route, name in ROUTES.items():
        html = client.get(route).get_data(as_text=True)
        html = static_html(html)
        if name == 'reader.html':
            html = re.sub(r'<section class="book-page.*?</section>', '', html, flags=re.S)
            html = html.replace('<article\n', '<p class="privacy-note" data-engine-status role="status">פותחים את הספר…</p>\n<article\n',1)
        if name == 'privacy.html':
            html = html.replace('שם או כינוי, גיל ותוכן הספר מקודדים בתוך הקישור לסיפור.', 'שם או כינוי, גיל ותוכן הספר מקודדים אחרי סימן # בקישור לסיפור. חלק זה אינו נשלח לשרת GitHub Pages.')
            html = html.replace('משוב שולח רק דירוג ומזהה תבנית, ללא שם, קישור לסיפור או הערה חופשית. אין ממשק ציבורי לקריאת משובים.', 'משוב שומר רק דירוג ומזהה תבנית בדפדפן שלכם. הוא אינו נשלח לשרת או לבעל הפרויקט. אין איסוף שמות, קישורים לסיפורים או הערות חופשיות.')
            html = html.replace('האתר טוען גופנים מ־Google Fonts. שרת האחסון עשוי לתעד בקשות, כתובות IP וכתובות עמודים לפי ההגדרות שלו. דפי הסיפורים מבקשים ממנועי חיפוש לא לאנדקס אותם, ומוגשים ללא שמירה במטמון וללא העברת כתובת הסיפור כ־referrer. אלה אינם תחליף לבקרת גישה.', 'האתר טוען גופנים מ־Google Fonts ומנוע הרצת Python מדפדפן CDN של jsDelivr. יצירת הסיפור מתבצעת במכשיר, ללא שליחת שם, גיל או רגעים לשירות חיצוני. ספקי האחסון עשויים לתעד כתובות IP ובקשות לקבצים. הסיפורים בקישורים משותפים נמצאים אחרי סימן # ואינם נכללים בבקשת השרת. אין העברת כתובת הסיפור כ־referrer. אלה אינם תחליף לבקרת גישה.')
        if name == 'reader.html':
            html = html.replace('<meta name="theme-color"', '<meta name="robots" content="noindex,nofollow" />\n  <meta name="theme-color"')
        (ROOT / name).write_text(html,encoding='utf-8')

for world in ('forest','sea'):
    story = _demo_story(world)
    art = [{'svg':page_svg(p,story['name'],story['seed'],story.get('companion') or 'moon',i),
            'image':page_image_url(p,story['seed'],i)} for i,p in enumerate(story['pages'])]
    (ROOT/'data'/f'demo-{world}.json').write_text(json.dumps({'story':story,'token':encode_story(story),'art':art},ensure_ascii=False),encoding='utf-8')
(ROOT/'.nojekyll').write_text('Static site; no Jekyll processing.\n', encoding='utf-8')
print('Built 5 Pages documents and 2 fictional demo books.')
