// scenes/example.js — a worked example (copy it as the start of a new scene): a request through a service.
// Roles follow style.md: ink tiles are the given parts, the accent path is the focus (the main request),
// grey is secondary, dashed is the retry. Data lives in specs.js (window.SPECS.example); nothing is computed here.
(function () {
  const SP = window.SPECS.example;
  const { dyn } = makeStage(SP.title);
  const TW = 150, TH = 56, R = 8;
  const byId = {};

  // tiles: pop in, one after another
  SP.nodes.forEach((n, i) => {
    const g = S('g', { opacity: 0 }, dyn);
    S('rect', { x: n.x - TW / 2, y: n.y - TH / 2, width: TW, height: TH, rx: R, fill: C.WHITE, stroke: C.INK, 'stroke-width': 1.5 }, g);
    T(g, n.x, n.y - 3, n.name, { 'font-family': FONT.sans, 'font-weight': 600, 'font-size': 14 });
    T(g, n.x, n.y + 14, n.role, { 'font-size': 11, fill: C.LABEL });
    byId[n.id] = Object.assign({ g, a: .4 + i * .3 }, n);
  });

  // the one thing to look at: an ink ring, drawn under the connections
  const hl = byId[SP.highlight];
  const ring = S('rect', { x: hl.x - TW / 2 - 4, y: hl.y - TH / 2 - 4, width: TW + 8, height: TH + 8, rx: R + 3.5, fill: 'none', stroke: C.INK, 'stroke-width': 1.6, opacity: 0 }, dyn);

  // connections: orthogonal, drawn after both ends exist; the retry is a dashed elbow under the row
  const arrow = (x, y, dir, fill) => S('path', { d: dir === 'right' ? `M${x},${y} l-8,-4.5 v9 z` : dir === 'up' ? `M${x},${y} l-4.5,8 h9 z` : `M${x},${y} l-4.5,-8 h9 z`, fill, opacity: 0 }, dyn);
  const edges = SP.edges.map((e, k) => {
    const a = byId[e.from], b = byId[e.to];
    const a0 = Math.max(a.a, b.a) + .5 + k * .35;
    let d, head, lx, ly, color, dash;
    if (e.kind === 'retry') {
      const x1 = a.x - 30, x2 = b.x + 30, yb = a.y + TH / 2, yl = a.y + 72;
      d = `M${x1},${yb} V${yl - R} Q${x1},${yl} ${x1 - R},${yl} H${x2 + R} Q${x2},${yl} ${x2},${yl - R} V${b.y + TH / 2 + 6}`;
      head = arrow(x2, b.y + TH / 2, 'up', C.SLOT); color = C.SLOT; dash = '4 3'; lx = (x1 + x2) / 2; ly = yl + 16;
    } else if (a.y === b.y) {
      const x1 = a.x + TW / 2, x2 = b.x - TW / 2;
      d = `M${x1},${a.y} H${x2 - 6}`; head = arrow(x2, a.y, 'right', e.kind === 'main' ? C.ACCENT : C.BASE);
      color = e.kind === 'main' ? C.ACCENT_MID : C.BASE; lx = (x1 + x2) / 2; ly = a.y - 10;
    } else {
      const y1 = a.y + TH / 2, y2 = b.y - TH / 2;
      d = `M${a.x},${y1} V${y2 - 6}`; head = arrow(a.x, y2, 'down', C.BASE); color = C.BASE; lx = a.x + 14; ly = (y1 + y2) / 2 + 4;
    }
    const path = S('path', Object.assign({ d, stroke: color, 'stroke-width': e.kind === 'main' ? 2.2 : 1.5, fill: 'none', 'stroke-linecap': 'round', opacity: 0 }, dash ? { 'stroke-dasharray': dash } : {}), dyn);
    const label = T(dyn, lx, ly, e.label, { 'font-size': 11, fill: C.LABEL, 'text-anchor': e.kind === 'secondary' ? 'start' : 'middle', opacity: 0 });
    return { e, path, head, label, a0, dash };
  });

  const END = 7.4;
  finish(dyn, END, t => {
    Object.values(byId).forEach(n => pop(n.g, seg(t, n.a, n.a + .25), n.x, n.y));
    edges.forEach(o => {
      const p = seg(t, o.a0, o.a0 + .4);
      o.path.setAttribute('opacity', t >= o.a0 ? 1 : 0);
      if (o.dash) o.path.setAttribute('opacity', ease.out(p)); else draw(o.path, ease.inOut(p));
      o.head.setAttribute('opacity', p >= 1 ? 1 : 0);
      o.label.setAttribute('opacity', seg(t, o.a0 + .3, o.a0 + .55));
    });
    ring.setAttribute('opacity', win(t, 5.6, 7.0, .2));
  });
})();
