# Data apps: Streamlit, Dash, Gradio

The framework draws most of the interface. Set the theme through the framework's own settings, then spend the effort on the charts and the layout of what the user sees first. Facts below were read from each framework's documentation on 11 November 2026; check the installed version.

## Streamlit

Theme options live in `.streamlit/config.toml` under `[theme]` (`[theme.light]` and `[theme.dark]` for per-scheme values, `[theme.sidebar]` for the sidebar). Map the tokens:

| Token | Option |
| --- | --- |
| `accent` | `primaryColor` |
| `surface` | `backgroundColor` |
| `zone` | `secondaryBackgroundColor` |
| `ink` | `textColor` |
| font | `font` (`"sans-serif"`, `"serif"`, `"monospace"`, or a font name with a CSS URL, comma-separated fallbacks allowed) |
| radius | `baseRadius`, `buttonRadius` |

```toml
[theme]
primaryColor = "#2F5BEA"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F6F9"
textColor = "#14171F"
```

`base` chooses the starting theme (`"light"`, `"dark"`, or a TOML file path or URL). Series colours for charts: `chartCategoricalColors`, `chartSequentialColors`, `chartDivergingColors`.

## Dash and Plotly

- Dash includes no styles of its own. Put CSS in an `assets/` folder next to the app: Dash loads every `.css` file there, in alphanumeric order (prefix names, `10_tokens.css`), after its component CSS. `external_stylesheets` loads before assets.
- One figure template for the whole app: `import plotly.io as pio; pio.templates.default = "plotly_white"` (it lasts for the session), or `fig.update_layout(template="plotly_white")` per figure. Built-in names include `plotly_white`, `plotly_dark`, `simple_white`, `presentation`, `none`.

## Gradio

Pass a theme to `launch`: `demo.launch(theme=gr.themes.Soft())`. Built-ins: `Base`, `Default`, `Origin`, `Citrus`, `Monochrome`, `Soft`, `Glass`, `Ocean`. `primary_hue`, `secondary_hue` and `neutral_hue` take Gradio's colour names or colour objects, not a hex value as far as the guide shows, so a brand colour is approximated by the nearest hue; say so in the report. Individual variables are overridden with `.set(...)` on the theme. Custom themes inherit from `gradio.themes.Base`.

## Design the screen, not just the theme

- **Mode is operate.** The user came to read a number or run a step. The first screen answers the main question; filters and controls sit where they are expected and keep their place.
- **Charts.** One accent for the series that carries the point, neutral grey for the rest; a title that states the finding, direct labels instead of a legend where there is room; axes that start where the data justify; units on the axis; no 3D, no dual axes, no gradient fills. Colour never carries a meaning alone.
- **Numbers.** Tabular figures, right aligned, units and period stated, the same precision down a column. Empty and loading states say what is missing and why.
- **Do not fight the framework.** Custom CSS that targets a framework's generated class names breaks on upgrade; prefer its theme options and layout primitives, and mark any CSS override with the framework version it was written for.
- **Check.** Run the app, point `ui-check.mjs` at the page, and look at it at 390 px and 1280 px. Framework-generated markup may fail rules you cannot fix (a control with no label): waive those with a reason and say so.
