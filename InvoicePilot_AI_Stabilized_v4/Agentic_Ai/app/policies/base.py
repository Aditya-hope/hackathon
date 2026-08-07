"""
Base Policy Engine.
"""

from abc import ABC, abstractmethod

from app.schemas.invoice import Invoice

from app.policies.policy_result import PolicyResult


class BasePolicyEngine(ABC):

    @abstractmethod
    def evaluate(
        self,
        invoice: Invoice,
    ) -> PolicyResult:

        raise NotImplementedError