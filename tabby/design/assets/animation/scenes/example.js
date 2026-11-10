// scenes/example.js — worked example of a split-screen scene (copy it as the start of a new one).
// Same input points on both sides (ink). Left (grey): points merge into per-bin averages.
// Right (accent): a line joins the points and is sampled on the grid. Both results drop into pills.
// Data lives in specs.js (window.SPECS.example); nothing is computed in the scene.
(function () {
  const SP = window.SPECS.example;
  const { dyn } = makeStage(SP.title);
  const head = splitHeader(dyn, SP.labels);
  const L = makeChart(dyn, PANELS.left, SP, { ticks: SP.ticks });
  const R = makeChart(dyn, PANELS.right, SP, { ticks: SP.ticks });
  const PILL_Y = 448, PW = 60;

  // input points on both sides: pop in with a slight overshoot
  const raw = [L, R].map(ch => SP.points.map((p, i) => ({
    c: S('circle', { cx: ch.xOf(p.x), cy: ch.yOf(p.y), r: 4.5, fill: C.INK, opacity: 0 }, ch.raw),
    i, x: ch.xOf(p.x), y: ch.yOf(p.y) })));

  // left: a dotted zone per bin, a dashed average line, then one dot at the bin start
  const BIN0 = 1.2, STEP = .45;
  const bins = SP.left.map((b, k) => {
    const x0 = L.xOf(b.x), x1 = L.xOf(b.x + SP.step), y = L.yOf(b.value), a = BIN0 + 0.6 + k * STEP;
    const zone = S('rect', { x: x0 + 2, y: L.plot.t, width: x1 - x0 - 4, height: 0, rx: 8, fill: C.BASE_ZONE,
      stroke: C.BASE, 'stroke-width': 1.2, 'stroke-dasharray': '1.5 3.5', 'stroke-linecap': 'round', opacity: 0 }, L.zones);
    const avg = S('path', { d: `M${x0 + 6},${y} H${x1 - 6}`, stroke: C.BASE, 'stroke-width': 1.4, 'stroke-dasharray': '4 3', fill: 'none', opacity: 0 }, L.lines);
    const dot = S('circle', { cx: x0, cy: y, r: 6, fill: C.BASE, opacity: 0 }, L.marks);
    return { b, k, x0, y, a, zone, avg, dot };
  });

  // right: the line draws left to right, then a guide + dot per grid step
  const LINE0 = 1.2, LINE1 = 2.4, SAMPLE0 = 2.6, SAMPLE_STEP = .4;
  const line = S('path', { d: 'M' + SP.points.map(p => `${R.xOf(p.x)},${R.yOf(p.y)}`).join(' L'), stroke: C.ACCENT_MID,
    'stroke-width': 2.2, fill: 'none', 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }, R.lines);
  const samples = SP.right.map((s, k) => {
    const x = R.xOf(s.x), y = R.yOf(s.value);
    return { s, k, x, y, a: SAMPLE0 + k * SAMPLE_STEP,
      guide: S('path', { d: `M${x},${R.plot.t} V${y}`, stroke: C.ACCENT_LIGHT, 'stroke-width': 1.4, 'stroke-dasharray': '2 4', fill: 'none', opacity: 0 }, R.lines),
      dot: S('circle', { cx: x, cy: y, r: 6, fill: C.ACCENT, opacity: 0 }, R.marks) };
  });

  // result pills: a dotted drop from each dot, then the pill pops
  const PILLS0 = 4.9;
  const pills = (ch, rows, fill, textFill) => rows.map((r, k) => {
    const x = ch.xOf(r.x);
    return { k, x, g: valuePill(ch.pills, PW, fill, r.text, textFill),
      drop: S('path', { d: `M${x},${ch.yOf(r.value) + 8} V${PILL_Y - PILL_H / 2 - 4}`, stroke: fill === C.BASE ? C.BASE : C.ACCENT_LIGHT,
        'stroke-width': 1.3, 'stroke-dasharray': '2 4', fill: 'none', opacity: 0 }, ch.lines),
      ring: k === SP.highlight ? ring(ch.pills, PW) : null };
  });
  const pl = pills(L, SP.left, C.BASE, C.INK), pr = pills(R, SP.right, C.ACCENT, C.ON_ACCENT);

  const END = 8.0;
  finish(dyn, END, t => {
    head.update(t); L.update(t); R.update(t);
    raw.forEach(side => side.forEach(r => pop(r.c, seg(t, .45 + r.i * .06, .7 + r.i * .06), r.x, r.y)));

    bins.forEach(o => {
      const pz = ease.out(seg(t, BIN0 + o.k * .08, BIN0 + .3 + o.k * .08));
      o.zone.setAttribute('y', lerp(L.plot.b, L.plot.t, pz)); o.zone.setAttribute('height', (L.plot.b - L.plot.t) * pz);
      o.zone.setAttribute('opacity', pz > 0 ? 1 : 0);
      o.avg.setAttribute('opacity', t >= o.a ? 1 : 0); draw(o.avg, ease.out(seg(t, o.a, o.a + .25)));
      pop(o.dot, seg(t, o.a + .2, o.a + .45), o.x0, o.y);
    });

    line.setAttribute('opacity', t >= LINE0 ? 1 : 0); draw(line, ease.inOut(seg(t, LINE0, LINE1)));
    samples.forEach(s => {
      s.guide.setAttribute('opacity', (t >= s.a ? 1 : 0) * (1 - seg(t, s.a + .5, s.a + .8)));
      draw(s.guide, ease.out(seg(t, s.a, s.a + .25)));
      pop(s.dot, seg(t, s.a + .22, s.a + .45), s.x, s.y);
    });

    [pl, pr].forEach(side => side.forEach(p => {
      const a = PILLS0 + p.k * .12;
      p.drop.setAttribute('opacity', (t >= a ? 1 : 0) * (1 - seg(t, a + .45, a + .7)));
      draw(p.drop, ease.out(seg(t, a, a + .2)));
      const q = seg(t, a + .15, a + .4);
      place(p.g, p.x, PILL_Y, ease.back(q)); p.g.setAttribute('opacity', q > 0 ? 1 : 0);
      if (p.ring) { p.ring.setAttribute('opacity', win(t, 5.9, 7.4, .15)); p.ring.setAttribute('transform', `translate(${p.x} ${PILL_Y})`); }
    }));
  });
})();
