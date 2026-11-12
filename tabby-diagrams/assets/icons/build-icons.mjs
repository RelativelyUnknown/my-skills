// Regenerates tabler-outline.json from the npm package @tabler/icons (MIT, see LICENSE.tabler).
// Usage: node build-icons.mjs <path-to-node_modules/@tabler/icons>
// Output: { "<icon-name>": "<inner SVG markup for a 24x24 outline icon>" }
import fs from 'fs';
import path from 'path';

const dir = process.argv[2];
if (!dir) { console.error('usage: node build-icons.mjs <path to @tabler/icons>'); process.exit(1); }
const nodes = JSON.parse(fs.readFileSync(path.join(dir, 'tabler-nodes-outline.json'), 'utf8'));
const version = JSON.parse(fs.readFileSync(path.join(dir, 'package.json'), 'utf8')).version;
const esc = v => String(v).replace(/&/g, '&amp;').replace(/"/g, '&quot;');
const out = {};
for (const [name, parts] of Object.entries(nodes)) {
  out[name] = parts.map(([tag, attrs]) => {
    const a = Object.entries(attrs).filter(([k]) => k !== 'key').map(([k, v]) => ` ${k}="${esc(v)}"`).join('');
    return `<${tag}${a}/>`;
  }).join('');
}
const dest = new URL('./tabler-outline.json', import.meta.url);
fs.writeFileSync(dest, JSON.stringify(out));
console.log(`${Object.keys(out).length} icons from @tabler/icons ${version} -> ${dest.pathname}`);
