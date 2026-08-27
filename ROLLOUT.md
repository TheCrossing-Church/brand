# Rollout — The Crossing Brand

The runbook for standing this repo up as the canonical brand home. Owner: the **Rock team** (`@TheCrossing-Church/rock-team`).

**Where things stand (Aug 2026):** the repos exist, the real assets are in, the site is live at
[brand.thecrossing.church](https://brand.thecrossing.church), and CI is green. What's left is print color
data and wiring the rest of the ecosystem to point here.

## Done

### Repos (org: TheCrossing-Church)
- [x] **`brand`** — *public*. Pushed; `main` is the default branch.
- [x] **`brand-internal`** — *private*. Holds the Bariol `.otf` files + license, the Brand Guides 2023 PDF, and the letterhead template. Its README points back here as the source of truth.
- [x] GitHub teams and access: `rock-team` = **admin** on both repos, `it` = **read**. `CODEOWNERS` assigns `*` to `rock-team`; the IT team is intentionally not an owner, since review routing requires write access.
- [x] Bariol licensing handled the right way — font files stay out of this public repo. `.gitignore` blocks `*.otf/.ttf/.woff/.woff2/.eot` **repo-wide**, not just under `fonts/`, so a font dropped anywhere is still blocked.

### Assets
- [x] Real logo set committed for all three marks — `logos/crossing`, `logos/kids-crossing`, `logos/youth-crossing` — using the names `brand-kit.json` references. CI confirms **0 missing referenced assets**.
- [x] `PLACEHOLDERS.md` files removed; `index.html` renders the real files (the drawn ring is only a load-failure fallback).
- [x] Colors, typography, and colorway names taken from **Brand Guides 2023** (the PDF itself lives in `brand-internal`, not published here).

### Site (GitHub Pages)
- [x] Source: `main` / `/ (root)`.
- [x] `CNAME` = `brand.thecrossing.church`; DNS in place.
- [x] **Enforce HTTPS** on, certificate approved.
- [x] Live and building — verified at `https://brand.thecrossing.church`.

## Still open

- [ ] **Add CMYK/Pantone values** to `brand-kit.json` and `colors/` so the palette is authoritative for print, not just screen. This is the last thing keeping `status` short of fully authoritative.
- [ ] **Rock BrandCentral →** replace the hand-maintained download wall with an HTML/Lava block that links to (or renders live from) `brand.thecrossing.church` / `brand-kit.json`. This is what kills the staleness — one place to update.
- [ ] **Reconcile creative's "fuller" version** into this repo so there's a single source rather than two competing decks.
- [ ] **Add editable design masters** (`.ai` / `.psd` / layered `.svg`) to `brand-internal/source/` — the folder exists but is empty.
- [ ] **Tell the team** where this lives and how to change it: commit to `main`, or open an issue in the repo.
- [ ] **Set a review rhythm.** Quarterly is the aim — put it on a calendar with an owner's name on it.
- [ ] **Flip the CI asset check from warn to fail** — `.github/workflows/validate.yml` still prints a `::warning::` for missing assets because it was written for the placeholder phase. Nothing is missing now, so changing it to `sys.exit(1)` would be a no-op today and would catch a broken reference tomorrow. Deliberately left as a decision, not a default.

## For AI users

> Use the brand at `raw.githubusercontent.com/TheCrossing-Church/brand/main/brand-kit.json` — follow its `rules`, `color_system`, `logos`, and `voice`.

Always review AI output before it's published or sent to members, per our org's AI-use guidelines.

## The public/private boundary, at a glance

| Public (`brand`) | Private (`brand-internal` / SharePoint) |
|---|---|
| Logos (SVG/PNG), colors, `brand-kit.json`, guidelines, rendered site | Editable source files, **Bariol font files**, Brand Guides 2023 PDF, Office templates, unreleased campaign art |
