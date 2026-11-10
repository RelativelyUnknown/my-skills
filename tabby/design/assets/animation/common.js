// common.js — frame, palette, typography and the split-screen chart shared by every scene.
//
// Colour roles (the whole visual language):
//   given data, names        = ink                   #111111
//   baseline / secondary     = grey                  #808080 (zones #F0F0F0)
//   focus: the result, or the main flow = accent blue #004A96 (line #4472AA, guides #7CA0C6, zones #E0E9F2)
//   no value                 = dashed grey outline   #BDBDBD
// Text: title, the two panel labels, axis ticks and result values. No legend, no captions.
// Re-brand by setting window.THEME in specs.js: ACCENT, BASE, SURFACE, INK, LABEL, MUTED, GRID, AXIS, SLOT, FONT { sans, mono }.
// ACCENT alone derives its three tints; unset keys keep the defaults. See design/diagrams/style.md.

const W = 960, H = 540;                       // 16:9 stage; render.js renders it at 2× (1920×1080)
window.STAGE_W = W; window.STAGE_H = H;

// Mix colour a over colour b at share t (hex strings #RRGGBB).
const mixHex = (a, b, t) => '#' + [1, 3, 5].map(i =>
  Math.round(parseInt(a.substr(i, 2), 16) * t + parseInt(b.substr(i, 2), 16) * (1 - t)).toString(16).padStart(2, '0')).join('').toUpperCase();
const THEME = window.THEME || {};
const SURFACE = THEME.SURFACE || THEME.WHITE || '#FFFFFF';
// Giving only ACCENT (or BASE) is enough: the tints are derived over the surface, as the defaults were
// (zone 12%, light 52%, mid 77% of the accent; the grey zone 12% of the grey).
// Neutrals follow from INK over the surface the same way (label 71%, muted 49%, grid 7%, axis 23%, empty slot 28%).
const luminance = h => { const f = c => (c /= 255) <= .03928 ? c / 12.92 : Math.pow((c + .055) / 1.055, 2.4);
  const [r, g, b] = [1, 3, 5].map(i => f(parseInt(h.substr(i, 2), 16))); return .2126 * r + .7152 * g + .0722 * b; };
const contrast = (a, b) => { const [x, y] = [luminance(a), luminance(b)].sort((p, q) => q - p); return (x + .05) / (y + .05); };
const INKC = THEME.INK || '#111111';
const derived = Object.assign({},
  THEME.INK || THEME.SURFACE || THEME.WHITE ? { LABEL: mixHex(INKC, SURFACE, .71), MUTED: mixHex(INKC, SURFACE, .49), GRID: mixHex(INKC, SURFACE, .07), AXIS: mixHex(INKC, SURFACE, .23), SLOT: mixHex(INKC, SURFACE, .28) } : {},
  THEME.ACCENT ? { ACCENT_MID: [.77, .85, .93, 1].map(t => mixHex(THEME.ACCENT, SURFACE, t)).find(c => contrast(c, SURFACE) >= 3) || THEME.ACCENT, ACCENT_LIGHT: mixHex(THEME.ACCENT, SURFACE, .52), ACCENT_ZONE: mixHex(THEME.ACCENT, SURFACE, .12) } : {},
  THEME.BASE ? { BASE_ZONE: mixHex(THEME.BASE, SURFACE, .12) } : {});
const C = Object.assign({
  INK: '#111111', LABEL: '#555555', MUTED: '#8A8A8A', GRID: '#EEEEEE', AXIS: '#C9C9C9', WHITE: '#FFFFFF',
  BASE: '#808080', BASE_ZONE: '#F0F0F0',
  ACCENT: '#004A96', ACCENT_MID: '#4472AA', ACCENT_LIGHT: '#7CA0C6', ACCENT_ZONE: '#E0E9F2',
  SLOT: '#BDBDBD',
}, derived, THEME, { WHITE: SURFACE });
// Text on an accent fill: whichever of the surface and the ink reads better on it.
C.ON_ACCENT = contrast(C.ACCENT, SURFACE) >= contrast(C.ACCENT, INKC) ? SURFACE : INKC;          // WHITE is the stage surface; THEME.SURFACE is its documented name
document.documentElement.style.background = SURFACE;
// Font stacks. 'IN' and 'JBM' are the bundled Inter and JetBrains Mono (style.css); a design.md font goes first.
const FONT = Object.assign({ sans: 'IN', mono: 'JBM' }, THEME.FONT || {});
const PILL_H = 24, PILL_R = 12;

// Text, centred by default, mono 14 px.
function T(parent, x, y, s, o = {}) {
  const e = S('text', Object.assign({ x, y, 'text-anchor': 'middle', 'font-family': FONT.mono, 'font-size': 14, fill: C.INK }, o), parent);
  e.textContent = s; return e;
}
// Sans label (Inter 500, 14 px, grey) — headers, row names, annotations.
const sans = (p, x, y, s, o = {}) => T(p, x, y, s, Object.assign({ 'font-family': FONT.sans, 'font-weight': 500, 'font-size': 14, fill: C.LABEL }, o));

// White stage with the centred title; everything in `dyn` fades at the end of the loop, the title stays.
function makeStage(title) {
  const stage = document.getElementById('stage');
  stage.style.width = W + 'px'; stage.style.height = H + 'px';
  const svg = S('svg', { class: 'layer', width: W, height: H, viewBox: `0 0 ${W} ${H}` }, stage);
  S('rect', { x: 0, y: 0, width: W, height: H, fill: C.WHITE }, svg);
  T(svg, W / 2, 50, title, { 'font-family': FONT.sans, 'font-weight': 600, 'font-size': 26, 'letter-spacing': '-0.01em' });
  const dyn = S('g', {}, svg);
  return { svg, dyn };
}

// Split screen: baseline left (grey), result right (accent), a hairline divider between them.
// Pass the two labels, e.g. splitHeader(dyn, ['Before', 'After']).
const PANELS = {
  left:  { x0: 40,  x1: 460, color: C.BASE },
  right: { x0: 500, x1: 920, color: C.ACCENT },
};
function splitHeader(parent, labels = ['Before', 'After'], y = 98) {
  const divider = S('line', { x1: W / 2, x2: W / 2, y1: 80, y2: 500, stroke: C.ACCENT_ZONE, 'stroke-width': 1.5 }, parent);
  const texts = ['left', 'right'].map((k, i) => T(parent, (PANELS[k].x0 + PANELS[k].x1) / 2, y, labels[i],
    { 'font-family': FONT.sans, 'font-weight': 600, 'font-size': 20, fill: PANELS[k].color }));
  return { divider, labels: texts, update: t => {
    divider.setAttribute('opacity', seg(t, .05, .35));
    texts.forEach(l => l.setAttribute('opacity', seg(t, .1, .4)));
  } };
}

// One time-series (or any x/y) chart inside a panel: y gridlines with labels, x axis with tick labels.
// spec: { domain:[x0,x1], yDomain:[y0,y1], yTicks:[…], tickFmt?: (x)=>string }
// Layers (back → front): zones, grid, lines, raw, marks, movers, pills.
function makeChart(parent, panel, sp, { ticks, top = 136, bottom = 382 } = {}) {
  const plot = { l: panel.x0 + 46, r: panel.x1 - 6, t: top, b: bottom };
  const [d0, d1] = sp.domain, [y0, y1] = sp.yDomain;
  const xOf = t => plot.l + (t - d0) / (d1 - d0) * (plot.r - plot.l);
  const yOf = v => plot.b - (v - y0) / (y1 - y0) * (plot.b - plot.t);
  const fmt = sp.tickFmt || String;
  const g = S('g', {}, parent);
  const zones = S('g', {}, g), grid = S('g', {}, g);
  sp.yTicks.forEach(v => {
    S('line', { x1: plot.l, x2: plot.r, y1: yOf(v), y2: yOf(v), stroke: C.GRID, 'stroke-width': 1 }, grid);
    T(grid, plot.l - 12, yOf(v) + 4, String(v), { 'text-anchor': 'end', 'font-size': 11.5, fill: C.MUTED });
  });
  S('line', { x1: plot.l, x2: plot.r, y1: plot.b, y2: plot.b, stroke: C.AXIS, 'stroke-width': 1.2 }, grid);
  (ticks || []).forEach(t => {
    S('line', { x1: xOf(t), x2: xOf(t), y1: plot.b, y2: plot.b + 5, stroke: C.AXIS, 'stroke-width': 1.2 }, grid);
    T(grid, xOf(t), plot.b + 22, fmt(t), { 'font-size': 12, fill: C.LABEL });
  });
  const L = () => S('g', {}, g);
  return { g, grid, zones, lines: L(), raw: L(), marks: L(), movers: L(), pills: L(), plot, xOf, yOf,
           update: t => grid.setAttribute('opacity', seg(t, .1, .5)) };
}

// A value pill drawn at (0,0), centred; place it with place().
function valuePill(parent, w, fill, text, textFill, { stroke, size = 13 } = {}) {
  const g = S('g', { opacity: 0 }, parent);
  S('rect', Object.assign({ x: -w / 2, y: -PILL_H / 2, width: w, height: PILL_H, rx: PILL_R, fill }, stroke ? { stroke, 'stroke-width': 1.3 } : {}), g);
  if (text) T(g, 0, size * .34, text, { fill: textFill, 'font-size': size });
  return g;
}
// An empty slot: dashed outline, no value.
function emptySlot(parent, w) {
  const g = S('g', { opacity: 0 }, parent);
  S('rect', { x: -w / 2, y: -PILL_H / 2, width: w, height: PILL_H, rx: PILL_R, fill: 'none', stroke: C.SLOT,
              'stroke-width': 1.3, 'stroke-dasharray': '3 3' }, g);
  return g;
}
// Place a (0,0)-centred group at (x, y), scaled by s around its centre.
const place = (g, x, y, s = 1) => g.setAttribute('transform', `translate(${x} ${y}) scale(${Math.max(0, s)})`);
// Selection ring around a pill, drawn at (0,0); position it with a translate transform.
function ring(parent, w) {
  return S('rect', { x: -w / 2 - 3.5, y: -PILL_H / 2 - 3.5, width: w + 7, height: PILL_H + 7, rx: PILL_R + 3.5,
                     fill: 'none', stroke: C.INK, 'stroke-width': 1.6, opacity: 0 }, parent);
}

// Shared loop bookkeeping: every scene calls finish(dyn, END, perFrame) after building itself.
function finish(dyn, END, perFrame) {
  window.DURATION = END + .8;                       // hold, fade over .45 s, then title-only frames
  window.renderAt = t => { dyn.style.opacity = 1 - seg(t, END, END + .45); perFrame(t); };
}
