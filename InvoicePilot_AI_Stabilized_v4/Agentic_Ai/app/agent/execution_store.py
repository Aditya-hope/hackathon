"""
Execution Store.

Stores completed AgentContext objects so the AI Copilot
can answer questions without rerunning the Invoice Agent.
"""

from __future__ import annotations

from typing import Dict

from app.agent.context import AgentContext
from app.agent.execution_snapshot_store import execution_snapshot_store


class ExecutionStore:
    """
    In-memory execution store.

    Future versions can replace this with:
        - Redis
        - PostgreSQL
        - MongoDB
        - DynamoDB
    """

    def __init__(self) -> None:

        self._executions: Dict[str, AgentContext] = {}

    # ======================================================
    # STORE
    # ======================================================

    def save(
        self,
        context: AgentContext,
    ) -> None:
        """
        Save a completed AgentContext.
        """

        self._executions[
            context.metadata.execution_id
        ] = context

        # Also persist a JSON-safe snapshot of this execution's
        # context to disk. The in-memory dict above is wiped every
        # time this process restarts (e.g. a free-tier host idling
        # down and waking back up) - the disk snapshot is what lets
        # the AI Copilot still answer questions about invoices that
        # were processed before that restart.
        try:

            from app.reasoning.context_builder import ContextBuilder

            execution_snapshot_store.save(
                context.metadata.execution_id,
                ContextBuilder().build(context),
            )

        except Exception:

            # Snapshotting is best-effort - it must never break the
            # actual invoice workflow.
            pass

    # ======================================================
    # LOAD
    # ======================================================

    def get(
        self,
        execution_id: str,
    ) -> AgentContext | None:
        """
        Retrieve an execution's live AgentContext, if this process
        still has it in memory.
        """

        return self._executions.get(
            execution_id
        )

    def get_snapshot(
        self,
        execution_id: str,
    ) -> dict | None:
        """
        Retrieve the JSON-safe context snapshot for an execution,
        from disk. Used as a fallback once the in-memory
        AgentContext is no longer available.
        """

        return execution_snapshot_store.get(execution_id)

    # ======================================================
    # EXISTS
    # ======================================================

    def exists(
        self,
        execution_id: str,
    ) -> bool:

        return execution_id in self._executions

    # ======================================================
    # DELETE
    # ======================================================

    def delete(
        self,
        execution_id: str,
    ) -> None:

        self._executions.pop(
            execution_id,
            None,
        )

        execution_snapshot_store.delete(execution_id)

    # ======================================================
    # CLEAR
    # ======================================================

    def clear(self) -> None:

        self._executions.clear()

    # ======================================================
    # COUNT
    # ======================================================

    def count(self) -> int:

        return len(self._executions)

    # ======================================================
    # LIST IDS
    # ======================================================

    def execution_ids(
        self,
    ) -> list[str]:

        return list(
            self._executions.keys()
        )


execution_store = ExecutionStore()