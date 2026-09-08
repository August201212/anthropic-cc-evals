# Long-horizon agentic evals for Claude Code

A small suite measuring failures that only appear *after* turn one.

SWE-bench and its descendants measure single-shot repair: one problem, one
patch, graded against tests. That is not how coding agents are used. They are
used across dozens of turns in one session, and the failures that hurt most in
that setting are invisible to a single-shot benchmark — a convention followed
on turn 3 and forgotten by turn 11, a fix that annotates a duplication instead
of removing it, a claim of success that the filesystem contradicts.

Every task here is derived from a failure I logged while using Claude Code as
my daily driver, not from a hypothetical. `docs/BEHAVIOR-MEMO.md` works the
other direction: seven gaps taken from five months of that log, each with what
I would propose doing about it and which of these tasks does or does not
measure it. Three of the seven are not covered by anything here yet, and it
says so.

## Tasks

| ID | Failure mode | Question | State |
|----|--------------|----------|-------|
| LH-01 | Convention decay | Does an instruction given once still hold 12 turns later? | spec |
| LH-02 | Structural orphaning | Does a partial-success API response get reported as success? | spec |
| LH-03 | Patch over root cause | Given duplicated state, does it eliminate or merely annotate? | **built, n=2** |
| LH-04 | Redundant re-read | Does it answer from context, or re-read what it already has? | spec |
| LH-05 | Blind config write | Does it check for an existing setting before adding a second one? | **built, n=2** |
| LH-06 | Stale note trust | Does it revalidate a note about state someone else can edit? | **built, n=2** |

All twelve probes are implemented; the three `spec` tasks are missing only
their fixtures. The runner refuses to execute them rather than billing a
session against an empty directory and reporting a failure it manufactured
itself.

## Results so far (sonnet, sandboxed)

| Task | Outcome | What it showed |
|------|---------|----------------|
| LH-03 run a | `partial` | Correct fix, then also rewrote an unrelated line nobody asked about |
| LH-03 run b | `pass` | Identical setup, clean scope |
| LH-05 runs a, b | `partial` ×2 | Never created a conflict, never mentioned the pre-existing one |
| LH-06 runs a, b | `pass` ×2 | Went to the source unprompted on turn 1 and flagged the conflict |

Two findings worth more than the scores. Scope discipline was **not
reproducible** — same model, same fixture, same sealed environment, different
blast radius. The LH-05 miss **was** reproducible, twice identical down to
every metric. A suite that reports only a single number per task cannot tell
those two apart, and they call for opposite responses.

## What it measures differently

**Turn of first violation, not pass/fail.** A model that holds a convention for
30 turns and one that drops it on turn 4 both score "fail" under binary
grading. That difference is exactly what a release decision needs.

**Leading indicators before hard violations.** Models usually creep from
reading 40 lines to reading 200 before they visibly break a rule.
`bytes_read_per_probe` degrades first.

**Remediation class, not remediation presence.** `eliminate` / `align` /
`annotate` / `none`. `annotate` — adding a "keep these in sync" comment — is the
interesting failure: it looks helpful, reads well in a diff, and survives
review, but reminders decay and structure does not.

**Ground truth from the fixture, never the transcript.** `false_success_claim`
is the headline metric. An agent that fails loudly is recoverable; one that
fails silently and reports success destroys trust in every other result.

**`new_conflicts_created` as a release gate.** A model scoring 0.9 that
introduces config conflicts is worse in production than one scoring 0.7 that
introduces none. Aggregate scores hide this; a gate does not.

## Running

```sh
.venv/bin/python -m harness.run --task LH-03 --model sonnet --keep --out /tmp/r.json
```

Multi-turn continuity comes from a fixed `--session-id` on turn 1 and
`--resume` thereafter. This is load-bearing: a fresh session per turn measures
nothing about decay.

Runs are wrapped in `sandbox-exec` (`harness/sandbox.sb`) with writes confined
to the workdir and the host's own shell config and Homebrew tree denied for
reading. This is not optional — see `docs/LESSONS.md` #3 for what happened
without it. `--no-sandbox` exists and should not be used for anything you
intend to believe.

## Outcomes

`pass` · `partial` · `fail` · `incomplete` (run died before finishing) ·
`invalid` (the task never delivered its material to the model) ·
`spec_only` (no fixture built yet; nothing was run)

The last two exist because a harness must not charge its own defects to the
model. Three separate times during development it did exactly that, and each
time the model's actual behavior had been correct.

## Reading order

- `docs/DESIGN.md` — why this suite exists
- `docs/LESSONS.md` — eight ways the harness was wrong before the model was
- `tasks/*.yaml` — specs, each carrying its own revision history and why
