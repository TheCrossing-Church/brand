#!/usr/bin/env python3
"""Regenerates the do / don't example tiles in this folder from the real logo files.

Optional helper — NOT part of CI and not required to use the brand. Run it only if the
logo files in ../../logos/crossing/ change and the examples need to be redrawn:

    python3 samples/logo-usage/generate.py     # run from the repo root

Every tile is a self-contained SVG: the logo paths are inlined (no external references),
so the files render anywhere — GitHub, the brand site, a slide deck, an email.
"""

import os, re
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
G_TAG, PATH_TAG = "{%s}g" % SVG_NS, "{%s}path" % SVG_NS
ET.register_namespace("", SVG_NS)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "samples", "logo-usage")
STACKED = os.path.join(ROOT, "logos", "crossing", "crossing-stacked-blue.svg")
HORIZ = os.path.join(ROOT, "logos", "crossing", "crossing-horizontal-blue.svg")

# Brand colors (brand-kit.json)
LIMED_SPRUCE = "#425964"
DARK_SPRUCE  = "#34474E"
LIGHT_FOREST = "#919C67"
LIFEBLOOD    = "#A1302B"   # the "don't" red
BURNT_ORANGE = "#AA6327"
ARMADILLO    = "#3C3A36"
STONE_PATH   = "#605D58"
ASH          = "#A8A49B"
BISON_HIDE   = "#CBC4B8"
WHITE        = "#FFFFFF"

SANS = "'Nunito Sans','Helvetica Neue',Helvetica,Arial,sans-serif"
SERIF = "Georgia,'Times New Roman',serif"

W, H = 720, 524
ART = (56, 92, 608, 268)      # x, y, w, h — where the logo art goes
NUM = re.compile(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?')
CMD = re.compile(r'([MmLlHhVvCcSsQqTtAaZz])([^MmLlHhVvCcSsQqTtAaZz]*)')


def path_bbox(d):
    """Approximate bbox of a path (control points included — good enough for layout)."""
    x = y = sx = sy = 0.0
    xs, ys = [], []
    for c, argstr in CMD.findall(d):
        a = [float(v) for v in NUM.findall(argstr)]
        u, rel, i = c.upper(), c.islower(), 0
        if u == 'Z':
            x, y = sx, sy
            xs.append(x); ys.append(y)
            continue
        step = {'M': 2, 'L': 2, 'T': 2, 'H': 1, 'V': 1, 'C': 6, 'S': 4, 'Q': 4, 'A': 7}[u]
        while i + step <= len(a):
            seg = a[i:i + step]; i += step
            if u in ('M', 'L', 'T'):
                nx, ny = (x + seg[0], y + seg[1]) if rel else (seg[0], seg[1])
                if u == 'M':
                    sx, sy = nx, ny
                x, y = nx, ny
            elif u == 'H':
                x = x + seg[0] if rel else seg[0]
            elif u == 'V':
                y = y + seg[0] if rel else seg[0]
            elif u in ('C', 'S', 'Q'):
                pts = [(seg[j], seg[j + 1]) for j in range(0, len(seg), 2)]
                for px, py in pts:
                    ax, ay = (x + px, y + py) if rel else (px, py)
                    xs.append(ax); ys.append(ay)
                lx, ly = pts[-1]
                x, y = (x + lx, y + ly) if rel else (lx, ly)
            elif u == 'A':
                x, y = (x + seg[5], y + seg[6]) if rel else (seg[5], seg[6])
            xs.append(x); ys.append(y)
    return min(xs), min(ys), max(xs), max(ys)


def union(bbs):
    return (min(b[0] for b in bbs), min(b[1] for b in bbs),
            max(b[2] for b in bbs), max(b[3] for b in bbs))


def load_paths(svg_path):
    """Return [(markup, bbox)] for each top-level <g> in the file, classes stripped
    so fill is inherited from the <use> element instead of the file's own <style>.

    Parsed as XML rather than matched with a regex — the icon group has nested <g>
    elements, which a non-greedy pattern silently truncates."""
    tree = ET.parse(svg_path)
    groups = []
    for child in list(tree.getroot()):
        if child.tag != G_TAG:
            continue
        ds = [el.get("d") for el in child.iter(PATH_TAG) if el.get("d")]
        if not ds:
            continue
        for el in child.iter():
            el.attrib.pop("class", None)
        groups.append((ET.tostring(child, encoding="unicode"),
                       union([path_bbox(d) for d in ds])))
    return groups


stacked = load_paths(STACKED)
crossing_wm, the_wm, icon = stacked[0], stacked[1], stacked[2]
horiz = load_paths(HORIZ)

# Path data, emitted at most once per file.
PRIMS = {
    "p-icon":     icon[0],
    "p-the":      the_wm[0],
    "p-crossing": crossing_wm[0],
    "p-horiz":    "\n".join(g[0] for g in horiz),
}

# Reusable units, each built from the primitives above via <use> so no path is duplicated.
DEFS = {
    "logo":     (("p-icon", "p-the", "p-crossing"),
                 union([g[1] for g in (icon, the_wm, crossing_wm)])),
    "icon":     (("p-icon",), icon[1]),
    "wordmark": (("p-the", "p-crossing"),
                 union([g[1] for g in (the_wm, crossing_wm)])),
    "horiz":    (("p-horiz",), union([g[1] for g in horiz])),
}


def defs_for(markup):
    """Only the units (and their path data) this tile actually references."""
    used = [k for k in DEFS if 'href="#%s"' % k in markup]
    prims, out = [], []
    for k in used:
        for p in DEFS[k][0]:
            if p not in prims:
                prims.append(p)
    for p in prims:
        out.append('<g id="%s">%s</g>' % (p, PRIMS[p]))
    for k in used:
        out.append('<g id="%s">%s</g>' % (
            k, "".join('<use href="#%s"/>' % p for p in DEFS[k][0])))
    return "\n".join(out)


def fit(name, box, sx_mult=1.0, sy_mult=1.0, shrink=1.0):
    """Transform that fits DEFS[name] into box=(x,y,w,h), centered."""
    x0, y0, x1, y1 = DEFS[name][1]
    bx, by, bw, bh = box
    w, h = x1 - x0, y1 - y0
    s = min(bw / w, bh / h) * shrink
    sx, sy = s * sx_mult, s * sy_mult
    tx = bx + (bw - w * sx) / 2 - x0 * sx
    ty = by + (bh - h * sy) / 2 - y0 * sy
    return "translate(%.2f,%.2f) scale(%.5f,%.5f)" % (tx, ty, sx, sy)


def use(name, box, fill=LIMED_SPRUCE, **kw):
    return '<use href="#%s" fill="%s" transform="%s"/>' % (name, fill, fit(name, box, **kw))


def wrap(text, limit=82):
    """Greedy word wrap — SVG <text> does not wrap on its own."""
    lines, line = [], ""
    for word in text.split():
        candidate = (line + " " + word).strip()
        if len(candidate) > limit and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines[:2]


def tile(filename, title, verdict, caption, art, bg=WHITE, ink=ARMADILLO,
         sub_ink=STONE_PATH, border=BISON_HIDE, x_over=None):
    """verdict: 'do' | 'dont'. art: SVG markup for the example itself."""
    ok = verdict == "do"
    accent = LIGHT_FOREST if ok else LIFEBLOOD
    label = "DO" if ok else "DON'T"
    stroke = border if ok else LIFEBLOOD
    sw = 1.5 if ok else 2.5
    ax, ay, aw, ah = x_over or ART
    cross = "" if ok else (
        '<g stroke="%s" stroke-width="9" stroke-linecap="round" opacity="0.85">'
        '<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f"/>'
        '<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f"/></g>'
        % (LIFEBLOOD, ax, ay, ax + aw, ay + ah, ax, ay + ah, ax + aw, ay)
    )
    head, _, tail = caption.partition("|")
    tail_svg = "\n".join(
        '  <text x="30" y="%d" fill="%s" font-size="16.5">%s</text>' % (450 + 24 * i, sub_ink, ln)
        for i, ln in enumerate(wrap(tail.strip())))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">{label} — {title}</title>
<desc id="d">{head.strip()} {tail.strip()}</desc>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{bg}" stroke="{stroke}" stroke-width="{sw}"/>
<g font-family="{SANS}">
  <rect x="28" y="26" width="{104 if ok else 128}" height="32" rx="16" fill="{accent}"/>
  <text x="{80 if ok else 92}" y="48" fill="{WHITE}" font-size="16" font-weight="700" letter-spacing="1.6" text-anchor="middle">{label}</text>
{art}
{cross}
  <text x="30" y="420" fill="{ink}" font-size="22" font-weight="700">{head.strip()}</text>
{tail_svg}
</g>
<defs>
''' + defs_for(art) + '''
</defs>
</svg>
'''
    open(os.path.join(OUT, filename), "w", encoding="utf-8").write(svg)
    print("wrote", filename)


# ---------------------------------------------------------------- DO tiles
inner = (ART[0] + 96, ART[1] + 40, ART[2] - 192, ART[3] - 80)
tile("do-primary-stacked.svg", "primary logo, generous clear space", "do",
     "Stacked logo in Limed Spruce on white.|The primary lockup. Leave generous space around it — the dashed line is breathing room, not a boundary to fill.",
     art=f'''  <rect x="{ART[0]}" y="{ART[1]}" width="{ART[2]}" height="{ART[3]}" rx="8" fill="none" stroke="{ASH}" stroke-width="1.5" stroke-dasharray="7 6"/>
  {use("logo", inner, shrink=0.92)}''')

tile("do-white-on-dark.svg", "Pure White on a dark field", "do",
     "Pure White on a dark background.|Use the white logo on medium-to-dark backgrounds and photographs — never the dark logo on a dark field.",
     bg=DARK_SPRUCE, ink=WHITE, sub_ink=BISON_HIDE, border=DARK_SPRUCE,
     art=f'  {use("logo", inner, fill=WHITE, shrink=0.92)}')

band = (ART[0] + 20, ART[1] + (ART[3] - 124) // 2, ART[2] - 40, 124)
tile("do-horizontal-tight.svg", "horizontal lockup where stacked won't fit", "do",
     "Horizontal lockup in a short, wide space.|Reach for horizontal only when the stacked version genuinely won't fit — a narrow header, a banner, a sign rail.",
     art=f'''  <rect x="{band[0]}" y="{band[1]}" width="{band[2]}" height="{band[3]}" rx="6" fill="none" stroke="{ASH}" stroke-width="1.5" stroke-dasharray="7 6"/>
  {use("horiz", (band[0]+30, band[1]+24, band[2]-60, band[3]-48))}''')

# -------------------------------------------------------------- DON'T tiles
tile("dont-relationship.svg", "icon and wordmark rearranged", "dont",
     "Don't change the size or position of the icon against the text.|The lockup is fixed. Don't shrink the icon, move it beside the words, or re-space the two.",
     art=f'''  {use("icon", (ART[0]+56, ART[1]+92, 118, 118))}
  {use("wordmark", (ART[0]+212, ART[1]+64, 330, 150))}''')

tile("dont-wordmark-font.svg", "wordmark re-typed in another font", "dont",
     "Don't re-type the wordmark in another font.|The wordmark is artwork, not editable text. Use the supplied files — never set “The Crossing” in a different typeface.",
     art=f'''  {use("icon", (ART[0]+245, ART[1]+8, 118, 118))}
  <text x="{ART[0]+ART[2]/2:.0f}" y="{ART[1]+212}" text-anchor="middle" font-family="{SERIF}" font-size="62" font-weight="700" letter-spacing="1" fill="{LIMED_SPRUCE}">THE CROSSING</text>''')

tile("dont-clear-space.svg", "type crowding the clear space", "dont",
     "Don't put anything inside the clear space.|Headlines, taglines, edges, other logos — keep them all outside the logo's margin.",
     art=f'''  <rect x="{ART[0]}" y="{ART[1]}" width="{ART[2]}" height="{ART[3]}" rx="8" fill="none" stroke="{ASH}" stroke-width="1.5" stroke-dasharray="7 6"/>
  {use("logo", (ART[0]+38, ART[1]+26, 250, 216))}
  <text x="{ART[0]+310}" y="{ART[1]+112}" font-size="34" font-weight="700" fill="{ARMADILLO}">Join us this</text>
  <text x="{ART[0]+310}" y="{ART[1]+156}" font-size="34" font-weight="700" fill="{ARMADILLO}">Sunday at 9 &amp; 11</text>
  <text x="{ART[0]+310}" y="{ART[1]+196}" font-size="19" fill="{STONE_PATH}">All four campuses · thecrossing.church</text>''')

tile("dont-stretch.svg", "logo stretched and squashed", "dont",
     "Don't stretch or squash the logo.|Scale it proportionally — hold Shift, or set one dimension and let the other follow.",
     art=f'''  {use("logo", (ART[0]+18, ART[1]+30, 268, 208), sx_mult=1.0, sy_mult=0.62)}
  {use("logo", (ART[0]+330, ART[1]+18, 250, 232), sx_mult=0.60, sy_mult=1.0)}''')

tile("dont-color.svg", "logo in an unapproved color", "dont",
     "Don't set the logo in any other color.|Limed Spruce, Armadillo, or Pure White — that's the whole list. Other brand colors are still off-limits for the logo.",
     art=f'  {use("logo", inner, fill=BURNT_ORANGE, shrink=0.92)}')

print("\n%d tiles in samples/logo-usage/" % len([f for f in os.listdir(OUT) if f.endswith('.svg')]))
