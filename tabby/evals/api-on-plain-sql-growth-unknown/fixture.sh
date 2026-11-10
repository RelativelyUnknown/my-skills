#!/usr/bin/env bash
# Builds the fixture project for the `api-on-plain-sql-growth-unknown` case in the empty workspace.
# Run by `claude plugin eval --scaffold`. Files only, plus git history.
set -euo pipefail

mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "bookshop"
version = "0.4.0"
requires-python = ">=3.12"
dependencies = []

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
__FIXTURE_EOF__
mkdir -p "$(dirname Makefile)"
cat > Makefile <<'__FIXTURE_EOF__'
.PHONY: check
check:
	python -m pytest
__FIXTURE_EOF__
mkdir -p "$(dirname src/bookshop/__init__.py)"
cat > src/bookshop/__init__.py <<'__FIXTURE_EOF__'

__FIXTURE_EOF__
mkdir -p "$(dirname src/bookshop/db.py)"
cat > src/bookshop/db.py <<'__FIXTURE_EOF__'
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS authors (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER NOT NULL REFERENCES authors(id), price REAL NOT NULL, stock INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id), placed_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS order_items (order_id INTEGER NOT NULL REFERENCES orders(id), book_id INTEGER NOT NULL REFERENCES books(id), quantity INTEGER NOT NULL);
"""


def connect(path: str = "shop.db") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn
__FIXTURE_EOF__
mkdir -p "$(dirname src/bookshop/queries.py)"
cat > src/bookshop/queries.py <<'__FIXTURE_EOF__'
import sqlite3


def list_books(conn: sqlite3.Connection, *, author: str | None = None, limit: int = 50) -> list[sqlite3.Row]:
    sql = "SELECT b.id, b.title, a.name AS author, b.price, b.stock FROM books b JOIN authors a ON a.id = b.author_id"
    params: list[object] = []
    if author is not None:
        sql += " WHERE a.name = ?"
        params.append(author)
    sql += " ORDER BY b.title LIMIT ?"
    params.append(limit)
    return conn.execute(sql, params).fetchall()


def get_book(conn: sqlite3.Connection, book_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT b.id, b.title, a.name AS author, b.price, b.stock FROM books b JOIN authors a ON a.id = b.author_id WHERE b.id = ?",
        (book_id,),
    ).fetchone()


def orders_for_customer(conn: sqlite3.Connection, customer_id: int) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT o.id, o.placed_at, SUM(i.quantity * b.price) AS total FROM orders o"
        " JOIN order_items i ON i.order_id = o.id JOIN books b ON b.id = i.book_id"
        " WHERE o.customer_id = ? GROUP BY o.id ORDER BY o.placed_at DESC",
        (customer_id,),
    ).fetchall()


def place_order(conn: sqlite3.Connection, customer_id: int, items: list[tuple[int, int]]) -> int:
    cur = conn.execute("INSERT INTO orders (customer_id, placed_at) VALUES (?, datetime('now'))", (customer_id,))
    order_id = int(cur.lastrowid)
    conn.executemany("INSERT INTO order_items (order_id, book_id, quantity) VALUES (?, ?, ?)", [(order_id, b, q) for b, q in items])
    conn.executemany("UPDATE books SET stock = stock - ? WHERE id = ?", [(q, b) for b, q in items])
    conn.commit()
    return order_id
__FIXTURE_EOF__
mkdir -p "$(dirname src/bookshop/web.py)"
cat > src/bookshop/web.py <<'__FIXTURE_EOF__'
"""Server-rendered pages for the shop staff: a catalogue and a customer's orders."""
from html import escape
from wsgiref.simple_server import make_server

from bookshop import db, queries


def app(environ, start_response):
    conn = db.connect()
    path = environ["PATH_INFO"]
    if path == "/":
        rows = queries.list_books(conn)
        body = "<h1>Catalogue</h1><ul>" + "".join(f"<li>{escape(r['title'])} by {escape(r['author'])}: {r['price']:.2f}</li>" for r in rows) + "</ul>"
    else:
        body = "<h1>Not found</h1>"
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [body.encode()]


if __name__ == "__main__":
    make_server("", 8000, app).serve_forever()
__FIXTURE_EOF__
mkdir -p "$(dirname tests/test_queries.py)"
cat > tests/test_queries.py <<'__FIXTURE_EOF__'
from bookshop import db, queries


def test_list_books_by_author():
    conn = db.connect(":memory:")
    conn.execute("INSERT INTO authors VALUES (1, 'Le Guin')")
    conn.execute("INSERT INTO books VALUES (1, 'The Dispossessed', 1, 12.5, 3)")
    conn.commit()
    assert [r["title"] for r in queries.list_books(conn, author="Le Guin")] == ["The Dispossessed"]
__FIXTURE_EOF__
mkdir -p "$(dirname README.md)"
cat > README.md <<'__FIXTURE_EOF__'
# bookshop

Staff pages for an independent bookshop: the catalogue and customer orders.
Run `python -m bookshop.web`. Tests: `make check`.
__FIXTURE_EOF__

git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
