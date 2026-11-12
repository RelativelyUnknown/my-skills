import pathlib, re
FENCE = chr(96) * 3
root = pathlib.Path('.'); bad = 0
mds = [p for p in root.rglob('*.md') if '.git/' not in str(p) and 'node_modules' not in str(p) and '/vendor/' not in str(p)]
for p in mds:
    t = re.sub(FENCE + '.*?' + FENCE, '', p.read_text(), flags=re.S)
    for m in re.finditer(r'\]\(([^)#\s]+)(#[^)]*)?\)', t):
        u = m.group(1)
        if not re.match(r'[a-z]+:', u) and not (p.parent / u).exists(): print('BROKEN', p, u); bad += 1
tab = [p for p in mds if str(p).startswith('tabby') and not str(p).startswith('evals')]
texts = {p: p.read_text() for p in tab}
for p in tab:
    if p.name not in ('README.md', 'SKILL.md', 'index.md', 'SOURCE.md') and not any(p.name in t for q, t in texts.items() if q != p): print('UNREFERENCED', p)
print('broken', bad)
