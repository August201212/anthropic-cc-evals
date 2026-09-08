# Long-Horizon Agentic Evals for Coding Agents

## Why this suite exists

Most coding-agent benchmarks (SWE-bench and its derivatives) measure **single-shot
repair**: given an issue and a repo, produce a patch that passes tests. That is a
real capability, but it is not the capability that determines whether an agent is
usable across a multi-hour, multi-file working session.

This suite measures the failure modes that only appear **after** the first turn:

- Does the agent still honor project conventions on turn 20?
- Does editing a structured document five times leave it internally consistent?
- When the agent finds duplication, does it eliminate the source or add a reminder?
- On second access to a large file, does it re-read everything or seek precisely?
- Before writing config, does it check whether that key is already defined elsewhere?

Each task in this suite was derived from a **logged, reproduced failure** during
daily production use of a coding agent, not from synthetic construction.

## Task taxonomy

| ID | Failure mode | What it measures |
|----|--------------|------------------|
| `LH-01` | Convention decay | Adherence to stated project rules as context grows |
| `LH-02` | Structural orphaning | Referential integrity across repeated block edits |
| `LH-03` | Patch-over-root-cause | Preference for eliminating a defect class vs. papering over an instance |
| `LH-04` | Redundant re-read | Incremental retrieval on repeat access to known files |
| `LH-05` | Blind config write | Pre-write checking for existing definitions of the same key |

## Scoring philosophy

Binary pass/fail per task is too lossy for behavioral evals. Each task emits:

- `outcome`: pass / partial / fail
- `turn_of_first_violation`: integer or null — for decay-type tasks, *when* it broke
- `evidence`: the specific transcript span that triggered the verdict

`turn_of_first_violation` matters more than the pass rate. A model that holds a
convention for 30 turns and one that breaks at turn 4 both "fail" — but they are
not the same model, and the difference is exactly what a model-performance team
needs to see between two release candidates.

## Non-goals

- Not a leaderboard. Small n, high per-task depth.
- Not measuring raw coding skill. Assumes the model can already write the code.
- Not provider-specific. Tasks are harness-agnostic.

## Status

Harness implemented; six tasks built and run, three still spec-only pending
fixtures. Current task list and results are in `README.md` — kept there rather
than duplicated here. Methodology in `docs/METHOD.md`.
