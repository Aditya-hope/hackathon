"""
Execution Snapshot Store.

`ExecutionStore` (execution_store.py) keeps the full, live
`AgentContext` for a processed invoice - but only in memory, for
the lifetime of this process. That's a problem for the AI Copilot:
free/low-tier hosting (this app runs on Render) idles a service
down after inactivity and restarts it on the next request, wiping
that in-memory dict clean. Every invoice processed before the
restart becomes invisible to the Copilot ("I couldn't find that
invoice execution."), even though the user can still see it sitting
right there in their History tab.

This store keeps a small, JSON-safe snapshot of each execution's
invoice context (the same shape `ContextBuilder.build()` already
produces) on disk, so the Copilot has something to fall back on
once the in-memory copy is gone. It is intentionally *not* a
replacement for `ExecutionStore` - just a durable backstop for the
one thing the Copilot actually needs to answer questions: the built
context dict.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Dict, Optional

# app/agent/execution_snapshot_store.py -> app/ -> Agentic_Ai/ -> data/
DEFAULT_STORE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "data"
    / "execution_snapshots.json"
)

# Keep at most this many snapshots on disk, oldest dropped first, so
# the file can't grow without bound on a long-lived deployment.
MAX_SNAPSHOTS = 500


class ExecutionSnapshotStore:
    """
    Thread-safe, file-persisted map of execution_id -> context dict.
    """

    def __init__(self, storage_path: Optional[Path] = None) -> None:

        self._path = storage_path or DEFAULT_STORE_PATH

        self._lock = threading.Lock()

        self._snapshots: Dict[str, dict] = {}

        self._load()

    # ======================================================
    # Persistence
    # ======================================================

    def _load(self) -> None:

        if not self._path.exists():

            self._snapshots = {}

            return

        try:

            with self._path.open("r", encoding="utf-8") as f:

                data = json.load(f)

            self._snapshots = data if isinstance(data, dict) else {}

        except Exception:

            # A corrupt/unreadable snapshot file shouldn't take down
            # the app - just start fresh in memory.
            self._snapshots = {}

    def _persist(self) -> None:

        try:

            self._path.parent.mkdir(parents=True, exist_ok=True)

            with self._path.open("w", encoding="utf-8") as f:

                json.dump(self._snapshots, f, default=str)

        except Exception:

            # Persistence is best-effort - a failed disk write should
            # never break invoice processing itself.
            pass

    # ======================================================
    # Writes
    # ======================================================

    def save(self, execution_id: str, snapshot: dict) -> None:
        """
        Persist a JSON-safe context snapshot for an execution.
        """

        with self._lock:

            self._snapshots[execution_id] = snapshot

            overflow = len(self._snapshots) - MAX_SNAPSHOTS

            if overflow > 0:

                for key in list(self._snapshots.keys())[:overflow]:

                    del self._snapshots[key]

            self._persist()

    def delete(self, execution_id: str) -> None:
        """
        Remove a persisted snapshot, e.g. when the user deletes the
        invoice from their history.
        """

        with self._lock:

            if execution_id in self._snapshots:

                del self._snapshots[execution_id]

                self._persist()

    # ======================================================
    # Reads
    # ======================================================

    def get(self, execution_id: str) -> Optional[dict]:

        with self._lock:

            snapshot = self._snapshots.get(execution_id)

            return dict(snapshot) if snapshot is not None else None


# Module-level singleton, mirroring
# app.assistant.chat_history_store.chat_history_store.
execution_snapshot_store = ExecutionSnapshotStore()
