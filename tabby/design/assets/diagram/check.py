#!/usr/bin/env python3
"""check.py: mechanical checks for a static diagram (SVG). Python standard library only.

    python3 check.py diagram.svg [more.svg] [--json]

Exit 0: no failures (warnings may print). Exit 2: at least one failure. Exit 1: a file could not be read.

It reads the structure `make.mjs` writes: <g data-node>, <rect data-box>, <path data-edge="a>b">,
<g data-pill="a>b">, <g data-zone>. A hand-drawn SVG without those still gets the accessibility,
viewBox, text-size and contrast checks; the geometry checks need the data attributes.

Rules (FAIL unless marked WARN):
  a11y-title        role="img", aria-labelledby, a first-child <title> and a <desc>, both non-empty
  viewbox           every node, zone, label and line point lies inside the viewBox
  diagonal          a straight line segment that is neither horizontal nor vertical
  node-overlap      two node boxes overlap
  edge-through-node a line crosses a node box that is not one of its two ends
  pill-clearance    a label overlaps a node, or sits closer than 16 px to its arrowhead
  tiny-text         text below 10 px
  budget            more than 9 nodes, 12 connections or 2 focal nodes
  contrast          a token pair below its minimum, in light or in dark
  grid (WARN)       a node box that is off the 4 px grid
"""
import json
import re
import sys
import xml.etree.ElementTree as ET

SVG = "{http://www.w3.org/2000/svg}"
ARROW = 12          # arrowhead length used by make.mjs
CLEAR = ARROW + 4   # a label keeps this far from the arrowhead
MAX_NODES, MAX_EDGES, MAX_FOCAL = 9, 12, 2
MIN_TEXT = 10


def tag(el):
    return el.tag.replace(SVG, "")


def num(v, d=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return d


def rect_of(g):
    for el in g.iter():
        if tag(el) == "rect":
            return (num(el.get("x")), num(el.get("y")), num(el.get("width")), num(el.get("height")))
    return None


def overlap(a, b, shrink=0.0):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax + shrink < bx + bw and bx + shrink < ax + aw and ay + shrink < by + bh and by + shrink < ay + ah


def dist_point_rect(px, py, r):
    x, y, w, h = r
    dx = max(x - px, 0, px - (x + w))
    dy = max(y - py, 0, py - (y + h))
    return (dx * dx + dy * dy) ** 0.5


def parse_path(d):
    """Return (segments, end). A segment is (x1, y1, x2, y2, cmd). Supports M H V L Q (absolute)."""
    toks = re.findall(r"[MHVLQ]|-?\d*\.?\d+", d)
    i, cx, cy, segs, cmd = 0, 0.0, 0.0, [], None
    while i < len(toks):
        if toks[i] in "MHVLQ":
            cmd = toks[i]
            i += 1
        if cmd == "M":
            cx, cy = float(toks[i]), float(toks[i + 1]); i += 2; cmd = "L"; first = True
            segs.append((cx, cy, cx, cy, "M"))
        elif cmd == "H":
            x = float(toks[i]); i += 1; segs.append((cx, cy, x, cy, "H")); cx = x
        elif cmd == "V":
            y = float(toks[i]); i += 1; segs.append((cx, cy, cx, y, "V")); cy = y
        elif cmd == "L":
            x, y = float(toks[i]), float(toks[i + 1]); i += 2; segs.append((cx, cy, x, y, "L")); cx, cy = x, y
        elif cmd == "Q":
            x, y = float(toks[i + 2]), float(toks[i + 3]); i += 4; segs.append((cx, cy, x, y, "Q")); cx, cy = x, y
        else:
            break
    return [s for s in segs if s[4] != "M"], (cx, cy), segs[0][:2] if segs else (0, 0)


def seg_hits_rect(s, r, shrink=1.0):
    x1, y1, x2, y2, _ = s
    x, y, w, h = r
    x += shrink; y += shrink; w -= 2 * shrink; h -= 2 * shrink
    if w <= 0 or h <= 0:
        return False
    return min(x1, x2) < x + w and max(x1, x2) > x and min(y1, y2) < y + h and max(y1, y2) > y


def lum(hexv):
    h = hexv.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


PAIRS = [  # (foreground, background, minimum, what)
    ("ink", "surface", 7.0, "title and names"), ("ink", "node", 7.0, "names on a node"),
    ("ink", "accent-tint", 7.0, "names on the focal node"), ("label", "surface", 4.5, "subtitle and labels"),
    ("label", "zone", 4.5, "zone label"), ("label", "node", 4.5, "role text"), ("accent-text", "surface", 4.5, "accent label text"), ("accent", "surface", 3.0, "the main flow line"),
    ("tile-ink", "tile", 3.0, "icon on a tile"), ("on-accent", "accent", 3.0, "icon on the focal tile"),
    ("line", "surface", 3.0, "connector lines"), ("line", "zone", 3.0, "connector lines on a zone"),
]


def css_vars(style):
    light = re.search(r":root\{([^}]*)\}", style)
    dark = re.search(r"prefers-color-scheme:\s*dark\)\s*\{\s*:root\{([^}]*)\}", style)
    def vars_of(m):
        return dict(re.findall(r"--([a-z-]+):\s*(#[0-9A-Fa-f]{3,6})", m.group(1))) if m else {}
    lv = vars_of(light)
    dv = dict(lv)
    dv.update(vars_of(dark))
    return lv, (dv if dark else None)


def check(path):
    findings = []  # (level, rule, detail)
    add = lambda lvl, rule, det: findings.append((lvl, rule, det))
    root = ET.parse(path).getroot()
    if tag(root) != "svg":
        raise ValueError("not an SVG")

    # accessibility
    labelled = (root.get("aria-labelledby") or "").split()
    kids = [k for k in root if tag(k) != "style"]
    first = kids[0] if kids else None
    ids = {el.get("id"): el for el in root.iter() if el.get("id")}
    if root.get("role") != "img":
        add("FAIL", "a11y-title", 'the <svg> needs role="img"')
    if not labelled or any(i not in ids for i in labelled):
        add("FAIL", "a11y-title", "aria-labelledby must name the ids of a <title> and a <desc>")
    else:
        for i in labelled:
            if not "".join(ids[i].itertext()).strip():
                add("FAIL", "a11y-title", f"#{i} is empty")
    if first is None or tag(first) != "title":
        add("FAIL", "a11y-title", "<title> must be the first child of <svg>")
    if not any(tag(el) == "desc" for el in root.iter()):
        add("FAIL", "a11y-title", "missing <desc>")

    vb = [num(v) for v in (root.get("viewBox") or "0 0 0 0").split()]
    vbox = (vb[0], vb[1], vb[2], vb[3]) if len(vb) == 4 else (0, 0, 0, 0)

    nodes, zones, pills, edges = {}, [], {}, []
    for g in root.iter():
        t = tag(g)
        if g.get("data-ghost"):
            continue
        if t == "g" and g.get("data-node"):
            r = rect_of(g)
            if r:
                nodes[g.get("data-node")] = (r, g.get("data-focal") == "1")
        elif t == "g" and g.get("data-zone"):
            r = rect_of(g)
            if r:
                zones.append(r)
        elif t == "g" and g.get("data-pill"):
            r = rect_of(g)
            if r:
                pills[g.get("data-pill")] = r
        elif t == "path" and g.get("data-edge"):
            edges.append((g.get("data-edge"), g.get("d") or ""))

    # viewBox containment
    def inside(r, what):
        x, y, w, h = r
        if x < vbox[0] or y < vbox[1] or x + w > vbox[0] + vbox[2] or y + h > vbox[1] + vbox[3]:
            add("FAIL", "viewbox", f"{what} leaves the viewBox")
    for k, (r, _) in nodes.items():
        inside(r, f"node {k}")
    for r in zones:
        inside(r, "a zone")
    for k, r in pills.items():
        inside(r, f"label {k}")

    parsed = {}
    for key, d in edges:
        segs, end, start = parse_path(d)
        parsed[key] = (segs, end, start)
        for s in segs:
            for (px, py) in ((s[0], s[1]), (s[2], s[3])):
                if px < vbox[0] or py < vbox[1] or px > vbox[0] + vbox[2] or py > vbox[1] + vbox[3]:
                    add("FAIL", "viewbox", f"connector {key} leaves the viewBox")
                    break
            if s[4] == "L" and abs(s[0] - s[2]) > 0.5 and abs(s[1] - s[3]) > 0.5:
                add("FAIL", "diagonal", f"connector {key} has a diagonal segment; use right angles")

    # node overlap
    names = list(nodes)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            if overlap(nodes[names[i]][0], nodes[names[j]][0]):
                add("FAIL", "node-overlap", f"{names[i]} and {names[j]} overlap")

    # connectors against nodes
    for key, (segs, end, start) in parsed.items():
        ends = set(key.split(">"))
        for name, (r, _) in nodes.items():
            if name in ends:
                continue
            if any(s[4] in "HVL" and seg_hits_rect(s, r) for s in segs):
                add("FAIL", "edge-through-node", f"connector {key} passes behind {name}")

    # labels
    for key, r in pills.items():
        for name, (nr, _) in nodes.items():
            if overlap(r, nr):
                add("FAIL", "pill-clearance", f"label {key} overlaps node {name}")
        if key in parsed:
            ex, ey = parsed[key][1]
            if dist_point_rect(ex, ey, r) < CLEAR:
                add("FAIL", "pill-clearance", f"label {key} is within {CLEAR} px of its arrowhead; widen the gap or shorten the label")

    # text
    for el in root.iter():
        if tag(el) == "text":
            fs = num(el.get("font-size"), 99)
            if fs < MIN_TEXT:
                add("FAIL", "tiny-text", f"text \"{''.join(el.itertext())[:20]}\" is {fs:g} px")

    # budget
    if len(nodes) > MAX_NODES:
        add("FAIL", "budget", f"{len(nodes)} nodes (max {MAX_NODES}); split into an overview and a detail picture")
    if len(edges) > MAX_EDGES:
        add("FAIL", "budget", f"{len(edges)} connections (max {MAX_EDGES})")
    focal = sum(1 for _, f in nodes.values() if f)
    if focal > MAX_FOCAL:
        add("FAIL", "budget", f"{focal} focal nodes (max {MAX_FOCAL}); accent only what the reader must see first")

    # grid
    for k, (r, _) in nodes.items():
        if any(abs(v / 4 - round(v / 4)) > 1e-6 for v in r):
            add("WARN", "grid", f"node {k} is off the 4 px grid")

    # contrast
    style = " ".join("".join(el.itertext()) for el in root.iter() if tag(el) == "style")
    lv, dv = css_vars(style)
    for theme, v in (("light" if dv else "theme", lv), ("dark", dv)):
        if not v:
            continue
        for fg, bg, mn, what in PAIRS:
            if fg in v and bg in v:
                c = ratio(v[fg], v[bg])
                if c < mn:
                    add("FAIL", "contrast", f"{theme}: --{fg} on --{bg} is {c:.1f}:1, needs {mn:g}:1 ({what})")
    return findings


def main(argv):
    as_json = "--json" in argv
    files = [a for a in argv if not a.startswith("--")]
    if not files:
        print(__doc__)
        return 1
    code, report = 0, {}
    for f in files:
        try:
            found = check(f)
        except (OSError, ET.ParseError, ValueError) as err:
            print(f"ERROR {f}: {err}")
            code = max(code, 1) if code != 2 else 2
            continue
        report[f] = found
        fails = [x for x in found if x[0] == "FAIL"]
        if not as_json:
            for lvl, rule, det in found:
                print(f"{lvl} {rule} {f}: {det}")
            if not found:
                print(f"OK {f}")
        if fails:
            code = 2
    if as_json:
        print(json.dumps({f: [dict(level=a, rule=b, detail=c) for a, b, c in v] for f, v in report.items()}, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
