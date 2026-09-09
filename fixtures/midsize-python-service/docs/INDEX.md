# Code index

Section-to-line-range map for the two large modules. The project rules
require reading only the range you need instead of the whole file.

## `src/pipeline.py` (2270 lines)

| Section | Lines | What lives here |
|---|---|---|
| Queue intake | 6-340 | Pull messages off the broker, ack/nack, dead-letter. |
| Retry and backoff | 341-720 | Exponential backoff, retry ceiling, jitter. |
| Normalization | 721-1205 | Coerce vendor shapes into the internal record. |
| Batching | 1206-1600 | Accumulate normalized records and flush by size or age. |
| Warehouse write | 1601-2010 | Transactional write with idempotency keys. |
| Metrics | 2011-2270 | Counters and timers exported to the collector. |

## `src/handlers.py` (1809 lines)

| Section | Lines | What lives here |
|---|---|---|
| Dispatch | 5-259 | Route a raw payload to the right vendor handler. |
| Vendor: acme | 260-574 | Acme sends nested JSON with ISO timestamps. |
| Vendor: globex | 575-874 | Globex sends CSV rows with epoch millis. |
| Vendor: initech | 875-1189 | Initech sends XML; namespaces are inconsistent. |
| Shared shaping | 1190-1584 | Field renames and unit conversions used by all vendors. |
| Error mapping | 1585-1809 | Translate vendor error codes to internal reasons. |
