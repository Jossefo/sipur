<div align="center">

# ☾ סיפור · Sipur

### Small moments. Big stories.

Turn three moments from a child's week into an illustrated Hebrew bedtime book.

**Hebrew & RTL · Ages 3–9 · 270 story templates · No signup · No runtime API keys**

[What it does](#a-little-week-a-whole-world) · [See the app](#a-look-inside) · [Run locally](#run-locally) · [Privacy](#privacy-by-design-and-its-limits)

</div>

![Sipur desktop — a warm, illustrated Hebrew bedtime-story experience](docs/screenshots/desktop.png)

## A little week. A whole world.

A lost tooth. Baking with Grandma. Making a new friend. Sipur turns those small, real moments into a 6–8 page Hebrew picture book, with a gentle moral and a quiet ending for bedtime.

The experience is deliberately simple: enter a first name or nickname, an age, and three moments; then read together. No account, payment flow, or language-model service is required.

- **Stories grounded in the week.** An event-driven Hebrew narrative engine combines concrete events with 270 templates, age-aware language, companions, settings, and morals.
- **Original visual world.** Three bundled, AI-generated gouache-style illustrations and a procedural SVG scene library, served locally. No image hotlinks or external image generation at runtime.
- **A proper little reader.** Page controls, keyboard navigation, touch swipes on artwork, reading progress, night mode, and a print layout for the full book.
- **Your own shelf.** Books are saved in the current browser, with individual removal. The fictional demo never adds itself to your library.
- **Made for Hebrew.** Right-to-left layouts, considered Hebrew typography, a responsive form, visible focus states, and reduced-motion support.

## A look inside

These are actual local app captures, using fictional sample data.

<table>
<tr><th>Made for small screens</th><th>The illustrated reader</th></tr>
<tr>
<td width="30%" align="center"><img src="docs/screenshots/mobile.png" width="260" alt="Sipur mobile homepage with Hebrew introduction and original storybook artwork" /></td>
<td width="70%" valign="top"><img src="docs/screenshots/reader.png" alt="Hebrew picture-book reader with local illustrations, page navigation and privacy guidance" /></td>
</tr>
</table>

<details>
<summary>Open the night-mode preview</summary>

![Sipur reader in night mode](docs/screenshots/night-mode.png)

</details>

### The artwork

![A whole world unfolds from a bedtime book](static/images/bedtime-world.webp)

| A lantern in the forest | A paper boat at dusk |
| --- | --- |
| ![A child and fox follow a softly lit forest path](static/images/lantern-forest.webp) | ![A child and rabbit watch a lantern-lit paper boat](static/images/paper-boat.webp) |

The artwork is bundled with the repository, so it is visible here and works without an image API. It is curated scene art, not a newly generated image for every book. [Artwork notes and generation prompts](docs/artwork.md).

## Run locally

Requires Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open [localhost:3000](http://localhost:3000). Try `/demo` for a fictional example, `/create` for your own story, or `/library` for your saved books.

The 270-template catalog is included. To rebuild it:

```bash
python scripts/build_templates.py
```

## How it works

```text
First name / nickname + age + 3 weekly moments
                      ↓
Hebrew event classification + template selection
                      ↓
Concrete scenes → gentle turning point → bedtime ending
                      ↓
6–8 page book + local artwork + procedural SVG scenes
                      ↓
Browser library / self-contained share link / print
```

Built with **Python, Flask, Jinja, vanilla JavaScript, CSS and SVG**. Stories are composed in Python; the generative artwork was created during development and committed as optimized WebP files. There is no language-model or image-model call when someone creates a story.

Template selection avoids fingerprints already produced by the current server process. This is not a global uniqueness guarantee across deployments or multiple workers.

## Privacy by design, and its limits

**A story link contains the story. Encoding is not encryption.** The name or nickname, age and generated pages are compressed into the URL. Anyone who receives the link can read or decode it. Use fictional examples or a first name/nickname and avoid sensitive details. Shared links cannot be revoked.

- No account database. The library lives in `localStorage` in that browser; clearing browser data removes the shelf.
- No story content is sent to an external image service. Google Fonts is still used for typography.
- Feedback accepts only a rating and a validated template ID. It discards story tokens and free-text notes, keeps at most 200 anonymous entries in memory, and has no public reading endpoint. Feedback is intentionally non-durable.
- Story responses use `Cache-Control: private, no-store`, `Referrer-Policy: no-referrer` and `X-Robots-Tag: noindex, nofollow`. These are best-effort precautions, not access controls.
- Request bodies and decoded story payloads are size-limited. Malformed story structures are rejected. A content security policy limits browser resource origins.
- The hosting provider may still log request URLs and IP addresses. Review hosting/log-retention settings before using real family information.

The in-app `/privacy` page explains these choices in Hebrew. This is a personal project and a public source-code showcase, not an authenticated private family archive.

## Checks

```bash
pytest -q
node --check static/js/app.js
```

The suite covers story generation, weekly-event relevance, Hebrew theme classification, share-link round trips, malformed payloads, decompression limits, private headers, bundled images, anonymous feedback and request size limits.

## Deploy on Render

`render.yaml` describes a Python web service. Use:

```text
Build: pip install -r requirements.txt
Start: gunicorn -b 0.0.0.0:$PORT app:app
Health endpoint: /health
```

This is a server-rendered Flask application; it requires a Python web service. No paid external AI service or API key is required. Hosting availability and pricing depend on your provider.

---

<div align="center">מהיום שהיה, ללילה של דמיון. ☾<br />From the day that was, to a night of imagination.</div>
