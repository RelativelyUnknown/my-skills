#!/usr/bin/env bash
# Builds the fixture project for the `ui-orders-page-accessibility` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# shop admin

Flask admin for orders. Run `flask run`.
__FIXTURE_EOF__
mkdir -p "$(dirname app.py)"
cat > app.py <<'__FIXTURE_EOF__'
from flask import Flask, render_template

app = Flask(__name__)


@app.get("/orders")
def orders():
    return render_template("orders.html", orders=[{"id": 1042, "status": "paid"}])
__FIXTURE_EOF__
mkdir -p "$(dirname templates/orders.html)"
cat > templates/orders.html <<'__FIXTURE_EOF__'
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Orders</title>
  <link rel="stylesheet" href="/static/app.css">
</head>
<body>
  <h1 class="hero">Orders</h1>
  <h4>Recent orders</h4>
  <img src="/static/chart.png" class="chart">
  <table>
    <tr><th>ID</th><th>Status</th></tr>
    {% for o in orders %}<tr><td>{{ o.id }}</td><td class="muted">{{ o.status }}</td></tr>{% endfor %}
  </table>
  <h4>Find an order</h4>
  <form action="/orders" method="get"><input name="q" placeholder="Order number"><button>Go</button></form>
  <p class="fine">Orders are kept for seven years.</p>
</body>
</html>
__FIXTURE_EOF__
mkdir -p "$(dirname static/app.css)"
cat > static/app.css <<'__FIXTURE_EOF__'
body { font-family: system-ui, sans-serif; color: #222; background: #fff; }
.hero { background: linear-gradient(90deg, #6a5cff, #ff5c9d); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; font-size: 32px; }
.muted { color: #bbbbbb; }
.fine { font-size: 10px; color: #aaaaaa; }
a:focus, button:focus, input:focus { outline: none; }
button { font-size: 12px; padding: 2px 4px; }
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
