#!/bin/sh
# Prints the downstream references of a content file, per manifest.json.
# Step 3 of the copy-change checklist.
f="$1"
if [ -z "$f" ]; then echo "usage: refs.sh <file>" >&2; exit 2; fi
id=$(grep -o 'id: [a-z-]*' "$f" 2>/dev/null | head -1 | cut -d' ' -f2)
if [ -z "$id" ]; then echo "no content id in $f" >&2; exit 1; fi
echo "REFS-FOR: $id"
python3 - "$id" <<'PY'
import json,sys
m=json.load(open("manifest.json"))
e=m["content"].get(sys.argv[1])
print("REFS:", " ".join(e["refs"]) if e else "(none)")
PY
