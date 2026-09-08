# Project notes — memory system rework

Maintained by me, updated when I remember to. The authoritative source for
anything about the spec is `spec.md` itself.

## Status

- **Phase:** v0.3 design draft
- **Spec:** `spec.md`, rev 37
- **Owner:** me (product), algo side not yet staffed

## Section status

| Section | State |
|---|---|
| §1 Scope | done |
| §2 Layer model | done |
| §3 Retrieval budget | done |
| §4 Write path | done |
| §5 Telemetry | **not written yet — fields undecided** |
| §6 Rollout | not started |

## Open questions

- §5: the `solution_status` enum is still undecided. Last discussion left it
  between a two-state and a three-state model; nobody has picked one.
- §6: rollout gating criteria not drafted.

## Next steps

1. Finish §5 once the enum question is settled.
2. Draft §6.
