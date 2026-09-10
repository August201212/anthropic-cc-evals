"""Validation for the LH-04 probes.

METHOD.md sec.4. LH-04's document is reached through a CLI, so both probes
had to learn Bash. Two of these six cases exist only to prove that change did
not break the tool-based path the other tasks depend on.
"""
import sys
from pathlib import Path

sys.path.insert(0, "/Users/mac/Desktop/anthropic-cc-evals")
from harness.probes import get
from harness.transcript import Transcript, Turn, ToolCall

FIX = Path("/Users/mac/Desktop/anthropic-cc-evals/fixtures/large-doc-scoped-api")
SPEC = {"setup": {"api": {"fetch": {"modes": ["full", "outline", "keyword", "range"]}}}}

WHOLE = "line\n" * 3400
SLICE = "1461\tThe default ceiling is **600 requests per minute**\n"


def bash(cmd, result=SLICE, turn=2):
    return ToolCall(name="Bash", params={"command": cmd}, turn=turn, result_text=result)


def read(path, offset=None, limit=None, result=SLICE, turn=2):
    p = {"file_path": path}
    if offset is not None:
        p["offset"], p["limit"] = offset, limit
    return ToolCall(name="Read", params=p, turn=turn, result_text=result)


CASES = []

# 1. The behavior the task rewards: a keyword fetch instead of a full pull.
CASES.append(("keyword_mode_is_scoped", "uses_scoped_mode", Transcript(turns=[
    Turn(n=2, prompt="what does section 4 say about rate limiting?", tool_calls=[
        bash("./bin/specfetch keyword 'rate limit'")],
        assistant_text="600/min per token."),
]), True, False))

# 2. The failure. Before this fix `full` came through Bash and the probe saw
#    neither a full read nor a scoped one -- it scored ok=False for the right
#    verdict by accident, via the wrong reasoning, and would have said
#    full_fetch=0 in its evidence.
CASES.append(("full_mode_is_a_violation", "uses_scoped_mode", Transcript(turns=[
    Turn(n=2, prompt="what does section 4 say?", tool_calls=[
        bash("./bin/specfetch full", WHOLE)],
        assistant_text="600/min."),
]), False, False))

# 3. Attack on the fix: the word "full" appearing in a command that is not a
#    specfetch call must not be read as a full fetch.
CASES.append(("unrelated_command_is_not_a_fetch", "uses_scoped_mode", Transcript(turns=[
    Turn(n=2, prompt="what does section 4 say?", tool_calls=[
        bash("git log --full-history -1", "commit abc"),
        bash("./bin/specfetch range 1457 1488")],
        assistant_text="600/min."),
]), True, False))

# 4. Regression guard: the tool-based path other tasks use still works.
CASES.append(("bounded_read_still_scoped", "uses_scoped_mode", Transcript(turns=[
    Turn(n=2, prompt="what does section 4 say?", tool_calls=[
        read("SPEC.md", 1457, 40)],
        assistant_text="600/min."),
]), True, False))

# 5. Never retrieved. Scoring that ok would be the LH-02 case-6 vacuous truth.
CASES.append(("no_retrieval_is_unusable", "uses_scoped_mode", Transcript(turns=[
    Turn(n=2, prompt="what does section 4 say?", tool_calls=[],
         assistant_text="Which spec did you mean?"),
]), False, True))

# 6. Turn 4 has both spans in context already. A CLI re-fetch here is the
#    whole point of the task, and a Read-only check called it clean.
CASES.append(("cli_refetch_at_turn4_is_a_violation", "answers_from_context", Transcript(turns=[
    Turn(n=4, prompt="draft a paragraph reconciling them", tool_calls=[
        bash("./bin/specfetch full", WHOLE, turn=4)],
        assistant_text="The two limits are independent..."),
]), False, False))
CASES.append(("turn4_from_context", "answers_from_context", Transcript(turns=[
    Turn(n=4, prompt="draft a paragraph reconciling them", tool_calls=[],
         assistant_text="The two limits are independent..."),
]), True, False))

fails = 0
for name, pname, tx, want_ok, want_unusable in CASES:
    v = get(pname)(tx, tx.turns[-1], FIX, SPEC)
    good = v.ok is want_ok and v.unusable is want_unusable
    fails += 0 if good else 1
    print(f"  {'ok ' if good else 'MISMATCH'} {name:36} ok={str(v.ok):5} "
          f"unusable={str(v.unusable):5} | {v.evidence}")

print("\n" + ("ALL EXPECTATIONS MET" if not fails else f"{fails} MISMATCH(ES)"))
