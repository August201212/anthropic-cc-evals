# Contributing

## Branches and commits

Work on a branch named `<area>/<short-description>`. Commit messages start with
the area in lowercase — `content:`, `i18n:`, `build:` — followed by what
changed and why, not what file it was in.

## Tests

`make test` runs the snapshot suite. Snapshots under `tests/` are checked in
deliberately; when one changes, the diff is the review, so update it in the
same commit as the change that caused it rather than in a follow-up.

## Review

One approval for anything under `content/` or `i18n/`, two for anything that
touches the build. Reviews are on the change, not the person who wrote it.

## Repository layout

- `content/` — user-facing copy, rendered at build time
- `i18n/` — translations, one file per locale
- `tests/` — snapshot fixtures
- `scripts/` — repo tooling
- `manifest.json` — the render graph: which sources feed which outputs
