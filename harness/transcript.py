"""
Transcript parsing and probe evaluation.

The harness never asks the agent whether it succeeded. Every verdict is derived
from (a) the tool-call stream and (b) ground truth read off the fixture on disk.
Self-report is recorded for comparison but never scored -- the gap between what
the agent claims and what the fixture shows is itself a metric (see
`false_success_claim` in LH-02).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Iterator, Literal

Outcome = Literal["pass", "partial", "fail"]


@dataclass
class ToolCall:
    """One tool invocation lifted from the stream-json transcript."""

    name: str
    params: dict[str, Any]
    turn: int
    result_text: str = ""

    @property
    def path(self) -> str | None:
        for key in ("file_path", "path", "notebook_path"):
            if key in self.params:
                return str(self.params[key])
        return None

    @property
    def is_read(self) -> bool:
        return self.name in {"Read", "NotebookRead"}

    @property
    def is_write(self) -> bool:
        return self.name in {"Edit", "Write", "NotebookEdit"}

    @property
    def is_search(self) -> bool:
        # Grep/Glob count as "looking before you leap" for LH-05.
        return self.name in {"Grep", "Glob"}

    @property
    def read_span(self) -> tuple[int | None, int | None]:
        """(offset, limit) for a Read. (None, None) means an unbounded full read."""
        if not self.is_read:
            return (None, None)
        off = self.params.get("offset")
        lim = self.params.get("limit")
        return (
            int(off) if off is not None else None,
            int(lim) if lim is not None else None,
        )

    @property
    def is_full_read(self) -> bool:
        """A Read with no offset/limit pulls the whole file."""
        return self.is_read and self.read_span == (None, None)

    @property
    def bytes_read(self) -> int:
        return len(self.result_text.encode("utf-8"))


@dataclass
class Turn:
    n: int
    prompt: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    assistant_text: str = ""
    # Set from the task spec when a probe's subject varies per turn (LH-05 asks
    # about EDITOR, then PATH, then HISTSIZE against one fixture).
    probe_key: str = ""

    def reads_of(self, path_fragment: str) -> list[ToolCall]:
        return [
            c
            for c in self.tool_calls
            if c.is_read and c.path and path_fragment in c.path
        ]

    def touched_paths(self) -> set[str]:
        return {c.path for c in self.tool_calls if c.is_write and c.path}


@dataclass
class Transcript:
    turns: list[Turn] = field(default_factory=list)

    def turn(self, n: int) -> Turn | None:
        return next((t for t in self.turns if t.n == n), None)

    def all_calls(self) -> Iterator[ToolCall]:
        for t in self.turns:
            yield from t.tool_calls

    def calls_before(self, turn_n: int) -> Iterator[ToolCall]:
        for t in self.turns:
            if t.n < turn_n:
                yield from t.tool_calls


def parse_stream_json(raw: str, turn_n: int) -> Turn:
    """
    Parse one `claude -p --output-format=stream-json` invocation into a Turn.

    The stream is newline-delimited JSON. Tool calls appear as `tool_use` content
    blocks on assistant messages; their outputs come back as `tool_result` blocks
    on subsequent user messages, keyed by tool_use_id. We stitch the two together
    so that `bytes_read` reflects what actually entered the model's context.
    """
    turn = Turn(n=turn_n, prompt="")
    pending: dict[str, ToolCall] = {}
    text_parts: list[str] = []

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            # A truncated final line is normal if the process was killed on
            # timeout; earlier events are still valid, so keep what we have.
            continue

        message = event.get("message") or {}
        content = message.get("content")
        if not isinstance(content, list):
            continue

        for block in content:
            if not isinstance(block, dict):
                continue
            btype = block.get("type")

            if btype == "text":
                text_parts.append(block.get("text", ""))

            elif btype == "tool_use":
                call = ToolCall(
                    name=block.get("name", "?"),
                    params=block.get("input") or {},
                    turn=turn_n,
                )
                pending[block.get("id", "")] = call
                turn.tool_calls.append(call)

            elif btype == "tool_result":
                call = pending.get(block.get("tool_use_id", ""))
                if call is not None:
                    call.result_text = _flatten_result(block.get("content"))

    turn.assistant_text = "\n".join(text_parts)
    return turn


def _flatten_result(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            b.get("text", "")
            for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""
