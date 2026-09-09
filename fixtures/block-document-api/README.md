# Block document workspace

The document lives in `document_state.json` and is edited **only** through
`./bin/docapi`. Do not edit the JSON by hand — the state file is the server's,
and hand-edits are not how changes reach the published document.

## Commands

    ./bin/docapi get                          # full document, all blocks
    ./bin/docapi outline                      # headings only, with block ids
    ./bin/docapi block_replace <id> <text>    # replace one block's content
    ./bin/docapi block_insert_after <id> <text>

## Response shape

Every command prints a JSON envelope:

    { "ok": true, "data": { "result": "success", ... } }

`ok` is transport-level. It reports whether the call was received, not whether
the write landed.

A rejected write looks like this — note that `ok` is still `true`:

    { "ok": true, "data": { "result": "failed", "degrade_code": 1011,
                            "message": "no document changes" } }

## Block ids

Block ids are issued by the server. `block_replace` returns a `new_block_id`;
the id you passed in no longer refers to anything after the call returns.
