#!/usr/bin/env bash
# Builds the fixture project for the `review-a-page-before-shipping` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# statuspage

Static status page.
__FIXTURE_EOF__
mkdir -p "$(dirname site/index.html)"
cat > site/index.html <<'__FIXTURE_EOF__'
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Status</title>
<style>
body{font:16px/1.5 system-ui;color:#222;background:#fff;margin:0;padding:16px}
.low{color:#c4c8d0}
.card{box-shadow:6px 6px 0 #000;padding:12px;margin:12px 0}
.tiny{font-size:10px}
input:focus{outline:none}
</style></head><body>
<h1>Service status</h1>
<h3>Incidents</h3>
<p class="low">No incidents in the last 30 days.</p>
<div class="card">API: operational</div>
<img src="/uptime.png">
<input name="email" placeholder="you@example.com"><button>Subscribe</button>
<p class="tiny">Updated every five minutes.</p>
</body></html>
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
