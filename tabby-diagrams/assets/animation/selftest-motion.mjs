#!/usr/bin/env node
// selftest-motion.mjs: prove check-motion.mjs can fail.
//   node selftest-motion.mjs
// Gate 1: every template in templates/ builds and passes. Gate 2: each seeded defect below trips the rule it targets.
// Needs Playwright (as check-motion.mjs does). Exit 0 if all hold, 1 otherwise.
import fs from 'fs';
import os from 'os';
import path from 'path';
import { spawnSync } from 'child_process';
import { fileURLToPath } from 'url';
import { buildHtml } from './animate.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'motion-'));
const run = f => { const r = spawnSync('node', [path.join(here, 'check-motion.mjs'), f, '--out', path.join(tmp, path.basename(f) + '-out')], { encoding: 'utf8' }); return { code: r.status, out: r.stdout + r.stderr }; };
let ok = true;

const templates = fs.readdirSync(path.join(here, 'templates')).filter(f => f.endsWith('.json'));
for (const t of templates) {
  const f = path.join(tmp, t.replace('.json', '.html'));
  fs.writeFileSync(f, buildHtml(JSON.parse(fs.readFileSync(path.join(here, 'templates', t), 'utf8'))));
  const r = run(f);
  console.log(r.code === 0 ? 'PASS' : 'FAIL', 'template clean:', t);
  if (r.code !== 0) { ok = false; console.log(r.out); }
}

const spec = JSON.parse(fs.readFileSync(path.join(here, 'templates', 'flow.json'), 'utf8'));
const withStory = story => buildHtml({ ...spec, story });
const base = buildHtml(spec);
const controls = {
  'purpose': () => withStory(spec.story.map(({ why, ...rest }) => rest)),
  'step-budget': () => withStory(Array.from({ length: 9 }, (_, i) => ({ t: i * 0.8, reveal: ['client', 'api', 'queue', 'worker'][i % 4], why: 'x' }))),
  'concurrency': () => withStory([{ t: 0, reveal: 'client', why: 'x' }, { t: 0.1, reveal: 'api', why: 'x' }, { t: 0.2, reveal: 'queue', why: 'x' }]),
  'loop-seam': () => base.replace(/var out = clamp\(\(T - \(END \+ HOLD\)\) \/ 0\.5\), alpha = 1 - out, inA = clamp\(T \/ 0\.4\);/, 'var out = 0, alpha = 1, inA = 1;'),
  'reduced-motion': () => base.replace("if (reduce && reduce.matches) { stop(); render(END); }", "if (false) {}"),
  'offline': () => base.replace('</head>', '<link rel="stylesheet" href="https://example.com/x.css"></head>'),
  'page-error': () => base.replace('</body>', '<script>throw new Error("boom")</script></body>'),
  'controls': () => base.replace(/<div class="ctl"[\s\S]*?<\/div>/, ''),
};
for (const [rule, make] of Object.entries(controls)) {
  const f = path.join(tmp, rule + '.html');
  let html; try { html = make(); } catch (e) { console.log('FAIL control', rule, '->', e.message); ok = false; continue; }
  if (html === base) { console.log('FAIL control', rule, '-> mutation did not apply'); ok = false; continue; }
  fs.writeFileSync(f, html);
  const r = run(f), hit = r.out.includes(`FAIL ${rule} `) && r.code === 2;
  console.log(hit ? 'PASS' : 'FAIL', 'control trips', rule);
  if (!hit) { ok = false; console.log(r.out); }
}
console.log('selftest-motion:', ok ? 'ok' : 'FAILED');
fs.rmSync(tmp, { recursive: true, force: true });
process.exit(ok ? 0 : 1);
