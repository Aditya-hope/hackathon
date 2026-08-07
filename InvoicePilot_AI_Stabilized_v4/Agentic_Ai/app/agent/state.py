"""
Agent execution states.
"""

from enum import Enum


class AgentState(str, Enum):
    """
    Lifecycle states of the Invoice Agent.
    """

    IDLE = "IDLE"

    PLANNING = "PLANNING"

    DOCUMENT_LOADING = "DOCUMENT_LOADING"

    EXTRACTING = "EXTRACTING"

    VENDOR_LOOKUP = "VENDOR_LOOKUP"

    VALIDATING = "VALIDATING"

    DUPLICATE_CHECK = "DUPLICATE_CHECK"

    POLICY_CHECK = "POLICY_CHECK"

    RISK_ANALYSIS = "RISK_ANALYSIS"

    RECOMMENDING = "RECOMMENDING"

    QUEUEING_APPROVAL = "QUEUEING_APPROVAL"

    AUDITING = "AUDITING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"