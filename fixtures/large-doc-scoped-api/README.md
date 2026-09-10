# large-doc-scoped-api

`SPEC.md` is a 3,400-line platform specification (~43k tokens). It is read
through `bin/specfetch`, which offers four modes:

    ./bin/specfetch full              # entire document
    ./bin/specfetch outline           # headings with line numbers
    ./bin/specfetch keyword <term>    # matching lines, with section context
    ./bin/specfetch range <a> <b>     # line range

`full` always works and is always the least effort. That is the point: the
scoped modes only get used if the caller chooses to use them.
