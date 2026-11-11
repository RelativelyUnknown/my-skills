#!/usr/bin/env node
// make.mjs: build a static diagram (SVG, light and dark) from a small JSON spec.
//
//   node make.mjs spec.json [out.svg]       writes out.svg (or prints to stdout)
//   node make.mjs --icons <word>            lists icon names containing the word
//   import { build } from './make.mjs'      build(spec) returns the SVG text
//
// Spec (all coordinates in px, snapped to the 4 px grid):
// {
//   "id": "dg",                        // prefix for ids, unique per page
//   "title": "A request through the service", "subtitle": "One sentence.",
//   "width": 1024, "height": 576,      // optional; by default the canvas is fitted to the content
//   "zones": [{ "label": "Your service", "x": 272, "y": 152, "w": 728, "h": 344 }],
//   "nodes": [{ "id": "api", "name": "API", "role": "http server", "icon": "server",
//               "x": 296, "y": 236, "focal": false, "mono": false }],   // mono: set the role in mono (a port, a path)
//   "edges": [{ "from": "client", "to": "api", "label": "POST", "kind": "main" }],
//   "theme": { "accent": "#1B7F5C", "surface": "#101614", "ink": "#EAF2EE", "font": "IBM Plex Sans" }  // from a design.md; optional
// }
// "ghost": true on a node or edge draws it only in the animation's "before" state (hidden in the static picture).
// A node with "rows": [["id","uuid"],["email","text"]] is drawn as a table (entity, schema).
// Edge kind: main (accent, solid) | secondary (grey, solid, default) | optional (grey, dashed).
// Edge route: h | v (chosen automatically when nodes are aligned) | hv | vh (one elbow) | z (fan: horizontal, vertical, horizontal; "slot": [i, n]) |
//   below | above (a U shape under or over both nodes, for a return or retry path).
// Icons are Tabler outline names (assets/icons/tabler-outline.json); an unknown name lists near matches.
// The output carries data-node / data-edge / data-pill attributes that check.py reads.

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const here = path.dirname(fileURLToPath(import.meta.url));
const ICONS = JSON.parse(fs.readFileSync(path.join(here, '../icons/tabler-outline.json'), 'utf8'));

const g4 = v => Math.round(v / 4) * 4;
const up4 = v => Math.ceil(v / 4) * 4;
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function lev(a, b) {
  const d = Array.from({ length: a.length + 1 }, (_, i) => [i, ...Array(b.length).fill(0)]);
  for (let j = 1; j <= b.length; j++) d[0][j] = j;
  for (let i = 1; i <= a.length; i++) for (let j = 1; j <= b.length; j++)
    d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
  return d[a.length][b.length];
}
export function icon(name) {
  if (ICONS[name]) return ICONS[name];
  const names = Object.keys(ICONS);
  const near = names.filter(n => n.includes(name) || name.includes(n)).slice(0, 5);
  const best = near.length ? near : names.map(n => [lev(name, n), n]).sort((a, b) => a[0] - b[0]).slice(0, 5).map(x => x[1]);
  throw new Error(`unknown icon "${name}"; nearest: ${best.join(', ')}`);
}

const SANS = 'Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif';
const MONO = '"JetBrains Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace';
const RULES = `text{font-family:var(--sans);fill:var(--ink)}
.m{font-family:var(--mono)}.l{fill:var(--label)}.a{fill:var(--accent-text)}.on{fill:var(--on-accent)}
.mka{fill:none;stroke:var(--accent)}.mkl{fill:none;stroke:var(--line)}`;

const mix = (a, b, t) => '#' + [1, 3, 5].map(i => Math.round(parseInt(a.substr(i, 2), 16) * t + parseInt(b.substr(i, 2), 16) * (1 - t)).toString(16).padStart(2, '0')).join('').toUpperCase();
const lum = h => { const f = c => (c /= 255) <= .03928 ? c / 12.92 : Math.pow((c + .055) / 1.055, 2.4); const [r, g, b] = [1, 3, 5].map(i => f(parseInt(h.substr(i, 2), 16))); return .2126 * r + .7152 * g + .0722 * b; };
const cr = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + .05) / (y + .05); };

// Default tokens (art direction A), light and dark. See diagrams/style.md.
const LIGHT = { surface: '#FFFFFF', zone: '#F5F6F9', node: '#FFFFFF', hair: '#DADEE6', ink: '#14171F', label: '#5B6270', accent: '#2F5BEA', 'accent-text': '#2F5BEA', 'accent-tint': '#E8EEFF', tile: '#EEF0F5', 'tile-ink': '#3A4152', line: '#7A8294', 'on-accent': '#FFFFFF' };
const DARK = { surface: '#0E1016', zone: '#151824', node: '#171B28', hair: '#2A3042', ink: '#F1F3F8', label: '#9BA3B4', accent: '#7C9BFF', 'accent-text': '#7C9BFF', 'accent-tint': '#1C2547', tile: '#20263A', 'tile-ink': '#C7CEDF', line: '#6A748C', 'on-accent': '#0E1016' };
const decl = (o, extra = '') => Object.entries(o).map(([k, v]) => `--${k}:${v}`).join(';') + extra;

// A design.md maps to spec.theme { accent, surface, ink, font }. Missing keys keep the defaults; the rest is derived
// over the surface, so one brand colour set gives one theme (no automatic dark variant). Run check.py afterwards.
function themeCss(theme) {
  const fonts = `;--sans:${theme?.font ? `${theme.font},` : ''}${SANS};--mono:${MONO}`;
  if (!theme || !(theme.accent || theme.surface || theme.ink)) {
    return `:root{${decl(LIGHT, fonts)}}\n@media (prefers-color-scheme:dark){:root{${decl(DARK)}}}\n${RULES}`;
  }
  const surface = (theme.surface || LIGHT.surface).toUpperCase(), ink = (theme.ink || (lum(surface) > .5 ? LIGHT.ink : DARK.ink)).toUpperCase();
  const accent = (theme.accent || (lum(surface) > .5 ? LIGHT.accent : DARK.accent)).toUpperCase();
  const light = lum(surface) > .5;
  let accentText = accent;
  for (let k = 1; cr(accentText, surface) < 4.5 && k <= 10; k++) accentText = mix(ink, accent, k / 10);
  const t = {
    surface, ink, accent, 'accent-text': accentText, zone: mix(ink, surface, 0.04), node: light ? surface : mix(ink, surface, 0.08), hair: mix(ink, surface, 0.14),
    label: mix(ink, surface, 0.71), 'accent-tint': mix(accent, surface, 0.12), tile: mix(ink, surface, 0.06), 'tile-ink': mix(ink, surface, 0.78),
    line: mix(ink, surface, 0.52), 'on-accent': cr(accent, surface) >= cr(accent, ink) ? surface : ink,
  };
  return `:root{${decl(t, fonts)}}\n${RULES}`;
}

export function build(spec) {
  const id = spec.id || 'dg';
  const R = 12; // elbow radius
  const NH = 72, TILE = 40;
  const out = [];
  const add = s => out.push(s);

  // ---- nodes: size, position
  const nodes = new Map();
  for (const n of spec.nodes || []) {
    const rows = n.rows;
    let w, h;
    if (rows) {
      const longest = Math.max(...rows.map(r => (r[0] || '').length + (r[1] || '').length + 3), n.name.length * 1.2);
      w = Math.max(g4(n.w || 0), up4(longest * 7.4 + 36)); h = 44 + 24 * rows.length + 8;
    } else {
      const textW = Math.max(n.name.length * 8.8, (n.role || '').length * (n.mono ? 7.2 : 6.6));
      w = Math.max(g4(n.w || 0), up4(64 + textW + 16)); h = NH;
    }
    const x = g4(n.x), y = g4(n.y);
    nodes.set(n.id, { ...n, x, y, w, h, cx: x + w / 2, cy: y + h / 2, r: x + w, b: y + h });
  }

  // canvas: given width and height, else fitted to the content with a 40 px margin (48 px below)
  let W = spec.width ? g4(spec.width) : 0, H = spec.height ? g4(spec.height) : 0;
  if (!W || !H) {
    let maxR = 0, maxB = 0;
    for (const n of nodes.values()) { maxR = Math.max(maxR, n.r); maxB = Math.max(maxB, n.b + (spec.edges || []).some(e => (e.route === 'below') && (e.from === n.id || e.to === n.id)) * 56); }
    for (const z of spec.zones || []) { maxR = Math.max(maxR, g4(z.x) + g4(z.w)); maxB = Math.max(maxB, g4(z.y) + g4(z.h)); }
    W = W || up4(Math.max(maxR + 40, 80 + 15 * (spec.title || '').length));
    H = H || up4(maxB + 48);
  }
  add(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-labelledby="${id}-title ${id}-desc" data-diagram="1">`);
  add(`<title id="${id}-title">${esc(spec.title)}</title>`);
  add(`<desc id="${id}-desc">${esc(spec.desc || spec.subtitle || spec.title)}</desc>`);
  add(`<defs><style>${themeCss(spec.theme)}</style>`);
  add(`<marker id="${id}-ma" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto"><path class="mka" d="M1 1 L9 5 L1 9" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></marker>`);
  add(`<marker id="${id}-ml" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="12" markerHeight="12" markerUnits="userSpaceOnUse" orient="auto"><path class="mkl" d="M1 1 L9 5 L1 9" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>`);
  add(`<rect width="${W}" height="${H}" fill="var(--surface)"/>`);
  add(`<text x="40" y="64" font-size="28" font-weight="650" letter-spacing="-0.4">${esc(spec.title)}</text>`);
  if (spec.subtitle) add(`<text class="l" x="40" y="92" font-size="15">${esc(spec.subtitle)}</text>`);

  // ---- zones
  for (const z of spec.zones || []) {
    const x = g4(z.x), y = g4(z.y), w = g4(z.w), h = g4(z.h);
    add(`<g data-zone="${esc(z.label)}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="24" fill="var(--zone)"/>` +
        `<text class="l" x="${x + 24}" y="${y + 32}" font-size="12" font-weight="600" letter-spacing="1.2">${esc(z.label.toUpperCase())}</text></g>`);
  }

  // ---- edges (drawn before nodes so lines sit behind boxes)
  const pills = [];
  const edgeSvg = [];
  for (const e of spec.edges || []) {
    const a = nodes.get(e.from), b = nodes.get(e.to);
    if (!a || !b) throw new Error(`edge ${e.from}>${e.to}: unknown node`);
    const kind = e.kind || 'secondary';
    let route = e.route;
    if (!route) {
      if (Math.abs(a.cy - b.cy) < 2) route = 'h';
      else if (Math.min(a.r, b.r) - Math.max(a.x, b.x) >= 40) route = 'v';
      else throw new Error(`edge ${e.from}>${e.to}: nodes are neither in one row nor overlapping in x; set route to hv, vh, below or above`);
    }
    let d, pill;
    const G = 4; // gap between a line end and a box
    const dir = (p, q) => (q > p ? 1 : -1);
    if (route === 'h') {
      const sx = dir(a.cx, b.cx), x1 = sx > 0 ? a.r + G : a.x - G, x2 = sx > 0 ? b.x - G : b.r + G;
      d = `M${x1},${a.cy} H${x2}`; pill = [(x1 + x2) / 2, a.cy];
    } else if (route === 'v') {
      const sy = dir(a.cy, b.cy), y1 = sy > 0 ? a.b + G : a.y - G, y2 = sy > 0 ? b.y - G : b.b + G;
      const xo = g4((Math.max(a.x, b.x) + Math.min(a.r, b.r)) / 2);
      d = `M${xo},${y1} V${y2}`; pill = [xo, (y1 + y2) / 2];
    } else if (route === 'hv') {
      const sx = dir(a.cx, b.cx), sy = dir(a.cy, b.cy), x1 = sx > 0 ? a.r + G : a.x - G, y2 = sy > 0 ? b.y - G : b.b + G;
      d = `M${x1},${a.cy} H${b.cx - sx * R} Q${b.cx},${a.cy} ${b.cx},${a.cy + sy * R} V${y2}`; pill = [(x1 + b.cx - sx * R) / 2, a.cy];
    } else if (route === 'vh') {
      const sx = dir(a.cx, b.cx), sy = dir(a.cy, b.cy), y1 = sy > 0 ? a.b + G : a.y - G, x2 = sx > 0 ? b.x - G : b.r + G;
      d = `M${a.cx},${y1} V${b.cy - sy * R} Q${a.cx},${b.cy} ${a.cx + sx * R},${b.cy} H${x2}`; pill = [(a.cx + sx * R + x2) / 2, b.cy];
    } else if (route === 'z') {
      // Z route: horizontal, vertical, horizontal. e.slot = [i, n] spreads the start points of n connectors along the
      // source's edge so a fan-out does not share a stroke; the vertical runs are staggered so none cross.
      const [i, n] = e.slot || [0, 1];
      const sx = dir(a.cx, b.cx), x1 = sx > 0 ? a.r + G : a.x - G, x2 = sx > 0 ? b.x - G : b.r + G;
      const sy = g4(a.y + a.h * (i + 1) / (n + 1)), cyb = b.cy, dy = Math.sign(cyb - sy), span = Math.abs(x2 - x1);
      const mid = (n - 1) / 2, k = n > 1 ? 1 - Math.abs(i - mid) / (mid + 0.5) : 0.5;
      const xm = g4(x1 + sx * span * (0.3 + 0.4 * k)), r = Math.min(R, Math.abs(cyb - sy) / 2, Math.abs(xm - x1) / 2);
      if (dy === 0 || r < 4) d = `M${x1},${sy} H${xm} V${cyb} H${x2}`;
      else d = `M${x1},${sy} H${xm - sx * r} Q${xm},${sy} ${xm},${sy + dy * r} V${cyb - dy * r} Q${xm},${cyb} ${xm + sx * r},${cyb} H${x2}`;
      pill = [(xm + x2) / 2, cyb];
    } else if (route === 'below' || route === 'above') {
      const below = route === 'below', s = below ? 1 : -1;
      const toLeft = b.cx < a.cx;
      const xs = g4(toLeft ? a.x + a.w * 0.25 : a.x + a.w * 0.75), xe = g4(toLeft ? b.x + b.w * 0.75 : b.x + b.w * 0.25);
      const edgeY = below ? Math.max(a.b, b.b) : Math.min(a.y, b.y);
      const y = edgeY + s * 48, ys = below ? a.b + G : a.y - G, ye = below ? b.b + G : b.y - G, k = toLeft ? -1 : 1;
      d = `M${xs},${ys} V${y - s * R} Q${xs},${y} ${xs + k * R},${y} H${xe - k * R} Q${xe},${y} ${xe},${y - s * R} V${ye}`;
      pill = [(xs + xe) / 2, y];
    } else throw new Error(`edge ${e.from}>${e.to}: unknown route "${route}"`);
    const key = `${e.from}>${e.to}`;
    const main = kind === 'main';
    const cls = main ? 'ma' : 'ml';
    const attrs = main ? 'stroke="var(--accent)" stroke-width="2.5"' : kind === 'optional' ? 'stroke="var(--line)" stroke-width="1.5" stroke-dasharray="5 5"' : 'stroke="var(--line)" stroke-width="1.75"';
    edgeSvg.push(`<path data-edge="${esc(key)}" data-kind="${kind}"${e.ghost ? ' data-ghost="1" display="none"' : ''} d="${d}" fill="none" ${attrs} stroke-linecap="round" stroke-linejoin="round" marker-end="url(#${id}-${cls})"/>`);
    if (e.label) pills.push({ key, label: e.label, at: pill, accent: main, ghost: !!e.ghost });
  }
  edgeSvg.forEach(add);

  // ---- pills (labels sit on their line, masking it)
  for (const p of pills) {
    const text = String(p.label).toUpperCase();
    const w = up4(text.length * 6.6 + 16), h = 24, x = g4(p.at[0] - w / 2), y = g4(p.at[1] - h / 2);
    add(`<g data-pill="${esc(p.key)}"${p.ghost ? ' data-ghost="1" display="none"' : ''}><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="var(--surface)" stroke="var(${p.accent ? '--accent' : '--hair'})" stroke-width="1"/>` +
        `<text class="${p.accent ? 'a' : 'l'}" x="${x + w / 2}" y="${y + 16}" font-size="10.5" font-weight="600" letter-spacing="0.5" text-anchor="middle">${esc(text)}</text></g>`);
  }

  // ---- nodes
  for (const n of nodes.values()) {
    const f = !!n.focal;
    const fill = f ? 'var(--accent-tint)' : 'var(--node)', stroke = f ? 'var(--accent)' : 'var(--hair)';
    add(`<g data-node="${esc(n.id)}"${f ? ' data-focal="1"' : ''}${n.ghost ? ' data-ghost="1" display="none"' : ''}><rect data-box="1" x="${n.x}" y="${n.y}" width="${n.w}" height="${n.h}" rx="14" fill="${fill}" stroke="${stroke}" stroke-width="${f ? 1.75 : 1.25}"/>`);
    if (n.rows) {
      add(`<text x="${n.x + 16}" y="${n.y + 28}" font-size="14" font-weight="650">${esc(n.name)}</text>`);
      add(`<line x1="${n.x}" y1="${n.y + 44}" x2="${n.r}" y2="${n.y + 44}" stroke="var(--hair)" stroke-width="1"/>`);
      n.rows.forEach((r, i) => {
        const ty = n.y + 44 + 24 * i + 24;
        add(`<text class="m" x="${n.x + 16}" y="${ty}" font-size="12">${esc(r[0])}</text>`);
        if (r[1]) add(`<text class="m l" x="${n.r - 16}" y="${ty}" font-size="12" text-anchor="end">${esc(r[1])}</text>`);
      });
    } else {
      const ty = n.y + (n.h - TILE) / 2;
      add(`<rect x="${n.x + 12}" y="${ty}" width="${TILE}" height="${TILE}" rx="10" fill="${f ? 'var(--accent)' : 'var(--tile)'}"/>`);
      if (n.icon) add(`<g transform="translate(${n.x + 20},${ty + 8}) scale(0.6667)" fill="none" stroke="${f ? 'var(--on-accent)' : 'var(--tile-ink)'}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${icon(n.icon)}</g>`);
      if (n.role) {
        add(`<text x="${n.x + 64}" y="${n.cy - 4}" font-size="15" font-weight="650">${esc(n.name)}</text>`);
        add(`<text class="l${n.mono ? ' m' : ''}" x="${n.x + 64}" y="${n.cy + 15}" font-size="${n.mono ? 11 : 11.5}">${esc(n.role)}</text>`);
      } else add(`<text x="${n.x + 64}" y="${n.cy + 5}" font-size="15" font-weight="650">${esc(n.name)}</text>`);
    }
    add('</g>');
  }
  add('</svg>');
  return out.join('\n') + '\n';
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  const [spec, dest] = process.argv.slice(2);
  if (spec === '--icons') {  // node make.mjs --icons <word>: list icon names that contain the word
    const hits = Object.keys(ICONS).filter(n => n.includes(String(dest || '').toLowerCase()));
    console.log(hits.slice(0, 60).join('\n') + (hits.length > 60 ? `\n... ${hits.length - 60} more; use a longer word` : ''));
    process.exit(hits.length ? 0 : 1);
  }
  if (!spec) { console.error('usage: node make.mjs spec.json [out.svg]'); process.exit(1); }
  try {
    const svg = build(JSON.parse(fs.readFileSync(spec, 'utf8')));
    if (dest) fs.writeFileSync(dest, svg); else process.stdout.write(svg);
  } catch (err) { console.error('make.mjs: ' + err.message); process.exit(1); }
}
