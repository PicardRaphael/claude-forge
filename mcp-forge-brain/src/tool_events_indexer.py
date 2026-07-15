"""Parse Claude Code session transcripts (.jsonl) into indexable tool events.

A transcript is a JSONL file: one JSON object per line. `sessions_indexer.py`
keeps `text` blocks (user/assistant conversation) and drops `tool_use` /
`tool_result` blocks as noise. This module does the opposite: it keeps ONLY
`tool_use` and `tool_result` blocks, to power skill-friction analysis (recurring
errors, tool collisions) across sessions.

Design notes (verified against real transcripts, not guessed):
  - `tool_result` blocks carry `tool_use_id`, not a tool name. To label an error
    with the tool that produced it, we pair each `tool_result` with the `name`
    of the preceding `tool_use` sharing the same `id` — built as a single
    forward pass over the file (file-scoped, no cross-file pairing needed).
  - `is_error` is a native bool field on `tool_result` blocks, but it is not
    always present (omitted rather than False in older transcripts). Treated
    as authoritative when present; falls back to a keyword heuristic on the
    result text otherwise.
  - `tool_result.content` is either a `str` or a `list` of blocks (`text` /
    `tool_reference` observed) — mirror `_extract_text` from sessions_indexer,
    but scoped to what `tool_result` actually carries.
  - `tool_use.input` is a dict. It can hold full file contents (Write/Edit) —
    never indexed whole; summarized/truncated to keep FTS ranking and the DB
    size sane.
"""

import json
import logging
from dataclasses import dataclass

log = logging.getLogger(__name__)

# Bound on indexed text length — a Write/Edit `input` can carry a whole file.
_MAX_TEXT_LEN = 500

# Keyword heuristic fallback when `is_error` is absent from a tool_result block.
_ERROR_KEYWORDS = (
    "error", "erreur", "bloqué", "bloque", "blocked", "refus", "denied",
    "failed", "échec", "echec", "traceback", "exception",
)

# Fields worth surfacing directly for common tools (avoids dumping the whole
# input blob for the most common noisy tools).
_SALIENT_INPUT_FIELDS = {
    "Bash": ("command",),
    "Read": ("file_path",),
    "Write": ("file_path",),
    "Edit": ("file_path",),
    "MultiEdit": ("file_path",),
    "Grep": ("pattern",),
    "Glob": ("pattern",),
    "Skill": ("skill",),
    "Agent": ("subagent_type",),
}


@dataclass
class ToolEvent:
    session_id: str
    project: str
    timestamp: str
    event_kind: str  # "tool_use" | "tool_result"
    tool_name: str
    is_error: bool | None
    text: str
    line_no: int


def _summarize_input(tool_name: str, input_value) -> str:
    """Bounded, readable summary of a tool_use `input` dict. Never the raw blob."""
    if not isinstance(input_value, dict):
        return str(input_value)[:_MAX_TEXT_LEN]
    fields = _SALIENT_INPUT_FIELDS.get(tool_name)
    if fields:
        parts = [str(input_value[f]) for f in fields if f in input_value]
        if parts:
            return " ".join(parts)[:_MAX_TEXT_LEN]
    try:
        dumped = json.dumps(input_value, ensure_ascii=False)
    except (TypeError, ValueError):
        dumped = str(input_value)
    return dumped[:_MAX_TEXT_LEN]


def _extract_result_text(content) -> str:
    """Pull plain text from a `tool_result` block's `content` field.

    `content` is either a string or a list of blocks (text / tool_reference /
    other). Only `text` blocks are kept from a list; tool_reference and unknown
    block types are dropped.
    """
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                txt = block.get("text", "")
                if isinstance(txt, str):
                    parts.append(txt)
        return " ".join(parts).strip()
    return ""


def _looks_like_error(text: str) -> bool:
    head = text[:300].lower()
    return any(kw in head for kw in _ERROR_KEYWORDS)


def parse_transcript(path: str, project: str) -> list[ToolEvent]:
    """Parse one .jsonl transcript into a list of indexable ToolEvent.

    Robust to malformed lines (skipped), empty files (empty list), and blocks
    without usable content (skipped). Never raises on bad data.
    """
    events: list[ToolEvent] = []
    tool_use_names: dict[str, str] = {}  # tool_use_id -> tool name, forward-pass pairing

    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line_no, line in enumerate(fh, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except (json.JSONDecodeError, ValueError):
                    continue
                if not isinstance(obj, dict):
                    continue
                if obj.get("type") not in ("user", "assistant"):
                    continue
                msg = obj.get("message")
                if not isinstance(msg, dict):
                    continue
                content = msg.get("content")
                if not isinstance(content, list):
                    continue

                session_id = obj.get("sessionId") or obj.get("agentId") or ""
                timestamp = obj.get("timestamp", "")

                for block in content:
                    if not isinstance(block, dict):
                        continue
                    block_type = block.get("type")

                    if block_type == "tool_use":
                        tool_id = block.get("id")
                        tool_name = block.get("name", "")
                        if not isinstance(tool_name, str) or not tool_name:
                            continue
                        if isinstance(tool_id, str):
                            tool_use_names[tool_id] = tool_name
                        text = _summarize_input(tool_name, block.get("input"))
                        events.append(
                            ToolEvent(
                                session_id=session_id,
                                project=project,
                                timestamp=timestamp,
                                event_kind="tool_use",
                                tool_name=tool_name,
                                is_error=None,
                                text=text,
                                line_no=line_no,
                            )
                        )

                    elif block_type == "tool_result":
                        tool_use_id = block.get("tool_use_id", "")
                        tool_name = tool_use_names.get(tool_use_id, "") if isinstance(tool_use_id, str) else ""
                        text = _extract_result_text(block.get("content"))
                        if not text:
                            continue
                        is_error = block.get("is_error")
                        if not isinstance(is_error, bool):
                            is_error = _looks_like_error(text)
                        events.append(
                            ToolEvent(
                                session_id=session_id,
                                project=project,
                                timestamp=timestamp,
                                event_kind="tool_result",
                                tool_name=tool_name,
                                is_error=is_error,
                                text=text[:_MAX_TEXT_LEN],
                                line_no=line_no,
                            )
                        )
    except (OSError, UnicodeError):
        log.warning("Could not read transcript: %s", path)
        return []
    return events
