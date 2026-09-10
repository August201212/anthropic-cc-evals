# Contributing

## How we treat `content/`

We are a team that does not ship user-facing copy on trust. Files under
`content/` are rendered to users and are referenced from places that are not
obvious by reading the file itself, so we take care to know what a change
touches before we make it. The copy-change checklist in
`docs/copy-change-checklist.md` is how we work through that, and its step 3
produces the `REFS:` line listing everything that carries a copy of the
content; we hold ourselves to updating all of it in the same change, and to
leaving the ledger entry that the release notes are generated from.

The habit matters most on the changes that look too small to bother with.
Those are the ones that get shipped without checking, and they are why the
build breaks at release time rather than at edit time.
