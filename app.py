"""Sipur — personalized Hebrew bedtime stories."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

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

FEEDBACK: list[dict] = []
FEEDBACK_PATH = Path(__file__).resolve().parent / "data" / "feedback.jsonl"


def _form_values(req=None) -> dict:
    src = req.form if req is not None else {}
    return {
        "name": (src.get("name") or "").strip(),
        "age": src.get("age") or "",
        "event1": (src.get("event1") or "").strip(),
        "event2": (src.get("event2") or "").strip(),
        "event3": (src.get("event3") or "").strip(),
    }


def _decorate_pages(story: dict) -> list[dict]:
    pages = []
    name = story.get("name") or ""
    seed = int(story.get("seed") or 1)
    companion = story.get("companion") or "moon"
    age = int(story.get("age") or 6)
    for i, page in enumerate(story.get("pages") or []):
        pages.append(
            {
                "text": page.get("t") or "",
                "svg": page_svg(page, name, seed, companion, i),
                "image_url": page_image_url(page, seed, i, age=age),
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
    story = generate_story(values["name"], int(values["age"]), events)
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
    return render_template("story.html", story=story, pages=pages, token=token)


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
    data = request.get_json(silent=True) or {}
    rating = str(data.get("rating") or "").strip()[:40]
    if rating not in {"אהבתי", "פחות אהבתי", "loved", "less"}:
        # still accept Hebrew product ratings and a couple of aliases
        if not rating:
            return jsonify({"ok": False, "error": "rating required"}), 400
    item = {
        "token": str(data.get("token") or "")[:8000],
        "rating": rating,
        "note": str(data.get("note") or "")[:500],
        "template_id": str(data.get("template_id") or "")[:200],
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    FEEDBACK.append(item)
    try:
        FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
        with FEEDBACK_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(item, ensure_ascii=False) + "\n")
    except OSError:
        pass
    return jsonify({"ok": True})


@app.get("/api/feedback")
def api_feedback_get():
    return jsonify(list(reversed(FEEDBACK[-50:])))


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
