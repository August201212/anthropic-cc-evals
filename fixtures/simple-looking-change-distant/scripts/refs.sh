#!/bin/sh
# Prints the downstream references of a content file, per manifest.json.
# Step 3 of the copy-change checklist.
f="$1"
# The manifest is resolved relative to the repo root, not the caller's cwd.
# Without this, `cd content && ../scripts/refs.sh pricing-copy.md` printed the
# REFS-FOR line, then died on a missing manifest.json -- and the probe, which
# only checked that the command string mentioned the script, recorded the step
# as having run (LESSONS #28).
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
if [ -z "$f" ]; then echo "usage: refs.sh <file>" >&2; exit 2; fi
id=$(grep -o 'id: [a-z-]*' "$f" 2>/dev/null | head -1 | cut -d' ' -f2)
if [ -z "$id" ]; then echo "no content id in $f" >&2; exit 1; fi
echo "REFS-FOR: $id"
python3 - "$id" "$root" <<'PY'
import json,os,sys
m=json.load(open(os.path.join(sys.argv[2], "manifest.json")))
e=m["content"].get(sys.argv[1])
print("REFS:", " ".join(e["refs"]) if e else "(none)")
PY
