#!/usr/bin/env python3
"""Render-graph generator.

The graph is derived from the render pipeline's own wiring, not maintained by
hand, so it is not checked in. `preflight.sh` invokes this; anything else that
needs it invokes this too.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Each content id declares its render targets inline; the consumers are found
# by resolving those declarations, which is why reading any single file does
# not tell you the set.
def build():
    graph = {}
    for dirpath, _, files in os.walk(os.path.join(ROOT, "content")):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dirpath, fn)
            body = open(p).read()
            m = re.search(r"<!-- id: ([a-z0-9-]+) -->", body)
            if not m:
                continue
            cid = m.group(1)
            refs = []
            for rel in sorted(_consumers(cid)):
                refs.append(rel)
            graph[cid] = {
                "source": os.path.relpath(p, ROOT),
                "refs": refs,
            }
    return graph


def _consumers(cid):
    """Files that declare themselves downstream of `cid`."""
    out = []
    for sub in ("content", "i18n", "tests"):
        d = os.path.join(ROOT, sub)
        if not os.path.isdir(d):
            continue
        for dirpath, _, files in os.walk(d):
            for fn in files:
                p = os.path.join(dirpath, fn)
                try:
                    body = open(p).read()
                except (OSError, UnicodeDecodeError):
                    continue
                if re.search(r"(?:derives-from|derivesFrom)\W+%s\b" % re.escape(cid), body):
                    out.append(os.path.relpath(p, ROOT))
    return out


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, ".build"), exist_ok=True)
    g = build()
    with open(os.path.join(ROOT, ".build", "graph.json"), "w") as f:
        json.dump(g, f, indent=2)
    if len(sys.argv) > 1:
        e = g.get(sys.argv[1])
        print("REFS:", " ".join(e["refs"]) if e else "(none)")
