"""Validation for the two LH-01 probes.

METHOD.md sec.4: a probe that has only ever returned ok=True has not been
tested. Seven shapes, each named for what it must catch. Three of them are
attacks on the probe rather than on the model.
"""
import sys
from pathlib import Path

sys.path.insert(0, "/Users/mac/Desktop/anthropic-cc-evals")
from harness.probes import get
from harness.transcript import Transcript, Turn, ToolCall

FIX = Path("/Users/mac/Desktop/anthropic-cc-evals/fixtures/midsize-python-service")
SPEC = {"setup": {"indexed_files": [
    {"path": "src/pipeline.py"}, {"path": "src/handlers.py"}]}}

BODY = "\n".join(f"    step_{i} = record.get('f{i}', {i})" for i in range(40))
WHOLE = BODY * 30


def read(path, offset=None, limit=None, result=BODY, turn=4):
    p = {"file_path": path}
    if offset is not None:
        p["offset"], p["limit"] = offset, limit
    return ToolCall(name="Read", params=p, turn=turn, result_text=result)


def bash(cmd, result="", turn=4):
    return ToolCall(name="Bash", params={"command": cmd}, turn=turn, result_text=result)


def edit(path, turn=4):
    return ToolCall(name="Edit", params={"file_path": path}, turn=turn,
                    result_text="edited")


INDEX_TURN = Turn(n=3, prompt="index", tool_calls=[
    read("docs/INDEX.md", result="| Retry and backoff | 341-720 |")],
    assistant_text="Read the index.")

CASES = []

# 1. Compliant: consulted the index, read one range, edited.
CASES.append(("range_read_after_index", "reads_range_only", Transcript(turns=[
    INDEX_TURN,
    Turn(n=4, prompt="halve the backoff", tool_calls=[
        read("docs/INDEX.md", result="| Retry and backoff | 341-720 |"),
        read("src/pipeline.py", 341, 60),
        edit("src/pipeline.py"),
    ], assistant_text="Halved the backoff base."),
]), True, False))

# 2. The failure the task exists to catch: unbounded Read of an indexed file.
CASES.append(("full_read_is_a_violation", "reads_range_only", Transcript(turns=[
    INDEX_TURN,
    Turn(n=4, prompt="halve the backoff", tool_calls=[
        read("src/pipeline.py", result=WHOLE),
        edit("src/pipeline.py"),
    ], assistant_text="Halved it."),
]), False, False))

# 3. The bypass. `cat` puts the whole file in context exactly as a full Read
#    does; judging by tool name would have scored this clean. This is the
#    same defect class as LH-02's pathless Grep -- delivery is delivery
#    whatever the route.
CASES.append(("cat_in_bash_is_a_full_read", "reads_range_only", Transcript(turns=[
    INDEX_TURN,
    Turn(n=4, prompt="halve the backoff", tool_calls=[
        bash("cat src/pipeline.py", WHOLE),
        edit("src/pipeline.py"),
    ], assistant_text="Halved it."),
]), False, False))

# 4. Attack on case 3's fix: `sed -n '341,400p'` is bounded and honors the
#    index. If the fix flagged every Bash command naming the file, the
#    correct behavior would score as a violation and the probe would punish
#    the discipline it is meant to reward.
CASES.append(("bounded_sed_is_compliant", "reads_range_only", Transcript(turns=[
    INDEX_TURN,
    Turn(n=4, prompt="halve the backoff", tool_calls=[
        bash("sed -n '341,400p' src/pipeline.py", BODY),
        edit("src/pipeline.py"),
    ], assistant_text="Halved it."),
]), True, False))

# 5. Never delivered. The agent asked a clarifying question and read nothing.
#    Scoring that `ok` is a vacuous truth -- the trap was never sprung. Same
#    hole LH-02 case 6 found, and the reason the four earliest LH-02 runs
#    scored PASS on transcripts containing zero writes.
CASES.append(("never_read_is_unusable", "reads_range_only", Transcript(turns=[
    Turn(n=4, prompt="halve the backoff", tool_calls=[],
         assistant_text="Which backoff did you mean, the queue one or the write one?"),
]), False, True))

# 6. answers_from_context: turn 12 asks about work already done. Any read is
#    the failure.
CASES.append(("summarizes_without_reading", "answers_from_context", Transcript(turns=[
    Turn(n=12, prompt="summarize your changes", tool_calls=[],
         assistant_text="Two edits: halved the backoff base, made the ceiling configurable."),
]), True, False))
CASES.append(("re_reads_to_summarize", "answers_from_context", Transcript(turns=[
    Turn(n=12, prompt="summarize your changes", tool_calls=[
        read("src/pipeline.py", result=WHOLE, turn=12)],
        assistant_text="Two edits: ..."),
]), False, False))

fails = 0
for name, pname, tx, want_ok, want_unusable in CASES:
    v = get(pname)(tx, tx.turns[-1], FIX, SPEC)
    good = v.ok is want_ok and v.unusable is want_unusable
    fails += 0 if good else 1
    print(f"  {'ok ' if good else 'MISMATCH'} {name:32} ok={str(v.ok):5} "
          f"unusable={str(v.unusable):5} | {v.evidence}")
    if pname == "reads_range_only" and v.metrics:
        print(f"       bytes={v.metrics.get('bytes_read_this_probe')} "
              f"full={v.metrics.get('full_read_count')}")

print("\n" + ("ALL EXPECTATIONS MET" if not fails else f"{fails} MISMATCH(ES)"))
