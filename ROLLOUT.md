# Rollout & Governance — The Crossing Brand

A short runbook for taking this scaffold from draft to the live, canonical brand home. Owners: **Rock/IT** (pipeline) + **Creative/Communications** (content).

## 0. Before anything ships publicly
- [ ] **Confirm Bariol licensing.** It's commercial and install-only. Keep font files out of the public `brand` repo (`.gitignore` already blocks the extensions). Real files live in the private repo / SharePoint.
- [ ] **Confirm color values.** The hex values in `brand-kit.json`, `colors/`, and the site were sampled from a screenshot. Verify each against **Brand Guides 2023** and add CMYK/Pantone for print.

## 1. Create the repos (org: TheCrossing-Church)
- [ ] **`brand`** — *public*. Push this scaffold to it.
- [ ] **`brand-internal`** — *private*. For editable source files (`.ai/.psd/.svg`), the Bariol font files, and internal-only templates. Add a README pointing back to `brand` as the source of truth.
- [ ] Create GitHub **teams** `creative` and `it`, then update `CODEOWNERS` (placeholder handles are in there now).

```bash
# from this scaffold folder, once the empty public repo exists:
git init -b main
git add .
git commit -m "Brand scaffold v0.1"
git remote add origin git@github.com:TheCrossing-Church/brand.git
git push -u origin main
```

## 2. Populate real assets
- [ ] Export the logo set from Rock BrandCentral (or the creative master files) and drop them into `logos/crossing`, `logos/kids-crossing`, `logos/youth-crossing` using the exact names listed in each folder's `PLACEHOLDERS.md` (those names match `brand-kit.json`).
- [ ] Delete the `PLACEHOLDERS.md` files as folders are filled.
- [ ] Replace the placeholder logo tiles in `index.html` with the real assets.
- [ ] Add the Brand Guides 2023 PDF (public if cleared, else link to the private/SharePoint copy).

## 3. Deploy the site (GitHub Pages)
- [ ] Repo → **Settings → Pages** → Source: `Deploy from a branch`, branch `main`, folder `/ (root)`.
- [ ] The `CNAME` file (`brand.thecrossing.church`) is already committed.
- [ ] **DNS** (whoever manages `thecrossing.church`): add a `CNAME` record `brand` → `thecrossing-church.github.io`.
- [ ] Back in Pages settings, tick **Enforce HTTPS** once the cert provisions.
- [ ] Verify the site loads at `https://brand.thecrossing.church`.

## 4. Wire into the ecosystem
- [ ] **Rock BrandCentral →** replace the hand-maintained download wall with an HTML/Lava block that links to (or renders live from) `brand.thecrossing.church` / `brand-kit.json`. This is what kills the staleness — one place to update.
- [ ] **Reconcile the creative "fuller" version** into this repo so there's a single source; creative reviews via `CODEOWNERS`.
- [ ] **SharePoint** keeps the working Office templates (letterhead, decks, signatures); link to them from the site rather than duplicating binaries.

## 5. Announce & maintain
- [ ] Tell the Rock team + creative where it lives and how to request changes (open a PR).
- [ ] Set a review cadence (quarterly + on any brand change).
- [ ] Give AI users the one-liner: *"Use the brand at `raw.githubusercontent.com/TheCrossing-Church/brand/main/brand-kit.json` — follow its rules, colors, and voice."*

## CI (already included)
`.github/workflows/validate.yml` validates `brand-kit.json` against `schema/` and checks that every referenced asset exists. During the placeholder phase, missing assets **warn** rather than fail — flip that to `sys.exit(1)` once real assets are in, so the build fails if the JSON ever references a missing file.

## The hybrid boundary, at a glance
| Public (`brand`) | Private (`brand-internal` / SharePoint) |
|---|---|
| Logos (SVG/PNG), colors, `brand-kit.json`, guidelines, rendered site | Editable source files, **Bariol font files**, internal templates, unreleased campaign art |
