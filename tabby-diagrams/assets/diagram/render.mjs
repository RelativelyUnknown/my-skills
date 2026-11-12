#!/usr/bin/env node
// render.mjs: render an SVG or animated HTML to PNG in light and dark, so it can be looked at.
//
//   node render.mjs in.svg [out]            writes out.png and out-dark.png (default: next to the input)
//   node render.mjs in.html out --at 0,2,4  stills at those seconds (animations; needs the page's controller)
//   options: --scale 2 (default 1; use 2 for a picture a person will see)  --width 1200
//
// Needs Playwright with Chromium (already required by the animation engine). Inter and JetBrains Mono are used
// when the @fontsource packages are resolvable from the working folder; otherwise the stack falls back.
import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
import { execSync } from 'child_process';

const args = process.argv.slice(2);
const opt = (name, d) => { const i = args.indexOf(name); if (i < 0) return d; const v = args[i + 1]; args.splice(i, 2); return v; };
const scale = Number(opt('--scale', 1)), width = Number(opt('--width', 0)), at = opt('--at', '');
const [input, outArg] = args;
if (!input) { console.error('usage: node render.mjs in.svg|in.html [out] [--scale 2] [--at 0,2,4]'); process.exit(1); }

function load(name) {
  for (const base of [process.cwd() + '/', ...(process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean).map(p => p + '/')]) {
    try { return createRequire(base)(name); } catch {}
  }
  try { return createRequire(execSync('npm root -g').toString().trim() + '/')(name); } catch {}
  return null;
}
const pw = load('playwright');
if (!pw) { console.error('render.mjs: Playwright is not installed here. Ask before installing it (npm i playwright, then npx playwright install chromium).'); process.exit(1); }

const base = outArg || input.replace(/\.(svg|html)$/i, '');
const src = fs.readFileSync(input, 'utf8');
const isHtml = /\.html?$/i.test(input);
let fonts = '';
try {
  const inter = path.dirname(createRequire(process.cwd() + '/')?.resolve?.('@fontsource/inter/package.json'));
  fonts = [400, 600, 700].map(w => `@font-face{font-family:Inter;font-weight:${w};src:url(file://${inter}/files/inter-latin-${w}-normal.woff2)}`).join('');
} catch { console.error('note: @fontsource/inter not found; using the fallback font stack'); }

const browser = await pw.chromium.launch();
try {
  for (const scheme of ['light', 'dark']) {
    const page = await browser.newPage({ colorScheme: scheme, deviceScaleFactor: scale, viewport: { width: width || 1280, height: 800 } });
    if (isHtml) await page.goto('file://' + path.resolve(input)); else await page.setContent(`<style>${fonts}html,body{margin:0}svg{display:block}</style>${src}`);
    await page.waitForTimeout(250);
    const times = at ? at.split(',').map(Number) : [null];
    for (const t of times) {
      if (t !== null) await page.evaluate(s => window.__seek && window.__seek(s), t);
      const suffix = (scheme === 'dark' ? '-dark' : '') + (t !== null ? `-t${t}` : '');
      const el = await page.$(isHtml ? 'svg' : 'svg');
      await (el || page).screenshot({ path: `${base}${suffix}.png` });
      console.log(`${base}${suffix}.png`);
    }
    await page.close();
  }
} finally { await browser.close(); }
