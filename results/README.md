# Results

One JSON per run. Filenames are `<task>-<condition>-<n>.json`:

- `ctx` — the operator's `CLAUDE.md` loaded (the condition the tool is
  actually used under)
- `noctx` — `--safe-mode`, user customization disabled

**Only compare entries whose `user_context` matches.** Two conditions are two
populations; averaging across them is the specific mistake `docs/METHOD.md`
sec.1 exists to prevent.

Every run in this directory was scored by the same grader. Results produced by
an earlier version of a probe are deleted rather than kept alongside, for the
same reason: a table mixing two graders cannot distinguish a change in the
model from a change in the measurement.

Metrics naming an end state (`stale_refs_remaining`, `definitions_remaining`,
`orphaned_block_count`) are terminal — the last reported value is the answer.
Summing them across turns is meaningless.
