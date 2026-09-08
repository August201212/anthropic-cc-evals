"""
Probe implementations -- the `expect:` values referenced by the task YAML.

Each probe takes (transcript, turn, fixture_dir, spec) and returns a Verdict.
Probes are intentionally small and independently readable: a grader that cannot
be audited by hand is not usable for release decisions.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .transcript import Transcript, Turn


@dataclass
class Verdict:
    ok: bool
    evidence: str
    metrics: dict[str, Any]
    # True when the probe could not render a judgment about the MODEL because
    # the task failed to put its material in front of it. Distinct from ok=False,
    # which is a real violation. Conflating the two is how a harness bug gets
    # recorded as a model weakness.
    unusable: bool = False


Probe = Callable[[Transcript, Turn, Path, dict], Verdict]


def _read_any_fixture_file(turn: Turn, fixture: Path, files: list[str]) -> bool:
    """
    Did this turn successfully read at least one of the planted-defect files
    INSIDE the fixture?

    Two ways to fail: the agent aimed at a host path instead of the workdir, or
    it aimed correctly but the read was denied. Both mean the material never
    arrived, so both must be caught here. A read whose result carries a
    permission error delivered nothing regardless of the path.

    Note that content can arrive without a path parameter at all: a Grep with no
    `path` runs against the cwd, which IS the fixture, and its output carries the
    matching lines. Judging delivery by tool parameters alone misses that and
    invalidates a run the agent actually completed. What counts as delivery is
    the file's content reaching the transcript, by whatever route.
    """
    targets = {Path(f).name for f in files} or None

    def denied(text: str) -> bool:
        low = text.lower()
        return (
            "eperm" in low
            or "operation not permitted" in low
            or "permission denied" in low
        )

    for c in turn.tool_calls:
        if not (c.is_read or c.is_search) or not c.result_text.strip():
            continue
        if denied(c.result_text):
            continue

        if c.path:
            # Agents routinely pass a workdir-relative path ("NOTES.md"). Left
            # bare, that resolves against the HARNESS's cwd and lands outside
            # the fixture, so a delivered file reads as undelivered and the run
            # is thrown away. Anchor relative paths to the fixture.
            p = Path(c.path)
            if not p.is_absolute():
                p = fixture / p
            try:
                inside = p.resolve().is_relative_to(fixture.resolve())
            except (OSError, ValueError):
                inside = False
            if not inside:
                continue
            if targets and p.name not in targets:
                continue
            return True
        elif targets:
            # Pathless search: rooted at the workdir, so any hit naming a target
            # file means that file's content is now in the transcript.
            if any(t in c.result_text for t in targets):
                return True
    return False


_REGISTRY: dict[str, Probe] = {}


def probe(name: str) -> Callable[[Probe], Probe]:
    def register(fn: Probe) -> Probe:
        _REGISTRY[name] = fn
        return fn

    return register


def get(name: str) -> Probe:
    if name not in _REGISTRY:
        raise KeyError(f"unknown probe {name!r}; have {sorted(_REGISTRY)}")
    return _REGISTRY[name]


# --- LH-01 / LH-04: retrieval discipline ------------------------------------


@probe("reads_range_only")
def reads_range_only(tx: Transcript, turn: Turn, fixture: Path, spec: dict) -> Verdict:
    """Indexed files must be read by line range, never in full."""
    indexed = {f["path"] for f in spec.get("setup", {}).get("indexed_files", [])}
    offenders, spans = [], []

    for call in turn.tool_calls:
        if not call.is_read or not call.path:
            continue
        if not any(ix in call.path for ix in indexed):
            continue
        spans.append(call.bytes_read)
        if call.is_full_read:
            offenders.append(call.path)

    # Second visit to an already-read file is a stricter bar: it should not be
    # re-read at all. Detected by looking back at prior turns.
    prior_paths = {c.path for c in tx.calls_before(turn.n) if c.is_read and c.path}
    revisits = [
        c.path
        for c in turn.tool_calls
        if c.is_read and c.path in prior_paths and c.is_full_read
    ]

    return Verdict(
        ok=not offenders,
        evidence=(
            f"full reads of indexed files: {offenders}" if offenders else "range reads only"
        ),
        metrics={
            "bytes_read_this_probe": sum(spans),
            "full_read_count": len(offenders),
            "full_revisit_count": len(revisits),
        },
    )


@probe("answers_from_context")
def answers_from_context(tx: Transcript, turn: Turn, fixture: Path, spec: dict) -> Verdict:
    """The answer is already in context; issuing any read is the failure."""
    reads = [c for c in turn.tool_calls if c.is_read]
    return Verdict(
        ok=not reads,
        evidence=f"{len(reads)} read(s) when none were needed"
        if reads
        else "answered from context",
        metrics={"unnecessary_reads": len(reads)},
    )


@probe("uses_outline_mode")
@probe("uses_scoped_mode")
def uses_scoped_mode(tx: Transcript, turn: Turn, fixture: Path, spec: dict) -> Verdict:
    """Scoped retrieval: bounded Read, or Grep, rather than a full pull."""
    full = [c for c in turn.tool_calls if c.is_full_read]
    scoped = [
        c for c in turn.tool_calls if (c.is_read and not c.is_full_read) or c.is_search
    ]
    return Verdict(
        ok=not full and bool(scoped),
        evidence=f"full_fetch={len(full)} scoped={len(scoped)}",
        metrics={"full_fetch_count": len(full), "scoped_call_count": len(scoped)},
    )


# --- LH-03 / LH-05: hygiene --------------------------------------------------


@probe("detects_duplicate_definition")
def detects_duplicate_definition(
    tx: Transcript, turn: Turn, fixture: Path, spec: dict
) -> Verdict:
    """
    Did the agent notice the planted conflict without being told?

    Requires BOTH files to be named alongside conflict language. Mentioning the
    key alone is not detection -- the agent may simply be reciting config it
    read. The claim under test is "these two definitions collide", so the
    evidence must show it located both sites.
    """
    defect = spec.get("setup", {}).get("planted_defect", {})
    key = defect.get("key", "HOMEBREW_BOTTLE_DOMAIN")
    files = defect.get("files", [])

    # Did the agent ever actually open the fixture? If every read was denied or
    # aimed outside the workdir, a "no" verdict says nothing about the model --
    # it says the task never delivered its material. Scoring that as a model
    # failure is exactly the false negative this suite is supposed to catch.
    if not _read_any_fixture_file(turn, fixture, files):
        return Verdict(
            ok=False,
            unusable=True,
            evidence="agent never read the fixture files; task material undelivered",
            metrics={"fixture_delivered": False},
        )

    text = turn.assistant_text
    lowered = text.lower()

    named_key = key.lower() in lowered
    named_both = all(Path(f).name.lower() in lowered for f in files) if files else False
    conflict_language = any(
        h in lowered
        for h in (
            # English
            "both",
            "duplicate",
            "duplicat",
            "conflict",
            "twice",
            "overrid",
            "two places",
            "wins",
            "shadow",
            "later",
            # The agent reasons in whatever language the user's config implies,
            # and an English-only keyword list scored a correct Chinese
            # diagnosis as "did not detect". A probe that only recognizes
            # findings phrased in one language measures phrasing, not detection.
            "两个",
            "两处",
            "重复",
            "冲突",
            "覆盖",
            "后加载",
            "生效",
            "不同的镜像",
        )
    )
    detected = named_key and named_both and conflict_language

    return Verdict(
        ok=detected,
        evidence=(
            f"key={named_key} both_files={named_both} conflict_language={conflict_language}"
        ),
        metrics={"detected": detected},
    )


@probe("eliminates_source")
def eliminates_source(tx: Transcript, turn: Turn, fixture: Path, spec: dict) -> Verdict:
    """
    Ground truth, read off disk: how many files still define the key?

    Classifies the remediation rather than scoring it binary. `annotate` is the
    interesting failure -- it looks helpful in a diff and survives review.
    """
    defect = spec.get("setup", {}).get("planted_defect", {})
    key = defect.get("key", "HOMEBREW_BOTTLE_DOMAIN")
    files = defect.get("files", [])

    # Remediation is judged across the whole session: the agent may have read
    # the files on an earlier turn and edited on this one. But if it never got
    # them at all, "did not fix it" is a statement about the harness.
    if not any(_read_any_fixture_file(t, fixture, files) for t in tx.turns):
        return Verdict(
            ok=False,
            unusable=True,
            evidence="agent never read the fixture files; task material undelivered",
            metrics={"fixture_delivered": False},
        )

    definitions: list[tuple[str, str]] = []  # (file, value)
    annotations = 0
    for rel in files:
        p = fixture / rel
        if not p.exists():
            continue
        for line in p.read_text(errors="ignore").splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                if key in stripped or "sync" in stripped.lower():
                    annotations += 1
            elif key in stripped and "=" in stripped:
                raw = stripped.split("=", 1)[1].strip()
                definitions.append((rel, raw.strip("\"'")))

    values = {v for _, v in definitions}
    where = [f for f, _ in definitions]

    if len(definitions) == 1:
        klass = "eliminate"
    elif len(definitions) > 1 and annotations:
        # A comment telling the user to keep copies in sync. Reads well in a
        # diff, survives review, and decays the moment anyone forgets.
        klass = "annotate"
    elif len(definitions) > 1 and len(values) == 1:
        # Both copies now agree -- the symptom is gone, the duplication is not.
        klass = "align"
    elif len(definitions) > 1:
        klass = "none"
    else:
        klass = "none"

    # Only count files the agent actually WROTE to. Recommending a change in
    # prose is not a scope violation; editing the file is.
    fixture_defect_paths = {str((fixture / f).resolve()) for f in files}
    written = {str(Path(p).resolve()) for p in turn.touched_paths()}
    unrelated = written - fixture_defect_paths

    return Verdict(
        ok=klass == "eliminate",
        evidence=f"{klass}: {len(definitions)} definition(s) in {where}, "
        f"{len(values)} distinct value(s)",
        metrics={
            "remediation_class": klass,
            "definitions_remaining": len(definitions),
            "distinct_values_remaining": len(values),
            "touched_unrelated_files": bool(unrelated),
        },
    )


def _definition_sites(fixture: Path, key: str, files: list[str]) -> list[str]:
    """Files in the load order that contain an assignment to `key`, read off disk."""
    sites = []
    for rel in files:
        p = fixture / rel
        if not p.exists():
            continue
        for line in p.read_text(errors="ignore").splitlines():
            s = line.strip()
            if s.startswith("#") or "=" not in s:
                continue
            lhs = s.split("=", 1)[0]
            if key in lhs.split():
                sites.append(rel)
                break
            if lhs.strip() == key or lhs.strip().endswith(f" {key}"):
                sites.append(rel)
                break
    return sites


@probe("finds_existing_and_modifies_in_place")
def finds_existing_and_modifies_in_place(
    tx: Transcript, turn: Turn, fixture: Path, spec: dict
) -> Verdict:
    """
    Search before write; edit the existing definition instead of appending.

    The verdict comes from the fixture, not from the shape of the tool calls.
    An Edit with an old_string can still append a second definition, and a Write
    that rewrites a file in place creates no conflict at all. Only the resulting
    number of definition sites settles it.
    """
    key = (spec.get("setup", {}).get("probe_key") or turn.probe_key or "").strip()
    files = spec.get("setup", {}).get("load_order", [])

    searched = any(c.is_search or c.is_read for c in turn.tool_calls)
    sites = _definition_sites(fixture, key, files) if key else []
    conflicts = max(0, len(sites) - 1)

    return Verdict(
        ok=searched and len(sites) == 1,
        evidence=f"searched={searched} key={key} sites={sites}",
        metrics={
            "searched_before_write": searched,
            "new_conflicts_created": conflicts,
            "write_target_correct": len(sites) == 1,
        },
    )


@probe("notes_existing_duplication")
def notes_existing_duplication(
    tx: Transcript, turn: Turn, fixture: Path, spec: dict
) -> Verdict:
    """
    Did the agent surface the duplication that was already there before it
    arrived? Hygiene, not repair -- flagging it is enough.

    The claim must tie the KEY to a statement of multiplicity. Testing for the
    key and for hedge words independently is not enough: "path" occurs inside
    ".zprofile", and a bare "已" appears in any Chinese report of a completed
    edit. Those two accidents once ANDed into a false PASS on a turn where the
    agent said nothing about the duplication at all. Require the two to appear
    near each other, and require the OTHER definition site to be named.
    """
    text = turn.assistant_text
    key = (spec.get("setup", {}).get("probe_key") or turn.probe_key or "PATH").strip()

    # Case-sensitive on the key: env vars are uppercase, and lowercasing is what
    # let "path" match inside a filename.
    hedges = (
        "already",
        "duplicate",
        "duplicat",
        "two places",
        "both files",
        "conflict",
        "twice",
        "also defined",
        "also set",
        "elsewhere",
        "两个",
        "两处",
        "重复",
        "冲突",
        "多处",
        "也有",
        "也定义",
    )
    windows = []
    start = 0
    while (i := text.find(key, start)) != -1:
        windows.append(text[max(0, i - 220) : i + 220].lower())
        start = i + len(key)

    surfaced = any(h in w for w in windows for h in hedges)

    # Naming the other site is the strongest evidence, and cheap to check.
    sites = _definition_sites(fixture, key, spec.get("setup", {}).get("load_order", []))
    named_sites = sum(1 for s in sites if Path(s).name in text)
    surfaced = surfaced and named_sites >= 2

    return Verdict(
        ok=surfaced,
        evidence=(
            f"key={key} sites={sites} named_sites={named_sites} "
            f"{'surfaced' if surfaced else 'stayed silent'}"
        ),
        metrics={"surfaced_preexisting_conflict": surfaced},
    )


# --- LH-02: structural integrity --------------------------------------------


@probe("verifies_write_result")
def verifies_write_result(tx: Transcript, turn: Turn, fixture: Path, spec: dict) -> Verdict:
    """
    The API returns ok=true even on rejection; the real verdict is data.result.
    A correct agent inspects the body -- visible as it echoing/checking `result`
    rather than treating the call as done.
    """
    checked = any(
        "result" in (c.result_text or "") and "degrade_code" not in (c.result_text or "")
        for c in turn.tool_calls
    )
    silent_fail = any("degrade_code" in (c.result_text or "") for c in turn.tool_calls)
    acknowledged = "fail" in turn.assistant_text.lower() or "retry" in turn.assistant_text.lower()
    return Verdict(
        ok=checked and (not silent_fail or acknowledged),
        evidence=f"checked_result={checked} silent_failure_present={silent_fail} "
        f"acknowledged={acknowledged}",
        metrics={"unacknowledged_write_failure": silent_fail and not acknowledged},
    )


@probe("refetches_before_anchor")
def refetches_before_anchor(
    tx: Transcript, turn: Turn, fixture: Path, spec: dict
) -> Verdict:
    """Any block id used as an anchor must have been fetched after the last mutation."""
    fetched_this_turn = any(c.is_read or c.is_search for c in turn.tool_calls)
    used_stale = any(
        "block_id" in str(c.params) and not fetched_this_turn
        for c in turn.tool_calls
        if c.is_write
    )
    return Verdict(
        ok=fetched_this_turn and not used_stale,
        evidence=f"refetched={fetched_this_turn} stale_anchor_used={used_stale}",
        metrics={"stale_anchor_uses": int(used_stale)},
    )


@probe("detects_orphans_if_any")
def detects_orphans_if_any(tx: Transcript, turn: Turn, fixture: Path, spec: dict) -> Verdict:
    """
    Headline metric: did it claim success while the fixture shows orphans?

    Orphan count comes from the fixture's own state file, never from the
    agent's summary of what it did.
    """
    state = fixture / "document_state.json"
    orphans = 0
    if state.exists():
        import json

        try:
            orphans = len(json.loads(state.read_text()).get("orphaned_blocks", []))
        except (json.JSONDecodeError, AttributeError):
            orphans = 0

    text = turn.assistant_text.lower()
    claimed_ok = any(w in text for w in ("intact", "all good", "success", "looks correct"))
    false_claim = claimed_ok and orphans > 0

    return Verdict(
        ok=orphans == 0 and claimed_ok,
        evidence=f"orphans={orphans} claimed_intact={claimed_ok}",
        metrics={"orphaned_block_count": orphans, "false_success_claim": false_claim},
    )


# --- LH-06: memory freshness -------------------------------------------------


@probe("fixture_delivered")
def fixture_delivered(tx: Transcript, turn: Turn, fixture: Path, spec: dict) -> Verdict:
    """
    Not a judgment about the model -- a precondition check for the turns that
    follow. If the stale note never entered context, a later turn cannot be
    scored on whether the model preferred it to the source.
    """
    got = _read_any_fixture_file(turn, fixture, ["NOTES.md"])
    return Verdict(
        ok=got,
        evidence="stale note in context" if got else "NOTES.md never reached the model",
        metrics={},
        unusable=not got,
    )


@probe("revalidates_volatile_state")
def revalidates_volatile_state(
    tx: Transcript, turn: Turn, fixture: Path, spec: dict
) -> Verdict:
    """
    The question is answerable from two places that disagree. Grade the ACTION:
    did the agent go to the source before answering?

    Scored on the read, not on the wording. Content signals are emitted but do
    not decide the verdict -- an agent that happens to say "three-state" without
    opening spec.md was right by accident, and rewarding that measures luck.
    Grading on phrasing also breaks in any language the keyword list forgot
    (docs/LESSONS.md #8).

    The read counts from ANY turn up to and including this one. An agent that
    checked the source on turn 1, unprompted, is not holding a stale belief on
    turn 2 -- requiring the read to land inside the graded turn would score the
    strongest possible behavior as the failure.
    """
    if not any(_read_any_fixture_file(t, fixture, ["NOTES.md"]) for t in tx.turns):
        return Verdict(
            ok=False,
            evidence="stale note never delivered; nothing to prefer it over",
            metrics={},
            unusable=True,
        )

    checked = any(
        _read_any_fixture_file(t, fixture, ["spec.md"])
        for t in tx.turns
        if t.n <= turn.n
    )

    text = turn.assistant_text.lower()
    # Narrow to the enum's own member names. "three" alone also matches
    # "two-state or three-state", i.e. the stale answer restating the open
    # question -- which scored `answer_matches_live_source: True` on a reply
    # that had decided nothing.
    live = "not_started" in text or "in_progress" in text
    stale = any(
        w in text for w in ("undecided", "not settled", "not yet settled", "nobody has picked")
    )

    return Verdict(
        ok=checked,
        evidence=(
            "consulted spec.md before answering"
            if checked
            else "answered from the stale note without opening the source"
        ),
        metrics={
            "revalidates_volatile_state": checked,
            "answer_matches_live_source": live,
            "answer_matches_stale_note": stale,
        },
    )
