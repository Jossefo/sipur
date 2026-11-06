"""Sipur — personalized Hebrew bedtime stories."""

from __future__ import annotations

import os
from collections import deque
from functools import lru_cache
import random
import re

from flask import Flask, abort, jsonify, redirect, render_template, request, url_for

from illustrator import page_image_url, page_svg
from story_generator import (
    catalog_stats,
    decode_story,
    encode_story,
    generate_story,
    validate_input,
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

# Anonymous, bounded and ephemeral: never retain story tokens or free-text notes.
FEEDBACK: deque[dict] = deque(maxlen=200)


@app.after_request
def privacy_headers(response):
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; script-src 'self'; "
        "connect-src 'self'; object-src 'none'; base-uri 'self'; "
        "form-action 'self'; frame-ancestors 'none'"
    )
    if request.path.startswith(("/s/", "/api/", "/create", "/library")):
        response.headers["Cache-Control"] = "private, no-store"
        response.headers["X-Robots-Tag"] = "noindex, nofollow"
    return response


def _form_values(req=None) -> dict:
    src = req.form if req is not None else {}
    return {
        "name": (src.get("name") or "").strip(),
        "age": src.get("age") or "",
        "gender": src.get("gender") if src.get("gender") in ("f", "m") else "",
        "event1": (src.get("event1") or "").strip(),
        "event2": (src.get("event2") or "").strip(),
        "event3": (src.get("event3") or "").strip(),
    }


def _decorate_pages(story: dict) -> list[dict]:
    pages = []
    name = story.get("name") or ""
    seed = int(story.get("seed") or 1)
    companion = story.get("companion") or "moon"
    for i, page in enumerate(story.get("pages") or []):
        pages.append(
            {
                "text": page.get("t") or "",
                "svg": page_svg(page, name, seed, companion, i),
                "image_url": page_image_url(page, seed, i),
                "kind": page.get("p") or "",
            }
        )
    return pages


@app.get("/")
def home():
    return render_template("home.html")


@app.get("/create")
def create_get():
    return render_template("create.html", errors=[], values=_form_values())


@app.post("/create")
def create_post():
    values = _form_values(request)
    events = [values["event1"], values["event2"], values["event3"]]
    errors = validate_input(values["name"], values["age"], events)
    if errors:
        return render_template("create.html", errors=errors, values=values), 400
    story = generate_story(values["name"], int(values["age"]), events, gender=values["gender"])
    token = encode_story(story)
    return redirect(url_for("story_page", token=token))


@app.get("/s/<token>")
def story_page(token: str):
    try:
        story = decode_story(token)
    except Exception:
        abort(404)
    pages = _decorate_pages(story)
    if not pages:
        abort(404)
    return render_template("story.html", story=story, pages=pages, token=token, is_demo=False)



@app.get("/privacy")
def privacy():
    return render_template("privacy.html")


@lru_cache(maxsize=2)
def _demo_story(world):
    events = (["טיילה ביער עם המשפחה", "עזרה לחבר למצוא את הדרך", "הקשיבה לציפורים"]
              if world == "forest" else
              ["השיטה סירת נייר", "חיכתה בסבלנות על החוף", "עזרה לחבר לאסוף צדפים"])
    return generate_story("נועה", 6, events, rng=random.Random(42 if world == "forest" else 73))


@app.get("/demo")
def demo():
    world = "sea" if request.args.get("world") == "sea" else "forest"
    story = _demo_story(world)
    return render_template("story.html", story=story, pages=_decorate_pages(story),
                           token=encode_story(story), is_demo=True)


@app.get("/library")
def library():
    return render_template("library.html")


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/api/catalog")
def api_catalog():
    return jsonify(catalog_stats())


@app.post("/api/feedback")
def api_feedback_post():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"ok": False, "error": "JSON object required"}), 400
    rating = data.get("rating")
    template_id = data.get("template_id", "")
    if rating not in ("אהבתי", "פחות אהבתי", "loved", "less"):
        return jsonify({"ok": False, "error": "invalid rating"}), 400
    if not isinstance(template_id, str) or not re.fullmatch(r"[a-z0-9-]{0,100}", template_id):
        return jsonify({"ok": False, "error": "invalid template"}), 400
    FEEDBACK.append({"rating": rating, "template_id": template_id})
    return jsonify({"ok": True})


# No public GET endpoint: feedback must never expose children's stories.
@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
