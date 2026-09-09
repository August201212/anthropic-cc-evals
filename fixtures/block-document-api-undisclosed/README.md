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

Block ids are issued by the server and appear in `outline` and `get` output.
