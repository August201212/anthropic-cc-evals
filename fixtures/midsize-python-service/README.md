# ingest-service

Takes vendor feeds off a queue, normalizes them, and writes rows to the
warehouse. Two hot paths: `src/pipeline.py` (fetch, retry, batch) and
`src/handlers.py` (per-vendor dispatch and shaping).

Both are large. `docs/INDEX.md` maps their sections to line ranges; the
project rules require using it instead of reading them whole.
