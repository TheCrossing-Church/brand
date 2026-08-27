# The Crossing — Brand

The single source of truth for The Crossing's brand: logos, colors, typography, and voice. Built for our Rock team, scripts, and AI tools first — and rendered as a human-friendly site at **[brand.thecrossing.church](https://brand.thecrossing.church)**.

> **Status: v0.2 — in use.** Colors, typography, and logo colorway names come from the official **Brand Guides 2023**, and the real logo files are in place. Still to add before this is authoritative for *print*: CMYK/Pantone values. Bariol font files are intentionally absent — see [Fonts](#fonts--important).

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
CNAME                   Custom domain for Pages (brand.thecrossing.church)
CODEOWNERS              Review routing — everything to @TheCrossing-Church/rock-team
ROLLOUT.md              Setup runbook: what's done, what's still open
PRACTICES.md            How we work today, and what we'd like to grow into
.github/workflows/      CI — validates brand-kit.json and its asset references
logos/                  crossing/ · kids-crossing/ · youth-crossing/
colors/                 Color tokens (CSS/SCSS)
fonts/                  (no font files — Bariol is licensed; see guidelines)
campuses/               CFD · FEN · GRT · MID (as needed)
samples/                logo-usage/ — do / don't example tiles (SVG)
schema/                 JSON Schema for brand-kit.json
```

## Fonts — important

**Bariol** is our official print/wordmark font and is **commercially licensed**. Its files are **not** committed to this public repo. Staff install Bariol from the internal source (private repo / SharePoint). See [`brand-guidelines.md`](brand-guidelines.md#typography).

## Contributing

This repo is owned by the **Rock team** (`@TheCrossing-Church/rock-team`), which has admin access. `CODEOWNERS` assigns every path to that team. The IT team has read-only access on purpose, which is why it isn't listed as an owner.

The process today is deliberately simple: **commit straight to `main`.** There's no branch protection and no required review. Brand changes are small and infrequent, so a bad one is easy to spot in the diff and undo:

```bash
git revert <commit>     # undo a commit, keeping the history honest
git log --stat          # see what changed, and when
```

Pull requests are welcome if you want a second set of eyes — nothing requires one. Pushing to `main` republishes the site automatically (GitHub Pages), so check the site after a change.

See the `governance` section of [`brand-kit.json`](brand-kit.json) for the same rules as data, and [`PRACTICES.md`](PRACTICES.md) for the tighter process we'd like to grow into once the team is comfortable.

## Related

- **Private assets** (source files, fonts, internal templates): `TheCrossing-Church/brand-internal` — private; same access as here (Rock team admin, IT read)
- **Rock BrandCentral**: should point here as the canonical source.
- **Office templates** (letterhead, decks, signatures): SharePoint.
