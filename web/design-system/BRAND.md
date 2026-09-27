Sovereign AI runtime. Every decision sealed.

PyraClaw is DD7 International's evidence-first runtime: a pyramid of agents whose every output is hashed four times (SHA-256 · SHA-512 · SHA3-256 · SHA3-512, the Quadruple-Dipped Protocol) and anchored. The interface says the same thing the runtime does — **pyramid geometry, precious-metal materials, a near-black stage, light as the protagonist.** Professional futurism: fine-art lighting and jewelry-grade surfaces, never cyberpunk, never neon-on-teal.

## Two registers

The codebase ships two skins of one brand. Pick one per surface and set it as the root class; the semantic tokens (`ui-*`) switch with the theme.

| | Sovereign — `.pc`, theme `sovereign` | Mission Control — `.mc`, theme `minted` |
|---|---|---|
| Where | Investor and iAiA showcases, decks, the Evidence OS | Product pages: Minted Green, Command, Evidence |
| Stage | `ink` #040610 | `mc-bg` #0a0f1a |
| Accent | `gold-3` Auric, `steel-3` for the data plane | `mc-green` Minted, `mc-cyan`, `mc-purple` per page |
| Type | Cinzel Decorative · Cinzel · Cormorant Garamond · Rajdhani · JetBrains Mono | Inter · JetBrains Mono |
| Shape | Square. `radius-none` on every panel, chip and control | Rounded: `radius-sm` 8 · `radius-md` 12 · `radius-lg` 16 · `radius-pill` |
| Glint | 1px gradient line along a panel's top edge | 1px `mc-border` |

Set Sovereign on anything an investor, regulator or partner sees. Mission Control is the operator-facing product register: page modifiers `.mc.minted`, `.mc.command`, `.mc.evidence` carry each page's accent (green, purple/amber, cyan/purple) exactly as shipped.

## Content fundamentals

- **Declarative, evidence-first, zero hedging on what is built.** Thesis sentence, then proof: *"Every AI Decision. Proven."* — then the four hashes. Never *revolutionary*, *disruptive*, *magic*. The repo rule is the brand rule: *No overclaiming. No grand claims. Results-driven only.*
- **Words we own:** sealed, provenance, verdict, lineage, tamper-evident, reduced to practice, gate-before-scale, ascend to descend.
- **Labels are uppercase and tracked**, separated by middle dots: `COMPLIANCE FIRST · QDP ACTIVE · PYRACLAW ONLINE`. Sentences are sentence case. Wordmarks: `PYRACLAW`, `iAiA`, `DD7 International GmbH`.
- **Sections are numbered** `§ 01`, `§ 02` in `label-section-num` beside a `heading-section` title and a fading `.sec-line`.
- **Hashes are a brand asset — show them.** Digests, DOIs, tx hashes, patent numbers are set in the mono families, never hidden behind "verified" alone. Truncate with an ellipsis after 32 characters (`dcd8bfb5e2b35a3c4af85cdd192d114e…`).
- **Every figure carries its status.** `PCT/EP2025/080977` and `US 19/541,276` are filed applications — cite as filed. "77 invention disclosures" is a portfolio count, not 77 patents. Coherence / consciousness metrics (Φ, I_G) are **simulated** — label them so wherever shown. Market-size figures without a named analyst source do not go on an external surface.
- **Status words travel with their colour.** `● FULLY COMPLIANT`, `PASS`, `VERIFIED`, `LIVE`, `FAIL` — the word is the signal; the colour (`ui-success`, `ui-warning`, `ui-danger`) confirms it.
- Glyph accents come from Unicode, one per panel title in `.pi` at 60% opacity: ◈ (evidence/gold), ⬡ (mechanism), ⟁ (governance), ⊕ (operations), ◭ (pyramid), ● (live), § (section).
- English, no emoji in the Sovereign register. The Mission Control Evidence page uses emoji file icons (📥 📤 🔐) in `.capsule-file .icon` — shipped, kept, and the one place they appear.

## Colour

- Stage first: `ui-stage` on the root, then `ui-panel` at 97% glass so the atmosphere reads through (`.pc .atmosphere` — three radial washes of steel, gold and warm grey, never above 4% alpha).
- **Dominance 65 / 30 / 5:** stage, the gold family, then one Champagne moment (`gold-5`, `chrome-4`) per surface. The colours people know the brand by take the big fields even where the UI spends them sparingly.
- Text: body in `ui-text` (`chrome-3`); panel paragraphs in `chrome-2`; labels and table heads in `ui-text-muted` (`platinum-2`); footers and hash tails in `ui-text-dim` (`platinum-1`, decorative only — 3.9:1).
- Accent discipline: `gold-3` is the accent for titles, active states and key figures; `steel-3` for the console, API and code surfaces; `platinum-3` for the third figure in a row of metals. A colour that only ever means a state stays small: `signal-pass` for dots and PASS cells, `signal-warn` for bear scenarios, `signal-fail` for FAIL.
- Chain colours (`chain-near`, `chain-poly`, `chain-eth`, `chain-bnb`) appear only on chain cards and their dots.
- Hairlines, not shadows: `hairline` on panels and rows, `hairline-2` on chips and hovered cards, `hairline-gold` / `hairline-steel` when a panel belongs to that plane (`.panel.pg`, `.panel.ps`). Washes (`tint-gold-1`, `tint-steel-1`) sit behind eyebrows, active pills and console headers.
- Contrast on `ink`: `chrome-3` 15.6:1, `chrome-2` 6.2:1, `platinum-2` 7.7:1, `gold-3` 9.2:1, `steel-3` 8.5:1, `signal-pass` 5.5:1, `signal-warn` 5.6:1. Two source pairs miss AA and are kept exact: `signal-fail` 3.4:1 (use with the word FAIL at 19px bold or larger) and `platinum-1` 3.9:1 (decorative). In Mission Control, `mc-muted` is 4.0:1 on `mc-bg` and `mc-purple` 3.4:1 — headings 24px+ only, as shipped.
- Focus: `ui-focus` (`steel-3` / `mc-cyan`), 2px solid, 2px offset, on every interactive element in both registers.

## Typography

Six families, all hosted on Google Fonts (`Cinzel:wght@400;600;700;900`, `Cinzel+Decorative:wght@700;900`, `Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400`, `JetBrains+Mono:wght@300;400;500;600`, `Rajdhani:wght@300;400;500;600;700`, `Inter:wght@300;400;500;600;700`). Root size 16px; the pages use rem, so every style is recorded at its pixel value.

- **Display — Cinzel Decorative 900** for the one hero title per page (`display-hero`, in `metal-chrome`) and feature headlines (`display-title`). Letter-spacing 0.04–0.05em, leading 1.0–1.1.
- **Heading — Cinzel** for section titles (`heading-section`, in `metal-gold`) and every panel title (`heading-panel`: 11.2px, uppercase, 0.25em — the quietest heading in the system).
- **Editorial — Cormorant Garamond** for the human voice: the hero tagline, italic pull quotes with a 2px gold-alpha left rule (`editorial-quote`), italic uppercase sub-lines (`editorial-sub`).
- **Body — Rajdhani** for copy in panels and cards (`body-copy` 12.48/1.7, `body-card` 12.8/1.7) and the uppercase labels under figures (`label-sphere`, `label-stat`, `label-tile`).
- **Mono — JetBrains Mono** for every number, hash, label chip and console line. Figures at 600 (`num-hero` 48 → `num-bench` 13.6); labels at 400 with wide tracking (`label-eyebrow` 0.26em is the widest); text at `mono-console`, `mono-code`, `mono-table`.
- **Sans — Inter** only in Mission Control (`mc-hero` 48/700, `mc-h2` 28.8/700, `mc-body` 16/1.8).
- Metallic gradients on hero elements only (`metal-chrome`, `metal-gold`, `metal-platinum`, `metal-steel` via `.t-chrome .t-gold .t-plat .t-steel`), never on body text. A subscript inside gradient text resets `-webkit-text-fill-color` to a solid token.
- The smallest live text is `label-badge` 7.36px, always uppercase inside a hairline box; do not go smaller.

## Spacing and layout

- Sovereign pages sit in `.wrap` (`container-max` 1480px, `space-7` gutters) under a sticky 52px `nav`. Mission Control reads in a `content-max` 1000px column with `space-10` section padding.
- Panels: `space-5` × `space-6` (`.pb`), grids `g2`/`g3`/`g4`/`g5` with `space-4`/17.6px/`space-3`/`space-3` gaps and `space-4` below each row. `.sec-hdr` takes `space-9` above.
- Dense data breathes at `space-2`; chips and pills at `space-1`; the agent matrix at `space-0`.
- Section rhythm: eyebrow → title → sub → tagline → pills → strip → spheres → numbered sections. One hero element per screen; generous negative space between.

## Borders, radii, depth

- The Sovereign register is square: `radius-none` everywhere except discs (`radius-disc`: spheres 82px, dots 4–10px, play button 60px).
- Depth is light, not shadow. A panel's top edge carries a 1px glint gradient (`transparent → rgba(200,215,240,0.09) → transparent`; gold or steel on `.pg`/`.ps`; `gold-3` on stat tiles). Left rules mark emphasis: `accent-rule` 4px `gold-3` on the QDP strip, `signal-pass` on the savings panel, 2px on steps, 3px chain colour on chain cards.
- The single box-shadow is `shadow-sphere` on the photoreal spheres; dots glow with `glow-pass` / `glow-gold` / `glow-steel` / `glow-chain`.
- Mission Control uses rounded cards (`radius-md`), pills (`radius-pill`) and one pulse ring (`pulse-mc`) on the Minted seal.

## Motion

Short and physical: hovers lift cards `translateY(-4px)` (`-3px` on feature/bench cards) over 0.25–0.28s `cubic-bezier(.2,.8,.3,1)`; borders and colours transition in 0.18–0.2s; agent nodes scale 1.06. Ambient: `bl` blink 1.1–1.4s on live dots, `shim` 4s sweep across the eyebrow, `fadeUp` 0.7s staggered 0.15s on entry, `mc-pulse` 2s on the seal. Bars fill over 1.2–1.5s. No parallax, no glitch.

## States

- Hover: border to `hairline-2`, text to `chrome-3`; lift as above.
- Active / selected: `gold-3` text and border with `tint-gold-2` (model pills, scenario tabs); `steel-3` with `tint-steel-2` on API modes.
- Disabled: 35% opacity, `cursor:not-allowed`.
- Live: a 5px `signal-pass` dot blinking beside the word, `● LIVE` / `PRODUCTION · v3.1`.

## Iconography

No icon font or SVG set ships in the codebase. Use the Unicode glyph set above for panel titles and section markers, `radius-disc` dots for status, and text for everything else. If a real icon set is added, it must be single-ink line icons in `platinum-2` at 1px, never filled or coloured.

## Imagery

Key art follows one rule: **one protagonist light source per scene** — darkness, then a precious-metal eruption at one edge (the Dimensionality Wall in `assets/Imagery/` is the reference). Metals: gold + chrome for Core; brushed steel + arc-blue for the Cybersecurity Division. Photographs sit in `.img-panel` at 72% opacity under a `ink`-to-transparent overlay with a `heading-caption` title and a mono tag. No text baked into generated art; typeset over it so copy stays governable.

## Logos

The Core sigil (gold/silver pyramid, wordmark below) is not in the codebase: set `PYRACLAW` in `display-brand` (Cinzel Decorative 900, 0.22em) until the mark is added. The Cybersecurity Division mark in `assets/Logos/` is for security products, audits and advisories only. Clear space: one triangle-height on all sides; on `ink` or white only; never recoloured, skewed or placed on a mid-tone.

## Data visualisation

Charts are canvas-drawn in the source (pyramid, I_G line, profit curve). Draw on `ink` with `hairline` grid rules; series in `gold-3`, `steel-3`, `platinum-3` in that order; fills as the progress gradients (`gold-2 → gold-3`, `steel-1 → steel-3`, `platinum-1 → platinum-3`); axis labels in `label-meta`. Bars are 3–6px tall (`progress-track`), never rounded.

## Not synced

Canvas charts (`#pyr-cv`, `#ig-cv`, `#scale-cv`) and the JavaScript behaviours (scenario switching, console send, agent-matrix generation, count-ups) are not componentised — previews are static renditions of the shipped markup. `clamp()` sizes are recorded at their maximum. Fonts are hosted (no files). The Core sigil is absent from the repository; `.github/agents/pyraclaw_pitch_deck.pptx` holds only a generic illustration and was skipped. Route taken: read-only extraction — no build was run.
