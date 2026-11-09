// helpers.js — tiny, dependency-free helpers shared by every scene (same as the join toolkit).
// Every animation is a pure function of time: renderAt(t) sets every attribute for that instant,
// so frames can be rendered in any order and the result is identical on every run.

const NS = 'http://www.w3.org/2000/svg';

// Create an SVG element with attributes and (optionally) append it to a parent.
function S(tag, attrs = {}, parent) {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}

const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, p) => a + (b - a) * p;
// Progress of t through [a, b] as 0..1 (clamped).
const seg = (t, a, b) => clamp((t - a) / (b - a));
// Fade in over [a, a+d], hold, fade out over [b-d, b].
const win = (t, a, b, d = .25) => Math.min(seg(t, a, a + d), 1 - seg(t, b - d, b));

const ease = {
  out: p => 1 - Math.pow(1 - p, 3),
  inOut: p => p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2,
  back: p => { const c1 = 1.9, c3 = c1 + 1; return p <= 0 ? 0 : 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); }
};

// Stroke-draw a path from 0 (nothing) to 1 (complete).
function draw(pathEl, p) {
  if (!pathEl._len) { pathEl._len = pathEl.getTotalLength() + 1; pathEl.style.strokeDasharray = pathEl._len; }
  pathEl.style.strokeDashoffset = pathEl._len * (1 - p);
}

// Pop a group (drawn at absolute coordinates) in with a slight overshoot, scaling around (cx, cy).
function pop(g, p, cx, cy) {
  const s = Math.max(0, ease.back(p));
  g.setAttribute('transform', `translate(${cx} ${cy}) scale(${s}) translate(${-cx} ${-cy})`);
  g.style.opacity = p > 0 ? 1 : 0;
}
