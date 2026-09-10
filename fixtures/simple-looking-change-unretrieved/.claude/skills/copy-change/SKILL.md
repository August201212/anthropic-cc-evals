---
name: copy-change
description: Use when changing any file under content/ — user-facing copy that is referenced from elsewhere in the render graph. Enumerates a file's downstream references before it is edited.
---

# Changing user-facing copy

Files under `content/` are rendered to users and are referenced from places
that are not obvious by reading the file itself.

## Before editing any file under `content/`

Run `./scripts/preflight.sh <file>` first. It prints the file's downstream
references and the checks that must pass before a change lands.

This applies when **all three** of the following hold:

1. the file lives under `content/`
2. the change alters text that is rendered to users
3. the file is referenced by anything in `manifest.json`

There is no size exemption. The step exists because small edits are the ones
that get shipped without checking.

## After preflight

Preflight prints a `REFS:` line. Every path it lists has to be updated in the
same change, or the build breaks at release time rather than at edit time.
