#!/usr/bin/env node
// ui-check.mjs: mechanical checks for a page or an app screen, in a real browser (Chromium).
//
//   node ui-check.mjs <url or file.html> [--waivers waivers.json] [--json]
//
// Exit 0: no failures (warnings may print). Exit 2: at least one failure. Exit 1: could not run.
// It loads the page at 390x844 and at 1280x800 and checks what is measurable. Judgment (hierarchy, fit, voice) is not here.
//
// FAIL: contrast (text under 4.5:1, large text under 3:1; skipped where the background is an image or gradient)
//       overflow-x (the page scrolls sideways)         tap-size (an interactive element under 24 px, at 390)
//       heading-order (not exactly one h1, or a skipped level)    focus-visible (Tab lands on something with no visible focus)
//       img-alt   form-label   document (lang or title missing)   tiny-text (under 12 px)
//       reduced-motion (an infinite animation still runs under prefers-reduced-motion)   page-error
//       refuse-gradient-text   refuse-hard-shadow (blur 0, offset 4 px or more)   refuse-side-stripe (a 3 px+ border on one side only)
//       refuse-glow (a coloured zero-offset shadow of 16 px or more)
// WARN: measure (lines over about 90 characters)   tap-comfort (under 44 px)   refuse-glass (backdrop blur on 3+ elements)
//
// Waivers (a finding judged false): a JSON list [{ "rule": "tap-size", "target": "a.skip", "reason": "at least 12 characters" }].
// A waiver covers findings whose rule matches and whose target text contains "target" (3+ characters). It prints as WAIVED.
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { execSync } from 'child_process';

const args = process.argv.slice(2);
const flag = n => { const i = args.indexOf(n); if (i < 0) return false; args.splice(i, 1); return true; };
const opt = n => { const i = args.indexOf(n); if (i < 0) return null; const v = args[i + 1]; args.splice(i, 2); return v; };
const asJson = flag('--json'); const wfile = opt('--waivers');
const target = args[0];
if (!target) { console.error('usage: node ui-check.mjs <url or file.html> [--waivers waivers.json] [--json]'); process.exit(1); }
const load = name => {
  for (const b of [process.cwd() + '/', ...(process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean).map(p => p + '/')]) { try { return createRequire(b)(name); } catch {} }
  try { return createRequire(execSync('npm root -g').toString().trim() + '/')(name); } catch {}
  return null;
};
const pw = load('playwright');
if (!pw) { console.error('ui-check.mjs: Playwright is not installed here. Ask before installing it.'); process.exit(1); }
const url = /^[a-z]+:\/\//i.test(target) ? target : 'file://' + path.resolve(target);
let waivers = [];
const wpath = wfile || (fs.existsSync('.tabby-ui-waivers.json') ? '.tabby-ui-waivers.json' : null);
if (wpath) { try { waivers = JSON.parse(fs.readFileSync(wpath, 'utf8')); } catch (e) { console.error('ui-check.mjs: cannot read waivers: ' + e.message); process.exit(1); } }

// runs inside the page
function inPage(vp) {
  const out = [];
  const add = (level, rule, el, detail) => out.push({ level, rule, vp, target: desc(el), detail });
  const desc = el => !el || !el.tagName ? 'page' : el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '');
  const vis = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && s.opacity !== '0'; };
  const rgba = c => { const m = String(c).match(/[\d.]+/g); if (!m) return null; const [r, g, b, a] = m.map(Number); return [r, g, b, a === undefined ? 1 : a]; };
  const over = (top, bot) => { const a = top[3]; return [top[0] * a + bot[0] * (1 - a), top[1] * a + bot[1] * (1 - a), top[2] * a + bot[2] * (1 - a), 1]; };
  const lum = c => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126 * f(c[0]) + .7152 * f(c[1]) + .0722 * f(c[2]); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
  const bgOf = el => {
    const layers = [];
    for (let e = el; e; e = e.parentElement) { const s = getComputedStyle(e); if (s.backgroundImage !== 'none') return null; const c = rgba(s.backgroundColor); if (c && c[3] > 0) layers.push(c); if (c && c[3] >= 1) break; }
    let base = [255, 255, 255, 1]; for (let i = layers.length - 1; i >= 0; i--) base = over(layers[i], base); return base;
  };

  const root = document.documentElement;
  // document
  if (!root.getAttribute('lang')) add('FAIL', 'document', root, 'the <html> element has no lang');
  if (!document.title.trim()) add('FAIL', 'document', root, 'the page has no <title>');
  // overflow
  if (root.scrollWidth > window.innerWidth + 1) add('FAIL', 'overflow-x', root, `the page is ${root.scrollWidth}px wide in a ${window.innerWidth}px window`);
  // text
  const seen = new Set();
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const n = walker.currentNode; if (!n.nodeValue.trim()) continue; const el = n.parentElement; if (!el || seen.has(el) || !vis(el)) continue;
    if (['SCRIPT', 'STYLE', 'NOSCRIPT'].includes(el.tagName)) continue; seen.add(el);
    const s = getComputedStyle(el), fs = parseFloat(s.fontSize), bold = parseInt(s.fontWeight) >= 700, large = fs >= 24 || (bold && fs >= 18.66);
    if (fs < 12) add('FAIL', 'tiny-text', el, `${fs}px text`);
    const fg = rgba(s.color), bg = bgOf(el);
    if (fg && bg) { const f = fg[3] < 1 ? over(fg, bg) : fg, r = ratio(f, bg), need = large ? 3 : 4.5; if (r < need) add('FAIL', 'contrast', el, `${r.toFixed(2)}:1, needs ${need}:1`); }
    if (['P', 'LI', 'DD', 'BLOCKQUOTE'].includes(el.tagName) && n.nodeValue.length > 120) { const cpl = el.getBoundingClientRect().width / (fs * 0.5); if (cpl > 95) add('WARN', 'measure', el, `about ${Math.round(cpl)} characters per line`); }
    if ((s.backgroundClip === 'text' || s.webkitBackgroundClip === 'text') && s.backgroundImage.includes('gradient')) add('FAIL', 'refuse-gradient-text', el, 'text filled with a gradient');
  }
  // interactive
  const interactive = [...document.querySelectorAll('a[href],button,input:not([type=hidden]),select,textarea,[role=button],[tabindex]:not([tabindex="-1"])')].filter(vis);
  if (vp === 390) for (const el of interactive) {
    const r = el.getBoundingClientRect(), s = getComputedStyle(el), inline = el.tagName === 'A' && s.display === 'inline';
    if (inline) continue; const m = Math.min(r.width, r.height);
    if (m < 24) add('FAIL', 'tap-size', el, `${Math.round(r.width)}x${Math.round(r.height)}px, needs 24`); else if (m < 44) add('WARN', 'tap-comfort', el, `${Math.round(r.width)}x${Math.round(r.height)}px, 44 is comfortable`);
  }
  // headings
  const hs = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(vis), h1 = hs.filter(h => h.tagName === 'H1').length;
  if (h1 !== 1) add('FAIL', 'heading-order', root, `${h1} h1 elements (needs exactly one)`);
  let prev = 0; for (const h of hs) { const l = +h.tagName[1]; if (prev && l > prev + 1) add('FAIL', 'heading-order', h, `h${prev} is followed by h${l}`); prev = l; }
  // images and forms
  for (const img of document.querySelectorAll('img')) if (!img.hasAttribute('alt')) add('FAIL', 'img-alt', img, 'no alt attribute (use alt="" for decoration)');
  for (const f of document.querySelectorAll('input:not([type=hidden]):not([type=submit]):not([type=button]),select,textarea')) {
    const labelled = f.getAttribute('aria-label') || f.getAttribute('aria-labelledby') || (f.id && document.querySelector(`label[for="${f.id}"]`)) || f.closest('label') || f.getAttribute('title');
    if (!labelled) add('FAIL', 'form-label', f, 'no label');
  }
  // known default looks
  let glass = 0;
  for (const el of document.querySelectorAll('body *')) {
    if (!vis(el)) continue; const s = getComputedStyle(el);
    if ((s.backdropFilter || s.webkitBackdropFilter || '').includes('blur')) glass++;
    const bl = parseFloat(s.borderLeftWidth), br = parseFloat(s.borderRightWidth), bt = parseFloat(s.borderTopWidth), bb = parseFloat(s.borderBottomWidth);
    if ((bl >= 3 && br <= 1 && bt <= 1 && bb <= 1 && s.borderLeftStyle !== 'none') || (br >= 3 && bl <= 1 && bt <= 1 && bb <= 1 && s.borderRightStyle !== 'none')) add('FAIL', 'refuse-side-stripe', el, 'a thick border on one side only');
    if (s.boxShadow && s.boxShadow !== 'none') for (const part of s.boxShadow.split(/,(?![^(]*\))/)) {
      if (/inset/.test(part)) continue; const nums = (part.replace(/rgba?\([^)]*\)/, '').match(/-?[\d.]+px/g) || []).map(parseFloat), col = rgba((part.match(/rgba?\([^)]*\)/) || [''])[0]);
      const [x = 0, y = 0, blur = 0] = nums;
      if (blur === 0 && (Math.abs(x) >= 4 || Math.abs(y) >= 4)) add('FAIL', 'refuse-hard-shadow', el, `hard offset shadow ${x}px ${y}px`);
      if (x === 0 && y === 0 && blur >= 16 && col && col[3] > 0.15 && !(col[0] === col[1] && col[1] === col[2] && col[0] < 40)) add('FAIL', 'refuse-glow', el, `coloured glow, ${blur}px`);
    }
  }
  if (glass >= 3) add('WARN', 'refuse-glass', root, `${glass} elements use backdrop blur`);
  return out;
}

const browser = await pw.chromium.launch();
const all = [];
try {
  for (const [w, h] of [[390, 844], [1280, 800]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h } }), page = await ctx.newPage();
    const errs = []; page.on('pageerror', e => errs.push(e.message));
    await page.goto(url); await page.waitForTimeout(300);
    all.push(...await page.evaluate(inPage, w));
    errs.forEach(e => all.push({ level: 'FAIL', rule: 'page-error', vp: w, target: 'page', detail: e }));
    // keyboard focus: Tab through the first dozen stops and read what shows
    const stops = new Set();
    for (let i = 0; i < 12; i++) {
      await page.keyboard.press('Tab');
      const r = await page.evaluate(() => { const e = document.activeElement; if (!e || e === document.body) return null; const s = getComputedStyle(e); const ok = (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0) || (s.boxShadow && s.boxShadow !== 'none'); const t = e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\s+/).slice(0, 2).join('.') : ''); return { t, ok }; });
      if (!r || stops.has(r.t + i)) continue; stops.add(r.t + i);
      if (!r.ok) all.push({ level: 'FAIL', rule: 'focus-visible', vp: w, target: r.t, detail: 'Tab lands here and nothing shows it' });
    }
    await ctx.close();
  }
  // reduced motion: an infinite animation must stop
  const rctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, reducedMotion: 'reduce' }), rp = await rctx.newPage();
  await rp.goto(url); await rp.waitForTimeout(400);
  const running = await rp.evaluate(() => document.getAnimations().filter(a => a.playState === 'running' && a.effect && a.effect.getComputedTiming().iterations === Infinity).length);
  if (running) all.push({ level: 'FAIL', rule: 'reduced-motion', vp: 1280, target: 'page', detail: `${running} infinite animation(s) still run under prefers-reduced-motion` });
  await rctx.close();
} catch (err) { console.error('ui-check.mjs: ' + err.message); await browser.close(); process.exit(1); }
await browser.close();

// merge across viewports, apply waivers
const merged = new Map();
for (const f of all) { const k = `${f.level}|${f.rule}|${f.target}|${f.detail}`; if (!merged.has(k)) merged.set(k, { ...f, vps: [f.vp] }); else merged.get(k).vps.push(f.vp); }
const waived = f => waivers.find(w => w.rule === f.rule && String(w.target || '').length >= 3 && f.target.includes(w.target) && String(w.reason || '').length >= 12);
const results = [...merged.values()].map(f => ({ ...f, waived: !!waived(f) }));
const fails = results.filter(f => f.level === 'FAIL' && !f.waived);
if (asJson) console.log(JSON.stringify(results, null, 2));
else {
  for (const f of results) console.log(`${f.waived ? 'WAIVED' : f.level} ${f.rule} ${f.target} @${[...new Set(f.vps)].join('/')}: ${f.detail}`);
  if (!results.length) console.log(`OK ${target}`);
}
process.exit(fails.length ? 2 : 0);
