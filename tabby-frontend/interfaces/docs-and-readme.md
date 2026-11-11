# Docs sites and README visuals

Documentation is *read* mode: a 60 to 70 character column, navigation that shows where you are, search, code that copies. The theme is set through the docs tool, and the pictures in it come from the `tabby-diagrams` skill (`../tabby-diagrams/diagrams/choosing.md`). Facts below were read from the tools' documentation on 11 November 2026.

## MkDocs Material

```yaml
theme:
  palette:
    - scheme: default          # light
      toggle: { icon: material/brightness-7, name: Switch to dark mode }
    - scheme: slate            # dark
      toggle: { icon: material/brightness-4, name: Switch to light mode }
extra_css:
  - stylesheets/extra.css      # docs/stylesheets/extra.css
```

`primary` and `accent` take a colour name; `custom` hands the colour to your CSS, where brand colours go in a `:root > *` block as `--md-primary-fg-color`. A `media: "(prefers-color-scheme: light)"` key on each palette entry follows the system setting.

## Sphinx

```python
html_theme = "alabaster"                  # or the theme the project already uses
html_static_path = ["_static"]
html_css_files = ["custom.css"]           # _static/custom.css
```

Theme options go in `html_theme_options`. Keep the project's theme; add only a small stylesheet for tokens.

## README and repository pictures

- **Social preview:** PNG, JPG or GIF under 1 MB; at least 640 by 320 px, 1280 by 640 px for the best display.
- **A diagram in a README:** the SVG from `../tabby-diagrams/assets/diagram/make.mjs` carries both themes through `prefers-color-scheme`. How a given host renders an SVG used as an image varies: look at it on the real page. GitHub renders `<picture>`; if one SVG does not follow the viewer's theme there, give two files (a light and a dark render from `../tabby-diagrams/assets/diagram/render.mjs`) with a `<picture>` whose dark `<source>` uses `media="(prefers-color-scheme: dark)"` (this pairing was not confirmed in GitHub's docs in this session: check the rendered README).
- **An animation in a README:** a GIF (`../tabby-diagrams/assets/animation/render-video.mjs`), since a README cannot run the HTML; link to the HTML for the interactive version.
- **Screenshots:** one real screenshot at 2x of the thing described, cropped to it, with `alt` text that says what it shows. No mock-ups of screens that do not exist.
- **Alt text** on every image; a decorative one gets `alt=""`.

## Check

For a built docs site, serve it locally and run `node assets/interfaces/ui-check.mjs http://localhost:8000/` on a page of each kind (home, a long reference page, a page with code and a table).
