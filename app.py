"""Sipur — personalized Hebrew bedtime stories."""

from __future__ import annotations

import os

from flask import Flask, abort, redirect, render_template, request, url_for

from illustrator import page_svg
from story_generator import (
    decode_story,
    encode_story,
    generate_story,
    validate_input,
)

app = Flask(__name__)


def _form_values(req=None) -> dict:
    src = req.form if req is not None else {}
    return {
        "name": (src.get("name") or "").strip(),
        "age": src.get("age") or "",
        "event1": (src.get("event1") or "").strip(),
        "event2": (src.get("event2") or "").strip(),
        "event3": (src.get("event3") or "").strip(),
    }


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
    pages = []
    name = story.get("name") or ""
    seed = int(story.get("seed") or 1)
    companion = story.get("companion") or "moon"
    for i, page in enumerate(story.get("pages") or []):
        pages.append(
            {
                "text": page.get("t") or "",
                "svg": page_svg(page, name, seed, companion, i),
            }
        )
    if not pages:
        abort(404)
    return render_template("story.html", story=story, pages=pages, token=token)


@app.get("/health")
def health():
    return {"ok": True}


@app.errorhandler(404)
def not_found(_e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
