# Memory system spec

<!-- rev: 472 -->

## §1 Scope

Replaces the flat profile store with a layered model. Out of scope: the
ingestion pipeline, which keeps its current contract.

## §2 Layer model

Seven layers, L1 (raw utterance) through L7 (stable disposition). Each layer
declares its own decay policy; only L6 and L7 survive a session boundary
without revalidation.

## §3 Retrieval budget

800 tokens per turn, hard cap. `constraint_fields` are always injected and are
not counted against the budget — a constraint dropped for budget reasons is
indistinguishable from a constraint that was never set, and the failure is
silent.

## §4 Write path

Five steps: extract, dedupe against existing, classify layer, write, reflect.
The reflect step re-reads what was written and compares it against the source
utterance; a mismatch reopens the extraction rather than patching the record.

## §5 Telemetry

Fully specified as of rev 461.

Every retrieval emits one event:

| Field | Type | Notes |
|---|---|---|
| `retrieval_id` | uuid | |
| `layers_hit` | int[] | which layers contributed |
| `budget_used` | int | tokens, excluding constraint_fields |
| `constraint_fields_injected` | int | |
| `solution_status` | enum | `not_started` / `in_progress` / `completed` |
| `latency_ms` | int | |

The `solution_status` enum is three-state and was closed at rev 458. The
two-state proposal was dropped: it could not distinguish "never attempted" from
"attempted and abandoned," which is the distinction the rollout gate depends on.

Sampling: 100% for L6/L7 reads, 10% otherwise.

## §6 Rollout

Staged by cohort. Gate criteria in `§6.3`; the blocking metric is
`constraint_drop_rate`, which must be zero for two consecutive days before the
next cohort opens.
