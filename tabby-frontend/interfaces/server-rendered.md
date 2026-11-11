# Server-rendered web apps

Jinja or Django templates, FastAPI or Flask with HTMX, admin and internal tools. The page is made on the server, so the design lives in one place: a base template and one stylesheet.

- **Use what the project uses.** If it has Tailwind, Bootstrap, Pico or its own CSS, set the tokens there (its theme config or custom properties) and build with its components. Do not add a second CSS system or a JavaScript framework for a look.
- **Tokens once.** The palette and type from [tokens-and-type.md](tokens-and-type.md) go in one `:root` block in the base stylesheet (or the framework's theme file). Templates use the variables; no colour literals in markup.
- **One base template** with the document skeleton: `lang`, a descriptive `<title>`, viewport, a skip link, a `<main>`, one `<h1>` per page. Pages extend it and fill blocks.
- **Mode.** Admin and internal tools are *operate*: dense tables, consistent placement, keyboard first. A public landing page is *persuade*. Do not mix them in one template.
- **Forms.** Label above each field, errors beside the field and also in a summary at the top, the user's input kept on a failed post, a button that names its action. A non-JS form must work first; enhance it.
- **Partial updates (HTMX or similar).** Keep focus where the user was, announce a swapped region that changes meaning (`aria-live="polite"`), keep the URL honest, and show a loading state that keeps the control's size. The page must still be usable if the request fails: show the error where the content would have been.
- **Static assets.** One stylesheet, system or self-hosted font, images with `width`, `height` and `alt`. No unused CSS framework bundle added just for a few components.
- **Check.** Serve the app (the project's own dev command; ask before running anything that needs services) and run `node assets/interfaces/ui-check.mjs http://localhost:PORT/page` for each distinct template, then look at it at 390 px and 1280 px with the keyboard.
