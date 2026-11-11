#!/usr/bin/env node
// render-video.mjs: encode an animated diagram (animate.mjs output) as MP4, WebM or GIF.
// Only on request: the animated HTML is the default deliverable. Frames come from seeking the page's
// pure function of time, so every run is identical.
//
//   node render-video.mjs anim.html out.mp4|out.webm|out.gif [--fps 30] [--scale 2] [--dark] [--loops 1]
//
// Needs Playwright with Chromium and ffmpeg: ask before installing either. Inter is used when @fontsource/inter
// resolves from the working folder, so install it there for video that matches the diagram exactly (otherwise a fallback font shows).
import fs from 'fs';
import os from 'os';
import path from 'path';
import { createRequire } from 'module';
import { execSync, spawnSync } from 'child_process';

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(n); if (i < 0) return d; const v = args[i + 1]; args.splice(i, 2); return v; };
const flag = n => { const i = args.indexOf(n); if (i < 0) return false; args.splice(i, 1); return true; };
const fps = Number(opt('--fps', 30)), scale = Number(opt('--scale', 2)), loops = Number(opt('--loops', 1)), dark = flag('--dark');
const [input, output] = args;
if (!input || !output || !/\.(mp4|webm|gif)$/i.test(output)) { console.error('usage: node render-video.mjs anim.html out.mp4|webm|gif [--fps 30] [--scale 2] [--dark] [--loops 1]'); process.exit(1); }
if (spawnSync('ffmpeg', ['-version']).status !== 0) { console.error('render-video.mjs: ffmpeg is not installed here. Ask before installing it.'); process.exit(1); }
const load = name => {
  for (const b of [process.cwd() + '/', ...(process.env.NODE_PATH || '').split(path.delimiter).filter(Boolean).map(p => p + '/')]) { try { return createRequire(b)(name); } catch {} }
  try { return createRequire(execSync('npm root -g').toString().trim() + '/')(name); } catch {}
  return null;
};
const pw = load('playwright');
if (!pw) { console.error('render-video.mjs: Playwright is not installed here. Ask before installing it.'); process.exit(1); }

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'frames-'));
const browser = await pw.chromium.launch();
try {
  const page = await browser.newPage({ colorScheme: dark ? 'dark' : 'light', deviceScaleFactor: scale, viewport: { width: 1280, height: 800 } });
  await page.goto('file://' + path.resolve(input));
  await page.waitForTimeout(300);
  const total = await page.evaluate(() => window.__anim.total);
  const n = Math.round(total * fps) * loops;
  const svg = page.locator('svg[data-diagram]');
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.__seek(t), (i / fps) % total);
    await svg.screenshot({ path: path.join(tmp, `f_${String(i + 1).padStart(5, '0')}.png`) });
  }
  const inp = ['-loglevel', 'error', '-y', '-framerate', String(fps), '-i', path.join(tmp, 'f_%05d.png')];
  const even = 'scale=trunc(iw/2)*2:trunc(ih/2)*2';
  let cmds;
  if (/\.mp4$/i.test(output)) cmds = [[...inp, '-vf', even, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'slow', '-movflags', '+faststart', output]];
  else if (/\.webm$/i.test(output)) cmds = [[...inp, '-vf', even, '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '34', '-row-mt', '1', '-pix_fmt', 'yuv420p', output]];
  else {
    const pal = path.join(tmp, 'palette.png'), sc = 'scale=iw/2:ih/2:flags=lanczos';
    cmds = [[...inp, '-vf', `${sc},palettegen=max_colors=96:stats_mode=full`, pal], [...inp, '-i', pal, '-lavfi', `${sc}[x];[x][1:v]paletteuse=dither=none:diff_mode=rectangle`, '-loop', '0', output]];
  }
  for (const c of cmds) { const r = spawnSync('ffmpeg', c, { encoding: 'utf8' }); if (r.status !== 0) { console.error(r.stderr); process.exit(1); } }
  console.log(`${output}: ${n} frames at ${fps} fps, ${(n / fps).toFixed(1)} s`);
} finally { await browser.close(); fs.rmSync(tmp, { recursive: true, force: true }); }
