#!/usr/bin/env node
// render.js — render one scene to PNG frames with headless Chromium (Playwright).
//
// Usage: node render.js <assets_dir> <scene> <out_dir> [--fps 25] [--times 1.5,3.3,6.2]
//   <assets_dir>  folder holding stage.html, specs.js, scenes/ and node_modules/ (fonts)
//   <scene>       a key of window.SPECS, and the file scenes/<scene>.js
//   --times       render only these moments (seconds): quick previews while designing
//
// Frames are 2× (1920×1080 for the 960×540 stage). Every frame is a pure function of time,
// so the same inputs give byte-identical frames.
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const [assets, scene, outDir, ...rest] = process.argv.slice(2);
if (!assets || !scene || !outDir) { console.error('usage: render.js <assets_dir> <scene> <out_dir> [--fps N] [--times a,b]'); process.exit(2); }
const opt = k => { const i = rest.indexOf(k); return i >= 0 ? rest[i + 1] : null; };
const fps = Number(opt('--fps') || 25);
const times = opt('--times') ? opt('--times').split(',').map(Number) : null;

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 960, height: 540 }, deviceScaleFactor: 2 });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(`file://${path.resolve(assets)}/stage.html?scene=${scene}`);
  await page.waitForFunction('window.renderAt !== undefined', null, { timeout: 10000 });
  await page.evaluate(() => Promise.all(['600 26px IN', '400 16px IN', '500 16px IN', '400 14px JBM'].map(f => document.fonts.load(f))));
  await page.evaluate(() => document.fonts.ready);
  if (errors.length) throw new Error(`${scene}: ${errors.join('; ')}`);
  const dur = await page.evaluate('window.DURATION');
  const [w, h] = await page.evaluate('[window.STAGE_W, window.STAGE_H]');
  await page.setViewportSize({ width: w, height: h });
  const stamps = times || Array.from({ length: Math.round(dur * fps) }, (_, i) => i / fps);
  for (let i = 0; i < stamps.length; i++) {
    await page.evaluate(t => renderAt(t), stamps[i]);
    const name = times ? `t_${stamps[i].toFixed(2).padStart(5, '0')}.png` : `f_${String(i).padStart(4, '0')}.png`;
    await page.screenshot({ path: path.join(outDir, name), clip: { x: 0, y: 0, width: w, height: h } });
  }
  if (errors.length) throw new Error(`${scene}: ${errors.join('; ')}`);
  await browser.close();
  console.log(`${scene}: ${stamps.length} frames → ${outDir}  (loop ${dur.toFixed(2)} s)`);
})().catch(e => { console.error(e.message); process.exit(1); });
