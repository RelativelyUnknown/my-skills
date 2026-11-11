# Entity-relationship

**The reader asks:** What does the data look like, and how do the tables relate?

A table node per entity: its name, then one mono row per column that matters (key, foreign key, a column the reader needs), with the type at the right. A connector per relationship, labelled with its cardinality (`1 : N`).

- Builder: `rows: [["id","uuid"],["user_id","uuid"]]` makes a table node. Example: `assets/diagram/examples/shop-tables.json`.
- Show columns that carry meaning (keys, status, the columns a query filters on), not every column; say so in the subtitle when you leave some out.
- Connectors run from the foreign key's table to the referenced one in the direction a reader says it (`users` to `orders` for "one user places many orders").
- Budget: 6 tables. A schema of 20 tables is a set of pictures, one per aggregate.
- Physical detail (indexes, constraints) belongs in the migration, not in the picture.

Visual rules: [../style.md](../style.md). Connectors: [../connectors.md](../connectors.md). Check before reporting: `python3 assets/diagram/check.py out.svg`.
