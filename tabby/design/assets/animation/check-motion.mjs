#!/usr/bin/env node
// check-motion.mjs: mechanical checks for an animated diagram built by animate.mjs, plus a contact sheet to look at.
//
//   node check-motion.mjs anim.html [--out dir]
//
// Exit 0: clean. Exit 2: at least one failure. Exit 1: could not run (no Playwright, unreadable file).
// Rules (all FAIL):
//   purpose         a step has no "why" (a motion with no purpose is cut)
//   step-budget     more than 8 steps
//   concurrency     more than 2 steps running at once
//   loop-seam       anything the story moves is still visible at the start or at the end of the loop (a jump when it restarts)
//   reduced-motion  with prefers-reduced-motion the page does not stand on its finished picture
//   offline         the page requested anything that is not a local file
//   page-error      a script error or a console error
//   controls        the play, step and restart buttons are missing
// Output: <out>/contact-sheet.png (stills at 0, 25%, 50%, 75% of the story, its end, and the last frame of the loop; light) and the stills.
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { execSync } from 'child_process';

const args = process.argv.slice(2);
const oi = args.indexOf('--out'); const outDir = oi >= 0 ? args.splice(oi, 2)[1] : null;
const file = args[0];
if (!file) { console.error('usage: node check-motion.mjs anim.html [--out dir]'); process.exit(1); }
const load = name => {
  for (const b of [process.cwd() + '/', ...(process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean).map(p => p + '/')]) { try { return createRequire(b)(name); } catch {} }
  try { return createRequire(execSync('npm root -g').toString().trim() + '/')(name); } catch {}
  return null;
};
const pw = load('playwright');
if (!pw) { console.error('check-motion.mjs: Playwright is not installed here; ask before installing it.'); process.exit(1); }

const url = 'file://' + path.resolve(file);
const findings = [];
const fail = (rule, detail) => findings.push([rule, detail]);
const out = outDir || path.join(path.dirname(path.resolve(file)), path.basename(file, '.html') + '-check');
fs.mkdirSync(out, { recursive: true });

const browser = await pw.chromium.launch();
try {
  const ctx = await browser.newContext({ viewport: { width: 1100, height: 700 } });
  const page = await ctx.newPage();
  const errors = [], remote = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => m.type() === 'error' && errors.push(m.text()));
  page.on('request', r => { const u = r.url(); if (!/^(file|data|blob|about):/.test(u)) remote.push(u); });
  await page.goto(url);
  await page.waitForTimeout(200);
  const info = await page.evaluate(() => ({ data: window.__DATA, anim: window.__anim && { end: window.__anim.end, total: window.__anim.total }, buttons: ['b-play', 'b-step', 'b-restart'].filter(id => document.getElementById(id)).length }));
  if (!info.data || !info.anim) { console.error('check-motion.mjs: not an animate.mjs page (no window.__DATA)'); process.exit(1); }
  const { story } = info.data, { end, total } = info.anim;

  story.forEach((s, i) => { if (!String(s.why || '').trim()) fail('purpose', `step ${i + 1} (${['reveal','draw','packet','pulse','badge','active','hide'].find(k => k in s) || 'step'} at ${s.t} s) has no "why"`); });
  if (story.length > 8) fail('step-budget', `${story.length} steps (max 8)`);
  let worst = 0, at = 0;
  for (let t = 0; t < end; t += 0.05) { const n = story.filter(s => s.t <= t && t < s.t + s.dur).length; if (n > worst) { worst = n; at = t; } }
  if (worst > 2) fail('concurrency', `${worst} steps run at once around t=${at.toFixed(2)} s (max 2)`);

  const m0 = await page.evaluate(() => window.__anim.maxOpacity(0));
  const m1 = await page.evaluate(t => window.__anim.maxOpacity(t), total - 0.001);
  if (m0 > 0.03 || m1 > 0.03) fail('loop-seam', `something the story moves is still visible at the loop boundary (start ${m0.toFixed(2)}, end ${m1.toFixed(2)})`);

  if (info.buttons < 3) fail('controls', 'the play, step and restart buttons are missing');
  if (errors.length) fail('page-error', errors[0]);
  if (remote.length) fail('offline', `requested ${remote[0]}`);

  // reduced motion: the page must stand on the finished picture and not play
  const rctx = await browser.newContext({ viewport: { width: 1100, height: 700 }, reducedMotion: 'reduce' });
  const rp = await rctx.newPage();
  await rp.goto(url); await rp.waitForTimeout(400);
  const a = await rp.locator('svg[data-diagram]').screenshot();
  await rp.waitForTimeout(700);
  const b = await rp.locator('svg[data-diagram]').screenshot();
  await rp.evaluate(t => window.__seek(t), end);
  const c = await rp.locator('svg[data-diagram]').screenshot();
  if (Buffer.compare(a, b) !== 0 || Buffer.compare(a, c) !== 0) fail('reduced-motion', 'with prefers-reduced-motion the picture still changes or is not the end state');
  await rctx.close();

  // contact sheet
  const times = [0, end * 0.25, end * 0.5, end * 0.75, end, total - 0.001].map(t => Math.round(t * 100) / 100);
  const shots = [];
  for (const t of times) {
    await page.evaluate(s => window.__seek(s), t); await page.waitForTimeout(60);
    const f = path.join(out, `t${String(t).replace('.', '_')}.png`);
    await page.locator('svg[data-diagram]').screenshot({ path: f }); shots.push([t, f]);
  }
  const sheetFile = path.join(out, 'contact-sheet.html');
  fs.writeFileSync(sheetFile, `<!doctype html><meta charset="utf-8"><style>body{margin:0;font:12px system-ui;background:#fff;display:grid;grid-template-columns:repeat(3,1fr);gap:8px;padding:8px}figure{margin:0}img{width:100%;border:1px solid #ddd}</style>` + shots.map(([t, f]) => `<figure><img src="${path.basename(f)}"><figcaption>t = ${t} s</figcaption></figure>`).join(''));
  const sheet = await ctx.newPage();
  await sheet.goto('file://' + sheetFile); await sheet.waitForTimeout(200);
  await sheet.screenshot({ path: path.join(out, 'contact-sheet.png'), fullPage: true });
} finally { await browser.close(); }

for (const [rule, detail] of findings) console.log(`FAIL ${rule} ${file}: ${detail}`);
if (!findings.length) console.log(`OK ${file}`);
console.log(`contact sheet: ${path.join(out, 'contact-sheet.png')}`);
process.exit(findings.length ? 2 : 0);
