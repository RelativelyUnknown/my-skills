# Motion

Use only these motions; each does one job.

| Motion | Job |
| --- | --- |
| **pop** (scale in with slight overshoot) | a new object appears: dot, pill, tile |
| **draw** (stroke grows along a path) | a line, average or guide is being built |
| **fly** (ease in-out between two positions) | an object moves to a new place or role |
| **grow** (zone rises from the axis) | a region is claimed |
| **drop** (dotted guide draws down, fades, pill pops) | a value is read off a chart into a result |
| **ring** (fade in, hold, fade out) | "look here" |
| **shake** (4 px, decaying, 0.45 s) | something failed, just before it changes |

Timing: 25 fps; whole loop 7–10 s; stagger siblings by 0.05–0.15 s; pop 0.25 s, draw 0.25–0.4 s, fly 0.5 s. Build in reading order (inputs, then method, then result). After the last event hold briefly, fade only the content (title stays) over 0.45 s, then show the title-only frame for 0.35 s so the loop restarts cleanly.

## Recipes

Copy the snippet, change names and times. All inside the `finish(dyn, END, t => { … })` callback; `a` is the start time.

## Pop in

```js
pop(dot, seg(t, a, a + .25), cx, cy);                    // scale 0 → 1 with overshoot, around (cx, cy)
```

For a pill drawn at (0,0): `const q = seg(t, a, a + .25); place(g, x, y, ease.back(q)); g.setAttribute('opacity', q > 0 ? 1 : 0);`

## Draw a line

```js
path.setAttribute('opacity', t >= a ? 1 : 0);
draw(path, ease.inOut(seg(t, a, a + .6)));               // stroke grows along the path
```

## Staggered list

```js
items.forEach((it, i) => pop(it.g, seg(t, a + i * .06, a + .25 + i * .06), it.x, it.y));
```

## Fly between two places

```js
const f = ease.inOut(seg(t, a, a + .5));
place(g, lerp(from.x, to.x, f), lerp(from.y, to.y, f), 1);
```

A copy that flies into another object (a value moving into its result): show the copy at `t >= a`, fly it, hide it at arrival (`1 - seg(t, a + .48, a + .52)`), pop the result at the same moment.

## Zone grows from the axis

```js
const p = ease.out(seg(t, a, a + .3));
zone.setAttribute('y', lerp(plot.b, plot.t, p));
zone.setAttribute('height', (plot.b - plot.t) * p);
zone.setAttribute('opacity', p > 0 ? 1 : 0);
```

## Dotted drop into a result

```js
drop.setAttribute('opacity', (t >= a ? 1 : 0) * (1 - seg(t, a + .45, a + .7)));
draw(drop, ease.out(seg(t, a, a + .2)));                 // dashed guide draws down, then fades
// then pop the result pill at a + .15
```

## Highlight ring

```js
ring.setAttribute('opacity', win(t, 5.9, 7.4, .15));     // fade in, hold, fade out
```

## Shake, then replace

```js
const k = seg(t, a, a + .45);
const dx = Math.sin((t - a) * 60) * 4 * (1 - k) * (t > a && k < 1 ? 1 : 0);
// apply dx to x, then hide the tile at a + .5 and pop what replaces it (one or several pieces, 0.06 s stagger)
```

## Fade a group out when it is replaced

```js
group.setAttribute('opacity', 1 - seg(t, a, a + .25));
```
