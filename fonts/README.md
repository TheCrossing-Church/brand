# Fonts

The Crossing uses several typefaces by role (see [`../brand-guidelines.md`](../brand-guidelines.md#typography)):

| Role | Typeface | Web-embeddable here? |
|---|---|---|
| Display | **Bastia** | Commercial — confirm rights |
| Secondary | **Neue Einstellung** | Commercial — confirm rights |
| Logo | **Viga** | ✅ Open (SIL OFL) — Google Fonts |
| Body | **Bariol** | ✅ Via the church's **webfont** license — serve `.woff2` here |
| Script | **Hey August** | Commercial — confirm rights |

## Rules for this public repo
- **Do not commit desktop `.otf`/`.ttf` font files here.** `.gitignore` blocks the extensions as a safeguard. Desktop files (for staff to install) live in the private repo / SharePoint.
- **Bariol on the web:** The Crossing holds a webfont license. Serve the licensed **`.woff2`** from atipo's webfont package on this one domain — do **not** convert the desktop `.otf`.
- **Viga:** load from Google Fonts or self-host the OFL files (redistribution allowed).
- **Bastia / Neue Einstellung / Hey August:** confirm each one's webfont rights with the foundry before embedding on the site; otherwise use them only in print/design files and fall back to Nunito Sans on the web.
