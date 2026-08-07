"""
Approval Queue Exceptions.
"""


class ApprovalError(Exception):
    """
    Base class for Approval Queue errors.
    """


class ApprovalItemNotFoundError(ApprovalError):
    """
    Raised when an execution_id has no matching queue entry.
    """


class ApprovalAlreadyDecidedError(ApprovalError):
    """
    Raised when trying to approve/reject an item that has
    already received a decision.
    """
