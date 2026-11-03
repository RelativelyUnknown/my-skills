# Motion recipes

Copy the snippet, change names and times. All inside the `finish(dyn, END, t => { … })` callback; `a` is the start time.

## Contents

- Pop in
- Draw a line
- Staggered list
- Fly between two places
- Zone grows from the axis
- Dotted drop into a result
- Highlight ring
- Shake then split
- Fade a group out when it is replaced

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

Copies that fly into a merge: show the copy at `t >= a`, fly it, hide it at arrival (`1 - seg(t, a + .48, a + .52)`), pop the merged result at the same moment.

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

## Shake then split

```js
const k = seg(t, a, a + .45);
const dx = Math.sin((t - a) * 60) * 4 * (1 - k) * (t > a && k < 1 ? 1 : 0);
// apply dx to x, then hide the tile at a + .5 and pop its two halves with a 0.06 s stagger
```

## Fade a group out when it is replaced

```js
group.setAttribute('opacity', 1 - seg(t, a, a + .25));
```
