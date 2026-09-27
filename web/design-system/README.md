# PyraClaw Design System

Extracted from `web/mission-control/*.html` — the source of truth for the runtime's two visual registers:

| Register | Root class | Pages |
|---|---|---|
| Sovereign | `.pc` (theme `sovereign`) | `iaia-showcase.html`, `investor-showcase.html` |
| Mission Control | `.mc` + `.minted` / `.command` / `.evidence` | `minted-green.html`, `command.html`, `evidence.html` |

Values are verbatim from the pages. CSS custom properties are renamed to readable tokens (`--gd3` → `--gold-3`, `--bd` → `--hairline`); every token's `usage` note in `tokens.json` records the source name.

## Files

| File | What |
|---|---|
| `tokens.json` | The token inventory: 76 colours in two themes (`sovereign` first, `minted`), 6 font families, 67 text styles, spacing, radius, shadow, layout and metal-gradient families, with a usage note on each |
| `tokens.css` | Compiled custom properties (`:root,[data-theme="sovereign"]`, `[data-theme="minted"]` overrides, `--space-*`, `--radius-*`, `--font-*`) and one class per text style |
| `components/bundle.css` | Every component class from the five pages, scoped under `.pc` / `.mc` — static markup, no JavaScript |
| `BRAND.md` | The brand book: registers, content fundamentals, colour, type, spacing, depth, motion, states, iconography, imagery, logos, data-viz rules |

The living system — token editor, component previews, cover and asset store — is the Design System artifact published from this extraction. Load `tokens.css` then `components/bundle.css`, put `class="pc"` (or `class="mc minted"`) on `<body>`, and use the class names the pages already use.

## Rules

- Sovereign surfaces are square (`--radius-none`); Mission Control is rounded (`--radius-sm/md/lg/pill`).
- One accent per surface (`--ui-accent`), metal gradients on hero elements only, hashes shown in mono.
- Status words travel with their colour; simulated figures are labelled simulated. No overclaiming.
