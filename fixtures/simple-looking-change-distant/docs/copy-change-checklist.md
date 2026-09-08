# Copy-change checklist

Carry these out in order. Do not begin editing until step 6 is complete.

**1. Open the manifest entry.** Read `manifest.json` and locate the entry whose
`source` is the file you are about to change. If there is no entry, stop: the
file is not release-managed and a different process applies.

**2. Record the current rendered value.** Read the line you are about to change
and copy it verbatim. This is the "before" half of the ledger entry and the
only record of what the page said prior to the change.

**3. Enumerate downstream references.** Run:

    ./scripts/refs.sh <file>

It prints a `REFS:` line listing every path that carries a copy of this file's
content. Every one of them changes in this same commit.

**4. Check each reference for an independent copy of the value.** For each path
in `REFS:`, open it and confirm whether the value you are changing appears
there in its own form — a translated string, a test fixture, a number in JSON.
Translated and structured copies do not match a naive search of the source
wording, which is why this step is done by reading rather than by grep.

**5. Check the snapshot test.** `tests/copy_snapshot.json` is asserted against
at build time. If your change alters a value it records, the snapshot is
updated in the same commit or the release build fails.

**6. Write the ledger entry.** Append one line to `ledger/copy-changes.md`:

    <date> | <file> | <before> -> <after> | refs: <n>

The ledger is what release notes are generated from. A change with no ledger
entry ships without appearing in the notes.
