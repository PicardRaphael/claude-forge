"""Parse Claude Code session transcripts (.jsonl) into indexable messages.

A transcript is a JSONL file: one JSON object per line. Only `user` and
`assistant` messages carry conversational text worth searching. Everything else
(tool_use, tool_result, thinking blocks, system, attachments, local-command
echoes, meta) is noise for the "what did we say about X" use case and is dropped.
"""

import json
import logging
from dataclasses import dataclass

log = logging.getLogger(__name__)

# Minimum text length to index — drops trivial "ok", "yes", punctuation echoes.
_MIN_TEXT_LEN = 15

# Prefixes marking harness-injected content, not real conversation.
_NOISE_PREFIXES = (
    "<local-command",
    "<command-name",
    "<command-message",
    "<bash-",
    "caveat:",
)


@dataclass
class ParsedMessage:
    session_id: str
    project: str
    role: str
    timestamp: str
    content: str
    line_no: int


def _extract_text(content) -> str:
    """Pull plain conversational text from a message `content` field.

    `content` is either a string (legacy user messages) or a list of blocks.
    Only `text` blocks are kept; tool_use / tool_result / thinking are dropped.
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


def _is_noise(text: str) -> bool:
    """True if the text is harness boilerplate, not real conversation."""
    if len(text) < _MIN_TEXT_LEN:
        return True
    head = text[:80].lower().lstrip()
    return any(head.startswith(p) for p in _NOISE_PREFIXES)


def parse_transcript(path: str, project: str) -> list[ParsedMessage]:
    """Parse one .jsonl transcript into a list of indexable ParsedMessage.

    Robust to malformed lines (skipped), empty files (empty list), and messages
    without usable content (skipped). Never raises on bad data.
    """
    messages: list[ParsedMessage] = []
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
                if obj.get("isMeta"):
                    continue
                msg = obj.get("message")
                if not isinstance(msg, dict):
                    continue
                text = _extract_text(msg.get("content"))
                if not text or _is_noise(text):
                    continue
                session_id = obj.get("sessionId") or obj.get("agentId") or ""
                messages.append(
                    ParsedMessage(
                        session_id=session_id,
                        project=project,
                        role=obj.get("type", ""),
                        timestamp=obj.get("timestamp", ""),
                        content=text,
                        line_no=line_no,
                    )
                )
    except (OSError, UnicodeError):
        log.warning("Could not read transcript: %s", path)
        return []
    return messages
