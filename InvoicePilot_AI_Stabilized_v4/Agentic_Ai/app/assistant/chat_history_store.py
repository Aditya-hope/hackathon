"""
Chat History Store.

Persists AI Copilot conversation turns per execution_id so that:

- Follow-up questions ("what about its tax?", "and the vendor?")
  can be answered using earlier turns in the same conversation.
- History survives process restarts, instead of living only in
  memory for the lifetime of the server process.

Storage is a small JSON file on disk. This keeps the project
dependency-free (no database required) while still giving real
persistence. Swapping in Redis/Postgres later only requires
replacing this class - callers only depend on the public methods
below.
"""

from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

# app/assistant/chat_history_store.py -> app/ -> Agentic_Ai/ -> data/
DEFAULT_STORE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "chat_history.json"
)

# Keep at most this many turns (user + assistant messages combined)
# per execution, so a long-lived conversation can't grow unbounded.
MAX_TURNS_PER_EXECUTION = 200

# How many recent turns get fed back into the LLM prompt as
# conversation history for follow-up questions.
DEFAULT_CONTEXT_TURNS = 12


class ChatHistoryStore:
    """
    Thread-safe, file-persisted AI Copilot chat history.

    Keyed by execution_id -> list of
    {"role": "user"|"assistant", "content": str, "timestamp": str}.
    """

    def __init__(self, storage_path: Optional[Path] = None) -> None:

        self._path = storage_path or DEFAULT_STORE_PATH

        self._lock = threading.Lock()

        self._history: Dict[str, List[dict]] = {}

        self._load()

    # ======================================================
    # Persistence
    # ======================================================

    def _load(self) -> None:

        if not self._path.exists():

            self._history = {}

            return

        try:

            with self._path.open("r", encoding="utf-8") as f:

                data = json.load(f)

            self._history = data if isinstance(data, dict) else {}

        except Exception:

            # A corrupt/unreadable history file shouldn't take down
            # the AI Copilot - just start fresh in memory.
            self._history = {}

    def _persist(self) -> None:

        try:

            self._path.parent.mkdir(parents=True, exist_ok=True)

            with self._path.open("w", encoding="utf-8") as f:

                json.dump(self._history, f, indent=2, default=str)

        except Exception:

            # Persistence is best-effort. If the disk write fails,
            # the conversation still works for the rest of this
            # process's lifetime via the in-memory copy.
            pass

    # ======================================================
    # Writes
    # ======================================================

    def append(
        self,
        execution_id: str,
        role: str,
        content: str,
    ) -> None:
        """
        Append a single turn (user question or assistant answer)
        to an execution's conversation.
        """

        with self._lock:

            turns = self._history.setdefault(execution_id, [])

            turns.append(
                {
                    "role": role,
                    "content": content,
                    "timestamp": datetime.now(
                        timezone.utc
                    ).isoformat(),
                }
            )

            overflow = len(turns) - MAX_TURNS_PER_EXECUTION

            if overflow > 0:

                del turns[:overflow]

            self._persist()

    def clear(self, execution_id: str) -> None:
        """
        Delete all stored conversation turns for an execution.
        """

        with self._lock:

            if execution_id in self._history:

                del self._history[execution_id]

                self._persist()

    # ======================================================
    # Reads
    # ======================================================

    def get(self, execution_id: str) -> List[dict]:
        """
        Full stored conversation for an execution, oldest first.
        """

        with self._lock:

            return list(self._history.get(execution_id, []))

    def recent(
        self,
        execution_id: str,
        limit: int = DEFAULT_CONTEXT_TURNS,
    ) -> List[dict]:
        """
        Most recent ``limit`` turns for an execution, oldest first -
        the slice that gets fed back into the LLM prompt so it can
        stay consistent with what it already told the user.
        """

        turns = self.get(execution_id)

        if limit <= 0:

            return []

        return turns[-limit:]


# Module-level singleton, mirroring the pattern used by
# app.agent.execution_store.execution_store.
chat_history_store = ChatHistoryStore()
