from dataclasses import dataclass

from app.agent.context import AgentContext


@dataclass
class PlanStep:
    """
    Represents a single executable step in the workflow.
    """

    skill: str

    required: bool = True

    retry: int = 1


class Planner:
    """
    Generates an execution plan for InvoiceAgent.
    """

    def create_plan(self, context: AgentContext) -> list[PlanStep]:
        """
        Build the ordered list of skills to execute.

        Step names must match the ``name`` attribute of the skill
        classes registered in ``SkillRegistry`` (see app/bootstrap.py).
        """

        return [

            PlanStep("extract_invoice"),

            PlanStep("vendor_lookup"),

            PlanStep("validate_invoice"),

            PlanStep("duplicate_detection"),

            PlanStep("policy_engine"),

            PlanStep("risk_assessment"),

            PlanStep("recommendation"),

            PlanStep("approval_queue"),

            PlanStep("audit_logger"),

        ]