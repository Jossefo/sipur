# סיפור (Sipur)

Personalized Hebrew bedtime picture-books. A child gets a 6–8 page illustrated story
woven from their name, age, and three things that happened this week — with a kind
educational moral (מוסר השכל), never scary or mean.

No API keys. Stories are generated on the server from 250+ templates and encoded into
a shareable URL, so they survive refreshes even on an ephemeral disk. The same book
is never generated twice.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/build_templates.py   # writes data/templates.json (already in the repo)
python app.py
```

The app listens on `0.0.0.0` and `PORT` (default `3000`).

```bash
PORT=3000 python app.py
# or
gunicorn -b 0.0.0.0:3000 app:app
```

Open http://localhost:3000

## Tests

```bash
pytest -q
```

## Render

This is a **web service**, not a static site.

| Setting | Value |
| --- | --- |
| Runtime | Python |
| Plan | Free |
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn -b 0.0.0.0:$PORT app:app` |

`render.yaml` in the repo already describes this service.

## Routes

- `GET /` — home
- `GET /create` — story form
- `POST /create` — generate and redirect to a shareable story URL
- `GET /s/<token>` — picture-book reader (token holds the full story)
- `GET /library` — הספרים שלי (client library)
- `GET /health` — `{ok: true}`
- `GET /api/catalog` — `{template_count, formats, themes}`
- `POST /api/feedback` — `{token, rating, note, template_id}`
- `GET /api/feedback` — last 50 notes (no auth in v1)

Illustrations: each page has an original SVG placeholder, then a Pollinations image
(`model=flux`, no API key) that fades in when loaded.
