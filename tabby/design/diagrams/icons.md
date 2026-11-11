# Icons

A node's icon says what kind of thing it is at a glance, so the reader finds the database before reading its name. The set is Tabler Icons outline (MIT, 5,233 icons, one consistent 24 px stroke), vendored as `assets/icons/tabler-outline.json`; the licence is next to it.

## Choosing

- Pick the icon for the **kind** of part, not the product: `database` for postgres, `server` for an http server, `stack-2` for a queue, `cpu` for a worker, `device-desktop` for a browser. A brand logo is not used: it would need the vendor's mark and a network fetch, and it breaks the single stroke style.
- Search by word: `node assets/diagram/make.mjs --icons <word>` lists names containing it (`--icons cloud`). A name that does not exist stops the build and prints the nearest five.
- Reuse one icon for one kind across a whole set of pictures. Two kinds never share an icon in the same picture.
- Abstract nodes (a cron job, a cache, a webhook) get a pictogram too (`clock`, `bolt`, `webhook`), never text in the tile and never an emoji.
- The tile is part of the node style: ordinary nodes get a `tile`, the focal node an `accent` tile with the icon in `on-accent`. Do not recolour an icon, add a second one, or scale it off 24 px × 0.667.

## Refreshing the set

`assets/icons/build-icons.mjs` regenerates the JSON from the npm package `@tabler/icons` (`node build-icons.mjs <path to the package>`). Installing the package is a new dependency: ask first, and do it in a scratch folder, not in the project.
