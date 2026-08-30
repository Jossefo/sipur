"""Original SVG illustrations derived from a story page."""

from __future__ import annotations

import hashlib
import random
from xml.sax.saxutils import escape


PALETTES = (
    # dusk apricot
    {"sky1": "#f3d3b0", "sky2": "#c9846a", "ink": "#3a2a22", "warm": "#f7e6cf", "accent": "#d9783a", "deep": "#5c3d3a", "soft": "#e7b48a"},
    # sage evening
    {"sky1": "#e7ecd8", "sky2": "#8aa17a", "ink": "#2c3326", "warm": "#f4efe2", "accent": "#c45c26", "deep": "#4a5a40", "soft": "#c5d1a8"},
    # lilac paper
    {"sky1": "#f0e4f2", "sky2": "#9a7ea8", "ink": "#32283a", "warm": "#fff6ea", "accent": "#c46b4a", "deep": "#5a4660", "soft": "#d4c0d8"},
    # honey night
    {"sky1": "#f6e2b8", "sky2": "#6d6a8d", "ink": "#2b241c", "warm": "#fff4d8", "accent": "#e0a04a", "deep": "#3f3c5c", "soft": "#d9c48a"},
    # terracotta window
    {"sky1": "#fde7d2", "sky2": "#c45c26", "ink": "#2b2218", "warm": "#fffaf4", "accent": "#9a4318", "deep": "#6b3a28", "soft": "#f0c9a8"},
    # sea dusk
    {"sky1": "#dce8ea", "sky2": "#5d7a86", "ink": "#243038", "warm": "#f7f1e8", "accent": "#d08a4c", "deep": "#3a5560", "soft": "#b7cdd3"},
)


def _rng(seed: int, extra: str) -> random.Random:
    h = hashlib.sha256(f"{seed}:{extra}".encode("utf-8")).digest()
    return random.Random(int.from_bytes(h[:8], "big"))


def _stars(rng: random.Random, n: int, pal: dict, y0: int = 20, y1: int = 180) -> str:
    parts = []
    for _ in range(n):
        x = rng.randint(20, 780)
        y = rng.randint(y0, y1)
        r = rng.choice((1.2, 1.6, 2.1, 2.8))
        o = rng.uniform(0.35, 0.9)
        parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{pal["warm"]}" opacity="{o:.2f}"/>')
        if r > 2:
            parts.append(
                f'<path d="M{x},{y-6} L{x+1.1},{y-1.1} L{x+6},{y} L{x+1.1},{y+1.1} '
                f'L{x},{y+6} L{x-1.1},{y+1.1} L{x-6},{y} L{x-1.1},{y-1.1} Z" '
                f'fill="{pal["warm"]}" opacity="{o*0.55:.2f}"/>'
            )
    return "\n".join(parts)


def _hills(rng: random.Random, pal: dict, y: int = 340) -> str:
    c1 = pal["deep"]
    c2 = pal["sky2"]
    d1 = f"M0,{y+80} C{rng.randint(80,160)},{y-40} {rng.randint(260,340)},{y+50} 420,{y+10} C580,{y-30} 700,{y+40} 800,{y} L800,500 L0,500 Z"
    d2 = f"M0,{y+40} C180,{y-20} 300,{y+70} 480,{y+8} C640,{y-35} 740,{y+30} 800,{y+18} L800,500 L0,500 Z"
    return (
        f'<path d="{d1}" fill="{c1}" opacity="0.55"/>'
        f'<path d="{d2}" fill="{c2}" opacity="0.7"/>'
    )


def _moon(cx: int, cy: int, pal: dict, wax: bool = True) -> str:
    if wax:
        return (
            f'<circle cx="{cx}" cy="{cy}" r="42" fill="{pal["warm"]}"/>'
            f'<circle cx="{cx+14}" cy="{cy-6}" r="34" fill="{pal["sky2"]}" opacity="0.95"/>'
        )
    return (
        f'<circle cx="{cx}" cy="{cy}" r="38" fill="{pal["warm"]}"/>'
        f'<circle cx="{cx-8}" cy="{cy+10}" r="7" fill="{pal["soft"]}" opacity="0.5"/>'
        f'<circle cx="{cx+12}" cy="{cy-8}" r="4" fill="{pal["soft"]}" opacity="0.4"/>'
    )


def _window(pal: dict, x: int = 470, y: int = 90) -> str:
    return f'''
    <rect x="{x}" y="{y}" width="210" height="250" rx="18" fill="{pal["ink"]}" opacity="0.18"/>
    <rect x="{x+12}" y="{y+12}" width="186" height="226" rx="12" fill="{pal["sky2"]}"/>
    <rect x="{x+12}" y="{y+12}" width="186" height="226" rx="12" fill="{pal["warm"]}" opacity="0.28"/>
    <path d="M{x+105} {y+12} V{y+238}" stroke="{pal["warm"]}" stroke-width="8" opacity="0.55"/>
    <path d="M{x+12} {y+125} H{x+198}" stroke="{pal["warm"]}" stroke-width="8" opacity="0.55"/>
    <rect x="{x}" y="{y+250}" width="210" height="18" rx="4" fill="{pal["deep"]}" opacity="0.55"/>
    '''


def _tree(rng: random.Random, x: int, y: int, pal: dict) -> str:
    w = rng.randint(50, 90)
    h = rng.randint(70, 120)
    return (
        f'<rect x="{x-6}" y="{y}" width="12" height="{int(h*0.55)}" rx="4" fill="{pal["deep"]}"/>'
        f'<ellipse cx="{x}" cy="{y-10}" rx="{w}" ry="{int(h*0.55)}" fill="{pal["sky2"]}"/>'
        f'<ellipse cx="{x-18}" cy="{y+8}" rx="{int(w*0.55)}" ry="{int(h*0.35)}" fill="{pal["deep"]}" opacity="0.35"/>'
    )


def _figure(x: int, y: int, pal: dict, scale: float = 1.0, sit: bool = False) -> str:
    s = scale
    head = f'<circle cx="{x}" cy="{y}" r="{14*s}" fill="{pal["warm"]}" stroke="{pal["ink"]}" stroke-width="1.5"/>'
    if sit:
        body = (
            f'<path d="M{x},{y+12*s} C{x-28*s},{y+38*s} {x+36*s},{y+40*s} {x+8*s},{y+22*s}" '
            f'fill="{pal["accent"]}"/>'
        )
    else:
        body = (
            f'<path d="M{x},{y+12*s} C{x-22*s},{y+18*s} {x-20*s},{y+70*s} {x},{y+68*s} '
            f'C{x+22*s},{y+70*s} {x+20*s},{y+18*s} {x},{y+12*s} Z" fill="{pal["accent"]}"/>'
        )
    return head + body


def _companion(kind: str, rng: random.Random, pal: dict) -> str:
    x, y = rng.choice(((70, 80), (680, 70), (120, 300), (640, 310), (400, 70)))
    if kind == "moon":
        return _moon(x, y if y < 200 else 90, pal, wax=rng.random() > 0.4)
    if kind == "fox":
        return f'''
        <g transform="translate({x},{y})">
          <ellipse cx="0" cy="10" rx="28" ry="16" fill="{pal["accent"]}"/>
          <circle cx="18" cy="-2" r="12" fill="{pal["accent"]}"/>
          <path d="M10,-10 L16,-28 L24,-6 Z" fill="{pal["deep"]}"/>
          <path d="M20,-10 L30,-26 L32,-4 Z" fill="{pal["deep"]}"/>
          <circle cx="22" cy="-2" r="1.6" fill="{pal["ink"]}"/>
          <path d="M28,2 Q36,8 30,10" stroke="{pal["ink"]}" fill="none" stroke-width="1.5"/>
        </g>'''
    if kind == "bird":
        return f'''
        <g transform="translate({x},{y})">
          <path d="M-30,0 Q0,-28 32,0 Q0,12 -30,0 Z" fill="{pal["deep"]}"/>
          <circle cx="18" cy="-2" r="7" fill="{pal["accent"]}"/>
          <circle cx="20" cy="-3" r="1.4" fill="{pal["warm"]}"/>
        </g>'''
    if kind == "lamp":
        return f'''
        <g transform="translate({x},{min(y, 220)})">
          <rect x="-6" y="40" width="12" height="70" fill="{pal["deep"]}"/>
          <path d="M-40,40 Q0,-10 40,40 Z" fill="{pal["accent"]}"/>
          <ellipse cx="0" cy="40" rx="40" ry="8" fill="{pal["warm"]}" opacity="0.8"/>
          <circle cx="0" cy="18" r="10" fill="{pal["warm"]}" opacity="0.9"/>
        </g>'''
    # paper star
    return f'''
    <g transform="translate({x},{y}) rotate({rng.randint(-20,20)})">
      <path d="M0,-28 L8,-8 L28,-8 L12,4 L18,24 L0,12 L-18,24 L-12,4 L-28,-8 L-8,-8 Z"
            fill="{pal["warm"]}" stroke="{pal["accent"]}" stroke-width="2"/>
    </g>'''


def _bed(pal: dict) -> str:
    return f'''
    <rect x="90" y="330" width="420" height="90" rx="28" fill="{pal["deep"]}" opacity="0.85"/>
    <rect x="110" y="300" width="380" height="70" rx="26" fill="{pal["accent"]}"/>
    <rect x="130" y="292" width="140" height="36" rx="16" fill="{pal["warm"]}"/>
    <path d="M250,320 C320,280 420,340 470,318" stroke="{pal["warm"]}" stroke-width="10" fill="none" opacity="0.7"/>
    '''


def _cake(pal: dict) -> str:
    return f'''
    <ellipse cx="260" cy="360" rx="70" ry="18" fill="{pal["deep"]}" opacity="0.25"/>
    <rect x="200" y="300" width="120" height="50" rx="10" fill="{pal["warm"]}"/>
    <rect x="200" y="278" width="120" height="32" rx="12" fill="{pal["accent"]}"/>
    <rect x="214" y="248" width="8" height="30" fill="{pal["deep"]}"/>
    <rect x="256" y="242" width="8" height="36" fill="{pal["deep"]}"/>
    <rect x="296" y="248" width="8" height="30" fill="{pal["deep"]}"/>
    <circle cx="218" cy="244" r="6" fill="{pal["sky1"]}"/>
    <circle cx="260" cy="238" r="6" fill="{pal["sky1"]}"/>
    <circle cx="300" cy="244" r="6" fill="{pal["sky1"]}"/>
    '''


def _scene_body(scene: str, rng: random.Random, pal: dict, name: str) -> str:
    bits = [_hills(rng, pal), _stars(rng, rng.randint(8, 18), pal)]
    if scene == "window":
        bits.append(_window(pal))
        bits.append(_moon(160, 110, pal))
        bits.append(_figure(250, 300, pal, sit=True))
    elif scene == "hallway":
        bits.append(f'<rect x="80" y="80" width="180" height="320" rx="8" fill="{pal["deep"]}" opacity="0.35"/>')
        bits.append(f'<rect x="300" y="120" width="140" height="280" rx="8" fill="{pal["accent"]}" opacity="0.35"/>')
        bits.append(f'<rect x="520" y="70" width="160" height="330" rx="8" fill="{pal["deep"]}" opacity="0.22"/>')
        bits.append(f'<ellipse cx="400" cy="430" rx="220" ry="24" fill="{pal["ink"]}" opacity="0.12"/>')
        bits.append(_figure(390, 260, pal))
    elif scene == "tooth":
        bits.append(_bed(pal))
        bits.append(
            f'<path d="M560,160 C540,120 580,90 610,120 C640,90 680,120 660,160 C650,210 570,210 560,160 Z" fill="{pal["warm"]}" stroke="{pal["accent"]}" stroke-width="3"/>'
        )
        bits.append(_stars(rng, 6, pal, 90, 200))
        bits.append(_figure(240, 250, pal, sit=True))
    elif scene == "kitchen":
        bits.append(f'<rect x="40" y="260" width="720" height="24" fill="{pal["deep"]}" opacity="0.4"/>')
        bits.append(_cake(pal))
        bits.append(_figure(430, 220, pal, scale=0.9))
        bits.append(_figure(510, 200, pal, scale=1.15))
        bits.append(f'<rect x="560" y="90" width="160" height="170" rx="12" fill="{pal["sky2"]}" opacity="0.55"/>')
        bits.append(_window(pal, 560, 70))
    elif scene == "nightlight":
        bits.append(_bed(pal))
        bits.append(f'<circle cx="640" cy="220" r="70" fill="{pal["warm"]}" opacity="0.35"/>')
        bits.append(f'<circle cx="640" cy="220" r="28" fill="{pal["accent"]}"/>')
        bits.append(_moon(180, 100, pal))
        bits.append(_figure(250, 250, pal, sit=True))
    elif scene == "water":
        bits.append(f'<path d="M0,300 C120,260 200,340 320,300 C460,250 560,340 800,290 L800,500 L0,500 Z" fill="{pal["sky2"]}" opacity="0.8"/>')
        bits.append(f'<path d="M0,360 C160,320 280,400 440,350 C600,300 700,390 800,350 L800,500 L0,500 Z" fill="{pal["deep"]}" opacity="0.45"/>')
        bits.append(_moon(620, 110, pal, wax=False))
        bits.append(_figure(200, 250, pal))
    elif scene == "rain":
        rain = []
        for _ in range(40):
            x = rng.randint(20, 780)
            y = rng.randint(20, 280)
            rain.append(f'<path d="M{x},{y} l{4} {18}" stroke="{pal["deep"]}" stroke-width="2" opacity="0.35"/>')
        bits.append("".join(rain))
        bits.append(_tree(rng, 160, 300, pal))
        bits.append(_tree(rng, 640, 310, pal))
        bits.append(_figure(400, 250, pal))
    elif scene == "bike":
        bits.append(f'<circle cx="300" cy="360" r="50" fill="none" stroke="{pal["ink"]}" stroke-width="6"/>')
        bits.append(f'<circle cx="470" cy="360" r="50" fill="none" stroke="{pal["ink"]}" stroke-width="6"/>')
        bits.append(f'<path d="M300,360 L380,360 L430,280 L470,360 M380,360 L350,280 H430" stroke="{pal["accent"]}" stroke-width="6" fill="none" stroke-linecap="round"/>')
        bits.append(_figure(410, 210, pal, scale=0.85))
    elif scene == "dog":
        bits.append(_figure(300, 230, pal))
        bits.append(f'''
        <g transform="translate(430,340)">
          <ellipse cx="0" cy="0" rx="40" ry="22" fill="{pal["deep"]}"/>
          <circle cx="34" cy="-10" r="16" fill="{pal["deep"]}"/>
          <path d="M24,-22 L28,-36 L40,-16" fill="{pal["accent"]}"/>
          <ellipse cx="-30" cy="10" rx="10" ry="6" fill="{pal["accent"]}"/>
        </g>''')
    elif scene == "cat":
        bits.append(_figure(280, 240, pal, sit=True))
        bits.append(f'''
        <g transform="translate(500,340)">
          <ellipse cx="0" cy="8" rx="32" ry="16" fill="{pal["deep"]}"/>
          <circle cx="24" cy="-6" r="14" fill="{pal["deep"]}"/>
          <path d="M14,-16 L16,-32 L26,-10 Z" fill="{pal["accent"]}"/>
          <path d="M26,-16 L36,-32 L38,-8 Z" fill="{pal["accent"]}"/>
          <path d="M-28,8 Q-50,-40 -10,-8" fill="none" stroke="{pal["accent"]}" stroke-width="4"/>
        </g>''')
    elif scene == "school":
        bits.append(f'<rect x="180" y="160" width="280" height="200" rx="8" fill="{pal["deep"]}" opacity="0.8"/>')
        for i in range(3):
            for j in range(2):
                bits.append(f'<rect x="{210+i*80}" y="{190+j*70}" width="40" height="36" rx="4" fill="{pal["warm"]}"/>')
        bits.append(f'<polygon points="170,160 320,80 470,160" fill="{pal["accent"]}"/>')
        bits.append(_figure(560, 250, pal))
    elif scene == "party":
        bits.append(_cake(pal))
        for i, x in enumerate((140, 220, 640, 710)):
            bits.append(f'<path d="M{x},80 q10,40 0,90" stroke="{pal["deep"]}" fill="none" stroke-width="3"/>')
            bits.append(f'<ellipse cx="{x}" cy="70" rx="16" ry="22" fill="{pal["accent"] if i%2==0 else pal["warm"]}"/>')
        bits.append(_figure(480, 230, pal))
    elif scene == "blanket":
        bits.append(_bed(pal))
        bits.append(f'<path d="M80,360 C200,300 360,420 520,330 C620,280 760,380 800,340 L800,500 L0,500 Z" fill="{pal["accent"]}" opacity="0.55"/>')
        bits.append(_figure(260, 250, pal, sit=True))
        bits.append(_moon(640, 120, pal))
    elif scene == "bedtime":
        bits.append(_bed(pal))
        bits.append(_window(pal, 500, 70))
        bits.append(_moon(160, 100, pal, wax=True))
        bits.append(_figure(250, 250, pal, sit=True))
        bits.append(f'<circle cx="400" cy="200" r="90" fill="{pal["warm"]}" opacity="0.15"/>')
    elif scene == "sky":
        bits.append(_moon(400, 150, pal, wax=False))
        bits.append(_stars(rng, 22, pal, 30, 260))
        bits.append(_figure(240, 300, pal, sit=True))
    else:  # garden / default
        bits.append(_tree(rng, 140, 300, pal))
        bits.append(_tree(rng, 250, 320, pal))
        bits.append(_tree(rng, 660, 290, pal))
        bits.append(_figure(420, 250, pal))
        bits.append(_moon(520, 90, pal, wax=rng.random() > 0.5))

    door = escape(name[:1] or "ס")
    bits.append(
        f'<g transform="translate(36,430)">'
        f'<circle cx="0" cy="0" r="22" fill="{pal["warm"]}" stroke="{pal["accent"]}" stroke-width="2"/>'
        f'<text x="0" y="7" text-anchor="middle" font-size="18" fill="{pal["ink"]}" '
        f'font-family="Frank Ruhl Libre, serif">{door}</text></g>'
    )
    return "\n".join(bits)


def page_svg(page: dict, name: str, seed: int, companion: str, index: int) -> str:
    text = page.get("t") or ""
    scene = page.get("k") or "garden"
    rng = _rng(seed, f"{index}:{scene}:{text[:80]}")
    pal = PALETTES[rng.randrange(len(PALETTES))]
    body = _scene_body(scene, rng, pal, name)
    friend = _companion(companion, rng, pal)
    gid = f"g{index}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" role="img" aria-label="איור לעמוד הסיפור">
  <defs>
    <linearGradient id="sky-{gid}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{pal["sky1"]}"/>
      <stop offset="1" stop-color="{pal["sky2"]}"/>
    </linearGradient>
    <radialGradient id="glow-{gid}" cx="50%" cy="30%" r="70%">
      <stop offset="0" stop-color="{pal["warm"]}" stop-opacity="0.9"/>
      <stop offset="1" stop-color="{pal["sky2"]}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="800" height="500" fill="url(#sky-{gid})"/>
  <rect width="800" height="500" fill="url(#glow-{gid})" opacity="0.55"/>
  {body}
  {friend}
</svg>'''
