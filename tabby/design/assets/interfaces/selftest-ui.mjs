#!/usr/bin/env node
// selftest-ui.mjs: prove ui-check.mjs can fail.   node selftest-ui.mjs
// Gate 1: fixtures/clean.html exits 0 with no FAIL. Gate 2: fixtures/bad.html reports every rule it seeds.
// Gate 3: a waiver with a real reason marks a finding WAIVED; one with a short reason does not.
import fs from 'fs';
import os from 'os';
import path from 'path';
import { spawnSync } from 'child_process';
import { fileURLToPath } from 'url';

const here = path.dirname(fileURLToPath(import.meta.url));
const run = (...a) => { const r = spawnSync('node', [path.join(here, 'ui-check.mjs'), ...a], { encoding: 'utf8' }); return { code: r.status, out: r.stdout + r.stderr }; };
let ok = true;
const check = (cond, msg) => { console.log(cond ? 'PASS' : 'FAIL', msg); if (!cond) ok = false; };

const clean = run(path.join(here, 'fixtures/clean.html'));
check(clean.code === 0 && !/^FAIL/m.test(clean.out), 'clean page has no failures'); if (clean.code !== 0) console.log(clean.out);

const bad = run(path.join(here, 'fixtures/bad.html'));
const seeded = ['document', 'overflow-x', 'tiny-text', 'contrast', 'tap-size', 'heading-order', 'focus-visible', 'img-alt', 'form-label', 'reduced-motion', 'refuse-gradient-text', 'refuse-hard-shadow', 'refuse-side-stripe', 'refuse-glow'];
check(bad.code === 2, 'bad page exits 2');
for (const rule of seeded) check(new RegExp(`^FAIL ${rule} `, 'm').test(bad.out), `bad page trips ${rule}`);

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'uiw-'));
const good = path.join(tmp, 'good.json'), short = path.join(tmp, 'short.json');
fs.writeFileSync(good, JSON.stringify([{ rule: 'img-alt', target: 'img', reason: 'decorative image in the fixture' }]));
fs.writeFileSync(short, JSON.stringify([{ rule: 'img-alt', target: 'img', reason: 'no' }]));
check(/^WAIVED img-alt /m.test(run(path.join(here, 'fixtures/bad.html'), '--waivers', good).out), 'a waiver with a reason waives');
check(/^FAIL img-alt /m.test(run(path.join(here, 'fixtures/bad.html'), '--waivers', short).out), 'a waiver with a short reason does not');
fs.rmSync(tmp, { recursive: true, force: true });
console.log('selftest-ui:', ok ? 'ok' : 'FAILED');
process.exit(ok ? 0 : 1);
