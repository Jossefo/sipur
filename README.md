# סיפור (Sipur)

Personalized Hebrew bedtime stories. A child gets a 5–7 page illustrated picture-book
story woven from their name, age, and three things that happened this week.

No API keys. Stories are generated on the server and encoded into a shareable URL,
so they survive refreshes even on an ephemeral disk.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
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
- `GET /health` — `{ok: true}`
