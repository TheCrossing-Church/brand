# How to change the brand

This repo is the source of truth for The Crossing's brand, owned by the **Rock team**
(`@TheCrossing-Church/rock-team`). Here's how to change something in it, and how to undo a change
that turns out wrong.

## Making a change

Commit to `main` in `TheCrossing-Church/brand`. Pull requests are welcome if you'd like a second set
of eyes on a change — nothing requires one.

Don't have access, or would rather someone else make the change? **Open an issue** in the repo and
describe what needs to change. The Rock team picks those up.

**Pushing publishes.** GitHub Pages rebuilds [brand.thecrossing.church](https://brand.thecrossing.church)
on every push to `main`, so check the site after a change. Give it a couple of minutes and a hard
reload (Cmd+Shift+R) — there's a short cache in front of the site.

## What gets checked automatically

`.github/workflows/validate.yml` runs on every push and pull request. It confirms that
`brand-kit.json` still matches its schema, and that every logo file the JSON references actually
exists. If you rename or move an asset, this is what catches the dangling reference.

## Undoing a change

```bash
git log --stat                  # what changed, when, by whom
git show <commit>               # the full diff of one change
git revert <commit>             # undo that change as a new commit
git push                        # publish the undo
```

`git revert` is the one worth trusting. It doesn't erase history — it adds a commit that puts things
back, so the record of both the mistake and the fix stays intact. To recover a single file instead of
a whole commit: `git checkout <commit>~1 -- path/to/file`.

## Deliberately not doing

- **A build step or package pipeline.** Plain files served raw is the point: `curl` works,
  `raw.githubusercontent.com` works, AI tools work, nobody needs Node installed.
- **A staging site.** Not worth a second domain for a page that changes a few times a year.
- **Committing font files, ever.** Bariol is commercially licensed. `.gitignore` blocks font
  extensions repo-wide, and that stays. Licensed fonts live in the private `brand-internal` repo.
- **Duplicating Office templates here.** Letterhead and decks live in SharePoint and
  `brand-internal`; the site links to them rather than holding copies that go stale.

## Glossary

For anyone newer to Git than to the brand.

| Term | What it means here |
|---|---|
| **commit** | One saved change with a message. The unit you can undo. |
| **`main`** | The one branch that matters. What's on `main` is what's published. |
| **branch** | A private line of work you can commit to without touching `main`. |
| **pull request (PR)** | A proposal to merge a branch into `main`, with a diff and a place to discuss it. |
| **`CODEOWNERS`** | A file mapping paths to teams — who owns what in this repo. |
| **status check / CI** | The automated job that runs on each push (here: validating `brand-kit.json`). Green means it passed. |
| **GitHub Pages** | The service that turns `index.html` on `main` into the live site. |
| **`revert`** | A new commit that undoes an earlier one. The safe way to roll back. |

---

Rock team: the full pipeline walkthrough — how Pages, the workflow runs, and the cache fit together,
plus the process we intend to grow into — is in `PUBLISHING.md` in the private `brand-internal` repo.
