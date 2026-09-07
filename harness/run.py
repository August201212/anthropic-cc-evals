"""
Runner: drives a multi-turn session against a fixture and scores the probes.

Multi-turn continuity is the whole point of this suite -- a fresh session per
turn would measure nothing about decay. Continuity is achieved with a fixed
`--session-id` on turn 1 and `--resume <id>` thereafter.

Fixtures are copied to a scratch directory per run so that (a) tasks are
idempotent and (b) ground truth can be diffed against the pristine original.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from . import probes
from .transcript import Transcript, parse_stream_json

ROOT = Path(__file__).resolve().parent.parent
SANDBOX_PROFILE = Path(__file__).resolve().parent / "sandbox.sb"
DEFAULT_TIMEOUT = 600

# Metrics describing the fixture's END STATE rather than a per-turn event.
# These are read fresh off disk by whichever probe reports them, so the last
# reported value is the answer; adding them across turns is meaningless.
TERMINAL_STATE_METRICS = frozenset(
    {
        "definitions_remaining",
        "distinct_values_remaining",
        "remediation_class",
        "orphaned_block_count",
    }
)


@dataclass
class ProbeResult:
    turn: int
    expect: str
    ok: bool
    evidence: str
    metrics: dict[str, Any]
    unusable: bool = False


@dataclass
class TaskResult:
    task_id: str
    name: str
    model: str
    outcome: str = "fail"
    turn_of_first_violation: int | None = None
    completed_turns: int = 0
    probes: list[ProbeResult] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    started_at: str = ""

    def aggregate(self, rules: dict, incomplete: bool = False) -> None:
        # Probes that never got their material judge nothing. They are excluded
        # from the violation set and instead invalidate the run: a suite that
        # reports "fail" for a task it failed to deliver is worse than one that
        # reports nothing.
        undelivered = [p.turn for p in self.probes if p.unusable]
        violations = [p.turn for p in self.probes if not p.ok and not p.unusable]
        first = min(violations) if violations else None
        self.turn_of_first_violation = first

        if first is not None:
            # Late failure is materially better than early failure for decay
            # tasks; the YAML sets the boundary per task.
            threshold = _partial_threshold(rules)
            self.outcome = (
                "partial" if threshold is not None and first >= threshold else "fail"
            )
        elif incomplete:            # No violation observed, but the run did not finish. Calling this a
            # pass would silently reward a task that crashed before its hardest
            # probe; calling it a fail would blame the model for a harness bug.
            self.outcome = "incomplete"
        else:
            self.outcome = "pass"

        # A run whose material never reached the model cannot be scored at all,
        # whatever the surviving probes said. This outranks pass/fail.
        if undelivered:
            self.outcome = "invalid"
            self.error = (
                (self.error + "; " if self.error else "")
                + f"fixture not delivered on turn(s) {undelivered}"
            )

        # Metric rollup. Booleans OR together (any turn tripping the flag trips
        # the run). Counters SUM only when they measure per-turn events; state
        # metrics describe the fixture's final condition and must be taken from
        # the last probe that reported them, not added up. Summing terminal
        # state is how you get "4 definitions remaining" from a two-file fixture.
        for p in self.probes:
            for k, v in p.metrics.items():
                if isinstance(v, bool):
                    self.metrics[k] = self.metrics.get(k, False) or v
                elif k in TERMINAL_STATE_METRICS:
                    self.metrics[k] = v
                elif isinstance(v, (int, float)):
                    self.metrics[k] = self.metrics.get(k, 0) + v
                else:
                    self.metrics[k] = v

        # Metric-conditioned softening, applied last because it reads the rolled-up
        # metrics. Only ever turns `fail` into `partial` -- never rescues an
        # invalid or incomplete run, whose problem is that nothing was measured.
        if self.outcome == "fail" and _downgrades_to_partial(rules, self.metrics):
            self.outcome = "partial"
        elif self.outcome == "pass" and _demotes_from_pass(rules, self.metrics):
            self.outcome = "partial"


def _partial_threshold(rules: dict) -> int | None:
    """Parse e.g. 'first violation at turn >= 10' out of the scoring block."""
    text = str(rules.get("partial", ""))
    for token in text.replace(">=", " ").split():
        if token.isdigit():
            return int(token)
    return None


def _downgrades_to_partial(rules: dict, metrics: dict) -> bool:
    """
    Some tasks separate "did harm" from "missed an opportunity", and the
    distinction is not about WHEN the violation happened but WHICH one it was.
    LH-05 is the case: creating a new config conflict is a release blocker,
    while failing to volunteer a pre-existing one is a lesser miss. A turn
    threshold cannot express that, so the task states the condition directly:

        partial_if: {new_conflicts_created: 0}

    Every listed metric must match for the run to be softened to `partial`.
    """
    cond = rules.get("partial_if")
    if not isinstance(cond, dict):
        return False
    return all(metrics.get(k) == v for k, v in cond.items())


def _demotes_from_pass(rules: dict, metrics: dict) -> bool:
    """
    Some defects are invisible to every individual probe because they are about
    what the agent did BESIDES the task. LH-03's agent made the requested fix
    and then also rewrote an unrelated line it considered an improvement -- each
    probe passes, the blast radius is still wrong.

        demote_if: {touched_unrelated_files: true}

    A clean run and a correct-but-sprawling run must not report the same, or the
    suite silently endorses scope creep.
    """
    cond = rules.get("demote_if")
    if not isinstance(cond, dict):
        return False
    return any(metrics.get(k) == v for k, v in cond.items())


def run_turn(
    prompt: str,
    cwd: Path,
    session_id: str,
    first: bool,
    model: str,
    timeout: int,
    disallowed: list[str] | None = None,
    sandbox: bool = True,
) -> str:
    cmd = [
        "claude",
        "-p",
        prompt,
        "--output-format",
        "stream-json",
        "--verbose",
        "--model",
        model,
        "--dangerously-skip-permissions",
    ]
    # Environment sealing. Any tool that can reach the network makes a run
    # unreproducible: the same prompt against the same fixture will score
    # differently depending on the day's latency. Tasks declare what they need
    # sealed; the default is to seal nothing.
    if disallowed:
        cmd += ["--disallowedTools", ",".join(disallowed)]
    cmd += ["--session-id", session_id] if first else ["--resume", session_id]

    # Filesystem isolation. Without this the agent reads the host's real config
    # as answer material -- and writes to it. See docs/LESSONS.md #3. The
    # fixture copy is not isolation on its own; this profile is the whitelist.
    if sandbox:
        cmd = [
            "sandbox-exec",
            "-f",
            str(SANDBOX_PROFILE),
            "-D",
            f"WORKDIR={cwd.resolve()}",
            "-D",
            f"HOME={Path.home()}",
        ] + cmd

    proc = subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        raise RuntimeError(proc.stderr.strip()[:400] or "claude exited non-zero")
    return proc.stdout


def run_task(
    spec_path: Path, model: str, keep: bool, timeout: int, sandbox: bool = True
) -> TaskResult:
    spec = yaml.safe_load(spec_path.read_text())
    result = TaskResult(
        task_id=spec["id"],
        name=spec["name"],
        model=model,
        started_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )

    fixture_src = ROOT / spec["setup"].get("fixture", spec["setup"].get("repo", ""))

    # Some tasks are specified but not yet built. Running one produces a real
    # session against an empty directory: billed, slow, and INVALID by
    # construction. Refuse before spending anything -- a missing fixture is a
    # statement about this repo, not about the model.
    if not fixture_src.exists():
        result.outcome = "spec_only"
        result.error = f"no fixture at {fixture_src.relative_to(ROOT)}"
        return result

    scratch = Path(tempfile.mkdtemp(prefix=f"{spec['id']}-"))
    workdir = scratch / "work"

    try:
        shutil.copytree(fixture_src, workdir)

        session_id = str(uuid.uuid4())
        tx = Transcript()
        sealed = spec.get("setup", {}).get("seal_tools") or []

        for i, turn_spec in enumerate(spec["turns"]):
            raw = run_turn(
                turn_spec["prompt"],
                workdir,
                session_id,
                first=(i == 0),
                model=model,
                timeout=timeout,
                disallowed=sealed,
                sandbox=sandbox,
            )
            turn = parse_stream_json(raw, turn_spec["n"])
            turn.prompt = turn_spec["prompt"]
            turn.probe_key = turn_spec.get("probe_key", "")
            tx.turns.append(turn)

            # Keep the raw stream. Every debugging session so far has ended with
            # "but what did it actually say?" -- and without this the only way to
            # answer is to pay for the run again.
            if keep:
                (scratch / f"turn-{turn.n}.jsonl").write_text(raw)

            if not turn_spec.get("probe"):
                continue

            expect = turn_spec["expect"]
            verdict = probes.get(expect)(tx, turn, workdir, spec)
            result.probes.append(
                ProbeResult(
                    turn=turn.n,
                    expect=expect,
                    ok=verdict.ok,
                    evidence=verdict.evidence,
                    metrics=verdict.metrics,
                    unusable=verdict.unusable,
                )
            )

        result.completed_turns = len(tx.turns)

    except subprocess.TimeoutExpired:
        result.error = f"timeout after {timeout}s on turn {len(tx.turns) + 1}"
    except Exception as exc:  # noqa: BLE001 - surfaced in the report, not swallowed
        result.error = f"{type(exc).__name__}: {exc}"
    finally:
        # Always aggregate. A run that dies on turn 4 still produced three turns
        # of real evidence, and discarding it would hide exactly the partial
        # signal these tasks exist to capture.
        result.completed_turns = len(tx.turns)
        result.aggregate(spec.get("scoring", {}), incomplete=bool(result.error))
        if keep:
            result.metrics["_workdir"] = str(workdir)
        else:
            shutil.rmtree(scratch, ignore_errors=True)

    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="Long-horizon agentic eval runner")
    ap.add_argument("--task", help="task id (e.g. LH-03); default: all")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    ap.add_argument("--keep", action="store_true", help="preserve scratch dirs")
    ap.add_argument("--out", type=Path, help="write JSON results here")
    ap.add_argument(
        "--no-sandbox",
        action="store_true",
        help="disable filesystem isolation (results are NOT trustworthy)",
    )
    args = ap.parse_args()

    specs = sorted((ROOT / "tasks").glob("*.yaml"))
    if args.task:
        specs = [s for s in specs if s.name.startswith(args.task)]
    if not specs:
        print(f"no task matching {args.task!r}", file=sys.stderr)
        return 2

    results = []
    for spec in specs:
        print(f"→ {spec.stem} [{args.model}]", flush=True)
        r = run_task(spec, args.model, args.keep, args.timeout, not args.no_sandbox)
        results.append(r)

        mark = {
            "pass": "PASS",
            "partial": "PART",
            "fail": "FAIL",
            "incomplete": "INCP",
            "invalid": "INVL",
            "spec_only": "SPEC",
        }[r.outcome]
        if r.outcome == "spec_only":
            print(f"  SPEC  specified but not built -- {r.error}")
            continue
        detail = f" first_violation=turn{r.turn_of_first_violation}" if r.turn_of_first_violation else ""
        print(f"  {mark}{detail}{'  ERROR: ' + r.error if r.error else ''}")
        for p in r.probes:
            status = "UNUSABLE" if p.unusable else ("ok" if p.ok else "VIOLATION")
            print(f"    turn {p.turn:>2} {p.expect:<36} {status}  {p.evidence}")

    if args.out:
        args.out.write_text(json.dumps([asdict(r) for r in results], indent=2))
        print(f"\nwrote {args.out}")

    # Unbuilt tasks are not failures of the model or of the run; they are work
    # this repo has not done yet.
    scored = [r for r in results if r.outcome != "spec_only"]
    return 0 if scored and all(r.outcome == "pass" for r in scored) else 1


if __name__ == "__main__":
    raise SystemExit(main())
