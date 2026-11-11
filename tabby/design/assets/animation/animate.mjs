#!/usr/bin/env node
// animate.mjs: build an animated diagram as ONE self-contained HTML file (inline SVG, a ~150-line player,
// no network, no dependencies). The same spec as make.mjs plus a "story".
//
//   node animate.mjs spec.json [out.html]
//
// The complete static picture is the base: the SVG is whole without JavaScript, the player only hides
// parts at start and reveals them in order. Under prefers-reduced-motion the page shows the end state and
// offers "Play once". The picture is a pure function of time, so any frame can be reproduced (window.__seek(t)).
//
// story: an ordered list of steps; every step has "t" (start, seconds) and an optional "dur".
//   { "t": 0.4, "reveal": "client" }                       node (or nodes: ["a","b"]) fades in and rises 8 px   (0.45 s)
//   reveal, draw and hide take a list and an optional "stagger" (seconds between items): one step, items in turn
//   { "t": 0.9, "draw": "client>api" }                     connector draws itself, then its label fades in      (0.55 s)
//   { "t": 3.0, "packet": ["client>api","api>queue"], "dur": 2.4 }   a dot travels along those connectors
//   { "t": 3.2, "pulse": "queue" }                         a ring expands once from the node                    (0.7 s)
//   { "t": 3.4, "badge": "queue", "text": "3" }            a count badge on the node (a later step changes it)
//   { "t": 4.0, "active": "paid" }                         the node takes the focal look until the next active step
//   { "t": 4.0, "hide": "old-node" } / "hide": "a>b"       fades out (used with "ghost": true elements: the before state)
// Without a story, a default one is generated: nodes and main connectors appear in order, then one packet runs the main path.
// Options: "hold" (seconds on the finished picture, default 2), "loop" (default true).
//
// Every step carries "why": a few words on what the motion explains (check-motion.mjs fails a step without one).
// Budget: at most 8 steps, and at most 2 running at once (check-motion.mjs fails more).

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { build } from '../diagram/make.mjs';

const DUR = { reveal: 0.45, draw: 0.55, pulse: 0.7, hide: 0.3, badge: 0.25, active: 0.2 };

export function defaultStory(spec) {
  const steps = [];
  const mains = (spec.edges || []).filter(e => e.kind === 'main' && !e.ghost);
  const order = [];
  for (const e of mains) for (const id of [e.from, e.to]) if (!order.includes(id)) order.push(id);
  let t = 0;
  order.forEach((id, i) => {
    steps.push({ t, reveal: id, why: 'a part appears in the order a request meets it' });
    const e = mains.find(m => m.to === id);
    if (e) steps.push({ t: t + 0.3, draw: `${e.from}>${e.to}`, why: 'the connection is made as the request would use it' });
    t += 0.7;
  });
  if (mains.length) steps.push({ t: t + 0.2, packet: mains.map(e => `${e.from}>${e.to}`), dur: Math.max(1.6, mains.length * 0.9), why: 'the dot shows the path one request takes' });
  return steps;
}

export function stepDur(s) {
  if (s.dur) return s.dur;
  for (const k of Object.keys(DUR)) if (k in s) {
    const n = Array.isArray(s[k]) ? s[k].length : 1;
    return DUR[k] + (k === 'draw' ? 0.25 : 0) + (n - 1) * (s.stagger || 0);
  }
  return 0.5;
}

export function timeline(spec) {
  const story = (spec.story && spec.story.length ? spec.story : defaultStory(spec)).map(s => ({ ...s, dur: stepDur(s) })).sort((a, b) => a.t - b.t);
  const end = Math.max(0, ...story.map(s => s.t + s.dur));
  const hold = spec.hold ?? 2;
  return { story, end, hold, total: end + hold + 0.5 };
}

const PLAYER = String.raw`
(function () {
  var D = window.__DATA, svg = document.querySelector('svg[data-diagram]');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)');
  var q = function (sel) { return svg.querySelector(sel); }, NS = 'http://www.w3.org/2000/svg';
  var node = function (id) { return q('[data-node="' + id.replace(/"/g, '\\"') + '"]'); };
  var edge = function (k) { return q('path[data-edge="' + k + '"]'); };
  var pill = function (k) { return q('[data-pill="' + k + '"]'); };
  var list = function (v) { return Array.isArray(v) ? v : [v]; };
  var clamp = function (x) { return Math.max(0, Math.min(1, x)); };
  var outExpo = function (p) { return p >= 1 ? 1 : 1 - Math.pow(2, -10 * p); };
  var inOut = function (p) { return p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2; };
  var story = D.story, END = D.end, HOLD = D.hold, TOTAL = D.total;

  // what moves: every element a step names
  var dyn = [], seen = new Set(), showers = new Set(), st = {}, layer = document.createElementNS(NS, 'g');
  svg.appendChild(layer);
  function track(el, kind) { if (el && !seen.has(el)) { seen.add(el); dyn.push(el); } return el; }
  story.forEach(function (s) {
    if (s.reveal) list(s.reveal).forEach(function (id) { var g = track(node(id)); if (g) showers.add(g); });
    if (s.draw) list(s.draw).forEach(function (k) { var e = edge(k), pp = pill(k); track(e); track(pp); if (e) showers.add(e); if (pp) showers.add(pp); if (e) { st[k] = { len: e.getTotalLength(), da: e.getAttribute('stroke-dasharray'), mk: e.getAttribute('marker-end') }; } });
    if (s.hide) list(s.hide).forEach(function (id) { track(node(id) || edge(id)); track(pill(id)); });
  });
  var ghosts = Array.prototype.slice.call(svg.querySelectorAll('[data-ghost]'));
  var active = story.filter(function (s) { return s.active; });
  var nodeLook = {};
  active.forEach(function (s) { var g = node(s.active); if (g && !nodeLook[s.active]) { var rects = g.querySelectorAll('rect'); nodeLook[s.active] = { g: g, box: rects[0], tile: rects[1], icon: g.querySelector('g[transform]'), o: { bf: rects[0].getAttribute('fill'), bs: rects[0].getAttribute('stroke'), tf: rects[1] && rects[1].getAttribute('fill'), is: g.querySelector('g[transform]') && g.querySelector('g[transform]').getAttribute('stroke') } }; } });
  var packets = story.filter(function (s) { return s.packet; }).map(function (s) {
    var segs = list(s.packet).map(edge).filter(Boolean), cum = [], tot = 0;
    segs.forEach(function (p) { cum.push(tot); tot += p.getTotalLength(); });
    var halo = document.createElementNS(NS, 'circle'), dot = document.createElementNS(NS, 'circle');
    halo.setAttribute('r', 12); halo.setAttribute('fill', 'var(--accent)'); dot.setAttribute('r', 5.5); dot.setAttribute('fill', 'var(--accent)');
    dot.setAttribute('stroke', 'var(--surface)'); dot.setAttribute('stroke-width', 2);
    layer.appendChild(halo); layer.appendChild(dot);
    return { s: s, segs: segs, cum: cum, tot: tot, halo: halo, dot: dot };
  });
  var rings = story.filter(function (s) { return s.pulse; }).map(function (s) {
    var g = node(s.pulse), b = g && g.querySelector('rect'), r = document.createElementNS(NS, 'rect');
    r.setAttribute('fill', 'none'); r.setAttribute('stroke', 'var(--accent)'); r.setAttribute('stroke-width', 2); layer.appendChild(r);
    return { s: s, b: b, r: r };
  });
  var badges = {};
  story.filter(function (s) { return s.badge; }).forEach(function (s) {
    if (badges[s.badge]) return; var g = node(s.badge), b = g && g.querySelector('rect'); if (!b) return;
    var grp = document.createElementNS(NS, 'g'), bg = document.createElementNS(NS, 'rect'), tx = document.createElementNS(NS, 'text');
    bg.setAttribute('height', 22); bg.setAttribute('rx', 11); bg.setAttribute('fill', 'var(--accent)'); tx.setAttribute('class', 'on'); tx.setAttribute('font-size', 12); tx.setAttribute('font-weight', 650); tx.setAttribute('text-anchor', 'middle'); tx.setAttribute('y', 16);
    grp.appendChild(bg); grp.appendChild(tx); layer.appendChild(grp);
    badges[s.badge] = { grp: grp, bg: bg, tx: tx, x: +b.getAttribute('x') + +b.getAttribute('width') - 8, y: +b.getAttribute('y') - 11 };
  });

  var el0 = function (el, v) { el.style.opacity = v; };
  function frame(T) {
    var out = clamp((T - (END + HOLD)) / 0.5), alpha = 1 - out, inA = clamp(T / 0.4);     // the last half second fades the story out and the first 0.4 s fades the before state in, so the loop has no jump
    var t = Math.min(T, END + HOLD);
    ghosts.forEach(function (g) { g.setAttribute('display', ''); });
    dyn.forEach(function (el) { el.style.opacity = showers.has(el) ? 0 : alpha * inA; el.removeAttribute('transform'); });
    Object.keys(st).forEach(function (k) { var e = edge(k); if (!e) return; e.style.strokeDasharray = st[k].len; e.style.strokeDashoffset = st[k].len; e.removeAttribute('marker-end'); });
    var shown = {}, activeNow = {};
    story.forEach(function (s) {
      if (t < s.t) return;
      var n = s.reveal ? list(s.reveal).length : s.draw ? list(s.draw).length : s.hide ? list(s.hide).length : 1, gap = s.stagger || 0, idur = s.dur - (n - 1) * gap, pi = function (i) { return clamp((t - s.t - i * gap) / idur); }, p = pi(0);
      if (s.reveal) list(s.reveal).forEach(function (id, i) { var g = node(id); if (!g) return; var k = outExpo(pi(i)); g.style.opacity = k * alpha; g.setAttribute('transform', 'translate(0,' + (8 * (1 - k)).toFixed(2) + ')'); shown[id] = 1; });
      if (s.draw) list(s.draw).forEach(function (key, i) { var e = edge(key), d = st[key], pj = pi(i); if (e) { var k = inOut(clamp(pj / DRAW_FRAC)); e.style.opacity = alpha; if (d.da) { e.style.strokeDasharray = d.da; e.style.opacity = k * alpha; } else { e.style.strokeDashoffset = d.len * (1 - k); } if (k >= 0.999 && d.mk) e.setAttribute('marker-end', d.mk); var pl = pill(key); if (pl) pl.style.opacity = clamp((pj - DRAW_FRAC) / (1 - DRAW_FRAC)) * alpha; } });
      if (s.hide) list(s.hide).forEach(function (id, i) { var g = node(id) || edge(id), ph = pi(i); if (g) g.style.opacity = (1 - ph) * alpha * inA; var pl = pill(id); if (pl) pl.style.opacity = (1 - ph) * alpha * inA; if (ph >= 1 && g) g.style.opacity = 0; });
      if (s.active) activeNow = { id: s.active };
    });
    Object.keys(nodeLook).forEach(function (id) { var L = nodeLook[id], on = activeNow.id === id; L.box.setAttribute('fill', on ? 'var(--accent-tint)' : L.o.bf); L.box.setAttribute('stroke', on ? 'var(--accent)' : L.o.bs); if (L.tile) L.tile.setAttribute('fill', on ? 'var(--accent)' : L.o.tf); if (L.icon) L.icon.setAttribute('stroke', on ? 'var(--on-accent)' : L.o.is); });
    packets.forEach(function (P) {
      var p = clamp((t - P.s.t) / P.s.dur), on = t >= P.s.t && p < 1 && P.segs.length;
      P.dot.style.opacity = P.halo.style.opacity = 0; if (!on) return;
      var dist = inOut(p) * P.tot, i = P.cum.length - 1; while (i > 0 && dist < P.cum[i]) i--;
      var pt = P.segs[i].getPointAtLength(Math.min(P.segs[i].getTotalLength(), dist - P.cum[i])), f = Math.min(1, p * 10, (1 - p) * 10) * alpha;
      P.dot.setAttribute('cx', pt.x); P.dot.setAttribute('cy', pt.y); P.halo.setAttribute('cx', pt.x); P.halo.setAttribute('cy', pt.y);
      P.dot.style.opacity = f; P.halo.style.opacity = f * 0.2;
    });
    rings.forEach(function (R) {
      var p = clamp((t - R.s.t) / R.s.dur); R.r.style.opacity = 0; if (!(t >= R.s.t && p < 1) || !R.b) return;
      var g = 14 * outExpo(p), x = +R.b.getAttribute('x'), y = +R.b.getAttribute('y'), w = +R.b.getAttribute('width'), h = +R.b.getAttribute('height');
      R.r.setAttribute('x', x - g); R.r.setAttribute('y', y - g); R.r.setAttribute('width', w + 2 * g); R.r.setAttribute('height', h + 2 * g); R.r.setAttribute('rx', 14 + g); R.r.style.opacity = (1 - p) * 0.55 * alpha;
    });
    Object.keys(badges).forEach(function (id) {
      var B = badges[id], cur = null; story.forEach(function (s) { if (s.badge === id && t >= s.t) cur = s; });
      if (!cur) { B.grp.style.opacity = 0; return; }
      var p = clamp((t - cur.t) / 0.25), w = Math.max(24, 12 + 8 * String(cur.text).length);
      B.tx.textContent = cur.text; B.bg.setAttribute('width', w); B.tx.setAttribute('x', w / 2);
      var k = 0.6 + 0.4 * outExpo(p); B.grp.setAttribute('transform', 'translate(' + (B.x - w / 2) + ',' + B.y + ') translate(' + (w / 2) + ',11) scale(' + k + ') translate(' + (-w / 2) + ',-11)'); B.grp.style.opacity = outExpo(p) * alpha;
    });
  }
  var DRAW_FRAC = 0.7;

  var t0 = 0, playing = false, T = 0, raf = 0;
  var render = function (t) { T = t; frame(t); };
  window.__seek = function (t) { stop(); render(t); };
  window.__anim = { end: END, total: TOTAL, hold: HOLD, maxOpacity: function (t) {   // the highest opacity of anything the story moves at time t
    stop(); render(t); var m = 0;
    dyn.concat(packets.map(function (P) { return P.dot; }), rings.map(function (R) { return R.r; }), Object.keys(badges).map(function (k) { return badges[k].grp; })).forEach(function (e) { m = Math.max(m, parseFloat(e.style.opacity || 0)); });
    return m; } };
  function tick(now) { if (!playing) return; var t = (now - t0) / 1000; if (t >= TOTAL) { if (D.loop) { t0 = now; t = 0; } else { stop(); render(END); return; } } render(t); raf = requestAnimationFrame(tick); }
  function play(from) { stop(); playing = true; t0 = performance.now() - (from || 0) * 1000; setBtn(); raf = requestAnimationFrame(tick); }
  function stop() { playing = false; cancelAnimationFrame(raf); setBtn(); }
  var bp = document.getElementById('b-play'), bs = document.getElementById('b-step'), br = document.getElementById('b-restart');
  function setBtn() { if (bp) bp.textContent = playing ? 'Pause' : (reduce && reduce.matches && T >= END ? 'Play once' : 'Play'); }
  if (bp) bp.onclick = function () { playing ? stop() : play(T >= TOTAL - 0.6 || (reduce && reduce.matches) ? 0 : T); };
  if (br) br.onclick = function () { play(0); };
  if (bs) bs.onclick = function () { stop(); var nxt = story.map(function (s) { return s.t + s.dur; }).filter(function (x) { return x > T + 0.01; }).sort(function (a, b) { return a - b; })[0]; render(nxt === undefined ? 0 : nxt); };
  svg.addEventListener('click', function () { playing ? stop() : play(T >= TOTAL - 0.6 ? 0 : T); });
  function init() { if (reduce && reduce.matches) { stop(); render(END); } else if (/[?&]t=/.test(location.search)) { render(parseFloat(location.search.split('t=')[1])); } else play(0); }
  if (reduce && reduce.addEventListener) reduce.addEventListener('change', init);
  init();
})();
`;

export function buildHtml(spec) {
  const tl = timeline(spec);
  let svg = build(spec).replace(/(<svg[^>]*?) width="\d+" height="\d+"/, '$1');
  const W = Number((svg.match(/viewBox="0 0 (\d+)/) || [])[1] || 1024);
  const data = JSON.stringify({ story: tl.story, end: tl.end, hold: tl.hold, total: tl.total, loop: spec.loop !== false });
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${String(spec.title).replace(/</g, '&lt;')}</title>
<style>
html,body{margin:0;background:var(--surface,#fff)}
body{font-family:var(--sans,Inter,system-ui,sans-serif);color:var(--ink,#14171F);padding:16px;box-sizing:border-box}
main{max-width:${W}px;margin:0 auto}
svg[data-diagram]{display:block;width:100%;height:auto;cursor:pointer}
.ctl{display:flex;gap:8px;margin:12px 0 0 0}
.ctl button{font:600 13px var(--sans);padding:6px 14px;border-radius:999px;border:1px solid var(--hair);background:var(--node);color:var(--ink);cursor:pointer}
.ctl button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
</style></head>
<body><main>
${svg.trim()}
<div class="ctl" role="group" aria-label="Animation controls"><button id="b-play" type="button">Pause</button><button id="b-step" type="button">Next step</button><button id="b-restart" type="button">Restart</button></div>
</main>
<script>window.__DATA=${data};</script>
<script>${PLAYER}</script>
</body></html>
`;
}

if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  const [spec, dest] = process.argv.slice(2);
  if (!spec) { console.error('usage: node animate.mjs spec.json [out.html]'); process.exit(1); }
  try {
    const html = buildHtml(JSON.parse(fs.readFileSync(spec, 'utf8')));
    if (dest) fs.writeFileSync(dest, html); else process.stdout.write(html);
  } catch (err) { console.error('animate.mjs: ' + err.message); process.exit(1); }
}
