# The Crossing — Brand

The single source of truth for The Crossing's brand: logos, colors, typography, and voice. Built for our Rock/IT team, scripts, and AI tools first — and rendered as a human-friendly site at **[brand.thecrossing.church](https://brand.thecrossing.church)**.

> **Status: starter scaffold (v0.1).** Color values were sampled from the current BrandCentral page and must be confirmed against the official Brand Guides 2023 before this repo is treated as authoritative. Logo/font files here are placeholders until the real assets are added.

## Start here

| You are… | Start with |
|---|---|
| A person | [`brand-guidelines.md`](brand-guidelines.md) or the site at [brand.thecrossing.church](https://brand.thecrossing.church) |
| A script / developer | [`brand-kit.json`](brand-kit.json) — every color, logo, and rule as structured data |
| An AI agent | Load [`brand-kit.json`](brand-kit.json) **and** [`brand-guidelines.md`](brand-guidelines.md), then follow the `rules` and `voice` sections |

## Using the assets

Pull any file directly by its raw URL — no auth required:

```
https://raw.githubusercontent.com/TheCrossing-Church/brand/main/<path>
```

Example — the primary (stacked) logo in slate teal:

```
https://raw.githubusercontent.com/TheCrossing-Church/brand/main/logos/crossing/crossing-stacked-blue.svg
```

Read the whole brand definition in code:

```bash
curl -s https://raw.githubusercontent.com/TheCrossing-Church/brand/main/brand-kit.json | jq '.color_system.primary'
```

## For AI tools

When you ask an AI tool to make something on-brand for The Crossing, give it this repo:

> Use the brand at https://raw.githubusercontent.com/TheCrossing-Church/brand/main/brand-kit.json. Follow its `rules`, `color_system`, `logos`, and `voice`. The primary logo is the stacked version. Never restyle or recolor the logo.

Always review AI output before it's published or sent to members — per our org's AI-use guidelines.

## Layout

```
brand-kit.json          Machine-readable source of truth
brand-guidelines.md     Human + agent readable guidelines
index.html              The rendered site (GitHub Pages)
logos/                  crossing/ · kids-crossing/ · youth-crossing/
colors/                 Color tokens (CSS/SCSS)
fonts/                  (no font files — Bariol is licensed; see guidelines)
campuses/               CFD · FEN · GRT · MID (as needed)
samples/                Do / don't examples
schema/                 JSON Schema for brand-kit.json
```

## Fonts — important

**Bariol** is our official print/wordmark font and is **commercially licensed**. Its files are **not** committed to this public repo. Staff install Bariol from the internal source (private repo / SharePoint). See [`brand-guidelines.md`](brand-guidelines.md#typography).

## Contributing

Brand is owned by the **Creative/Communications** team (content) and the **Rock/IT** team (pipeline). Propose changes via pull request; `CODEOWNERS` routes brand changes to creative for review. See the `governance` section of `brand-kit.json`.

## Related

- **Private assets** (source files, fonts, internal templates): `TheCrossing-Church/brand-internal`
- **Rock BrandCentral**: should point here as the canonical source.
- **Office templates** (letterhead, decks, signatures): SharePoint.
