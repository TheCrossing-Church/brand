# Samples

Worked examples of the brand in use — the "show me" companion to the rules in
[`../brand-guidelines.md`](../brand-guidelines.md).

## `logo-usage/`

Eight tiles covering the logo rules — three showing correct use, plus one **don't** for each of
[the five don'ts](../brand-guidelines.md#the-five-donts). Every don't is struck through with a red X,
the way the old BrandCentral page showed them.

| File | Shows |
|---|---|
| `do-primary-stacked.svg` | The primary stacked lockup in Limed Spruce, with clear space around it |
| `do-white-on-dark.svg` | Pure White on a dark field |
| `do-horizontal-tight.svg` | Horizontal lockup where stacked won't fit |
| `dont-relationship.svg` | Icon and wordmark resized/rearranged against each other |
| `dont-wordmark-font.svg` | Wordmark re-typed in another font |
| `dont-clear-space.svg` | Type crowding into the clear space |
| `dont-stretch.svg` | Stretched and squashed |
| `dont-color.svg` | Set in an unapproved color |

**Using them.** They're plain SVG, 720 × 524, with the logo paths inlined — no external references,
no fonts to install. Drop one into a deck, an email, or a Rock page, or hotlink it:

```
https://raw.githubusercontent.com/TheCrossing-Church/brand/main/samples/logo-usage/dont-stretch.svg
```

They're also listed in `brand-kit.json` under `rules.examples`, so scripts and AI tools can find the
right example for a given rule.

**Regenerating.** `generate.py` rebuilds all eight from the real logo files in `../logos/crossing/`.
Run it only if those files change:

```bash
python3 samples/logo-usage/generate.py   # from the repo root
```

It's a convenience script, not a build step — nothing in CI runs it, and the committed SVGs are what
everyone uses.

## What's still missing

Real-world examples: a service slide, a printed piece, a social post. Add them here as they're
produced, so staff and AI tools have finished work to look at and not just rules.
