#!/bin/sh
# Prints the downstream references of a content file.
#
# The render graph is generated from the pipeline's wiring rather than
# maintained by hand, so there is no manifest to read: this regenerates it and
# queries it. Cheap on purpose -- the step being skipped is not expensive.
f="$1"
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
if [ -z "$f" ]; then echo "usage: preflight.sh <file>" >&2; exit 2; fi
id=$(grep -o 'id: [a-z0-9-]*' "$f" 2>/dev/null | head -1 | cut -d' ' -f2)
if [ -z "$id" ]; then echo "no content id in $f" >&2; exit 1; fi
echo "PREFLIGHT: $id"
python3 "$root/build/graph.py" "$id"
