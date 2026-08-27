# How we work on the brand repo

Two parts: **how we actually work today**, and **what we'd like to grow into**. The second half is a
wish list, not a rulebook — nothing in it is expected of anyone right now. It's written down so the
gap between "simple on purpose" and "we forgot" stays visible.

Owner: the **Rock team** (`@TheCrossing-Church/rock-team`).

---

## Today

- **One repo, one branch.** Everything lands on `main` in `TheCrossing-Church/brand`.
- **Commit straight to `main`.** No pull request required, no review required, no branch protection.
- **Pushing publishes.** GitHub Pages rebuilds `brand.thecrossing.church` on every push to `main`. There's no staging site, so a mistake is live until it's fixed — glance at the site after a change.
- **CI runs on every push and PR.** `.github/workflows/validate.yml` checks `brand-kit.json` against the schema and confirms every asset it references exists. The schema check fails the build; the missing-asset check currently only warns.
- **`CODEOWNERS` exists but doesn't bite.** It assigns every path to `rock-team`. Code-owner review only takes effect on pull requests with protection enabled, so today it's documentation of who owns this, not an enforced gate.
- **Undo beats prevent.** Brand changes are small and infrequent, so the honest safety net is the diff and `git revert`, not process.

### Why it's this simple

The Rock team is still getting comfortable with version control, and with Git inside the Claude +
GitHub workflow specifically. Process that isn't understood doesn't add safety; it adds mystery
about why a push was rejected. Small repo, small changes, easy rollback — the cost of a mistake
here is minutes, so the tooling stays out of the way.

### The three commands that cover almost everything

```bash
git log --stat                  # what changed, when, by whom
git show <commit>               # the full diff of one change
git revert <commit>             # undo that change as a new commit
```

`git revert` is the one worth trusting. It doesn't erase history — it adds a commit that puts things
back, so the record of both the mistake and the fix stays intact. To recover a single file instead of
a whole commit: `git checkout <commit>~1 -- path/to/file`.

---

## Someday

Roughly in order of value-for-effort. Each is a step up in safety and a step down in convenience —
adopt one at a time, once the previous one feels routine rather than magical.

### 1. Pull requests for brand-content changes
Open a PR instead of committing directly when changing colors, logos, or guidelines. Keeps a written
reason attached to every change and gives someone a chance to catch a typo before it's on the public
site. **Cost:** two extra commands, or a few clicks. **Do this first** — it's the change that makes
everything below meaningful.

### 2. Branch protection on `main`
Settings → Branches → require a pull request before merging (and 1 approval). This is what makes
`CODEOWNERS` actually route reviews. **Wait until PRs are a habit** — turning it on first means
pushes start getting rejected before anyone knows why.

### 3. Require CI to pass before merge
Add `Validate brand-kit` as a required status check. Stops a `brand-kit.json` that doesn't parse from
reaching `main` and breaking every script and AI prompt pointed at it.

### 4. Make the missing-asset check fail instead of warn
In `validate.yml`, change the `::warning::` to `sys.exit(1)`. Nothing is missing today, so it's a
no-op now and a real guard later — it catches the case where `brand-kit.json` points at a logo path
that was renamed or deleted, which is exactly the failure that quietly breaks other people's tools.

### 5. Tag releases
`git tag -a v0.3.0 -m "Added CMYK values"` + a GitHub release. Gives BrandCentral, scripts, and AI
prompts something stable to pin to (`.../brand/v0.3.0/brand-kit.json`) instead of always tracking
`main`. Useful the first time a change to `main` breaks something downstream.

### 6. A standing review rhythm
Quarterly, plus any time the brand changes — put it on a calendar with an owner's name on it. An
unowned cadence is the same as no cadence; that's how BrandCentral went stale in the first place.

### 7. Split ownership in `CODEOWNERS` if ownership ever splits
Right now the Rock team owns content *and* pipeline, so one line covers it. If Communications ever
takes ownership of brand content, it needs **write access** to this repo plus its own `CODEOWNERS`
lines — an owner team with read-only access silently can't be assigned reviews. Example:

```
*                       @TheCrossing-Church/rock-team
/brand-kit.json         @TheCrossing-Church/communications
/brand-guidelines.md    @TheCrossing-Church/communications
/logos/                 @TheCrossing-Church/communications
```

### 8. A CHANGELOG
Once there are enough versions that "what changed since we printed those banners?" becomes a real
question. Release notes on tags cover this too — don't maintain both.

---

## Deliberately not doing

- **A build step or package pipeline.** Plain files served raw is the whole point: `curl` works,
  `raw.githubusercontent.com` works, AI tools work, nobody needs Node installed.
- **A staging site.** Not worth the second domain for a page that changes a few times a year.
- **Committing font files, ever.** Bariol is commercially licensed. `.gitignore` blocks font
  extensions repo-wide, and that stays.
- **Duplicating Office templates here.** Letterhead and decks live in SharePoint and
  `brand-internal`; the site links to them rather than holding stale copies.

---

## Glossary

For anyone newer to Git than to the brand.

| Term | What it means here |
|---|---|
| **commit** | One saved change with a message. The unit you can undo. |
| **`main`** | The one branch that matters. What's on `main` is what's published. |
| **branch** | A private line of work you can commit to without touching `main`. |
| **pull request (PR)** | A proposal to merge a branch into `main`, with a diff and a place to discuss it. |
| **branch protection** | Repo settings that block direct pushes to `main` and require a PR/review. Not enabled here. |
| **`CODEOWNERS`** | A file mapping paths to teams. GitHub auto-requests review from the owner on PRs touching those paths. |
| **status check / CI** | The automated job that runs on each push (here: validating `brand-kit.json`). Green means it passed. |
| **GitHub Pages** | The service that turns `index.html` on `main` into the live site. |
| **tag / release** | A permanent name pinned to one commit, so others can depend on a fixed version. |
| **`revert`** | A new commit that undoes an earlier one. The safe way to roll back. |
